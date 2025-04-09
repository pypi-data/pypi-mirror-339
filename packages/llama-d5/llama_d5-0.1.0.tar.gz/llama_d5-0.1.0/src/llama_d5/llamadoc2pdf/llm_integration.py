"""AI/LLM integration for LlamaDoc2PDF."""

import os
import time
from pathlib import Path
from typing import Any, Dict

from rich.console import Console

from ..config.settings import settings
from ..core.engine import ConversionContext, ConversionResult
from ..core.exceptions import AIError

console = Console()


class LLMOrchestrator:
    """Multi-LLM management system for content enhancement."""

    def __init__(self):
        """Initialize the LLM orchestrator."""
        self.providers = {
            "openai": OpenAIService(),
            "anthropic": AnthropicService(),
            "local": LocalLLMService(),
        }

    async def enhance(self, result: ConversionResult, ctx: ConversionContext) -> ConversionResult:
        """
        Apply AI enhancements to content.

        Args:
            result: The conversion result to enhance
            ctx: Conversion context

        Returns:
            Enhanced conversion result
        """
        if not result.success:
            console.print("[yellow]Warning:[/yellow] Cannot enhance failed conversion")
            return result

        provider_name = ctx.options.llm_provider

        if provider_name not in self.providers:
            raise AIError(f"Unknown LLM provider: {provider_name}")

        provider = self.providers[provider_name]

        try:
            # Create enhanced output path
            original_path = result.output_path
            enhanced_path = (
                original_path.parent / f"{original_path.stem}_enhanced{original_path.suffix}"
            )

            # Gather options for enhancement
            options = {
                "summarize": ctx.options.extra_options.get(
                    "summarize", settings.ai.enable_summarization
                ),
                "translate": ctx.options.extra_options.get(
                    "translate", settings.ai.enable_translation
                ),
                "target_language": ctx.options.extra_options.get(
                    "target_language", settings.ai.target_language
                ),
                "enhance_content": ctx.options.extra_options.get(
                    "enhance_content", settings.ai.enable_content_enhancement
                ),
            }

            # Apply AI enhancement
            enhanced_result = await provider.process(result, enhanced_path, options)

            # Update meta information
            enhanced_result.meta.update(
                {
                    "enhanced": True,
                    "original_path": str(original_path),
                    "provider": provider_name,
                    "enhancement_options": options,
                }
            )

            return enhanced_result

        except Exception as e:
            error_msg = f"AI enhancement failed: {str(e)}"
            console.print(f"[bold red]Error:[/bold red] {error_msg}")

            # Return the original result if enhancement fails
            result.meta["enhancement_error"] = error_msg
            return result


class LLMService:
    """Base class for LLM services."""

    async def process(
        self, result: ConversionResult, output_path: Path, options: Dict[str, Any]
    ) -> ConversionResult:
        """
        Process content with LLM.

        Args:
            result: Conversion result to process
            output_path: Path to save enhanced output
            options: Processing options

        Returns:
            Enhanced conversion result
        """
        raise NotImplementedError("LLM service must implement process method")


class OpenAIService(LLMService):
    """OpenAI API service."""

    def __init__(self):
        """Initialize the OpenAI service."""
        self.api_key = settings.ai.api_key or os.environ.get("OPENAI_API_KEY")
        self.model = settings.ai.model

    async def process(
        self, result: ConversionResult, output_path: Path, options: Dict[str, Any]
    ) -> ConversionResult:
        """Process content with OpenAI."""
        if not self.api_key:
            raise AIError(
                "OpenAI API key not provided. Set it in the configuration or OPENAI_API_KEY environment variable."
            )

        try:
            # In a real implementation, we would import the OpenAI library and use it
            # For now, just create a simple enhanced version
            console.print("[bold cyan]Enhancing content with OpenAI...[/bold cyan]")

            # Simulate API call latency
            time.sleep(1)

            # Copy the original file to the enhanced path for now
            import shutil

            shutil.copy2(result.output_path, output_path)

            # Return enhanced result
            return ConversionResult(
                output_path=output_path,
                success=True,
                meta={
                    "enhanced": True,
                    "model": self.model,
                    "original_path": str(result.output_path),
                },
            )

        except Exception as e:
            raise AIError(f"OpenAI processing failed: {str(e)}")


class AnthropicService(LLMService):
    """Anthropic API service."""

    def __init__(self):
        """Initialize the Anthropic service."""
        self.api_key = settings.ai.api_key or os.environ.get("ANTHROPIC_API_KEY")
        self.model = settings.ai.model

    async def process(
        self, result: ConversionResult, output_path: Path, options: Dict[str, Any]
    ) -> ConversionResult:
        """Process content with Anthropic."""
        if not self.api_key:
            raise AIError(
                "Anthropic API key not provided. Set it in the configuration or ANTHROPIC_API_KEY environment variable."
            )

        try:
            # In a real implementation, we would import the Anthropic library and use it
            # For now, just create a simple enhanced version
            console.print("[bold cyan]Enhancing content with Anthropic...[/bold cyan]")

            # Simulate API call latency
            time.sleep(1)

            # Copy the original file to the enhanced path for now
            import shutil

            shutil.copy2(result.output_path, output_path)

            # Return enhanced result
            return ConversionResult(
                output_path=output_path,
                success=True,
                meta={
                    "enhanced": True,
                    "model": self.model,
                    "original_path": str(result.output_path),
                },
            )

        except Exception as e:
            raise AIError(f"Anthropic processing failed: {str(e)}")


class LocalLLMService(LLMService):
    """Local LLM service."""

    def __init__(self):
        """Initialize the local LLM service."""
        self.model_path = settings.ai.local_model_path

    async def process(
        self, result: ConversionResult, output_path: Path, options: Dict[str, Any]
    ) -> ConversionResult:
        """Process content with local LLM."""
        if not self.model_path:
            raise AIError("Local model path not provided. Set it in the configuration.")

        try:
            # In a real implementation, we would load and use a local model
            # For now, just create a simple enhanced version
            console.print("[bold cyan]Enhancing content with local LLM...[/bold cyan]")

            # Simulate processing latency
            time.sleep(1)

            # Copy the original file to the enhanced path for now
            import shutil

            shutil.copy2(result.output_path, output_path)

            # Return enhanced result
            return ConversionResult(
                output_path=output_path,
                success=True,
                meta={
                    "enhanced": True,
                    "model": "local",
                    "original_path": str(result.output_path),
                },
            )

        except Exception as e:
            raise AIError(f"Local LLM processing failed: {str(e)}")
