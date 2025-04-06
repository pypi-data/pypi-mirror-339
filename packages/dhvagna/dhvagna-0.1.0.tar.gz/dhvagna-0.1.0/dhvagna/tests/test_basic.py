"""
Basic tests for the Dhvagna package.

These tests verify that the package imports correctly and can be used
without errors. They don't test actual audio recording or API calls.
"""

import unittest
import os
import sys

# Add the parent directory to the path so we can import the package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from dhvagna import __version__

class TestDhvagna(unittest.TestCase):
    """Basic tests for the Dhvagna package."""
    
    def test_version(self):
        """Test that the package has a version."""
        self.assertIsNotNone(__version__)
        self.assertTrue(isinstance(__version__, str))
    
    def test_imports(self):
        """Test that the package imports correctly."""
        try:
            from dhvagna import record_audio, transcribe_wav_file
            self.assertTrue(callable(record_audio))
            self.assertTrue(callable(transcribe_wav_file))
        except ImportError as e:
            self.fail(f"Import failed: {e}")
            
if __name__ == "__main__":
    unittest.main()