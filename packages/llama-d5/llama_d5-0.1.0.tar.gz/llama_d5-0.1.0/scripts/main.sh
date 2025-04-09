#!/bin/bash
# run_all.sh - A self-contained installer, configurator, tester, and runner for the llama_screenshot tool.
# This script creates a virtual environment, writes the program files, installs dependencies,
# sets up Playwright, runs a simple test, and finally starts the interactive program.
#
# Usage: ./run_all.sh

set -e

# Check for Python 3
if ! command -v python3 >/dev/null 2>&1; then
    echo "Python 3 is required but not installed. Exiting."
    exit 1
fi

# Create a virtual environment in the 'venv' folder
echo "Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Write requirements.txt
cat > requirements.txt << 'EOF'
playwright
playwright-stealth
playwright-extra
axe-playwright
undetected-playwright
aiohttp
beautifulsoup4
img2pdf
rich
fake-useragent
cloudscraper
pypdf2
pikepdf
EOF

# Write the full Python program file: llama_screenshot.py
cat > llama_screenshot.py << 'EOF'
import asyncio
import os
import re
import sys
from urllib.parse import urlparse, urljoin
import aiohttp
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError
from playwright_stealth import stealth_async
import img2pdf
from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.panel import Panel
from rich.text import Text
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn
from fake_useragent import UserAgent
import cloudscraper
import pikepdf
from pathlib import Path
import logging
import random
import time
import traceback

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler("llamadoc.log"), logging.StreamHandler()]
)
logger = logging.getLogger("llamadoc2pdf")

console = Console()
ua = UserAgent()

class StealthScraper:
    """Advanced scraping with anti-detection measures"""
    
    def __init__(self):
        self.browser = self.init_browser()
        self.scraper = cloudscraper.create_scraper()
        
    def init_browser(self):
        return async_playwright().start().chromium.launch(
            headless=True,
            proxy=config.proxy_settings,
            stealth=True
        )
    
    async def scrape_page(self, url: str) -> ScrapedContent:
        """Execute full scraping pipeline"""
        try:
            async with self.browser.new_page() as page:
                await page.goto(url, wait_until='networkidle')
                await self.anti_detect(page)
                content = await self.capture_content(page)
                return self.process_content(content)
        except ScrapingError as e:
            self.handle_error(e)
            
    async def anti_detect(self, page):
        """Apply anti-detection measures"""
        await page.evaluate(stealth_script)
        await page.route('**/*', self.block_analytics)
        await page.set_extra_http_headers(fake_headers)

class LlamaDocScreenshot:
    def __init__(self):
        self.visited_links = set()
        self.all_links = set()
        self.screenshot_files = []
        self.output_folder = ""
        self.use_fake_ua = True
        self.use_cloud_for_links = False
        self.use_cloud_for_screenshot = False
        self.use_stealth = True
        self.wait_time = (1, 3)  # Random wait between 1-3 seconds
        self.viewport_size = {"width": 1280, "height": 800}
        self.pdf_quality = 100
        self.max_retries = 3
        self.headless = True

    async def get_sub_links(self, url: str, base_url: str, visited: set, use_cloudscraper: bool = False) -> set:
        """Finds sub-links within the given URL using aiohttp or cloudscraper."""
        if url in visited or not url.startswith(base_url):
            return set()
        visited.add(url)
        sub_links = set()
        
        for attempt in range(self.max_retries):
            try:
                if use_cloudscraper:
                    scraper = cloudscraper.create_scraper()
                    response = scraper.get(url, timeout=15)
                    if response.status_code == 200:
                        html = response.text
                        soup = BeautifulSoup(html, 'html.parser')
                        for link in soup.find_all('a', href=True):
                            href = link['href']
                            absolute_url = urljoin(url, href).split('#')[0]
                            if absolute_url.startswith(base_url) and absolute_url not in visited:
                                sub_links.add(absolute_url)
                    else:
                        logger.warning(f"Could not access {url} (Status: {response.status_code})")
                else:
                    async with aiohttp.ClientSession() as session:
                        async with session.get(url, timeout=15) as response:
                            if response.status == 200:
                                html = await response.text()
                                soup = BeautifulSoup(html, 'html.parser')
                                for link in soup.find_all('a', href=True):
                                    href = link['href']
                                    absolute_url = urljoin(url, href).split('#')[0]
                                    if absolute_url.startswith(base_url) and absolute_url not in visited:
                                        sub_links.add(absolute_url)
                            else:
                                logger.warning(f"Could not access {url} (Status: {response.status})")
                # If successful, break out of retry loop
                break
            except Exception as e:
                logger.warning(f"Error accessing {url}: {e}. Attempt {attempt+1}/{self.max_retries}")
                if attempt == self.max_retries - 1:
                    logger.error(f"Failed to access {url} after {self.max_retries} attempts")
                # Wait before retrying
                await asyncio.sleep(random.uniform(1, 3))
        
        return sub_links

    async def capture_fullpage_screenshot(self, url: str, save_path: str):
        """Captures a full-page screenshot of a given URL with enhanced anti-detection."""
        for attempt in range(self.max_retries):
            try:
                async with async_playwright() as p:
                    browser_type = p.chromium
                    browser = await browser_type.launch(headless=self.headless)
                    context = await browser.new_context(
                        viewport=self.viewport_size,
                        user_agent=ua.random if self.use_fake_ua else "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
                    )
                    
                    # Add various privacy and anti-detection measures
                    await context.add_init_script("""
                    Object.defineProperty(navigator, 'webdriver', { get: () => false });
                    Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3, 4, 5] });
                    Object.defineProperty(navigator, 'languages', { get: () => ['en-US', 'en'] });
                    """)

                    page = await context.new_page()
                    
                    if self.use_stealth:
                        await stealth_async(page)
                    
                    # Random wait time to simulate human behavior
                    await asyncio.sleep(random.uniform(*self.wait_time))

                    # Try with cloudscraper if enabled
                    if self.use_cloud_for_screenshot:
                        scraper = cloudscraper.create_scraper()
                        response = scraper.get(url)
                        if response.status_code == 200:
                            await page.set_content(response.text)
                        else:
                            logger.error(f"Could not get content for {url} (Status: {response.status_code})")
                            return None
                    else:
                        await page.goto(url, timeout=60000, wait_until="networkidle")
                        # Additional wait for dynamic content
                        await asyncio.sleep(2)

                    title = await page.title()
                    sanitized_title = re.sub(r'[^\w\s-]', '', title).strip()
                    sanitized_title = re.sub(r'\s+', '_', sanitized_title)
                    filename = f"{sanitized_title}.png" if sanitized_title else f"page_{urlparse(url).netloc.replace('.', '_')}_{os.path.basename(urlparse(url).path) or 'home'}.png"
                    full_save_path = os.path.join(save_path, filename)
                    
                    await page.screenshot(path=full_save_path, full_page=True, quality=self.pdf_quality)
                    logger.info(f"Successfully captured screenshot of {url}")
                    await browser.close()
                    return full_save_path
            except PlaywrightTimeoutError:
                logger.error(f"Timeout occurred while loading {url}. Attempt {attempt+1}/{self.max_retries}")
            except Exception as e:
                logger.error(f"Error processing {url}: {e}. Attempt {attempt+1}/{self.max_retries}")
                logger.debug(traceback.format_exc())
            
            # Wait before retrying
            if attempt < self.max_retries - 1:
                await asyncio.sleep(random.uniform(2, 5))
        
        return None

    async def merge_pdfs(self, output_path, img_paths):
        """Merge screenshots into a PDF with improved quality."""
        try:
            # First convert images to PDF using img2pdf
            with open(output_path, "wb") as f:
                f.write(img2pdf.convert(img_paths))
            
            # Then optimize the PDF using pikepdf
            with pikepdf.open(output_path) as pdf:
                pdf.save(output_path, compress_streams=True, object_stream_mode=pikepdf.ObjectStreamMode.generate)
            
            return True
        except Exception as e:
            logger.error(f"Error creating PDF: {e}")
            logger.debug(traceback.format_exc())
            return False
                
    async def run(self):
        console.print(Panel(Text("Llama Screenshot PDF Tool", style="bold blue"), title="[bold green]Welcome![/]"))
        
        # Get user inputs
        start_url = Prompt.ask("[cyan]Enter the starting URL of the documentation site[/cyan]")
        parsed_url = urlparse(start_url)
        if not parsed_url.scheme:
            start_url = f"https://{start_url}"
            parsed_url = urlparse(start_url)
        base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"

        # Advanced options
        show_advanced = Confirm.ask("[yellow]Show advanced options?[/yellow]", default=False)
        if show_advanced:
            self.use_fake_ua = Confirm.ask("[yellow]Use fake user-agent?[/yellow]", default=True)
            self.use_cloud_for_links = Confirm.ask("[yellow]Use cloudscraper for link discovery?[/yellow]", default=False)
            self.use_cloud_for_screenshot = Confirm.ask("[yellow]Use cloudscraper for screenshot content?[/yellow]", default=False)
            self.use_stealth = Confirm.ask("[yellow]Use stealth mode?[/yellow]", default=True)
            self.headless = Confirm.ask("[yellow]Run browser in headless mode?[/yellow]", default=True)
            
            # Viewport size options
            viewport_preset = Prompt.ask("[yellow]Choose viewport size (desktop/tablet/mobile/custom)[/yellow]", default="desktop")
            if viewport_preset == "desktop":
                self.viewport_size = {"width": 1280, "height": 800}
            elif viewport_preset == "tablet":
                self.viewport_size = {"width": 1024, "height": 768}
            elif viewport_preset == "mobile":
                self.viewport_size = {"width": 390, "height": 844}
            elif viewport_preset == "custom":
                width = int(Prompt.ask("[yellow]Enter viewport width[/yellow]", default="1280"))
                height = int(Prompt.ask("[yellow]Enter viewport height[/yellow]", default="800"))
                self.viewport_size = {"width": width, "height": height}
            
            self.pdf_quality = int(Prompt.ask("[yellow]Enter image quality (1-100)[/yellow]", default="100"))
            self.wait_time = (
                float(Prompt.ask("[yellow]Enter minimum wait time between pages (seconds)[/yellow]", default="1")),
                float(Prompt.ask("[yellow]Enter maximum wait time between pages (seconds)[/yellow]", default="3"))
            )
            self.max_retries = int(Prompt.ask("[yellow]Enter maximum retries for each page[/yellow]", default="3"))

        # Set up output folder
        downloads_folder = os.path.expanduser("~/Downloads")
        self.output_folder = os.path.join(downloads_folder, "documentation_screenshots")
        os.makedirs(self.output_folder, exist_ok=True)
        console.print(f"[yellow]Screenshots will be saved to: [bold]{self.output_folder}[/bold][/yellow]")

        # Crawl for links
        console.print(f"[magenta]Finding sub-links starting from: [bold]{start_url}[/bold][/magenta]")
        self.visited_links = {start_url}
        self.all_links = {start_url}
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TimeElapsedColumn(),
            console=console
        ) as progress:
            task = progress.add_task("[green]Discovering Links...", total=None)
            newly_found = await self.get_sub_links(start_url, base_url, self.visited_links, self.use_cloud_for_links)
            self.all_links.update(newly_found)
            progress.update(task, total=len(self.all_links), completed=len(self.visited_links))
            
            while newly_found:
                next_links = set()
                for link in list(newly_found):
                    more_links = await self.get_sub_links(link, base_url, self.visited_links, self.use_cloud_for_links)
                    next_links.update(more_links)
                    self.all_links.update(more_links)
                    progress.update(task, completed=len(self.visited_links))
                newly_found = next_links - self.visited_links
                self.visited_links.update(newly_found)

        console.print(f"[blue]Found [bold]{len(self.all_links)}[/bold] unique links.[/blue]")

        # Take screenshots
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TimeElapsedColumn(),
            console=console
        ) as progress:
            task = progress.add_task("[green]Capturing Screenshots...", total=len(self.all_links))
            for url in self.all_links:
                progress.update(task, description=f"[cyan]Capturing: {url}[/cyan]")
                screenshot_path = await self.capture_fullpage_screenshot(url, self.output_folder)
                if screenshot_path:
                    self.screenshot_files.append(screenshot_path)
                progress.advance(task)

        # Create PDF
        if self.screenshot_files:
            pdf_filename = Prompt.ask("[cyan]Enter the desired filename for the combined PDF[/cyan]", default="combined_documentation.pdf")
            pdf_path = os.path.join(downloads_folder, pdf_filename)
            
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console
            ) as progress:
                task = progress.add_task("[green]Creating PDF...", total=1)
                success = await self.merge_pdfs(pdf_path, self.screenshot_files)
                progress.update(task, completed=1)
            
            if success:
                console.print(Panel(Text(f"[bold green]Successfully created PDF: {pdf_path}[/bold green]", style="bold green")))
            
            # Clean up
            if Confirm.ask("[yellow]Do you want to delete the individual screenshot files?[/yellow]", default=False):
                with Progress(console=console) as progress:
                    task = progress.add_task("[red]Deleting screenshots...", total=len(self.screenshot_files))
                    for file in self.screenshot_files:
                        try:
                            os.remove(file)
                            progress.advance(task)
                        except Exception as e:
                            logger.warning(f"Could not delete {file}: {e}")
        else:
            console.print("[yellow]No screenshots were successfully captured.[/yellow]")

async def main():
    try:
        app = LlamaDocScreenshot()
        await app.run()
    except KeyboardInterrupt:
        console.print("[yellow]Operation cancelled by user[/yellow]")
    except Exception as e:
        console.print(f"[red]An unexpected error occurred: {e}[/red]")
        logger.error(f"Unhandled exception: {e}")
        logger.debug(traceback.format_exc())

if __name__ == "__main__":
    asyncio.run(main())
EOF

# Write a helper setup script (optional) - setup.sh
cat > setup.sh << 'EOF'
#!/bin/bash
# setup.sh - Installs dependencies and Playwright browsers for llama_screenshot tool

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Installing Playwright browsers..."
playwright install

# Install additional browsers for more compatibility
playwright install firefox
playwright install webkit

echo "Setup complete! You can now run the script using: python llama_screenshot.py"
EOF
chmod +x setup.sh

# Run the setup script to install dependencies and browsers
echo "Running setup script..."
./setup.sh

# Optional Test: Display versions of key packages
echo "Testing installation by displaying key package versions:"
python3 -c "import playwright; import playwright_stealth; print(f'Playwright version: {playwright.__version__ if hasattr(playwright, \"__version__\") else \"installed\"}')"
python3 -c "import fake_useragent; print('fake-useragent installed')"
python3 -c "import cloudscraper; print('cloudscraper installed')"
python3 -c "import img2pdf; import pikepdf; print('PDF libraries installed')"

echo "All tests passed."

# Start the interactive program
echo "Starting the Llama Screenshot PDF Tool..."
python llama_screenshot.py

# Install with all features
pip install "llamadoc2pdf[all]"

# Initialize AI services
llama init --enable-ai --model mistral-7b

# Configure proxies
llama config set scraping.proxy_rotation=true

# Convert mixed inputs with AI enhancement
llama super-convert \
  input.docx http://example.com ./images/ \
  --output ./results \
  --format pdf \
  --enhance \
  --parallel 8 \
  --verbose
