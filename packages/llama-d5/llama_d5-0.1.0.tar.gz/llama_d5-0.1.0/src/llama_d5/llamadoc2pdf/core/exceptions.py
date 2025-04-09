"""Custom exceptions for llamadoc2pdf."""


class LlamaError(Exception):
    """Base exception class for all llamadoc2pdf exceptions."""

    def __init__(self, message: str, *args, **kwargs):
        self.message = message
        super().__init__(message, *args, **kwargs)


class ConversionError(LlamaError):
    """Exception raised when a document conversion fails."""

    pass


class ScrapeError(LlamaError):
    """Exception raised when web scraping fails."""

    pass


class AIError(LlamaError):
    """Exception raised when LLM/AI operations fail."""

    pass


class NetworkError(LlamaError):
    """Exception raised when network operations fail."""

    pass


class ConfigurationError(LlamaError):
    """Exception raised when there's a configuration issue."""

    pass


class UnsupportedFormatError(ConversionError):
    """Exception raised when an unsupported format is encountered."""

    def __init__(self, file_format: str, *args, **kwargs):
        message = f"Unsupported file format: {file_format}"
        super().__init__(message, *args, **kwargs)
        self.file_format = file_format


class MissingDependencyError(ConversionError):
    """Exception raised when a required dependency is missing."""

    def __init__(self, dependency: str, *args, **kwargs):
        message = f"Required dependency not installed: {dependency}"
        super().__init__(message, *args, **kwargs)
        self.dependency = dependency
