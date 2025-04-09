import os
import sys
import tempfile
import unittest
from unittest.mock import MagicMock, patch

# Add the parent directory to the path to import the module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from mlxpipeline.scraper import (
    ai_extract_webpage_content,
    scrape_audio,
    scrape_csv,
    scrape_docx,
    scrape_html,
    scrape_image,
    scrape_json,
    scrape_markdown,
    scrape_pdf,
    scrape_text,
    scrape_video,
    scrape_webpage,
)


class TestScraper(unittest.TestCase):
    """Test cases for scraper module functions."""

    def test_scrape_text(self):
        """Test scraping text from a text file."""
        # Create a temporary text file
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as temp_file:
            temp_file.write("This is test content.")
            temp_file_path = temp_file.name

        try:
            # Test scraping
            content = scrape_text(temp_file_path)
            self.assertEqual(content, "This is test content.")
        finally:
            # Clean up
            os.unlink(temp_file_path)

    def test_scrape_html(self):
        """Test scraping text from an HTML file."""
        # Create a temporary HTML file
        html_content = """
        <html>
            <head><title>Test Page</title></head>
            <body>
                <h1>Test Header</h1>
                <p>This is test content.</p>
                <script>This should be removed.</script>
                <style>This should also be removed.</style>
            </body>
        </html>
        """
        with tempfile.NamedTemporaryFile(mode="w", suffix=".html", delete=False) as temp_file:
            temp_file.write(html_content)
            temp_file_path = temp_file.name

        try:
            # Test scraping
            content = scrape_html(temp_file_path)
            self.assertIn("Test Header", content)
            self.assertIn("This is test content.", content)
            self.assertNotIn("This should be removed.", content)
            self.assertNotIn("This should also be removed.", content)
        finally:
            # Clean up
            os.unlink(temp_file_path)

    @patch("fitz.open")
    def test_scrape_pdf(self, mock_fitz_open):
        """Test scraping text from a PDF file."""
        # Mock PyMuPDF
        mock_doc = MagicMock()
        mock_page = MagicMock()
        mock_page.get_text.return_value = "This is page content."
        mock_doc.load_page.return_value = mock_page
        mock_doc.__len__.return_value = 1
        mock_fitz_open.return_value = mock_doc

        # Test scraping
        content = scrape_pdf("test.pdf")
        self.assertEqual(content.strip(), "This is page content.")
        mock_fitz_open.assert_called_once_with("test.pdf")
        mock_doc.load_page.assert_called_once_with(0)

    @patch("docx.Document")
    def test_scrape_docx(self, mock_docx):
        """Test scraping text from a DOCX file."""
        # Mock python-docx
        mock_doc = MagicMock()
        mock_para1 = MagicMock()
        mock_para1.text = "This is paragraph 1."
        mock_para2 = MagicMock()
        mock_para2.text = "This is paragraph 2."
        mock_doc.paragraphs = [mock_para1, mock_para2]
        mock_docx.return_value = mock_doc

        # Test scraping
        content = scrape_docx("test.docx")
        self.assertEqual(content, "This is paragraph 1.\n\nThis is paragraph 2.")
        mock_docx.assert_called_once_with("test.docx")

    @patch("pytesseract.image_to_string")
    @patch("PIL.Image.open")
    def test_scrape_image(self, mock_image_open, mock_image_to_string):
        """Test scraping text from an image using OCR."""
        # Mock PIL and pytesseract
        mock_image = MagicMock()
        mock_image_open.return_value = mock_image
        mock_image_to_string.return_value = "OCR extracted text."

        # Test scraping
        content = scrape_image("test.jpg")
        self.assertEqual(content, "OCR extracted text.")
        mock_image_open.assert_called_once_with("test.jpg")
        mock_image_to_string.assert_called_once_with(mock_image)

    @patch("mlxpipeline.scraper.WhisperMLX")
    def test_scrape_audio(self, mock_whisper_class):
        """Test transcribing audio."""
        # Mock Whisper
        mock_whisper = MagicMock()
        mock_whisper_class.return_value = mock_whisper
        mock_whisper.transcribe.return_value = {"text": "This is a transcription."}

        # Test transcription
        content = scrape_audio("test.mp3", whisper_model_path="test_model")
        self.assertEqual(content, "This is a transcription.")
        mock_whisper_class.assert_called_once_with("test_model")
        mock_whisper.transcribe.assert_called_once_with("test.mp3")

    @patch("subprocess.run")
    @patch("mlxpipeline.scraper.scrape_audio")
    def test_scrape_video(self, mock_scrape_audio, mock_subprocess_run):
        """Test extracting audio from video and transcribing it."""
        # Mock dependencies
        mock_scrape_audio.return_value = "This is a video transcription."

        # Test transcription
        content = scrape_video("test.mp4", whisper_model_path="test_model")
        self.assertEqual(content, "This is a video transcription.")
        mock_subprocess_run.assert_called_once()
        mock_scrape_audio.assert_called_once()

    @patch("frontmatter.load")
    def test_scrape_markdown(self, mock_frontmatter_load):
        """Test extracting text from markdown with frontmatter."""
        # Mock frontmatter
        mock_post = MagicMock()
        mock_post.content = "This is markdown content."
        mock_post.metadata = {"title": "Test", "date": "2023-01-01"}
        mock_frontmatter_load.return_value = mock_post

        # Test extraction
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as temp_file:
            temp_file.write("---\ntitle: Test\ndate: 2023-01-01\n---\nThis is markdown content.")
            temp_file_path = temp_file.name

        try:
            content = scrape_markdown(temp_file_path)
            self.assertIn("title: Test", content)
            self.assertIn("This is markdown content.", content)
        finally:
            # Clean up
            os.unlink(temp_file_path)

    def test_scrape_json(self):
        """Test extracting text from a JSON file."""
        # Create a temporary JSON file
        json_content = {"name": "Test", "age": 30}
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as temp_file:
            import json

            json.dump(json_content, temp_file)
            temp_file_path = temp_file.name

        try:
            # Test extraction
            content = scrape_json(temp_file_path)
            parsed = json.loads(content)
            self.assertEqual(parsed["name"], "Test")
            self.assertEqual(parsed["age"], 30)
        finally:
            # Clean up
            os.unlink(temp_file_path)

    def test_scrape_csv(self):
        """Test extracting text from a CSV file."""
        # Create a temporary CSV file
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as temp_file:
            temp_file.write("name,age\nJohn,25\nJane,30")
            temp_file_path = temp_file.name

        try:
            # Test extraction
            content = scrape_csv(temp_file_path)
            self.assertIn("name, age", content)
            self.assertIn("John, 25", content)
            self.assertIn("Jane, 30", content)
        finally:
            # Clean up
            os.unlink(temp_file_path)

    @patch("requests.get")
    def test_scrape_webpage(self, mock_get):
        """Test scraping content from a webpage."""
        # Mock requests
        mock_response = MagicMock()
        mock_response.text = """
        <html>
            <head><title>Test Page</title></head>
            <body>
                <h1>Test Header</h1>
                <p>This is test content.</p>
                <script>This should be removed.</script>
                <style>This should also be removed.</style>
            </body>
        </html>
        """
        mock_response.apparent_encoding = "utf-8"
        mock_get.return_value = mock_response

        # Test scraping
        content = scrape_webpage("https://example.com")
        self.assertIn("Test Header", content)
        self.assertIn("This is test content.", content)
        self.assertNotIn("This should be removed.", content)
        mock_get.assert_called_once()

    @patch("mlxpipeline.scraper.scrape_webpage")
    @patch("mlxpipeline.extract.extract_from_chunk")
    def test_ai_extract_webpage_content(self, mock_extract, mock_scrape):
        """Test AI extraction of webpage content."""
        # Mock dependencies
        mock_scrape.return_value = "Raw webpage content with navigation menus and other stuff."
        mock_extract.return_value = (
            '{"title": "Test", "main_content": "This is the extracted main content."}'
        )

        # Test extraction
        content = ai_extract_webpage_content("https://example.com")
        self.assertEqual(content, "This is the extracted main content.")
        mock_scrape.assert_called_once_with("https://example.com")
        mock_extract.assert_called_once()


if __name__ == "__main__":
    unittest.main()
