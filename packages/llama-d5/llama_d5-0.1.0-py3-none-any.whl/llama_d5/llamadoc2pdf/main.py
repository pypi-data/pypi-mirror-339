"""Command-line interface for LlamaDoc2PDF."""

import asyncio
import sys
import time
import os  # Added for path checks in info command
from pathlib import Path
from typing import List, Optional
from urllib.parse import urlparse

import typer

# Corrected import: Use settings from .config.settings
from llamadoc2pdf.config.settings import QualityPreset, settings

# Use relative imports for engine and exceptions
from .core.engine import ConversionEngine, ConversionOptions, InputSource
from .core.exceptions import AIError

# Corrected import: Use EnhancedScraper from .core.scraper
from .core.scraper import EnhancedScraper

from rich.align import Align
from rich.console import Console
from rich.table import Table
from rich.panel import Panel  # Added for info and scrape commands
from rich.layout import Layout  # Added for info command

# from rich.confirm import Confirm # Removed unused import

app = typer.Typer(help="LlamaDoc2PDF - The Ultimate Document Toolkit")
console = Console()

# Llama ASCII art with color
LLAMA_ASCII = """
[bold magenta]                 /\\/\\
               /    \\
              /      \\   
             [bright_magenta] /*/[/bright_magenta][bright_yellow]oo[/bright_yellow][bright_magenta]\\*\\[/bright_magenta]   [bold magenta]🦙
             [/bold magenta]|        |   
             |  L L  /    
            /|  UU  |\\   
           / |  M M | \\  
          *  |  A A |  *  
             |  !   |     
             |      |     
             |      |   
[/bold magenta]"""


def animate_llama():
    """Display an animated llama at startup."""
    frames = [
        "[bold magenta]   🦙 [/bold magenta]",
        "[bold magenta]  🦙  [/bold magenta]",
        "[bold magenta] 🦙   [/bold magenta]",
        "[bold magenta]🦙    [/bold magenta]",
        "[bold magenta] 🦙   [/bold magenta]",
        "[bold magenta]  🦙  [/bold magenta]",
        "[bold magenta]   🦙 [/bold magenta]",
        "[bold magenta]    🦙[/bold magenta]",
    ]

    console.print("\n" + LLAMA_ASCII + "\n")
    console.print(Align.center("[bold yellow]Loading Supreme Llama Interface...[/bold yellow]"))

    # Use console.status for cleaner loading indication
    with console.status("[bold magenta]Llama is preparing...[/bold magenta]", spinner="dots"):
        time.sleep(1)  # Simplified animation for brevity

    console.print("\n")


@app.command(name="convert")  # Renamed super_convert to convert
def convert_command(
    inputs: List[str] = typer.Argument(..., help="Files/URLs/Directories to process"),
    output: Optional[str] = typer.Option(None, "--output", "-o", help="Output directory/file"),
    format: str = typer.Option("pdf", "--format", "-f", help="Output format: pdf, docx, html"),
    enhance: bool = typer.Option(False, "--enhance", "-e", help="Use AI enhancement"),
    recursive: bool = typer.Option(
        False, "--recursive", "-r", help="Process directories recursively"
    ),
    parallel: int = typer.Option(4, "--parallel", "-p", help="Parallel workers"),
    quality: QualityPreset = typer.Option(
        QualityPreset.high,
        "--quality",
        "-q",
        help="Quality preset: low, medium, high, ultra",
    ),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Enable verbose output"),
    provider: str = typer.Option(
        settings.ai.provider,  # Use default from settings
        "--provider",
        help="AI provider: openai, anthropic, local",
    ),
):
    """Convert files, URLs, or directories with enhanced options."""  # Updated docstring
    # Initialize the conversion engine
    # Pass settings to the engine if it requires them upon init (assuming it does)
    engine = ConversionEngine(settings)

    # Process inputs
    processed_inputs = []
    for input_path in inputs:
        # Check if it's a URL first
        if input_path.lower().startswith(("http://", "https://")):
            processed_inputs.append(InputSource(input_path))
            continue

        # Check if it's an existing file or directory
        path = Path(input_path)
        if path.exists():
            if path.is_dir():
                # Process directory
                found_files = False
                glob_pattern = "**/*" if recursive else "*"
                for file_path in path.glob(glob_pattern):
                    if (
                        file_path.is_file()
                        # Use settings for supported extensions
                        and file_path.suffix.lower() in settings.supported_extensions
                    ):
                        processed_inputs.append(InputSource(file_path))
                        found_files = True
                if not found_files and verbose:
                    console.print(
                        f"[yellow]Warning:[/yellow] No supported files found in directory: {input_path}"
                    )
            elif path.is_file():
                # Process file
                # Check extension before adding
                if path.suffix.lower() in settings.supported_extensions:
                    processed_inputs.append(InputSource(path))
                elif verbose:
                    console.print(
                        f"[yellow]Warning:[/yellow] Skipping unsupported file type: {input_path}"
                    )
            else:
                console.print(
                    f"[yellow]Warning:[/yellow] Input is neither file nor directory: {input_path}"
                )
        else:
            console.print(
                f"[bold red]Error:[/bold red] Input not found or invalid URL: {input_path}"
            )

    if not processed_inputs:
        console.print("[bold red]Error:[/bold red] No valid inputs to process.")
        sys.exit(1)

    # Set output path
    output_path = None
    output_is_dir = False
    if output:
        output_path = Path(output)
        # If output exists and is a dir, or ends with '/', treat as dir
        if output_path.is_dir() or output.endswith(os.sep):
            output_is_dir = True
            output_path.mkdir(parents=True, exist_ok=True)
        else:
            # Treat as file, ensure parent dir exists
            output_path.parent.mkdir(parents=True, exist_ok=True)
            if len(processed_inputs) > 1:
                console.print(
                    "[bold red]Error:[/bold red] Cannot output multiple inputs to a single file."
                )
                sys.exit(1)
    else:
        # Default output logic
        if len(processed_inputs) == 1:
            source = processed_inputs[0]
            if source.is_file:
                output_path = source.path.with_suffix(f".{format}")
            elif source.is_url:
                parsed_url = urlparse(source.url)
                domain = parsed_url.netloc.replace(".", "_").replace(":", "_")
                url_path = parsed_url.path.replace("/", "_").replace(":", "_")
                output_path = Path(f"{domain}{url_path or '_index'}.{format}")
            else:  # Should not happen based on input processing
                output_path = Path(f"llamadoc_output_0.{format}")
        else:
            output_path = Path("llamadoc_output")
            output_is_dir = True
            output_path.mkdir(parents=True, exist_ok=True)

    # Create conversion options
    # Include specific conversion settings if needed, passed via kwargs
    extra_opts = {
        # Example: map specific CLI args to engine options if needed
        # 'page_size': page_size_arg_if_exists
    }
    options = ConversionOptions(
        output_format=format,
        quality=quality.value,  # Use enum value
        use_llm=enhance,
        llm_provider=provider,
        parallel=parallel,
        verbose=verbose,
        **extra_opts,
    )

    # Run the conversion using asyncio
    async def run_conversion():
        try:
            if len(processed_inputs) == 1 and not output_is_dir:
                # Single input to single output
                result = await engine.convert(processed_inputs[0], output_path, options)
                return [result]  # Return as list for consistent handling
            else:
                # Multiple inputs or output is a directory
                results = await engine.batch_convert(processed_inputs, output_path, options)
                return results
        except Exception as e:
            console.print(f"[bold red]An unexpected error occurred:[/bold red] {str(e)}")
            if verbose:
                import traceback

                console.print(traceback.format_exc())
            sys.exit(1)

    # Execute async conversion
    results = asyncio.run(run_conversion())

    # Display summary
    successful = sum(1 for r in results if r.success)
    total = len(results)

    console.print("\n[bold]Conversion Summary:[/bold]")
    console.print(f"✅ [green]{successful} conversions successful[/green]")
    if successful < total:
        console.print(f"❌ [red]{total - successful} conversions failed[/red]")

    if verbose and successful < total:
        table = Table(title="Failed Conversions")
        table.add_column("Input", style="red", no_wrap=True)
        table.add_column("Output Path", style="yellow", no_wrap=True)
        table.add_column("Error", style="white")

        # Get input sources back from results if possible (engine needs to add this meta)
        # For now, use the processed_inputs list assuming order matches results
        failed_inputs = [inp for i, inp in enumerate(processed_inputs) if not results[i].success]
        failed_results = [res for res in results if not res.success]

        for i, result in enumerate(failed_results):
            input_obj = failed_inputs[i] if i < len(failed_inputs) else None
            input_str = "Unknown"
            if input_obj:
                input_str = str(input_obj.path) if input_obj.is_file else input_obj.url

            error_str = str(result.error) if result.error else "Unknown error"
            table.add_row(input_str, str(result.output_path), error_str)

        console.print(table)
        sys.exit(1)  # Exit with error if any conversion failed
    elif successful < total:
        sys.exit(1)  # Exit with error if any conversion failed even if not verbose


# Removed the compatibility 'convert' command as 'super_convert' (now 'convert') handles all cases.


@app.command()
def scrape(
    url: str = typer.Argument(..., help="URL to scrape"),
    output_dir: str = typer.Option("output", "--output", "-o", help="Output directory"),
    max_pages: int = typer.Option(10, "--max-pages", "-m", help="Maximum pages to scrape"),
    depth: int = typer.Option(1, "--depth", "-d", help="Crawl depth"),
    same_domain: bool = typer.Option(
        True, "--same-domain", help="Only crawl pages from the same domain"
    ),
    format: str = typer.Option(
        "pdf", "--format", "-f", help="Output format for scraped pages: pdf, html, both"
    ),
    headless: bool = typer.Option(True, "--headless", help="Run browser in headless mode"),
    timeout: int = typer.Option(
        settings.scraping.timeout, "--timeout", "-t", help="Timeout in seconds"
    ),
    screenshot: bool = typer.Option(
        settings.scraping.capture_network, "--screenshot", help="Capture screenshot of each page"
    ),  # Added screenshot option
    verbose: bool = typer.Option(
        False, "--verbose", "-v", help="Enable verbose output"
    ),  # Added verbose
):
    """Scrape web pages and optionally convert to PDF/HTML."""
    # Create output directory
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    screenshots_dir = output_path / "screenshots"
    if screenshot:
        screenshots_dir.mkdir(parents=True, exist_ok=True)

    # Set up scraper options from config and CLI args
    # Note: The core.scraper.EnhancedScraper doesn't seem to have a crawl method or accept these options directly.
    # The implementation below assumes a hypothetical scraper API or needs adjustment.
    scrape_options = {
        "max_pages": max_pages,
        "max_depth": depth,
        "same_domain_only": same_domain,
        "timeout": timeout,
        # Options potentially needed by EnhancedScraper methods:
        "screenshot_dir": str(screenshots_dir) if screenshot else None,
        "headless": headless,
        # Add other relevant options from settings.scraping if needed
    }

    console.print(
        Panel.fit(
            f"[bold magenta]🦙 SUPREME LLAMA WEB SCRAPER 🦙[/bold magenta]\n\n"
            f"[bold cyan]URL:[/bold cyan] {url}\n"
            f"[bold cyan]Max Pages:[/bold cyan] {max_pages}\n"
            f"[bold cyan]Depth:[/bold cyan] {depth}\n"
            f"[bold cyan]Same Domain Only:[/bold cyan] {same_domain}\n"
            f"[bold cyan]Output Format:[/bold cyan] {format}\n"
            f"[bold cyan]Screenshot:[/bold cyan] {screenshot}\n"
            f"[bold cyan]Output Directory:[/bold cyan] {output_path}",
            title="Scraping Configuration",
            border_style="magenta",
        )
    )

    # --- Scraper Implementation Placeholder ---
    # The following assumes EnhancedScraper has a crawl method.
    # This needs to be verified or adapted based on the actual EnhancedScraper API.
    async def run_scraper():
        scraper = EnhancedScraper()  # Instatiate the correct scraper
        all_scraped_content = (
            []
        )  # Store results (e.g., dicts with url, html, title, screenshot_path)

        # --- Hypothetical Crawl Logic ---
        # This is a basic structure; a real crawler is more complex.
        visited = set()
        queue = asyncio.Queue()
        await queue.put((url, 0))
        visited.add(url)
        pages_processed = 0

        engine = ConversionEngine(settings)  # Conversion engine for outputs

        while not queue.empty() and pages_processed < max_pages:
            current_url, current_depth = await queue.get()
            if current_depth > depth:
                continue

            console.print(f"Scraping [cyan]{current_url}[/cyan] at depth {current_depth}...")
            try:
                # Scrape basic info
                scraped_page = await scraper.scrape(current_url, options=scrape_options)
                if scraped_page.get("error"):
                    console.print(
                        f"[yellow]Warning:[/yellow] Failed to scrape {current_url}: {scraped_page['error']}"
                    )
                    continue

                # Capture screenshot if requested
                screenshot_path = None
                if screenshot:
                    screenshot_path = await scraper.capture_screenshot(
                        current_url,
                        str(
                            screenshots_dir
                            / f"{Path(urlparse(current_url).path).name or urlparse(current_url).netloc}.png"
                        ),
                    )
                    if screenshot_path:
                        console.print(f"  Screenshot saved to [green]{screenshot_path}[/green]")
                    else:
                        console.print(
                            f"  [yellow]Warning:[/yellow] Failed to capture screenshot for {current_url}"
                        )

                # Add result
                scraped_page["screenshot_path"] = screenshot_path
                all_scraped_content.append(scraped_page)
                pages_processed += 1

                # Generate output files (HTML/PDF)
                try:
                    parsed_url = urlparse(scraped_page["url"])
                    domain = parsed_url.netloc.replace(".", "_").replace(":", "_")
                    url_path = parsed_url.path.replace("/", "_").replace(":", "_")
                    base_filename = f"{domain}{url_path or '_index'}"

                    if format in ["html", "both"]:
                        html_path = output_path / f"{base_filename}.html"
                        with open(html_path, "w", encoding="utf-8") as f:
                            f.write(scraped_page.get("html", ""))
                        if verbose:
                            console.print(f"  HTML saved to [green]{html_path}[/green]")

                    if format in ["pdf", "both"]:
                        pdf_path = output_path / f"{base_filename}.pdf"
                        source_for_pdf = None
                        temp_html_path = None

                        if screenshot_path:
                            # Prefer screenshot for PDF conversion if available
                            source_for_pdf = InputSource(screenshot_path)
                        elif scraped_page.get("html"):
                            # Fallback to HTML conversion
                            temp_html_path = output_path / f"_temp_{base_filename}.html"
                            with open(temp_html_path, "w", encoding="utf-8") as f:
                                f.write(scraped_page["html"])
                            source_for_pdf = InputSource(temp_html_path)

                        if source_for_pdf:
                            opts = ConversionOptions(output_format="pdf", verbose=verbose)
                            pdf_result = await engine.convert(source_for_pdf, pdf_path, opts)
                            if pdf_result.success:
                                if verbose:
                                    console.print(f"  PDF saved to [green]{pdf_path}[/green]")
                            else:
                                console.print(
                                    f"  [yellow]Warning:[/yellow] Failed to convert {scraped_page['url']} to PDF: {pdf_result.error}"
                                )
                        else:
                            console.print(
                                f"  [yellow]Warning:[/yellow] No content (HTML/Screenshot) to convert to PDF for {scraped_page['url']}"
                            )

                        # Clean up temporary HTML file
                        if temp_html_path and temp_html_path.exists():
                            try:
                                temp_html_path.unlink()
                            except OSError:
                                pass  # Ignore cleanup errors

                except Exception as convert_err:
                    console.print(
                        f"[yellow]Warning:[/yellow] Error generating output for {scraped_page['url']}: {convert_err}"
                    )

                # Add new links to queue
                if current_depth < depth:
                    for link in scraped_page.get("links", []):
                        # Basic link normalization/filtering needed here
                        # E.g., handle relative links, check domain if same_domain=True
                        # This is a simplified placeholder
                        parsed_link = urlparse(link)
                        if parsed_link.scheme in ["http", "https"] and link not in visited:
                            if same_domain and parsed_link.netloc != urlparse(url).netloc:
                                continue
                            visited.add(link)
                            await queue.put((link, current_depth + 1))

            except Exception as scrape_err:
                console.print(
                    f"[bold red]Error scraping {current_url}:[/bold red] {str(scrape_err)}"
                )
            finally:
                queue.task_done()

        await scraper.close()  # Ensure scraper resources are released
        return all_scraped_content

    # --- End Scraper Implementation Placeholder ---

    try:
        # Run the scraper
        results = asyncio.run(run_scraper())

        # Display summary
        console.print(
            f"\n[bold green]Scraping Complete![/bold green] Processed {len(results)} pages."
        )

        # Display table of results
        if results:
            table = Table(title="Scraping Results", show_header=True, header_style="bold magenta")
            table.add_column("URL", style="cyan", no_wrap=True)
            table.add_column("Title", style="green")
            table.add_column("Links Found", justify="right")
            table.add_column("Screenshot", justify="center")

            for content in results:
                screenshot_status = "✅" if content.get("screenshot_path") else "❌"
                table.add_row(
                    content.get("url", "N/A"),
                    content.get("title", "N/A")[:70]
                    + ("..." if len(content.get("title", "")) > 70 else ""),
                    str(len(content.get("links", []))),
                    screenshot_status,
                )
            console.print(table)

    except ImportError as e:
        # Specific error for missing dependencies like playwright
        console.print(f"[bold red]Error:[/bold red] Required scraping dependency missing: {e}")
        console.print("Please install necessary extras, e.g., `pip install llamadoc2pdf[scrape]`")
        sys.exit(1)
    except Exception as e:
        console.print(f"[bold red]Scraping Error:[/bold red] {str(e)}")
        if verbose:
            import traceback

            console.print(traceback.format_exc())
        sys.exit(1)


@app.command()
def info():
    """Show system information, configuration, and detected tools."""
    # Ensure directories exist using settings
    settings.ensure_directories()

    console.print(
        Panel.fit(
            Align.center("[bold yellow]🦙 SUPREME LLAMA SYSTEM INFO 🦙[/bold yellow]"),
            border_style="yellow",
            padding=(1, 2),
        )
    )

    # Create layout
    layout = Layout()
    layout.split_column(
        Layout(name="file_types", size=12),  # Adjusted size
        Layout(name="config"),
        Layout(name="tools", size=8),  # Adjusted size
    )

    # Supported file types
    format_table = Table(
        title="[bold yellow]Supported File Formats[/bold yellow]",
        show_header=True,
        header_style="bold cyan",
    )
    format_table.add_column("Extension", style="cyan", justify="left")
    format_table.add_column("Description", style="white")

    # Example descriptions (can be expanded)
    format_descriptions = {
        ".txt": "Plain Text",
        ".md": "Markdown",
        ".doc": "MS Word (Legacy)",
        ".docx": "MS Word (OOXML)",
        ".html": "HTML Document",
        ".rtf": "Rich Text Format",
        ".odt": "OpenDocument Text",
        ".jpg": "JPEG Image",
        ".jpeg": "JPEG Image",
        ".png": "PNG Image",
        ".gif": "GIF Image",
        ".bmp": "Bitmap Image",
        ".tiff": "TIFF Image",
        ".webp": "WebP Image",
    }

    # Use settings for extensions
    for ext in sorted(settings.supported_extensions):
        format_table.add_row(ext, format_descriptions.get(ext, "N/A"))

    layout["file_types"].update(Align.center(format_table))

    # Configuration - Display key settings
    config_table = Table(
        title="[bold yellow]Key Configuration[/bold yellow]",
        show_header=True,
        header_style="bold green",
    )
    config_table.add_column("Setting", style="bright_green", no_wrap=True)
    config_table.add_column("Value", style="bright_white")

    # Add key settings from the settings object
    config_table.add_row("Temp Directory", settings.temp_dir)
    config_table.add_row("Cache Directory", settings.cache_dir)
    config_table.add_row("Default Output Dir", settings.output_dir)
    config_table.add_row("Conversion Timeout (s)", str(settings.conversion.timeout))
    config_table.add_row("Default Quality", settings.conversion.quality_preset.value)
    config_table.add_row("Default Page Size", settings.conversion.page_size)
    config_table.add_row(
        "Default Margin (T/R/B/L mm)",
        f"{settings.conversion.margin_top}/{settings.conversion.margin_right}/"
        f"{settings.conversion.margin_bottom}/{settings.conversion.margin_left}",
    )
    config_table.add_row("Scraper Timeout (s)", str(settings.scraping.timeout))
    config_table.add_row("Scraper Headless", str(settings.scraping.headless))
    config_table.add_row("AI Provider", settings.ai.provider)
    config_table.add_row("AI Model", settings.ai.model)

    layout["config"].update(Align.center(config_table))

    # External tools detection
    tools_table = Table(
        title="[bold yellow]External Tools Status[/bold yellow]",
        show_header=True,
        header_style="bold magenta",
    )
    tools_table.add_column("Tool", style="bright_green")
    tools_table.add_column("Status", style="bright_white")
    tools_table.add_column("Path/Info", style="dim", no_wrap=True)

    # Check wkhtmltopdf using settings path first
    wkhtmltopdf_path = settings.wkhtmltopdf_path
    if wkhtmltopdf_path and Path(wkhtmltopdf_path).exists():
        tools_table.add_row("wkhtmltopdf", "✅ Found (Config)", wkhtmltopdf_path)
    else:
        # Search common paths if not found via config
        found_path = None
        for path in [
            "/usr/bin/wkhtmltopdf",
            "/usr/local/bin/wkhtmltopdf",
            "/opt/homebrew/bin/wkhtmltopdf",
        ]:
            if Path(path).exists():
                found_path = path
                break
        if found_path:
            tools_table.add_row("wkhtmltopdf", "✅ Found (System)", found_path)
        else:
            tools_table.add_row("wkhtmltopdf", "❌ Not found", "HTML conversion may be limited")

    # Check LibreOffice using settings path first
    libreoffice_path = settings.libreoffice_path
    if libreoffice_path and Path(libreoffice_path).exists():
        tools_table.add_row("LibreOffice", "✅ Found (Config)", libreoffice_path)
    else:
        # Search common paths
        found_path = None
        for path in [
            "/usr/bin/soffice",
            "/usr/bin/libreoffice",
            "/Applications/LibreOffice.app/Contents/MacOS/soffice",
        ]:
            if Path(path).exists():
                found_path = path
                break
        if found_path:
            tools_table.add_row("LibreOffice", "✅ Found (System)", found_path)
        else:
            tools_table.add_row("LibreOffice", "❌ Not found", "Office doc conversion may fail")

    # Check Playwright (needed for EnhancedScraper)
    try:
        # Attempt a more reliable check if possible, e.g., importing a core component
        from playwright.sync_api import sync_playwright

        # If import works, assume it's installed correctly
        tools_table.add_row("Playwright", "✅ Found (Importable)", "Needed for web scraping")
    except ImportError:
        tools_table.add_row("Playwright", "❌ Not found", "Web scraping requires Playwright")

    layout["tools"].update(Align.center(tools_table))

    console.print(layout)


def run():
    """Entry point for the CLI application."""
    # animate_llama() # Optional: uncomment to enable animation
    app()


# This check remains, but the run() function is the preferred entry point
if __name__ == "__main__":
    run()
