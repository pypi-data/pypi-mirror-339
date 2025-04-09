"""Document processing functionality for LlamaDoc2PDF."""

import os
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Any, Dict, Union

from llamadoc2pdf.config.settings import config
from llamadoc2pdf.core.engine import ConversionContext, ConversionResult, InputSource
from llamadoc2pdf.core.exceptions import (
    ConversionError,
    MissingDependencyError,
    UnsupportedFormatError,
)
from rich.console import Console

# Import optional dependencies
try:
    import markdown

    MARKDOWN_AVAILABLE = True
except ImportError:
    MARKDOWN_AVAILABLE = False

try:
    import img2pdf

    IMG2PDF_AVAILABLE = True
except ImportError:
    IMG2PDF_AVAILABLE = False

try:
    from PIL import Image

    PILLOW_AVAILABLE = True
except ImportError:
    PILLOW_AVAILABLE = False

console = Console()


class DocumentProcessor:
    """Process document files of various formats."""

    def __init__(self):
        self._converters = {
            "txt": self._convert_text,
            "md": self._convert_markdown,
            "doc": self._convert_office_document,
            "docx": self._convert_office_document,
            "html": self._convert_html,
            "rtf": self._convert_office_document,
            "odt": self._convert_office_document,
            "jpg": self._convert_image,
            "jpeg": self._convert_image,
            "png": self._convert_image,
            "gif": self._convert_image,
        }

    async def process(
        self, source: InputSource, output_path: Path, ctx: ConversionContext
    ) -> ConversionResult:
        """
        Process an input document file.

        Args:
            source: Input source
            output_path: Path to output file
            ctx: Conversion context

        Returns:
            ConversionResult object
        """
        if not source.is_file:
            raise ConversionError(f"Expected a file source, got {source.detected_type}")

        input_path = source.path
        file_type = source.file_type

        if file_type not in self._converters:
            raise UnsupportedFormatError(file_type)

        try:
            # Create output directory if needed
            output_path.parent.mkdir(parents=True, exist_ok=True)

            # Extract options from context
            options = {
                "page_size": config.conversion.page_size,
                "margin_top": config.conversion.margin_top,
                "margin_right": config.conversion.margin_right,
                "margin_bottom": config.conversion.margin_bottom,
                "margin_left": config.conversion.margin_left,
                "enable_toc": config.conversion.enable_toc,
                "timeout": config.conversion.timeout,
                "custom_css": config.conversion.custom_css,
            }

            # Add any extra options from context
            options.update(ctx.options.extra_options)

            # Perform conversion
            result_path = await self._converters[file_type](input_path, output_path, options)

            # Create successful result
            return ConversionResult(
                output_path=Path(result_path),
                success=True,
                meta={
                    "input_path": str(input_path),
                    "input_type": file_type,
                    "output_format": output_path.suffix[1:],
                },
            )

        except Exception as e:
            error_msg = f"Failed to convert {input_path}: {str(e)}"
            console.print(f"[bold red]Error:[/bold red] {error_msg}")

            # Create failed result
            return ConversionResult(
                output_path=output_path,
                success=False,
                error=e,
                meta={
                    "input_path": str(input_path),
                    "input_type": file_type,
                    "error_message": str(e),
                },
            )

    async def _convert_text(
        self, input_path: Path, output_path: Path, options: Dict[str, Any]
    ) -> str:
        """Convert a text file to PDF."""
        try:
            with open(input_path, "r", encoding="utf-8") as f:
                text = f.read()

            # Create simple HTML from text
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
                <title>{input_path.stem}</title>
                <style>
                    body {{ font-family: Arial, sans-serif; margin: {options['margin_top']}mm {options['margin_right']}mm {options['margin_bottom']}mm {options['margin_left']}mm; }}
                    pre {{ white-space: pre-wrap; }}
                </style>
            </head>
            <body>
                <pre>{text}</pre>
            </body>
            </html>
            """

            # Save to temporary HTML file
            with tempfile.NamedTemporaryFile(suffix=".html", delete=False) as tmp:
                tmp.write(html_content.encode("utf-8"))
                tmp_path = tmp.name

            # Convert HTML to PDF
            await self._html_to_pdf(tmp_path, output_path, options)

            # Cleanup
            os.unlink(tmp_path)

            return str(output_path)
        except Exception as e:
            console.print(
                f"[yellow]Warning:[/yellow] Text conversion failed, using fallback: {str(e)}"
            )
            return await self._fallback_conversion(input_path, output_path, options)

    async def _convert_markdown(
        self, input_path: Path, output_path: Path, options: Dict[str, Any]
    ) -> str:
        """Convert a Markdown file to PDF."""
        if not MARKDOWN_AVAILABLE:
            console.print(
                "[yellow]Warning:[/yellow] Markdown module not available, using fallback."
            )
            return await self._fallback_conversion(input_path, output_path, options)

        try:
            with open(input_path, "r", encoding="utf-8") as f:
                md_content = f.read()

            # Convert markdown to HTML
            html_content = markdown.markdown(
                md_content, extensions=["extra", "codehilite", "tables", "toc"]
            )

            # Create full HTML document
            html_doc = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
                <title>{input_path.stem}</title>
                <style>
                    body {{ font-family: Arial, sans-serif; margin: {options['margin_top']}mm {options['margin_right']}mm {options['margin_bottom']}mm {options['margin_left']}mm; }}
                    h1, h2, h3, h4, h5, h6 {{ color: #333; }}
                    pre, code {{ background-color: #f5f5f5; padding: 5px; border-radius: 3px; }}
                    img {{ max-width: 100%; }}
                    table {{ border-collapse: collapse; width: 100%; }}
                    table, th, td {{ border: 1px solid #ddd; padding: 8px; }}
                </style>
                {f'<link rel="stylesheet" href="{options["custom_css"]}">' if options.get("custom_css") else ''}
            </head>
            <body>
                <h1>{input_path.stem}</h1>
                {html_content}
            </body>
            </html>
            """

            # Save to temporary HTML file
            with tempfile.NamedTemporaryFile(suffix=".html", delete=False) as tmp:
                tmp.write(html_doc.encode("utf-8"))
                tmp_path = tmp.name

            # Convert HTML to PDF
            await self._html_to_pdf(tmp_path, output_path, options)

            # Cleanup
            os.unlink(tmp_path)

            return str(output_path)
        except Exception as e:
            console.print(
                f"[yellow]Warning:[/yellow] Markdown conversion failed, using fallback: {str(e)}"
            )
            return await self._fallback_conversion(input_path, output_path, options)

    async def _convert_office_document(
        self, input_path: Path, output_path: Path, options: Dict[str, Any]
    ) -> str:
        """Convert an office document to PDF using LibreOffice or other available tools."""
        # Try LibreOffice if available
        if await self._try_libreoffice_conversion(input_path, output_path):
            return str(output_path)

        # Fallback
        return await self._fallback_conversion(input_path, output_path, options)

    async def _convert_image(
        self, input_path: Path, output_path: Path, options: Dict[str, Any]
    ) -> str:
        """Convert an image file to PDF."""
        if not (IMG2PDF_AVAILABLE or PILLOW_AVAILABLE):
            raise MissingDependencyError("img2pdf or Pillow is required for image conversion")

        try:
            # Try using img2pdf first
            if IMG2PDF_AVAILABLE:
                try:
                    with open(output_path, "wb") as f:
                        f.write(img2pdf.convert(str(input_path)))
                    return str(output_path)
                except Exception as img2pdf_error:
                    console.print(
                        f"[yellow]Warning:[/yellow] img2pdf failed, trying PIL: {str(img2pdf_error)}"
                    )

            # Fallback to PIL
            if PILLOW_AVAILABLE:
                image = Image.open(input_path)
                rgb_image = image.convert("RGB")
                rgb_image.save(output_path, format="PDF")
                return str(output_path)
            else:
                raise MissingDependencyError("Pillow is required for image conversion")

        except Exception as e:
            console.print(
                f"[yellow]Warning:[/yellow] Image conversion failed, using fallback: {str(e)}"
            )
            return await self._fallback_conversion(input_path, output_path, options)

    async def _convert_html(
        self, input_path: Path, output_path: Path, options: Dict[str, Any]
    ) -> str:
        """Convert an HTML file to PDF."""
        try:
            await self._html_to_pdf(str(input_path), output_path, options)
            return str(output_path)
        except Exception as e:
            console.print(
                f"[yellow]Warning:[/yellow] HTML conversion failed, using fallback: {str(e)}"
            )
            return await self._fallback_conversion(input_path, output_path, options)

    async def _try_libreoffice_conversion(self, input_path: Path, output_path: Path) -> bool:
        """Try to convert document using LibreOffice."""
        libreoffice = config.libreoffice_path
        if not libreoffice:
            # Try to find LibreOffice/OpenOffice
            possible_paths = [
                "/usr/bin/soffice",
                "/usr/bin/libreoffice",
                "/Applications/LibreOffice.app/Contents/MacOS/soffice",
                r"C:\Program Files\LibreOffice\program\soffice.exe",
                r"C:\Program Files (x86)\LibreOffice\program\soffice.exe",
            ]

            for path in possible_paths:
                if os.path.exists(path):
                    libreoffice = path
                    break

        if libreoffice:
            try:
                # Use temporary directory for output
                temp_dir = tempfile.mkdtemp()

                # Run LibreOffice to convert
                subprocess.run(
                    [
                        libreoffice,
                        "--headless",
                        "--convert-to",
                        "pdf",
                        "--outdir",
                        temp_dir,
                        str(input_path),
                    ],
                    check=True,
                    timeout=config.conversion.timeout,
                )

                # Find the output file
                temp_pdf = os.path.join(temp_dir, f"{input_path.stem}.pdf")

                # Copy to final destination
                if os.path.exists(temp_pdf):
                    shutil.copy2(temp_pdf, output_path)
                    shutil.rmtree(temp_dir)
                    return True
                else:
                    console.print(
                        f"[yellow]LibreOffice did not create output file:[/yellow] {temp_pdf}"
                    )
                    shutil.rmtree(temp_dir)
            except Exception as e:
                console.print(f"[yellow]LibreOffice conversion failed:[/yellow] {str(e)}")
                if "temp_dir" in locals():
                    shutil.rmtree(temp_dir)

        return False

    async def _html_to_pdf(
        self, html_path: Union[str, Path], output_path: Path, options: Dict[str, Any]
    ) -> None:
        """Convert HTML to PDF using wkhtmltopdf or other available methods."""
        # Try wkhtmltopdf if available
        wkhtmltopdf = config.wkhtmltopdf_path
        if not wkhtmltopdf:
            # Try to find wkhtmltopdf
            possible_paths = [
                "/usr/bin/wkhtmltopdf",
                "/usr/local/bin/wkhtmltopdf",
                r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe",
            ]

            for path in possible_paths:
                if os.path.exists(path):
                    wkhtmltopdf = path
                    break

        if wkhtmltopdf:
            try:
                cmd = [
                    wkhtmltopdf,
                    "--page-size",
                    options["page_size"],
                    "--margin-top",
                    str(options["margin_top"]),
                    "--margin-right",
                    str(options["margin_right"]),
                    "--margin-bottom",
                    str(options["margin_bottom"]),
                    "--margin-left",
                    str(options["margin_left"]),
                ]

                if options.get("enable_toc", False):
                    cmd.append("--toc")

                if options.get("custom_css"):
                    cmd.extend(["--user-style-sheet", options["custom_css"]])

                cmd.extend([str(html_path), str(output_path)])

                subprocess.run(cmd, check=True, timeout=options.get("timeout", 60))
                return
            except Exception as e:
                console.print(f"[yellow]wkhtmltopdf conversion failed:[/yellow] {str(e)}")
                raise

    async def _fallback_conversion(
        self, input_path: Path, output_path: Path, options: Dict[str, Any]
    ) -> str:
        """Fallback conversion method for when other methods fail."""
        # Create output directory if it doesn't exist
        output_path.parent.mkdir(exist_ok=True, parents=True)

        try:
            # Read some content from the input file for the PDF
            try:
                with open(input_path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read(1000)  # Read up to 1000 chars
            except:
                content = f"Content of {input_path.name}"

            # Create a minimal PDF with the content
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
                <title>Fallback Conversion: {input_path.name}</title>
                <style>
                    body {{ font-family: Arial, sans-serif; margin: 20mm; }}
                    .filename {{ color: #555; font-weight: bold; }}
                    .content {{ margin-top: 20px; font-family: monospace; white-space: pre-wrap; }}
                </style>
            </head>
            <body>
                <h1>Document Conversion (Fallback Method)</h1>
                <div class="filename">Original file: {input_path.name}</div>
                <div class="content">{content}</div>
            </body>
            </html>
            """

            # Save to temporary HTML file
            with tempfile.NamedTemporaryFile(suffix=".html", delete=False) as tmp:
                tmp.write(html_content.encode("utf-8"))
                tmp_path = tmp.name

            try:
                # Try to convert HTML to PDF
                await self._html_to_pdf(tmp_path, output_path, options)
            except:
                # If that fails, create a really minimal PDF
                with open(output_path, "w") as f:
                    f.write("%PDF-1.7\n1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n")
                    f.write("2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n")
                    f.write("3 0 obj\n<< /Type /Page /Parent 2 0 R /Resources << >> ")
                    f.write("/MediaBox [0 0 612 792] /Contents 4 0 R >>\nendobj\n")
                    f.write("4 0 obj\n<< /Length 0 >>\nstream\nendstream\nendobj\n")
                    f.write("xref\n0 5\n0000000000 65535 f\n0000000010 00000 n\n")
                    f.write("0000000060 00000 n\n0000000120 00000 n\n0000000210 00000 n\n")
                    f.write("trailer\n<< /Size 5 /Root 1 0 R >>\nstartxref\n260\n%%EOF\n")

            # Cleanup
            os.unlink(tmp_path)

            return str(output_path)
        except:
            # Last resort - create an empty but valid PDF
            with open(output_path, "w") as f:
                f.write("%PDF-1.7\n1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n")
                f.write("2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n")
                f.write("3 0 obj\n<< /Type /Page /Parent 2 0 R /Resources << >> ")
                f.write("/MediaBox [0 0 612 792] /Contents 4 0 R >>\nendobj\n")
                f.write("4 0 obj\n<< /Length 0 >>\nstream\nendstream\nendobj\n")
                f.write("xref\n0 5\n0000000000 65535 f\n0000000010 00000 n\n")
                f.write("0000000060 00000 n\n0000000120 00000 n\n0000000210 00000 n\n")
                f.write("trailer\n<< /Size 5 /Root 1 0 R >>\nstartxref\n260\n%%EOF\n")
