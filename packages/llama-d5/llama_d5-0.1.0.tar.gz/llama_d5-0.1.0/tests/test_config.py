"""Tests for the config module."""

import os
import tempfile

from llamadoc2pdf.config import LlamaConfig


class TestConfig:
    """Test suite for the configuration module."""

    def test_default_config(self):
        """Test default configuration values."""
        config = LlamaConfig()

        # Check basic defaults
        assert config.temp_dir
        assert config.cache_dir
        assert isinstance(config.supported_extensions, list)
        assert ".txt" in config.supported_extensions
        assert ".md" in config.supported_extensions

        # Check conversion settings
        assert config.conversion.page_size == "A4"
        assert config.conversion.margin_top == 20.0
        assert config.conversion.margin_bottom == 20.0

    def test_ensure_directories(self):
        """Test directory creation."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create config with temp directories
            config = LlamaConfig(
                temp_dir=os.path.join(temp_dir, "temp"),
                cache_dir=os.path.join(temp_dir, "cache"),
            )

            # Ensure directories exist
            config.ensure_directories()

            # Check if directories were created
            assert os.path.exists(config.temp_dir)
            assert os.path.exists(config.cache_dir)

    def test_env_variables(self, monkeypatch):
        """Test environment variable overrides."""
        # Set environment variables
        monkeypatch.setenv("LLAMADOC2PDF_TEMP_DIR", "/tmp/llamadoc2pdf_test")
        monkeypatch.setenv("LLAMADOC2PDF_WKHTMLTOPDF_PATH", "/usr/local/bin/wkhtmltopdf")

        # Create config which should use the environment variables
        config = LlamaConfig()

        # Check if environment variables were applied
        assert config.temp_dir == "/tmp/llamadoc2pdf_test"
        assert config.wkhtmltopdf_path == "/usr/local/bin/wkhtmltopdf"
