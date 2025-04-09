#!/usr/bin/env python3
"""
test_screenshot.py - Simple test script to verify screenshot capabilities
This script takes a URL as input and attempts to capture a screenshot using
the enhanced techniques from llama_screenshot.py
"""

import asyncio
import logging
import os
import sys
from urllib.parse import urlparse

from PIL import Image, ImageStat
from playwright.async_api import async_playwright
from playwright_stealth import stealth_async

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("test_screenshot")

# Browser fingerprints
FINGERPRINTS = [
    {
        "userAgent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "viewport": {"width": 1440, "height": 900},
        "deviceScaleFactor": 2,
        "hasTouch": False,
    }
]


async def take_screenshot(url, output_path="output"):
    """Take a screenshot of the given URL using enhanced techniques"""
    os.makedirs(output_path, exist_ok=True)

    logger.info(f"Taking screenshot of: {url}")
    async with async_playwright() as p:
        # Launch browser with improved settings
        browser = await p.chromium.launch(
            headless=True,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--disable-features=IsolateOrigins,site-per-process",
                "--disable-site-isolation-trials",
                "--disable-web-security",
                "--no-sandbox",
                "--disable-dev-shm-usage",
            ],
        )

        # Create a context with specific fingerprint
        fingerprint = FINGERPRINTS[0]
        context = await browser.new_context(
            viewport=fingerprint["viewport"],
            user_agent=fingerprint["userAgent"],
            device_scale_factor=fingerprint["deviceScaleFactor"],
            locale="en-US",
            timezone_id="America/New_York",
        )

        # Create a page with stealth mode
        page = await context.new_page()
        await stealth_async(page)

        # Anti-detection script
        await page.add_init_script(
            """
            Object.defineProperty(navigator, 'webdriver', { get: () => false });
            Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3, 4, 5] });
            Object.defineProperty(navigator, 'languages', { get: () => ['en-US', 'en'] });
        """
        )

        try:
            # Navigate to page with longer timeout and explicit wait conditions
            logger.info(f"Navigating to {url}")
            await page.goto(url, wait_until="domcontentloaded", timeout=120000)

            # Wait for SPA content to render
            logger.info("Waiting for page content to render...")
            await asyncio.sleep(5)

            # Wait for network idle
            try:
                await page.wait_for_load_state("networkidle", timeout=60000)
                logger.info("Network idle reached")
            except Exception as e:
                logger.warning(f"Network didn't become idle, but continuing: {e}")

            # Try to wait for content selectors
            content_found = False
            for selector in [
                "main",
                "article",
                ".content",
                "#content",
                "div.main",
                "h1",
                ".docs-content",
                "nav",
            ]:
                try:
                    await page.wait_for_selector(selector, timeout=10000)
                    logger.info(f"Found content element: {selector}")
                    content_found = True
                    break
                except Exception:
                    pass

            if not content_found:
                logger.warning("Could not find specific content elements, continuing anyway")

            # Scroll through the page to load lazy content
            logger.info("Scrolling to load all content...")
            await page.evaluate(
                """
                async () => {
                    const delay = (ms) => new Promise(resolve => setTimeout(resolve, ms));
                    
                    // Get page height
                    const height = document.body.scrollHeight;
                    const steps = 10;
                    const stepSize = height / steps;
                    
                    // Scroll down gradually
                    for (let i = 0; i <= steps; i++) {
                        window.scrollTo(0, i * stepSize);
                        await delay(300);
                    }
                    
                    // Scroll back to top
                    window.scrollTo(0, 0);
                }
            """
            )

            # Wait after scrolling
            await asyncio.sleep(3)

            # Special case for OpenAI docs
            if "openai.com/docs" in url:
                logger.info("OpenAI docs detected, applying special handling")
                await asyncio.sleep(3)  # Extra wait

                # Try to click menu buttons to force render hidden content
                try:
                    for menu_selector in [
                        "nav button",
                        ".menu-button",
                        'button[aria-label="Menu"]',
                        '[role="button"]',
                    ]:
                        menu_button = await page.query_selector(menu_selector)
                        if menu_button:
                            await menu_button.click()
                            logger.info(f"Clicked menu button: {menu_selector}")
                            await asyncio.sleep(2)
                            break
                except Exception as e:
                    logger.warning(f"Could not click menu: {e}")

            # Create output filename
            filename = f"{urlparse(url).netloc.replace('.', '_')}.png"
            output_file = os.path.join(output_path, filename)

            # Take screenshot
            logger.info(f"Taking screenshot, saving to: {output_file}")
            await page.screenshot(path=output_file, full_page=True, scale="device")

            # Verify screenshot has content
            validate_result = await validate_screenshot(output_file)
            if not validate_result:
                logger.warning("Screenshot appears empty! Trying additional fixes...")

                # Try forcing styles and scripts to load
                await page.evaluate(
                    """
                    () => {
                        // Force background color
                        document.body.style.backgroundColor = '#ffffff';
                        
                        // Force visibility
                        const allElements = document.querySelectorAll('*');
                        for (const el of allElements) {
                            if (el.style.display === 'none') {
                                el.style.display = 'block';
                            }
                            if (el.style.visibility === 'hidden') {
                                el.style.visibility = 'visible';
                            }
                        }
                    }
                """
                )

                # Wait for styles to apply
                await asyncio.sleep(2)

                # Try screenshot again
                logger.info("Retaking screenshot...")
                await page.screenshot(path=output_file, full_page=True, scale="device")

                # Check again
                validate_result = await validate_screenshot(output_file)
                logger.info(f"Retry validation result: {validate_result}")
            else:
                logger.info("Screenshot validated successfully!")

            # Close browser
            await browser.close()

            return output_file

        except Exception as e:
            logger.error(f"Error capturing screenshot: {e}")
            await browser.close()
            return None


async def validate_screenshot(filepath):
    """Validate that screenshot is not blank"""
    try:
        # Check if file exists and has size
        if not os.path.exists(filepath) or os.path.getsize(filepath) < 1000:
            logger.warning(f"Screenshot file is too small: {os.path.getsize(filepath)} bytes")
            return False

        # Load image with PIL
        img = Image.open(filepath)
        img_gray = img.convert("L")  # Convert to grayscale

        # Get image statistics
        extrema = img_gray.getextrema()
        stats = ImageStat.Stat(img_gray)
        std_dev = stats.stddev[0]
        mean = stats.mean[0]

        # Check if image is blank (low contrast)
        min_val, max_val = extrema
        logger.info(
            f"Image stats - min: {min_val}, max: {max_val}, stddev: {std_dev:.2f}, mean: {mean:.2f}"
        )

        if max_val - min_val < 20 or std_dev < 10:
            logger.warning("Image appears blank - low contrast detected")
            return False

        return True
    except Exception as e:
        logger.error(f"Error validating screenshot: {e}")
        return False


async def main():
    # Get URL from command line
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <url>")
        return

    url = sys.argv[1]
    screenshot_path = await take_screenshot(url)

    if screenshot_path:
        print(f"\nScreenshot successfully saved to: {screenshot_path}")
    else:
        print("\nFailed to take screenshot")


if __name__ == "__main__":
    asyncio.run(main())
