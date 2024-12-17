from sentence_transformers import SentenceTransformer

class EmbeddingGenerator:
    """Class to generate embeddings for text."""

    def __init__(self, model_name):
        self.model = SentenceTransformer(model_name)

    def generate_embedding(self, text):
        """Generate embedding for a given text."""
        return self.model.encode(text).tolist()