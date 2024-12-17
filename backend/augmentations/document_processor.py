from backend.parsers.docx_parser import DocxParser
from llama_index.core.node_parser import SentenceSplitter


class DocumentProcessor:
    """Class to process documents and split them into chunks."""

    def __init__(self, chunk_size=1000, chunk_overlap=10):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.splitter = SentenceSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)

    def process_docx(self, file_path):
        """
        Process a DOCX file and split its content into chunks.
        """
        parser = DocxParser()
        text = parser.extract_text(file_path)
        chunks = self.splitter.split_text(text)
        
        # Debugging statements to verify the output
        print(f"Number of chunks: {len(chunks)}")
        for i, chunk in enumerate(chunks):
            print(f"Chunk {i}: {chunk[:50]}...")  # Print first 50 characters of each chunk
        
        return chunks