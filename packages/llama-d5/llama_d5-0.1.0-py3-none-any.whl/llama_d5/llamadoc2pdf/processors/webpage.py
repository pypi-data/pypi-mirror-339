"""Web page processing for LlamaDoc2PDF."""

import os
import tempfile
from pathlib import Path

# Corrected relative imports
from ..config import config
from ..core.engine import ConversionContext, ConversionResult, InputSource
from ..core.exceptions import ConversionError
from ..core.scraper import ScrapedContent, StealthScraper
from rich.console import Console

console = Console()


class WebProcessor:
    """Process web pages for conversion to PDF."""

    def __init__(self):
        """Initialize the web processor."""
        pass

    async def process(
        self, source: InputSource, output_path: Path, ctx: ConversionContext
    ) -> ConversionResult:
        """
        Process a web page.

        Args:
            source: Input source (should be a URL)
            output_path: Path to output file
            ctx: Conversion context

        Returns:
            ConversionResult object
        """
        if not source.is_url:
            raise ConversionError(f"Expected a URL source, got {source.detected_type}")

        url = source.url
        take_screenshot = ctx.options.extra_options.get("screenshot", True)

        try:
            # Extract options from context
            options = {
                "screenshot": take_screenshot,
                "extract_links": ctx.options.extra_options.get("extract_links", True),
                "extract_text": ctx.options.extra_options.get("extract_text", True),
                "auto_scroll": config.scraping.auto_scroll,
                "screenshot_dir": ctx.options.extra_options.get("screenshot_dir", "screenshots"),
            }

            # Create output directory if needed
            output_path.parent.mkdir(parents=True, exist_ok=True)

            # Create scraper and scrape the URL
            async with StealthScraper(
                headless=config.scraping.headless,
                use_stealth=config.scraping.stealth_mode,
            ) as scraper:
                content = await scraper.scrape(url, options)

                # Convert the scraped content to PDF
                pdf_path = await self._content_to_pdf(content, output_path, ctx)

                return ConversionResult(
                    output_path=pdf_path,
                    success=True,
                    meta={
                        "url": url,
                        "title": content.title,
                        "links": len(content.links),
                        "images": len(content.images),
                        "screenshot_path": (
                            str(content.screenshot_path) if content.screenshot_path else None
                        ),
                    },
                )

        except Exception as e:
            error_msg = f"Failed to process URL {url}: {str(e)}"
            console.print(f"[bold red]Error:[/bold red] {error_msg}")

            # If we have a partial result, try to save it
            try:
                pdf_path = await self._create_error_pdf(url, output_path, str(e))
                return ConversionResult(
                    output_path=pdf_path,
                    success=False,
                    error=e,
                    meta={
                        "url": url,
                        "error_message": str(e),
                    },
                )
            except:
                # If even the error PDF fails, return a failed result
                return ConversionResult(
                    output_path=output_path,
                    success=False,
                    error=e,
                    meta={
                        "url": url,
                        "error_message": str(e),
                    },
                )

    async def _content_to_pdf(
        self, content: ScrapedContent, output_path: Path, ctx: ConversionContext
    ) -> Path:
        """
        Convert scraped content to PDF.

        This can be done either by using the screenshot, or by rendering the HTML content.

        Args:
            content: Scraped content
            output_path: Output path
            ctx: Conversion context

        Returns:
            Path to the generated PDF
        """
        if content.screenshot_path and ctx.options.extra_options.get(
            "use_screenshot_for_pdf", True
        ):
            # Corrected relative import
            from .document import DocumentProcessor

            document_processor = DocumentProcessor()
            image_source = InputSource(content.screenshot_path)

            # Convert the screenshot to PDF and save to output path
            result = await document_processor.process(image_source, output_path, ctx)
            if not result.success:
                raise ConversionError(f"Failed to convert screenshot to PDF: {result.error}")

            return result.output_path
        else:
            # Corrected relative import
            from .document import DocumentProcessor

            # Otherwise, create PDF from HTML content
            html_path = await self._save_html_content(content)

            try:
                document_processor = DocumentProcessor()
                html_source = InputSource(html_path)

                # Convert the HTML to PDF and save to output path
                result = await document_processor.process(html_source, output_path, ctx)

                # Clean up the temporary HTML file
                os.unlink(html_path)

                if not result.success:
                    raise ConversionError(f"Failed to convert HTML to PDF: {result.error}")

                return result.output_path
            except Exception as e:
                # Clean up the temporary HTML file
                os.unlink(html_path)
                raise e

    async def _save_html_content(self, content: ScrapedContent) -> Path:
        """
        Save HTML content to a temporary file.

        Args:
            content: Scraped content

        Returns:
            Path to the temporary HTML file
        """
        # Create temporary HTML file
        with tempfile.NamedTemporaryFile(suffix=".html", delete=False) as tmp:
            # Write HTML content
            tmp.write(content.html.encode("utf-8"))
            return Path(tmp.name)

    async def _create_error_pdf(self, url: str, output_path: Path, error_message: str) -> Path:
        """
        Create a PDF indicating an error occurred during processing.

        Args:
            url: URL that failed
            output_path: Output path
            error_message: Error message

        Returns:
            Path to the generated error PDF
        """
        # Create HTML content for the error
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>Error Processing URL</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20mm; }}
                h1 {{ color: #d9534f; }}
                .url {{ color: #0275d8; word-break: break-all; }}
                .error {{ color: #d9534f; background-color: #f9f2f4; padding: 10px; border-radius: 4px; }}
            </style>
        </head>
        <body>
            <h1>Error Processing URL</h1>
            <p>An error occurred while processing the following URL:</p>
            <p class="url">{url}</p>
            <h2>Error Message:</h2>
            <div class="error">{error_message}</div>
            <hr>
            <p>Generated by LlamaDoc2PDF</p>
        </body>
        </html>
        """

        # Create temporary HTML file
        with tempfile.NamedTemporaryFile(suffix=".html", delete=False) as tmp:
            tmp.write(html_content.encode("utf-8"))
            html_path = Path(tmp.name)

        try:
            # Corrected relative import
            from .document import DocumentProcessor

            document_processor = DocumentProcessor()
            html_source = InputSource(html_path)

            # Create a simple context
            class SimpleContext:
                def __init__(self):
                    self.options = type("Options", (), {"extra_options": {}})
                    self.stats = {
                        "processed_files": 0,
                        "success_count": 0,
                        "error_count": 0,
                    }

            # Convert the HTML to PDF and save to output path
            result = await document_processor.process(html_source, output_path, SimpleContext())

            # Clean up the temporary HTML file
            os.unlink(html_path)

            if not result.success:
                raise ConversionError(f"Failed to create error PDF: {result.error}")

            return result.output_path
        except Exception as e:
            # Clean up the temporary HTML file
            os.unlink(html_path)
            raise e
