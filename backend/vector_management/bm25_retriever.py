from elasticsearch import Elasticsearch
from backend.config import Config

class BM25Retriever:
    """BM25 Retriever for keyword-based search using Elasticsearch."""

    def __init__(self):
        """
        Initialize Elasticsearch client and ensure index exists.
        """
        self.client = Elasticsearch(
            hosts=[Config.ELASTICSEARCH_HOST],
            http_auth=(Config.ELASTICSEARCH_USERNAME, Config.ELASTICSEARCH_PASSWORD)
        )
        self.index_name = "documents"

    def index_document(self, doc_id, content):
        """
        Index a single document into Elasticsearch.

        Args:
            doc_id (str): Unique identifier for the document.
            content (str): Text content of the document.
        """
        self.client.index(index=self.index_name, id=doc_id, document={"content": content})

    def search(self, query, top_k=10):
        """
        Perform a BM25 keyword search.

        Args:
            query (str): Query string.
            top_k (int): Number of results to retrieve.

        Returns:
            list: List of matching documents with scores.
        """
        response = self.client.search(
            index=self.index_name,
            body={
                "query": {
                    "match": {"content": query}
                }
            },
            size=top_k
        )
        results = []
        for hit in response["hits"]["hits"]:
            results.append({
                "id": hit["_id"],
                "score": hit["_score"],
                "metadata": {"chunk": hit["_source"]["content"]}
            })
        return results