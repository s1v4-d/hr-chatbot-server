# backend/augmentations/redundancy_filter.py

from sklearn.metrics.pairwise import cosine_similarity
import torch
from transformers import AutoTokenizer, AutoModel

class RedundancyFilter:
    def __init__(self, threshold=0.90):
        self.threshold = threshold
        self.tokenizer = AutoTokenizer.from_pretrained('bge-rerank-base')
        self.model = AutoModel.from_pretrained('bge-rank-base')

    def encode(self, text):
        # Tokenize and encode the input text
        inputs = self.tokenizer(text, return_tensors="pt", padding=True, truncation=True)
        with torch.no_grad():
            outputs = self.model(**inputs)
        return outputs.pooler_output.squeeze().numpy()

    def filter(self, documents):
        embeddings = [self.encode(doc) for doc in documents]
        similarities = cosine_similarity(embeddings)
        filtered_docs = []
        
        for i, doc in enumerate(documents):
            is_redundant = False
            for j in range(i):
                if similarities[i, j] > self.threshold:
                    is_redundant = True
                    break
            if not is_redundant:
                filtered_docs.append(doc)
        
        return filtered_docs