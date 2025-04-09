"""Tests for the batch processing module."""

import os
import tempfile
from pathlib import Path

from llamadoc2pdf.batch import BatchProcessor, process_directory


class TestBatchProcessing:
    """Test suite for the batch processing module."""

    def setup_method(self):
        """Set up test environment."""
        self.temp_dir = tempfile.TemporaryDirectory()
        self.output_dir = Path(self.temp_dir.name) / "output"
        self.output_dir.mkdir()

        # Create test files
        self.test_files = []
        for i, ext in enumerate([".txt", ".md"]):
            input_path = Path(self.temp_dir.name) / f"test{i}{ext}"
            output_path = self.output_dir / f"test{i}.pdf"
            with open(input_path, "w") as f:
                f.write(f"Test content for file {i}")
            self.test_files.append((input_path, output_path))

    def teardown_method(self):
        """Clean up after tests."""
        self.temp_dir.cleanup()

    def test_batch_processor(self):
        """Test batch processing of files."""
        processor = BatchProcessor(max_workers=2)
        results = processor.process(self.test_files)

        # Check results
        assert len(results) == len(self.test_files)

        # All conversions should succeed
        for _, _, success in results:
            assert success

        # Check output files
        for _, output_path, _ in results:
            assert os.path.exists(output_path)

    def test_process_directory(self):
        """Test processing a directory of files."""
        input_dir = Path(self.temp_dir.name)
        output_dir = self.output_dir

        results = process_directory(input_dir, output_dir, recursive=False)

        # Check results
        assert len(results) == len(self.test_files)

        # All conversions should succeed
        for _, _, success in results:
            assert success

        # Check output files exist
        assert os.path.exists(output_dir / "test0.pdf")
        assert os.path.exists(output_dir / "test1.pdf")
