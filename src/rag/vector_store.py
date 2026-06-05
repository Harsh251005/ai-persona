# src/rag/vector_store.py

import hashlib
from typing import List

from langchain_core.documents import Document
from langchain_core.vectorstores import VectorStoreRetriever
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

from src.rag.embeddings import EmbeddingManager


class VectorStoreManager:
    """
    Manages Qdrant vector store operations.

    Responsibilities:
    - Create/load collection
    - Generate deterministic chunk IDs
    - Index documents
    - Provide retrievers
    """

    def __init__(
            self,
            embedding_manager: EmbeddingManager,
            collection_name: str = "portfolio_rag",
            db_path: str = "./qdrant_db",
    ):
        self.collection_name = collection_name

        self.client = QdrantClient(
            path=db_path,
        )

        collections = self.client.get_collections().collections

        collection_exists = any(
            c.name == collection_name
            for c in collections
        )

        if not collection_exists:
            self.client.create_collection(
                collection_name=collection_name,
                vectors_config=VectorParams(
                    size=1536,  # text-embedding-3-small
                    distance=Distance.COSINE,
                ),
            )

        self.vector_store = QdrantVectorStore(
            client=self.client,
            collection_name=collection_name,
            embedding=embedding_manager.embeddings,
        )

    @staticmethod
    def _generate_chunk_id(
        document: Document,
    ) -> str:
        """
        Generates a deterministic ID for a chunk.

        This prevents duplicate vectors from being
        inserted when re-indexing the same data.
        """

        source_id = document.metadata.get(
            "source_id",
            "unknown_source",
        )

        content = document.page_content

        return hashlib.md5(
            f"{source_id}:{content}".encode("utf-8")
        ).hexdigest()

    def add_documents(
        self,
        documents: List[Document],
    ) -> None:
        """
        Adds documents to Qdrant.
        """

        ids = [
            self._generate_chunk_id(doc)
            for doc in documents
        ]

        self.vector_store.add_documents(
            documents=documents,
            ids=ids,
        )

    def get_retriever(
        self,
        k: int = 5,
    ) -> VectorStoreRetriever:
        """
        Returns a retriever for semantic search.
        """

        return self.vector_store.as_retriever(
            search_kwargs={
                "k": k,
            }
        )

    def similarity_search(
        self,
        query: str,
        k: int = 5,
    ) -> List[Document]:
        """
        Direct similarity search.
        """

        return self.vector_store.similarity_search(
            query=query,
            k=k,
        )

    def similarity_search_with_score(
        self,
        query: str,
        k: int = 5,
    ):
        """
        Similarity search with relevance scores.
        """

        return self.vector_store.similarity_search_with_score(
            query=query,
            k=k,
        )

    def count_documents(self) -> int:
        """
        Returns total vectors in collection.
        """

        collection_info = self.client.get_collection(
            self.collection_name
        )

        return collection_info.points_count

    def delete_collection(self) -> None:
        """
        Deletes the entire collection.
        Useful during development.
        """

        self.client.delete_collection(
            collection_name=self.collection_name
        )

    def close(self) -> None:
        self.client.close()