"""HTML rendering and processing module for LlamaDoc2PDF."""

import asyncio
import os
from pathlib import Path
from typing import Any, Dict, Optional, Union

from bs4 import BeautifulSoup
from playwright.async_api import async_playwright

# Optional dependencies for enhanced functionality
try:
    import weasyprint

    WEASYPRINT_AVAILABLE = True
except ImportError:
    WEASYPRINT_AVAILABLE = False

try:
    from reportlab.lib.pagesizes import A4, letter
    from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
    from reportlab.platypus import Image as RLImage
    from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer

    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False


class HtmlRenderer:
    """Advanced HTML rendering and processing for PDF conversion."""

    def __init__(
        self,
        headless: bool = True,
        media_enabled: bool = True,
        javascript_enabled: bool = True,
        css_enabled: bool = True,
    ):
        """
        Initialize the HTML renderer.

        Args:
            headless: Run browser in headless mode
            media_enabled: Enable media (images, etc)
            javascript_enabled: Enable JavaScript
            css_enabled: Enable CSS
        """
        self.headless = headless
        self.media_enabled = media_enabled
        self.javascript_enabled = javascript_enabled
        self.css_enabled = css_enabled

    async def render_html(self, html_content: str, base_url: Optional[str] = None) -> str:
        """
        Render HTML content with JavaScript execution.

        Args:
            html_content: HTML content to render
            base_url: Base URL for relative resources

        Returns:
            Fully rendered HTML content
        """
        async with async_playwright() as playwright:
            browser = await playwright.chromium.launch(headless=self.headless)

            # Create context with appropriate settings
            context = await browser.new_context(
                viewport={"width": 1280, "height": 800},
                java_script_enabled=self.javascript_enabled,
                has_touch=False,
                bypass_csp=True,  # Bypass Content-Security-Policy
                ignore_https_errors=True,
            )

            # Create page and load content
            page = await context.new_page()

            # Set content with base URL if provided
            if base_url:
                await page.set_content(html_content, wait_until="networkidle", timeout=30000)
            else:
                await page.set_content(html_content, wait_until="networkidle", timeout=30000)

            # Wait for any remaining JavaScript to execute
            await asyncio.sleep(1)

            # Get the fully rendered HTML
            rendered_html = await page.content()

            # Clean up
            await context.close()
            await browser.close()

            return rendered_html

    async def html_to_pdf_via_playwright(
        self,
        html_content: str,
        output_path: Union[str, Path],
        options: Dict[str, Any] = None,
    ) -> Path:
        """
        Convert HTML content to PDF using Playwright's built-in PDF generation.

        Args:
            html_content: HTML content to convert
            output_path: Path to save the generated PDF
            options: PDF options

        Returns:
            Path to the generated PDF
        """
        options = options or {}
        output_path = Path(output_path) if isinstance(output_path, str) else output_path

        # Ensure output directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Default PDF options
        pdf_options = {
            "format": options.get("format", "A4"),
            "printBackground": options.get("print_background", True),
            "margin": {
                "top": f"{options.get('margin_top', 20)}mm",
                "right": f"{options.get('margin_right', 20)}mm",
                "bottom": f"{options.get('margin_bottom', 20)}mm",
                "left": f"{options.get('margin_left', 20)}mm",
            },
            "displayHeaderFooter": options.get("display_header_footer", False),
        }

        # Add header/footer if enabled
        if pdf_options["displayHeaderFooter"]:
            pdf_options["headerTemplate"] = options.get("header_template", "")
            pdf_options["footerTemplate"] = options.get(
                "footer_template",
                "<div style='font-size:10px; text-align:center; width:100%;'><span class='pageNumber'></span> / <span class='totalPages'></span></div>",
            )

        # PDF scaling options
        pdf_options["scale"] = options.get("scale", 1.0)

        async with async_playwright() as playwright:
            browser = await playwright.chromium.launch(headless=True)
            context = await browser.new_context(viewport={"width": 1280, "height": 800})
            page = await context.new_page()

            # Load the HTML content
            await page.set_content(html_content, wait_until="networkidle")

            # Generate PDF
            await page.pdf(path=str(output_path), **pdf_options)

            # Clean up
            await context.close()
            await browser.close()

        return output_path

    def html_to_pdf_via_weasyprint(
        self,
        html_content: str,
        output_path: Union[str, Path],
        options: Dict[str, Any] = None,
    ) -> Path:
        """
        Convert HTML content to PDF using WeasyPrint.

        Args:
            html_content: HTML content to convert
            output_path: Path to save the generated PDF
            options: PDF options

        Returns:
            Path to the generated PDF
        """
        if not WEASYPRINT_AVAILABLE:
            raise ImportError("WeasyPrint is required for this conversion method")

        options = options or {}
        output_path = Path(output_path) if isinstance(output_path, str) else output_path

        # Ensure output directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Create WeasyPrint HTML object
        html = weasyprint.HTML(string=html_content)

        # Get CSS from options
        css_files = options.get("css_files", [])
        css_string = options.get("css_string", "")

        # Create CSS list
        css = []
        for css_file in css_files:
            if os.path.exists(css_file):
                css.append(weasyprint.CSS(filename=css_file))

        if css_string:
            css.append(weasyprint.CSS(string=css_string))

        # Generate PDF
        if css:
            html.write_pdf(str(output_path), stylesheets=css)
        else:
            html.write_pdf(str(output_path))

        return output_path

    def html_to_pdf_via_reportlab(
        self,
        html_content: str,
        output_path: Union[str, Path],
        options: Dict[str, Any] = None,
    ) -> Path:
        """
        Convert HTML content to PDF using ReportLab (for simpler HTML).

        Args:
            html_content: HTML content to convert
            output_path: Path to save the generated PDF
            options: PDF options

        Returns:
            Path to the generated PDF
        """
        if not REPORTLAB_AVAILABLE:
            raise ImportError("ReportLab is required for this conversion method")

        options = options or {}
        output_path = Path(output_path) if isinstance(output_path, str) else output_path

        # Ensure output directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Parse the HTML
        soup = BeautifulSoup(html_content, "html.parser")

        # Get page size
        page_size_name = options.get("page_size", "A4")
        page_size = A4 if page_size_name.upper() == "A4" else letter

        # Create the PDF document
        doc = SimpleDocTemplate(
            str(output_path),
            pagesize=page_size,
            leftMargin=options.get("margin_left", 20) * 2.83,  # Convert mm to points
            rightMargin=options.get("margin_right", 20) * 2.83,
            topMargin=options.get("margin_top", 20) * 2.83,
            bottomMargin=options.get("margin_bottom", 20) * 2.83,
        )

        # Get styles
        styles = getSampleStyleSheet()
        title_style = styles["Title"]
        heading1_style = styles["Heading1"]
        heading2_style = styles["Heading2"]
        normal_style = styles["Normal"]

        # Create document elements
        elements = []

        # Process HTML elements
        title = soup.find("title")
        if title and title.text.strip():
            elements.append(Paragraph(title.text.strip(), title_style))
            elements.append(Spacer(1, 12))

        # Handle basic elements
        for element in soup.find_all(["h1", "h2", "p", "div"]):
            if element.name == "h1":
                elements.append(Paragraph(element.text.strip(), heading1_style))
            elif element.name == "h2":
                elements.append(Paragraph(element.text.strip(), heading2_style))
            elif element.name in ("p", "div"):
                # Skip empty paragraphs
                if element.text.strip():
                    elements.append(Paragraph(element.text.strip(), normal_style))

            elements.append(Spacer(1, 6))

        # Build the PDF
        doc.build(elements)

        return output_path

    async def convert_html_to_pdf(
        self,
        html_content: str,
        output_path: Union[str, Path],
        options: Dict[str, Any] = None,
    ) -> Path:
        """
        Convert HTML to PDF using the best available method.

        Args:
            html_content: HTML content to convert
            output_path: Path to save the generated PDF
            options: PDF options

        Returns:
            Path to the generated PDF
        """
        options = options or {}
        output_path = Path(output_path) if isinstance(output_path, str) else output_path

        # Ensure output directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Determine the conversion method
        method = options.get("method", "auto")

        if method == "playwright" or (method == "auto" and self.javascript_enabled):
            # Use Playwright for JavaScript-enabled content
            return await self.html_to_pdf_via_playwright(html_content, output_path, options)
        elif method == "weasyprint" or (method == "auto" and WEASYPRINT_AVAILABLE):
            # Use WeasyPrint for static content with good CSS support
            return self.html_to_pdf_via_weasyprint(html_content, output_path, options)
        elif method == "reportlab" or (method == "auto" and REPORTLAB_AVAILABLE):
            # Use ReportLab as a last resort for simple content
            return self.html_to_pdf_via_reportlab(html_content, output_path, options)
        else:
            # Fallback to Playwright if no method is explicitly available
            return await self.html_to_pdf_via_playwright(html_content, output_path, options)

    async def convert_html_file_to_pdf(
        self,
        html_file: Union[str, Path],
        output_path: Union[str, Path],
        options: Dict[str, Any] = None,
    ) -> Path:
        """
        Convert an HTML file to PDF.

        Args:
            html_file: Path to the HTML file
            output_path: Path to save the generated PDF
            options: PDF options

        Returns:
            Path to the generated PDF
        """
        html_file = Path(html_file) if isinstance(html_file, str) else html_file

        # Check if the file exists
        if not html_file.exists():
            raise FileNotFoundError(f"HTML file not found: {html_file}")

        # Read the HTML content
        with open(html_file, "r", encoding="utf-8") as f:
            html_content = f.read()

        # Add base_url option based on the file path
        if options is None:
            options = {}

        if "base_url" not in options:
            options["base_url"] = f"file://{html_file.parent.absolute()}/"

        # Convert the HTML to PDF
        return await self.convert_html_to_pdf(html_content, output_path, options)

    async def url_to_pdf(
        self, url: str, output_path: Union[str, Path], options: Dict[str, Any] = None
    ) -> Path:
        """
        Convert a URL directly to PDF.

        Args:
            url: URL to convert
            output_path: Path to save the generated PDF
            options: PDF options

        Returns:
            Path to the generated PDF
        """
        options = options or {}
        output_path = Path(output_path) if isinstance(output_path, str) else output_path

        # Ensure output directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Create PDF options
        pdf_options = {
            "format": options.get("format", "A4"),
            "printBackground": options.get("print_background", True),
            "margin": {
                "top": f"{options.get('margin_top', 20)}mm",
                "right": f"{options.get('margin_right', 20)}mm",
                "bottom": f"{options.get('margin_bottom', 20)}mm",
                "left": f"{options.get('margin_left', 20)}mm",
            },
            "displayHeaderFooter": options.get("display_header_footer", False),
            "scale": options.get("scale", 1.0),
        }

        # Add header/footer if enabled
        if pdf_options["displayHeaderFooter"]:
            pdf_options["headerTemplate"] = options.get("header_template", "")
            pdf_options["footerTemplate"] = options.get(
                "footer_template",
                "<div style='font-size:10px; text-align:center; width:100%;'><span class='pageNumber'></span> / <span class='totalPages'></span></div>",
            )

        # Use Playwright to load the URL and generate PDF
        async with async_playwright() as playwright:
            browser = await playwright.chromium.launch(headless=True)

            # Create context with appropriate settings
            context = await browser.new_context(
                viewport={"width": 1280, "height": 800},
                java_script_enabled=self.javascript_enabled,
                bypass_csp=True,
                ignore_https_errors=True,
            )

            # Create page and navigate to URL
            page = await context.new_page()

            # Add timeout option
            timeout = options.get("timeout", 60000)  # Default 60 seconds

            # Navigate to the URL
            try:
                await page.goto(url, wait_until="networkidle", timeout=timeout)
            except Exception as e:
                print(f"Navigation error: {e}. Attempting to continue...")

            # Wait for content to load
            await asyncio.sleep(options.get("wait_time", 2))

            # Auto-scroll if enabled
            if options.get("auto_scroll", True):
                await page.evaluate(
                    """
                async () => {
                    await new Promise((resolve) => {
                        let totalHeight = 0;
                        const distance = 100;
                        const timer = setInterval(() => {
                            const scrollHeight = document.body.scrollHeight;
                            window.scrollBy(0, distance);
                            totalHeight += distance;
                            
                            if(totalHeight >= scrollHeight){
                                clearInterval(timer);
                                window.scrollTo(0, 0);
                                resolve();
                            }
                        }, 100);
                    });
                }
                """
                )

                # Wait after scrolling
                await asyncio.sleep(1)

            # Generate PDF
            await page.pdf(path=str(output_path), **pdf_options)

            # Clean up
            await context.close()
            await browser.close()

        return output_path
