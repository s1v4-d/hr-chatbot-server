from FlagEmbedding import FlagReranker

class DocumentReranker:
    def __init__(self, model_name="BAAI/bge-reranker-base", use_fp16=True):
        """
        Initializes the reranker with the given model and options.
        """
        self.reranker = FlagReranker(model_name_or_path=model_name, use_fp16=use_fp16)
    
    def rerank_documents(self, query, scored_chunks, top_k=3):
        """
        Reranks the documents based on the provided query and returns the top-k results.
        The input `scored_chunks` is expected to be a list of dictionaries containing 'chunk' and 'score'.
        
        :param top_k: The number of top results to return.
        :param query: The query string to be used for reranking.
        :param scored_chunks: A list of dictionaries where each dictionary contains 'chunk' and 'score'.
        
        :return: A list of dictionaries with 'chunk' and the new computed 'score'.
        """
        # Extract the chunks (text) from the scored_chunks list of dictionaries
        chunks = [chunk['chunk'] for chunk in scored_chunks]
        
        # Prepare input for reranking by pairing query with each chunk
        query_chunk_pairs = [[query, chunk] for chunk in chunks]
        
        # Perform reranking using the FlagReranker compute_score method
        results = self.reranker.compute_score(query_chunk_pairs)
        
        # Now we need to pair the reranked scores back with the corresponding chunks.
        reranked_chunks_with_scores = [
            {"chunk": scored_chunks[i]['chunk'], "score": results[i]}
            for i in range(len(results))
        ]
        
         # Sort the results by score in descending order
        reranked_chunks_with_scores.sort(key=lambda x: x['score'], reverse=True)
        
        # Return the top-k results
        return reranked_chunks_with_scores[:top_k]