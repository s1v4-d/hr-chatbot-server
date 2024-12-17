from backend.embeddings.embedding_generator import EmbeddingGenerator
from backend.vector_management.pinecone_manager import PineconeManager
from backend.augmentations.multi_query_generator import MultiQueryGenerator
from backend.config import Config
from backend.augmentations.document_reranker import DocumentReranker

class VectorSearch:
    """Hybrid search with optional multiquery and reranking."""

    def __init__(self, embedding_model_name, pinecone_api_key, pinecone_index_name, dimension=1024):
        self.embedding_generator = EmbeddingGenerator(model_name=embedding_model_name)
        self.pinecone_manager = PineconeManager(
            api_key=pinecone_api_key,
            index_name=pinecone_index_name,
            dimension=dimension
        )
        self.reranker = DocumentReranker()
        
    def search_vector_db(self, query, top_k=3):
        return self._perform_vector_search(query, top_k)

    def _perform_vector_search(self, query, top_k):
        query_embedding = self.embedding_generator.generate_embedding(query)
        vector_search_results = self.pinecone_manager.query_vectors(query_embedding, top_k=top_k)
        return vector_search_results

    def get_context(self, query, top_k=3, multiquery=True, reranking=True):
        if multiquery:
            generator = MultiQueryGenerator(query, 2)
            queries = generator.generate_queries()
            retrievals = []
            for q in queries:
                results = self.search_vector_db(q, top_k=top_k)
                retrievals.append(results)
            scored_chunks = []
            for retrieval in retrievals:
                for match in retrieval['matches']:
                    scored_chunks.append({
                        'chunk': match['metadata']['chunk'],
                        'score': match['score']
                    })
        else:
            single_results = self.search_vector_db(query, top_k=top_k)
            scored_chunks = []
            for match in single_results['matches']:
                scored_chunks.append({
                    'chunk': match['metadata']['chunk'],
                    'score': match['score']
                })


        if reranking:
            scored_chunks = self.reranker.rerank_documents(query, scored_chunks, top_k=top_k)

        context = ''
        for chunk in scored_chunks:
            context += chunk['chunk'] + '\n'
        return context