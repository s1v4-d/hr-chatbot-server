# backend/augmentations/vector_search_with_filtering.py

from backend.augmentations.multi_query_generator import MultiQueryGenerator  # assuming this is your multi-query generator
from backend.augmentations.redundancy_filter import RedundancyFilter
from backend.augmentations.reranker import Reranker
from backend.vector_management.pinecone_manager import PineconeManager  # assuming this is how you access Pinecone

class VectorSearchWithFiltering:
    def __init__(self, query, multi_query_generator, pinecone_manager, redundancy_threshold=0.90):
        self.query = query
        self.multi_query_generator = multi_query_generator
        self.redundancy_filter = RedundancyFilter(threshold=redundancy_threshold)
        self.reranker = Reranker()
        self.pinecone_manager = pinecone_manager

    def perform_search(self):
        # Step 1: Generate multi-queries from the original query
        expanded_queries = self.multi_query_generator.generate(self.query)
        
        # Step 2: Perform vector search for each expanded query and collect results
        all_results = []
        for query in expanded_queries:
            results_for_query = self.vector_search(query)  # perform search using Pinecone
            all_results.extend(results_for_query)
        
        # Step 3: Remove redundant documents based on cosine similarity
        filtered_results = self.redundancy_filter.filter(all_results)
        
        # Step 4: Rerank remaining documents based on the original query
        final_results = self.reranker.rerank(self.query, filtered_results)
        
        return final_results

    def vector_search(self, query):
        # Use PineconeManager to retrieve results from Pinecone vector search
        return self.pinecone_manager.search(query)