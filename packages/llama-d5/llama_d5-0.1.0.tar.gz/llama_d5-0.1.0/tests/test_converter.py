"""Tests for the converter module."""

import os
import tempfile
from pathlib import Path

import pytest
from llamadoc2pdf.converter import DocumentConverter


class TestDocumentConverter:
    """Test suite for the DocumentConverter class."""

    def setup_method(self):
        """Set up test environment."""
        self.converter = DocumentConverter()
        self.temp_dir = tempfile.TemporaryDirectory()

    def teardown_method(self):
        """Clean up after tests."""
        self.temp_dir.cleanup()

    def create_test_file(self, extension):
        """Create a test file with the given extension."""
        input_path = Path(self.temp_dir.name) / f"test{extension}"
        with open(input_path, "w") as f:
            f.write("Test content")
        return input_path

    def test_convert_text(self):
        """Test converting a text file."""
        input_path = self.create_test_file(".txt")
        output_path = Path(self.temp_dir.name) / "output.pdf"

        result = self.converter.convert(str(input_path), str(output_path))

        assert os.path.exists(result)
        assert result == str(output_path)

    def test_convert_markdown(self):
        """Test converting a markdown file."""
        input_path = self.create_test_file(".md")
        output_path = Path(self.temp_dir.name) / "output.pdf"

        result = self.converter.convert(str(input_path), str(output_path))

        assert os.path.exists(result)
        assert result == str(output_path)

    def test_unsupported_format(self):
        """Test handling of unsupported file formats."""
        input_path = self.create_test_file(".xyz")
        output_path = Path(self.temp_dir.name) / "output.pdf"

        with pytest.raises(ValueError, match="Unsupported file format"):
            self.converter.convert(str(input_path), str(output_path))

    def test_file_not_found(self):
        """Test handling of non-existent files."""
        input_path = Path(self.temp_dir.name) / "nonexistent.txt"
        output_path = Path(self.temp_dir.name) / "output.pdf"

        with pytest.raises(FileNotFoundError):
            self.converter.convert(str(input_path), str(output_path))
