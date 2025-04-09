"""Media processing functionality for LlamaDoc2PDF."""

from pathlib import Path

# Corrected relative imports
from ..core.engine import ConversionContext, ConversionResult, InputSource
from ..core.exceptions import ConversionError, MissingDependencyError
from rich.console import Console

# Import optional dependencies
try:
    import img2pdf

    IMG2PDF_AVAILABLE = True
except ImportError:
    IMG2PDF_AVAILABLE = False

try:
    from PIL import Image, ImageEnhance

    PILLOW_AVAILABLE = True
except ImportError:
    PILLOW_AVAILABLE = False

console = Console()


class ImageProcessor:
    """Process image files."""

    def __init__(self):
        """Initialize the image processor."""
        if not (IMG2PDF_AVAILABLE or PILLOW_AVAILABLE):
            console.print(
                "[yellow]Warning:[/yellow] Both img2pdf and Pillow are missing. Image processing will be limited."
            )

    async def process(
        self, source: InputSource, output_path: Path, ctx: ConversionContext
    ) -> ConversionResult:
        """
        Process an image file.

        Args:
            source: Input source (should be an image file)
            output_path: Path to output file
            ctx: Conversion context

        Returns:
            ConversionResult object
        """
        if not source.is_file:
            raise ConversionError(f"Expected a file source, got {source.detected_type}")

        input_path = source.path

        # Check if this is an image file
        if source.file_type not in ("jpg", "jpeg", "png", "gif", "bmp", "tiff", "webp"):
            raise ConversionError(f"Expected an image file, got {source.file_type}")

        try:
            # Create output directory if needed
            output_path.parent.mkdir(parents=True, exist_ok=True)

            # Determine output format
            output_format = output_path.suffix.lower()[1:]

            # Process the image
            if output_format == "pdf":
                result_path = await self._convert_to_pdf(input_path, output_path, ctx.options)
            else:
                result_path = await self._convert_image(
                    input_path, output_path, output_format, ctx.options
                )

            # Create successful result
            return ConversionResult(
                output_path=Path(result_path),
                success=True,
                meta={
                    "input_path": str(input_path),
                    "input_type": source.file_type,
                    "output_format": output_format,
                },
            )

        except Exception as e:
            error_msg = f"Failed to process image {input_path}: {str(e)}"
            console.print(f"[bold red]Error:[/bold red] {error_msg}")

            # Create failed result
            return ConversionResult(
                output_path=output_path,
                success=False,
                error=e,
                meta={
                    "input_path": str(input_path),
                    "input_type": source.file_type,
                    "error_message": str(e),
                },
            )

    async def _convert_to_pdf(self, input_path: Path, output_path: Path, options) -> str:
        """
        Convert an image to PDF.

        Args:
            input_path: Path to input image
            output_path: Path to output PDF
            options: Conversion options

        Returns:
            Path to the generated PDF
        """
        # Try img2pdf first if available
        if IMG2PDF_AVAILABLE:
            try:
                with open(output_path, "wb") as f:
                    f.write(img2pdf.convert(str(input_path)))
                return str(output_path)
            except Exception as e:
                console.print(f"[yellow]Warning:[/yellow] img2pdf conversion failed: {str(e)}")

        # Fall back to PIL
        if PILLOW_AVAILABLE:
            try:
                image = Image.open(input_path)

                # Apply enhancements based on quality setting
                quality = options.quality.value
                if quality in ("high", "ultra"):
                    # Enhance the image
                    image = self._enhance_image(image, quality)

                # Convert to RGB (required for PDF)
                if image.mode != "RGB":
                    image = image.convert("RGB")

                # Save as PDF
                image.save(output_path, format="PDF")
                return str(output_path)
            except Exception as e:
                console.print(f"[yellow]Warning:[/yellow] PIL conversion failed: {str(e)}")

        raise MissingDependencyError("img2pdf or Pillow is required for image to PDF conversion")

    async def _convert_image(
        self, input_path: Path, output_path: Path, output_format: str, options
    ) -> str:
        """
        Convert an image to another image format.

        Args:
            input_path: Path to input image
            output_path: Path to output image
            output_format: Output format (e.g., 'png', 'jpg')
            options: Conversion options

        Returns:
            Path to the generated image
        """
        if not PILLOW_AVAILABLE:
            raise MissingDependencyError("Pillow is required for image conversion")

        try:
            # Open the image
            image = Image.open(input_path)

            # Apply enhancements based on quality setting
            quality = options.quality.value
            if quality in ("high", "ultra"):
                # Enhance the image
                image = self._enhance_image(image, quality)

            # Convert color mode if needed
            if output_format in ("jpg", "jpeg") and image.mode != "RGB":
                image = image.convert("RGB")

            # Set quality for JPEG images
            save_options = {}
            if output_format in ("jpg", "jpeg"):
                if quality == "low":
                    save_options["quality"] = 65
                elif quality == "medium":
                    save_options["quality"] = 80
                elif quality == "high":
                    save_options["quality"] = 90
                elif quality == "ultra":
                    save_options["quality"] = 95

            # Save the image
            image.save(output_path, format=output_format.upper(), **save_options)
            return str(output_path)

        except Exception as e:
            raise ConversionError(f"Image conversion failed: {str(e)}")

    def _enhance_image(self, image, quality):
        """
        Apply enhancements to an image based on quality setting.

        Args:
            image: PIL Image to enhance
            quality: Quality setting ('low', 'medium', 'high', 'ultra')

        Returns:
            Enhanced PIL Image
        """
        try:
            # Skip for low quality
            if quality == "low":
                return image

            # Apply basic enhancements for medium quality
            if quality == "medium":
                return image

            # Apply stronger enhancements for high quality
            if quality == "high":
                # Enhance contrast slightly
                enhancer = ImageEnhance.Contrast(image)
                image = enhancer.enhance(1.2)

                # Enhance sharpness slightly
                enhancer = ImageEnhance.Sharpness(image)
                image = enhancer.enhance(1.1)

                return image

            # Apply maximum enhancements for ultra quality
            if quality == "ultra":
                # Enhance contrast
                enhancer = ImageEnhance.Contrast(image)
                image = enhancer.enhance(1.3)

                # Enhance color
                enhancer = ImageEnhance.Color(image)
                image = enhancer.enhance(1.1)

                # Enhance sharpness
                enhancer = ImageEnhance.Sharpness(image)
                image = enhancer.enhance(1.2)

                return image

            # Default case
            return image

        except Exception as e:
            console.print(f"[yellow]Warning:[/yellow] Image enhancement failed: {str(e)}")
            return image
