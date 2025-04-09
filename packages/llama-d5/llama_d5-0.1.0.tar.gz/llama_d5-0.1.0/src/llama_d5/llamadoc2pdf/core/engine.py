"""Unified conversion engine for llamadoc2pdf."""

import asyncio
import logging
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

try:
    from rich.console import Console

    RICH_AVAILABLE = True
    console = Console()
except ImportError:
    RICH_AVAILABLE = False
    console = None

from llamadoc2pdf.processors.document import DocumentProcessor
from llamadoc2pdf.processors.webpage import WebProcessor

# Set up logging
logger = logging.getLogger("llamadoc2pdf.engine")


class InputSource:
    """Unified representation of an input source (file, URL, etc.)"""

    def __init__(self, source: Union[str, Path, bytes], source_type: Optional[str] = None):
        self.raw_source = source
        self.detected_type = source_type or self._detect_type(source)

    def _detect_type(self, source) -> str:
        """Auto-detect the type of input source"""
        if isinstance(source, bytes):
            return "content"
        elif isinstance(source, Path) or (isinstance(source, str) and Path(source).exists()):
            path = Path(source) if isinstance(source, str) else source
            return f"file:{path.suffix.lower()[1:]}" if path.suffix else "file:unknown"
        elif isinstance(source, str) and (
            source.startswith("http://") or source.startswith("https://")
        ):
            return "url"
        else:
            return "unknown"

    @property
    def is_file(self) -> bool:
        return self.detected_type.startswith("file:")

    @property
    def is_url(self) -> bool:
        return self.detected_type == "url"

    @property
    def is_content(self) -> bool:
        return self.detected_type == "content"

    @property
    def file_type(self) -> Optional[str]:
        return self.detected_type.split(":", 1)[1] if self.is_file else None

    @property
    def path(self) -> Optional[Path]:
        if self.is_file:
            return Path(self.raw_source) if isinstance(self.raw_source, str) else self.raw_source
        return None

    @property
    def url(self) -> Optional[str]:
        return self.raw_source if self.is_url else None

    @property
    def content(self) -> Optional[bytes]:
        return self.raw_source if self.is_content else None


class ConversionResult:
    """Result of a conversion operation"""

    def __init__(
        self,
        output_path: Path,
        success: bool = True,
        error: Optional[Exception] = None,
        meta: Optional[Dict[str, Any]] = None,
    ):
        self.output_path = output_path
        self.success = success
        self.error = error
        self.meta = meta or {}


class ConversionOptions:
    """Unified conversion options"""

    def __init__(
        self,
        output_format: str = "pdf",
        quality: str = "high",
        use_llm: bool = False,
        llm_provider: str = "openai",
        parallel: int = 4,
        verbose: bool = False,
        **kwargs,
    ):
        self.output_format = output_format
        self.quality = quality
        self.use_llm = use_llm
        self.llm_provider = llm_provider
        self.parallel = parallel
        self.verbose = verbose
        self.extra_options = kwargs


class ConversionContext:
    """Context manager for conversion operations"""

    def __init__(self, options: ConversionOptions):
        self.options = options
        self.stats = {
            "start_time": None,
            "end_time": None,
            "processed_files": 0,
            "success_count": 0,
            "error_count": 0,
            "warnings": [],
        }

    def __enter__(self):
        self.stats["start_time"] = time.time()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stats["end_time"] = time.time()
        if self.options.verbose:
            self._print_summary()

    def _print_summary(self):
        """Print a summary of the conversion operation"""
        duration = self.stats["end_time"] - self.stats["start_time"]
        if RICH_AVAILABLE and console:
            console.print("\n[bold]Conversion Summary:[/bold]")
            console.print(
                f"✅ [green]{self.stats['success_count']} files converted successfully[/green]"
            )
            if self.stats["error_count"] > 0:
                console.print(f"❌ [red]{self.stats['error_count']} files failed[/red]")
            console.print(f"⏱️ Total time: [cyan]{duration:.2f}[/cyan] seconds")
        else:
            print("\nConversion Summary:")
            print(f"- {self.stats['success_count']} files converted successfully")
            if self.stats["error_count"] > 0:
                print(f"- {self.stats['error_count']} files failed")
            print(f"- Total time: {duration:.2f} seconds")


class ConversionEngine:
    """Orchestrates all conversion types with plugin architecture"""

    def __init__(self):
        # Import processors here to avoid circular imports

        self.document_processor = DocumentProcessor()
        self.web_processor = WebProcessor()

        # Initialize LLM orchestrator if available
        try:
            from ..llm_integration import LLMOrchestrator

            self.llm = LLMOrchestrator()
            self.llm_available = True
        except (ImportError, ModuleNotFoundError):
            self.llm_available = False

    async def convert(
        self,
        source: Union[str, Path, bytes, InputSource],
        output: Optional[Union[str, Path]] = None,
        options: Optional[Union[Dict[str, Any], ConversionOptions]] = None,
    ) -> ConversionResult:
        """
        Unified conversion method for all input types

        Args:
            source: Input source (file path, URL, or raw content)
            output: Output path (optional, auto-generated if not provided)
            options: Conversion options

        Returns:
            ConversionResult object
        """
        # Normalize inputs
        if not isinstance(source, InputSource):
            source = InputSource(source)

        if isinstance(options, dict):
            options = ConversionOptions(**options)
        elif options is None:
            options = ConversionOptions()

        # Set default output path if not provided
        if output is None:
            if source.is_file:
                output = source.path.with_suffix(f".{options.output_format}")
            else:
                output = Path(f"llamadoc_output.{options.output_format}")
        elif isinstance(output, str):
            output = Path(output)

        # Ensure output directory exists
        output.parent.mkdir(parents=True, exist_ok=True)

        try:
            # Select appropriate processor based on input type
            processor = self._select_processor(source)

            # Create conversion context
            with ConversionContext(options) as ctx:
                # Process the input
                result = await processor.process(source, output, ctx)

                # Apply LLM enhancement if requested
                if options.use_llm and result.success and self.llm_available:
                    try:
                        result = await self.llm.enhance(result, ctx)
                    except Exception as e:
                        if RICH_AVAILABLE and console:
                            console.print(
                                f"[yellow]Warning:[/yellow] LLM enhancement failed: {str(e)}"
                            )
                        else:
                            print(f"Warning: LLM enhancement failed: {str(e)}")
                elif options.use_llm and not self.llm_available:
                    logger.warning("LLM enhancement requested but LLM integration is not available")

                # Update stats
                ctx.stats["processed_files"] += 1
                if result.success:
                    ctx.stats["success_count"] += 1
                else:
                    ctx.stats["error_count"] += 1

            return result

        except Exception as e:
            error_msg = f"Conversion failed: {str(e)}"
            if RICH_AVAILABLE and console:
                console.print(f"[bold red]Error:[/bold red] {error_msg}")
            else:
                print(f"Error: {error_msg}")
            return ConversionResult(output, success=False, error=e)

    def _select_processor(self, source: InputSource):
        """Select the appropriate processor for the input type"""
        if source.is_file:
            # Check if it's an image
            image_types = ("jpg", "jpeg", "png", "gif", "bmp", "tiff", "webp")
            if source.file_type in image_types:
                # Use document processor for images too
                return self.document_processor
            else:
                return self.document_processor
        elif source.is_url:
            return self.web_processor
        else:
            # Default to document processor for raw content
            return self.document_processor

    async def batch_convert(
        self,
        sources: List[Union[str, Path, bytes, InputSource]],
        output_dir: Union[str, Path],
        options: Optional[Union[Dict[str, Any], ConversionOptions]] = None,
    ) -> List[ConversionResult]:
        """
        Convert multiple sources in parallel

        Args:
            sources: List of input sources
            output_dir: Output directory
            options: Conversion options

        Returns:
            List of ConversionResult objects
        """
        if isinstance(output_dir, str):
            output_dir = Path(output_dir)

        if isinstance(options, dict):
            options = ConversionOptions(**options)
        elif options is None:
            options = ConversionOptions()

        # Create output directory
        output_dir.mkdir(parents=True, exist_ok=True)

        # Normalize all sources to InputSource objects
        sources = [src if isinstance(src, InputSource) else InputSource(src) for src in sources]

        # Create a list of tasks to run
        tasks = []
        for i, source in enumerate(sources):
            # Generate output path
            if source.is_file:
                output_name = source.path.name
                output_path = output_dir / f"{source.path.stem}.{options.output_format}"
            elif source.is_url:
                from urllib.parse import urlparse

                parsed_url = urlparse(source.url)
                domain = parsed_url.netloc.replace(".", "_")
                path = parsed_url.path.replace("/", "_")
                output_name = f"{domain}{path or 'index'}"
                output_path = output_dir / f"{output_name}.{options.output_format}"
            else:
                output_path = output_dir / f"content_{i}.{options.output_format}"

            # Create the task
            task = self.convert(source, output_path, options)
            tasks.append(task)

        # Run tasks in parallel, limiting concurrency
        parallel_count = min(options.parallel, len(tasks))
        batches = [tasks[i : i + parallel_count] for i in range(0, len(tasks), parallel_count)]

        results = []
        for batch in batches:
            batch_results = await asyncio.gather(*batch, return_exceptions=True)

            # Process batch results
            for i, result in enumerate(batch_results):
                if isinstance(result, Exception):
                    # If an exception was raised, create a failed result
                    idx = len(results)
                    source = sources[idx]
                    if source.is_file:
                        output_path = output_dir / f"{source.path.stem}.{options.output_format}"
                    else:
                        output_path = output_dir / f"failed_{idx}.{options.output_format}"
                    results.append(ConversionResult(output_path, success=False, error=result))
                else:
                    results.append(result)

        return results
