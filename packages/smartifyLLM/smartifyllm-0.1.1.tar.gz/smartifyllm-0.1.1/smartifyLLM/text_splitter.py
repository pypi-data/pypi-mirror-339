import re
import pdfplumber
from docx import Document

class TextSplitter:
    def __init__(self, chunk_size: int = 300, chunk_overlap: int = 50):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def split_text(self, text: str) -> list[str]:
        """
        Splits raw text into overlapping chunks.

        Args:
            text (str): The input text.

        Returns:
            list[str]: List of text chunks.
        """
        words = re.split(r'\s+', text.strip())
        chunks = []
        start = 0
        while start < len(words):
            end = min(start + self.chunk_size, len(words))
            chunks.append(' '.join(words[start:end]))
            start += self.chunk_size - self.chunk_overlap
        return chunks

    def split_pdf(self, pdf_path: str) -> list[str]:
        """
        Extracts and splits text from a PDF.

        Args:
            pdf_path (str): Path to the PDF file.

        Returns:
            list[str]: List of text chunks.
        """
        with pdfplumber.open(pdf_path) as pdf:
            full_text = '\n'.join(page.extract_text() for page in pdf.pages)
        return self.split_text(full_text)

    def split_docx(self, docx_path: str) -> list[str]:
        """
        Extracts and splits text from a Word document.

        Args:
            docx_path (str): Path to the .docx file.

        Returns:
            list[str]: List of text chunks.
        """
        doc = Document(docx_path)
        full_text = '\n'.join(para.text for para in doc.paragraphs)
        return self.split_text(full_text)