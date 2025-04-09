"""Advanced configuration system for LlamaDoc2PDF."""

import json
import logging
import os
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Literal, Optional, Union

from pydantic import BaseModel, Field, validator
from pydantic_settings import BaseSettings

logger = logging.getLogger("llamadoc2pdf.config")


class OutputFormat(str, Enum):
    """Available output formats."""

    PDF = "pdf"
    DOCX = "docx"
    HTML = "html"
    TEXT = "txt"
    MARKDOWN = "md"
    JSON = "json"


class QualityPreset(str, Enum):
    """Quality presets for conversion."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    ULTRA = "ultra"


class AIProvider(str, Enum):
    """Available AI providers."""

    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    HUGGINGFACE = "huggingface"
    COHERE = "cohere"
    LOCAL = "local"
    NONE = "none"


class WebDriverType(str, Enum):
    """Available web driver types."""

    PLAYWRIGHT = "playwright"
    SELENIUM = "selenium"
    REQUESTS_HTML = "requests-html"


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

    # Output settings
    output_format: OutputFormat = Field(OutputFormat.PDF, description="Default output format")
    overwrite_existing: bool = Field(True, description="Overwrite existing output files")

    # Page settings
    page_size: str = Field("A4", description="Page size for the output (A4, Letter, etc.)")
    page_width: Optional[float] = Field(
        None, description="Custom page width in mm (overrides page_size)"
    )
    page_height: Optional[float] = Field(
        None, description="Custom page height in mm (overrides page_size)"
    )

    # Margin settings
    margin_top: float = Field(20.0, description="Top margin in mm")
    margin_right: float = Field(20.0, description="Right margin in mm")
    margin_bottom: float = Field(20.0, description="Bottom margin in mm")
    margin_left: float = Field(20.0, description="Left margin in mm")

    # Content settings
    enable_toc: bool = Field(True, description="Generate table of contents for documents")
    enable_hyperlinks: bool = Field(True, description="Enable hyperlinks in output")
    enable_images: bool = Field(True, description="Include images in output")
    custom_css: Optional[str] = Field(
        None, description="Path to custom CSS for HTML-based conversion"
    )
    custom_templates_dir: Optional[str] = Field(
        None, description="Path to custom templates directory"
    )

    # Processing settings
    quality_preset: QualityPreset = Field(
        QualityPreset.HIGH, description="Quality preset for conversion"
    )
    verbose_logging: bool = Field(False, description="Enable verbose logging during conversion")
    timeout: int = Field(60, description="Timeout for conversion operations in seconds")

    # Enhancement settings
    watermark: Optional[str] = Field(None, description="Text to use as watermark")
    watermark_opacity: float = Field(0.1, description="Watermark opacity (0.0-1.0)")

    # AI enhancement
    use_llm: bool = Field(False, description="Use AI/LLM to enhance document conversion")
    llm_provider: AIProvider = Field(AIProvider.OPENAI, description="AI provider for enhancements")

    @validator("custom_css")
    def validate_custom_css(cls, v):
        if v is not None and not os.path.exists(v):
            logger.warning(f"Custom CSS file not found: {v}")
        return v

    @validator("custom_templates_dir")
    def validate_custom_templates_dir(cls, v):
        if v is not None and not os.path.exists(v):
            logger.warning(f"Custom templates directory not found: {v}")
        return v


class ScrapeConfig(BaseModel):
    """Settings for web scraping."""

    # General settings
    driver_type: WebDriverType = Field(WebDriverType.PLAYWRIGHT, description="Web driver type")
    headless: bool = Field(True, description="Run browser in headless mode")
    stealth_mode: bool = Field(True, description="Use stealth mode to avoid detection")

    # Navigation settings
    wait_time: float = Field(2.0, description="Wait time after page load in seconds")
    timeout: int = Field(60, description="Timeout for scraping operations in seconds")
    retry_count: int = Field(3, description="Number of retries for failed requests")
    delay_min: float = Field(1.0, description="Minimum delay between requests in seconds")
    delay_max: float = Field(3.0, description="Maximum delay between requests in seconds")

    # Content processing
    auto_scroll: bool = Field(True, description="Auto-scroll pages to load all content")
    javascript_enabled: bool = Field(True, description="Enable JavaScript execution")
    load_images: bool = Field(True, description="Load images during scraping")

    # Browser settings
    screenshot_format: str = Field("png", description="Format for screenshots")
    viewport_width: int = Field(1920, description="Browser viewport width")
    viewport_height: int = Field(1080, description="Browser viewport height")
    device_scale_factor: float = Field(1.0, description="Device scale factor")

    # Crawler settings
    max_depth: int = Field(2, description="Maximum crawl depth")
    max_pages: int = Field(50, description="Maximum pages to crawl")
    same_domain_only: bool = Field(True, description="Only crawl pages from the same domain")
    follow_redirects: bool = Field(True, description="Follow HTTP redirects")
    honor_robots_txt: bool = Field(True, description="Honor robots.txt restrictions")

    # Identity settings
    user_agent_rotation: bool = Field(True, description="Rotate user agents")
    user_agents: List[str] = Field([], description="List of user agents for rotation")

    # Storage settings
    screenshot_dir: str = Field("screenshots", description="Directory for screenshots")
    cookies_file: Optional[str] = Field(None, description="Path to cookies file")
    cookies_domain: Optional[str] = Field(None, description="Domain for cookies")

    # Advanced settings
    capture_network: bool = Field(False, description="Capture network traffic during scraping")
    emulate_device: Optional[str] = Field(
        None, description="Device to emulate (mobile, tablet, etc.)"
    )
    bypass_csp: bool = Field(True, description="Bypass Content Security Policy")
    disable_cache: bool = Field(True, description="Disable browser cache")


class AIConfig(BaseModel):
    """Settings for AI/LLM integration."""

    # General settings
    provider: AIProvider = Field(AIProvider.OPENAI, description="LLM provider")
    api_key: Optional[str] = Field(None, description="API key for the LLM provider")
    api_base: Optional[str] = Field(None, description="Base URL for API")
    model: str = Field("gpt-4o", description="Model to use")

    # Request settings
    max_tokens: int = Field(4000, description="Maximum tokens for AI responses")
    temperature: float = Field(0.7, description="Temperature for AI responses")
    top_p: float = Field(1.0, description="Top-p for AI responses")
    timeout: int = Field(60, description="Timeout for AI requests in seconds")

    # Feature settings
    enable_summarization: bool = Field(False, description="Enable document summarization")
    enable_translation: bool = Field(False, description="Enable document translation")
    enable_content_enhancement: bool = Field(False, description="Enable content enhancement")
    enable_formatting: bool = Field(False, description="Enable document formatting improvement")

    # Translation settings
    source_language: Optional[str] = Field(None, description="Source language for translation")
    target_language: Optional[str] = Field(None, description="Target language for translation")

    # Local models
    local_model_path: Optional[str] = Field(None, description="Path to local model")
    local_model_args: Dict[str, Any] = Field({}, description="Arguments for local model")

    # Performance settings
    cache_responses: bool = Field(True, description="Cache AI responses")
    cache_ttl: int = Field(86400, description="Cache TTL in seconds (default: 1 day)")
    max_retries: int = Field(3, description="Maximum retries for failed API calls")

    @validator("api_key")
    def validate_api_key(cls, v, values):
        provider = values.get("provider")
        if provider in [AIProvider.OPENAI, AIProvider.ANTHROPIC, AIProvider.COHERE] and not v:
            # Check environment variables
            env_var = f"{provider.value.upper()}_API_KEY"
            if os.environ.get(env_var):
                return os.environ.get(env_var)
            logger.warning(
                f"No API key provided for {provider}. Set it in the configuration or {env_var} environment variable."
            )
        return v


class MasterConfig(BaseSettings):
    """Master configuration for LlamaDoc2PDF."""

    # Core application settings
    app_name: str = Field("LlamaDoc2PDF", description="Application name")
    version: str = Field("1.0.0", description="Application version")
    mode: Literal["cli", "api", "gui"] = Field("cli", description="Application mode")
    log_level: str = Field("INFO", description="Logging level")

    # Directory settings
    temp_dir: str = Field(
        os.path.join(os.path.expanduser("~"), ".llamadoc2pdf", "temp"),
        description="Directory for temporary files",
    )
    cache_dir: str = Field(
        os.path.join(os.path.expanduser("~"), ".llamadoc2pdf", "cache"),
        description="Directory for caching",
    )
    output_dir: str = Field("output", description="Default output directory")
    data_dir: str = Field(
        os.path.join(os.path.expanduser("~"), ".llamadoc2pdf", "data"),
        description="Directory for application data",
    )

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

    # Supported file types with metadata
    supported_extensions: Dict[str, Dict[str, Any]] = Field(
        default_factory=lambda: {
            ".txt": {"description": "Text files", "category": "document"},
            ".md": {"description": "Markdown documents", "category": "document"},
            ".doc": {
                "description": "Microsoft Word (pre-2007)",
                "category": "document",
            },
            ".docx": {"description": "Microsoft Word", "category": "document"},
            ".html": {"description": "HTML web pages", "category": "web"},
            ".rtf": {"description": "Rich Text Format", "category": "document"},
            ".odt": {"description": "OpenDocument Text", "category": "document"},
            ".jpg": {"description": "JPEG images", "category": "image"},
            ".jpeg": {"description": "JPEG images", "category": "image"},
            ".png": {"description": "PNG images", "category": "image"},
            ".gif": {"description": "GIF images", "category": "image"},
            ".bmp": {"description": "Bitmap images", "category": "image"},
            ".tiff": {"description": "TIFF images", "category": "image"},
            ".webp": {"description": "WebP images", "category": "image"},
            ".pdf": {"description": "PDF documents", "category": "document"},
        },
        description="Supported file extensions with metadata",
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
        for dir_path in [self.temp_dir, self.cache_dir, self.output_dir, self.data_dir]:
            path = Path(dir_path)
            if not path.exists():
                try:
                    path.mkdir(parents=True, exist_ok=True)
                    logger.info(f"Created directory: {dir_path}")
                except Exception as e:
                    logger.warning(f"Could not create directory {dir_path}: {str(e)}")

    def get_supported_extensions(self) -> List[str]:
        """Get list of supported file extensions."""
        return list(self.supported_extensions.keys())

    def save_to_file(self, file_path: Union[str, Path] = None, format: str = "json") -> bool:
        """
        Save configuration to file.

        Args:
            file_path: Path to save the configuration file
            format: File format (json or yaml)

        Returns:
            True if successful, False otherwise
        """
        if file_path is None:
            file_path = os.path.join(self.cache_dir, f"config.{format}")

        path = Path(file_path)
        path.parent.mkdir(parents=True, exist_ok=True)

        try:
            # Convert to dict
            config_dict = self.dict()

            # Save in the requested format
            if format.lower() == "yaml":
                with open(path, "w") as f:
                    yaml.dump(config_dict, f, default_flow_style=False)
            else:
                with open(path, "w") as f:
                    json.dump(config_dict, f, indent=2)

            logger.info(f"Configuration saved to {path}")
            return True
        except Exception as e:
            logger.error(f"Failed to save configuration: {str(e)}")
            return False

    @classmethod
    def load_from_file(cls, file_path: Union[str, Path]) -> "MasterConfig":
        """
        Load configuration from file.

        Args:
            file_path: Path to the configuration file

        Returns:
            MasterConfig instance
        """
        path = Path(file_path)

        if not path.exists():
            logger.warning(f"Configuration file not found: {path}")
            return cls()

        try:
            # Determine format based on extension
            format = path.suffix.lower().lstrip(".")

            if format == "yaml" or format == "yml":
                try:
                    import yaml
                except ImportError:
                    logger.error("PyYAML package is required for YAML support")
                    return cls()
                with open(path, "r") as f:
                    config_dict = yaml.safe_load(f)
            else:
                with open(path, "r") as f:
                    config_dict = json.load(f)

            return cls(**config_dict)
        except Exception as e:
            logger.error(f"Failed to load configuration: {str(e)}")

            return cls()


# Global configuration instance
master_config = MasterConfig()
