import numpy as np

class Reranker:
    """Class to handle deduplication and re-ranking of retrieval results."""

    @staticmethod
    def deduplicate_and_rank(results):
        """
        Deduplicate results by ID and re-rank based on normalized scores.

        Args:
            results (list): List of retrieval results from hybrid search.

        Returns:
            list: Deduplicated and re-ranked results.
        """
        # Deduplicate by ID
        unique_results = {}
        for result in results:
            result_id = result["id"]
            if result_id not in unique_results or unique_results[result_id]["score"] < result["score"]:
                unique_results[result_id] = result

        # Normalize scores for fair ranking
        scores = np.array([result["score"] for result in unique_results.values()])
        if len(scores) > 0:
            normalized_scores = (scores - scores.min()) / (scores.max() - scores.min() + 1e-10)
            for i, result in enumerate(unique_results.values()):
                result["normalized_score"] = normalized_scores[i]

        # Sort by normalized score in descending order
        ranked_results = sorted(unique_results.values(), key=lambda x: x["normalized_score"], reverse=True)
        return ranked_results