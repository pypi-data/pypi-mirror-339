"""
https://github.com/barseghyanartur/sphinx-no-pragma/
"""

import shutil
import unittest
from pathlib import Path

from sphinx.application import Sphinx
from sphinx_no_pragma import DEFAULT_IGNORE_COMMENTS_ENDINGS

__author__ = "Artur Barseghyan <artur.barseghyan@gmail.com>"
__copyright__ = "2023-2025 Artur Barseghyan"
__license__ = "MIT"
__all__ = ("TestNoPragmaLiteralInclude",)


class TestNoPragmaLiteralInclude(unittest.TestCase):
    def setUp(self):
        root_dir = Path(__file__).parent
        self.docs_dir = root_dir / "docs"
        self.build_dir = root_dir / "test_build_docs"
        self.doc_tree_dir = self.build_dir / "doc_trees"

    def test_build_docs(self):
        # Build the docs using Sphinx
        test_app = Sphinx(
            self.docs_dir,  # Source directory
            self.docs_dir,  # Config directory
            self.build_dir,  # Output directory
            self.doc_tree_dir,  # Doc-tree directory
            "html",  # Builder
        )
        test_app.build()

        # Check if usage.html exists
        demo_html_path = self.build_dir / "demo.html"
        self.assertTrue(demo_html_path.exists())

        # Read the content of demo.html
        content = demo_html_path.read_text()

        # Check for the absence of pragma comments
        for ignore_comment_ending in DEFAULT_IGNORE_COMMENTS_ENDINGS:
            with self.subTest(ignore_comment_ending):
                self.assertNotIn(ignore_comment_ending, content)

    def tearDown(self):
        # Clean up the build directory
        if self.build_dir.exists():
            shutil.rmtree(self.build_dir)
