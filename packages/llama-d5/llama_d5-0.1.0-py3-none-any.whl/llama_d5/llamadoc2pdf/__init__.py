"""LlamaDoc2PDF - The Supreme Document Toolkit."""

__version__ = "0.2.0"
__author__ = "LlamaTeam"

# Import core components directly for easier access
# Making the engine, options, settings, and processors readily available.
try:
    from .config.settings import settings
    from .core.engine import (
        ConversionEngine,
        ConversionOptions,
        ConversionResult,
        InputSource,
    )
    from .processors.document import DocumentProcessor
    from .processors.webpage import WebProcessor

    # Import other key components as needed, e.g.:
    # from .llm_integration import LLMProcessor # Assuming this is the correct class

except ImportError as e:
    # This might happen during setup or if dependencies are missing
    # Log this appropriately in a real application
    print(f"Warning: Could not import core llamadoc2pdf components: {e}")
    # Define dummy placeholders only if absolutely necessary for basic loading
    settings = None
    ConversionEngine = None
    ConversionOptions = None
    ConversionResult = None
    InputSource = None
    DocumentProcessor = None
    WebProcessor = None

# Define the public API of the package
__all__ = [
    "__version__",
    "__author__",
    "settings",  # Configuration settings
    "ConversionEngine",  # The main engine for conversions
    "ConversionOptions",  # Options for conversion
    "ConversionResult",  # Result object from conversion
    "InputSource",  # Enum for input types (file/URL)
    "DocumentProcessor",  # Processor for local documents
    "WebProcessor",  # Processor for web pages/URLs
    # Key submodules/subpackages if intended for direct use:
    "core",
    "processors",
    "config",
    "llm_integration",  # Expose if users need direct access
    "scraper",  # Expose if EnhancedScraper is part of public API
]

# Optional: Import submodules if you want them accessible directly
# e.g., import .core, .processors
# This allows users to do `import llamadoc2pdf; llamadoc2pdf.core.some_function()`
# The __all__ list controls `from llamadoc2pdf import *` behavior

# --- Removed Old/Redundant Code ---
# Removed try-except block importing top-level functions (convert_document, etc.)
# Removed complex __all__ list with assumed functions
# Removed multiple redundant imports of DocumentConverter
# Removed import of top-level converter module
# Removed import of master_config as config
# Removed placeholder initializations like `from . import agents...`

"""LlamaDoc2PDF package - Cleaned up __init__."""  # Updated docstring end
