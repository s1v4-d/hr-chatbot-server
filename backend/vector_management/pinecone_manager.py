from pinecone import Pinecone, ServerlessSpec
from backend.config import Config

class PineconeManager:
    def __init__(self, api_key, index_name, dimension=Config.PINECONE_DIMENSION):
        """
        Initialize Pinecone client and index.

        Args:
            api_key (str): Pinecone API key.
            index_name (str): Name of the index to manage.
            dimension (int): Dimensionality of the vectors.
        """
        print("Initializing PineconeManager...")
        self.index_name = index_name
        self.dimension = dimension
        self.cloud = Config.PINECONE_CLOUD
        self.region = Config.PINECONE_ENVIRONMENT

        # print(f"Connecting to Pinecone with API key: {api_key}")
        # Initialize Pinecone client
        self.client = Pinecone(api_key=api_key)

        # Create the index if it doesn't exist
        # print(f"Checking if index '{self.index_name}' exists...")
        if self.index_name not in self.client.list_indexes().names():
            print(f"Index '{self.index_name}' not found. Creating a new index...")
            self.client.create_index(
                name=self.index_name,
                dimension=self.dimension,
                metric="cosine",  # Metric can be adjusted if needed
                spec=ServerlessSpec(cloud=self.cloud, region=self.region)
            )
            print(f"Index '{self.index_name}' created successfully.")
        else:
            print(f"Index '{self.index_name}' already exists.")

        # Connect to the index
        # print(f"Connecting to the index '{self.index_name}'...")
        self.index = self.client.Index(self.index_name)
        # print(f"Connected to the index '{self.index_name}' successfully.")

    def upsert_vectors(self, vectors):
        """
        Upsert vectors to the Pinecone index.

        Args:
            vectors (list): List of tuples in the format (id, vector, metadata).
        """
        # print(f"Upserting {len(vectors)} vectors into the index '{self.index_name}'...")
        self.index.upsert(vectors)
        # print(f"Upserted {len(vectors)} vectors successfully.")

    def query_vectors(self, vector, top_k=5):
        """
        Query vectors in the Pinecone index.

        Args:
            vector (list): Query vector.
            top_k (int): Number of top results to retrieve.

        Returns:
            dict: Query results.
        """
        # print(f"Querying the index '{self.index_name}' with a vector. Top {top_k} results requested...")
        results = self.index.query(vector=vector, top_k=top_k, include_metadata=True)
        # print(f"Query completed. Retrieved {len(results.get('matches', []))} results.")
        return results