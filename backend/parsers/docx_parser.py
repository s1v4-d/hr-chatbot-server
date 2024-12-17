from docx import Document

class DocxParser:
    """Class to parse DOCX files and extract text."""

    @staticmethod
    def extract_text(file_path):
        """
        Extract text from a DOCX file.

        Args:
            file_path (str): Path to the DOCX file.

        Returns:
            str: Extracted text as a single string.
        """
        doc = Document(file_path)
        return "\n".join([para.text.strip() for para in doc.paragraphs if para.text.strip()])