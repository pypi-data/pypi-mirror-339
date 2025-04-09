"""Configuration management for LlamaDoc2PDF."""

import json
import logging
import os
from enum import Enum
from pathlib import Path
from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field, validator
from pydantic_settings import BaseSettings

try:
    from rich.console import Console

    RICH_AVAILABLE = True
    console = Console()
except ImportError:
    RICH_AVAILABLE = False
    console = None

# Set up logging
logger = logging.getLogger("llamadoc2pdf.config")


def log_info(msg):
    """Log info message with console if available, otherwise use standard logging."""
    if RICH_AVAILABLE and console:
        console.print(f"[green]{msg}[/green]")
    logger.info(msg)


def log_warning(msg):
    """Log warning message with console if available, otherwise use standard logging."""
    if RICH_AVAILABLE and console:
        console.print(f"[yellow]Warning:[/yellow] {msg}")
    logger.warning(msg)


def log_error(msg):
    """Log error message with console if available, otherwise use standard logging."""
    if RICH_AVAILABLE and console:
        console.print(f"[bold red]Error:[/bold red] {msg}")
    logger.error(msg)


# Quality presets
class QualityPreset(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"
    ultra = "ultra"


class ProxyConfig(BaseModel):
    """Configuration for proxy settings."""

    enabled: bool = Field(False, description="Enable proxy for network requests")
    url: Optional[str] = Field(None, description="Proxy URL (e.g., http://proxy:port)")
    username: Optional[str] = Field(None, description="Proxy username")
    password: Optional[str] = Field(None, description="Proxy password")
    rotation: bool = Field(False, description="Enable proxy rotation")
    proxy_list: List[str] = Field([], description="List of proxy URLs for rotation")


class ConversionConfig(BaseModel):
    """Settings for document conversion."""

    page_size: str = Field("A4", description="Page size for the output PDF")
    margin_top: float = Field(20.0, description="Top margin in mm")
    margin_right: float = Field(20.0, description="Right margin in mm")
    margin_bottom: float = Field(20.0, description="Bottom margin in mm")
    margin_left: float = Field(20.0, description="Left margin in mm")
    enable_toc: bool = Field(True, description="Generate table of contents for documents")
    verbose_logging: bool = Field(False, description="Enable verbose logging during conversion")
    timeout: int = Field(60, description="Timeout for conversion operations in seconds")
    custom_css: Optional[str] = Field(
        None, description="Path to custom CSS for HTML-based conversion"
    )
    watermark: Optional[str] = Field(None, description="Text to use as watermark")
    use_llm: bool = Field(False, description="Use AI/LLM to enhance document conversion")
    quality_preset: QualityPreset = Field(
        QualityPreset.high, description="Quality preset for conversion"
    )
    default_format: str = Field("pdf", description="Default output format")

    @validator("custom_css")
    def validate_custom_css(cls, v):
        if v is not None and not os.path.exists(v):
            log_warning(f"Custom CSS file not found: {v}")
        return v


class ScrapeConfig(BaseModel):
    """Settings for web scraping."""

    headless: bool = Field(True, description="Run browser in headless mode")
    stealth_mode: bool = Field(True, description="Use stealth mode to avoid detection")
    auto_scroll: bool = Field(True, description="Auto-scroll pages to load all content")
    wait_time: float = Field(2.0, description="Wait time after page load in seconds")
    screenshot_format: str = Field("png", description="Format for screenshots")
    max_depth: int = Field(2, description="Maximum crawl depth")
    max_pages: int = Field(50, description="Maximum pages to crawl")
    same_domain_only: bool = Field(True, description="Only crawl pages from the same domain")
    user_agent_rotation: bool = Field(True, description="Rotate user agents")
    js_render: bool = Field(True, description="Render JavaScript")
    timeout: int = Field(60, description="Timeout for scraping operations in seconds")
    retry_count: int = Field(3, description="Number of retries for failed requests")
    delay_min: float = Field(1.0, description="Minimum delay between requests in seconds")
    delay_max: float = Field(3.0, description="Maximum delay between requests in seconds")
    user_agents: List[str] = Field([], description="List of user agents for rotation")
    screenshot_dir: str = Field("screenshots", description="Directory for screenshots")
    cookies_file: Optional[str] = Field(None, description="Path to cookies file")
    capture_network: bool = Field(False, description="Capture network traffic during scraping")


class AIConfig(BaseModel):
    """Settings for AI/LLM integration."""

    provider: Literal["openai", "anthropic", "local"] = Field("openai", description="LLM provider")
    api_key: Optional[str] = Field(None, description="API key for the LLM provider")
    model: str = Field("gpt-3.5-turbo", description="Model to use")
    max_tokens: int = Field(4000, description="Maximum tokens for AI responses")
    temperature: float = Field(0.7, description="Temperature for AI responses")
    enable_summarization: bool = Field(False, description="Enable document summarization")
    enable_translation: bool = Field(False, description="Enable document translation")
    target_language: Optional[str] = Field(None, description="Target language for translation")
    enable_content_enhancement: bool = Field(False, description="Enable content enhancement")
    local_model_path: Optional[str] = Field(None, description="Path to local model")
    cache_responses: bool = Field(True, description="Cache AI responses")

    @validator("api_key")
    def validate_api_key(cls, v, values):
        provider = values.get("provider")
        if provider in ["openai", "anthropic"] and not v:
            # Check environment variables
            env_var = f"{provider.upper()}_API_KEY"
            if os.environ.get(env_var):
                return os.environ.get(env_var)
            log_warning(
                f"No API key provided for {provider}. Set it in the configuration or {env_var} environment variable."
            )
        return v


class UnifiedSettings(BaseSettings):
    """Unified configuration for LlamaDoc2PDF."""

    # Core Settings
    mode: Literal["cli", "api", "gui"] = Field("cli", description="Application mode")
    log_level: str = Field("INFO", description="Logging level")
    temp_dir: str = Field(
        os.path.join(os.path.expanduser("~"), ".llamadoc2pdf", "temp"),
        description="Directory for temporary files",
    )
    cache_dir: str = Field(
        os.path.join(os.path.expanduser("~"), ".llamadoc2pdf", "cache"),
        description="Directory for caching",
    )
    output_dir: str = Field("output", description="Default output directory")

    # External tools configuration
    wkhtmltopdf_path: Optional[str] = Field(None, description="Path to wkhtmltopdf executable")
    libreoffice_path: Optional[str] = Field(None, description="Path to LibreOffice executable")
    pandoc_path: Optional[str] = Field(None, description="Path to Pandoc executable")

    # Module configurations
    conversion: ConversionConfig = Field(
        default_factory=ConversionConfig, description="Document conversion settings"
    )
    scraping: ScrapeConfig = Field(
        default_factory=ScrapeConfig, description="Web scraping settings"
    )
    ai: AIConfig = Field(default_factory=AIConfig, description="AI/LLM settings")
    proxy: ProxyConfig = Field(default_factory=ProxyConfig, description="Proxy settings")

    # Supported file types
    supported_extensions: List[str] = Field(
        [
            ".txt",
            ".md",
            ".doc",
            ".docx",
            ".html",
            ".rtf",
            ".odt",
            ".jpg",
            ".jpeg",
            ".png",
            ".gif",
            ".bmp",
            ".tiff",
            ".webp",
        ],
        description="List of supported file extensions",
    )

    class Config:
        """Pydantic config."""

        env_prefix = "LLAMADOC2PDF_"
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        extra = "ignore"

    def ensure_directories(self) -> None:
        """Ensure required directories exist."""
        for dir_path in [self.temp_dir, self.cache_dir, self.output_dir]:
            path = Path(dir_path)
            if not path.exists():
                try:
                    path.mkdir(parents=True, exist_ok=True)
                    log_info(f"Created directory: {dir_path}")
                except Exception as e:
                    log_warning(f"Could not create directory {dir_path}: {str(e)}")

    def save_to_file(self, file_path: Union[str, Path] = None) -> None:
        """Save configuration to file."""
        if file_path is None:
            file_path = os.path.join(self.cache_dir, "config.json")

        path = Path(file_path)
        path.parent.mkdir(parents=True, exist_ok=True)

        try:
            # Convert to dict and save as JSON
            config_dict = json.loads(self.json(indent=2))
            with open(path, "w") as f:
                json.dump(config_dict, f, indent=2)
            log_info(f"Configuration saved to {path}")
        except Exception as e:
            log_error(f"Failed to save configuration: {str(e)}")

    @classmethod
    def load_from_file(cls, file_path: Union[str, Path]) -> "UnifiedSettings":
        """Load configuration from file."""
        path = Path(file_path)

        if not path.exists():
            log_warning(f"Configuration file not found: {path}")
            return cls()

        try:
            with open(path, "r") as f:
                config_dict = json.load(f)
            return cls(**config_dict)
        except Exception as e:
            log_error(f"Failed to load configuration: {str(e)}")
            return cls()


# Global configuration instance
config = UnifiedSettings()

# Initialize logging based on config
logging.basicConfig(
    level=getattr(logging, config.log_level),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(os.path.join(config.cache_dir, "llamadoc2pdf.log"), mode="a"),
    ],
)

# Global settings instance
settings = UnifiedSettings()
