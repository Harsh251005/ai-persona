from typing import List

from langchain_core.documents import Document
from langsmith import traceable

from src.rag.vector_store import VectorStoreManager


class PortfolioRetriever:
    """
    Handles retrieval operations for the portfolio RAG system.
    """

    def __init__(
        self,
        vector_store: VectorStoreManager,
    ):
        self.vector_store = vector_store

    @traceable(name="retrieve_documents")
    def retrieve(
        self,
        query: str,
        k: int = 5,
    ) -> List[Document]:
        """
        Retrieve the most relevant documents for a query.
        """

        return self.vector_store.similarity_search(
            query=query,
            k=k,
        )

    def retrieve_with_scores(
        self,
        query: str,
        k: int = 5,
    ):
        """
        Retrieve documents along with similarity scores.
        """

        return self.vector_store.similarity_search_with_score(
            query=query,
            k=k,
        )

    @staticmethod
    def format_context(
            documents: List[Document],
    ) -> str:
        """
        Convert retrieved documents into a prompt-friendly string.
        """

        sections = []

        for idx, doc in enumerate(documents, start=1):
            source = doc.metadata.get(
                "source_type",
                "unknown",
            )

            content = doc.page_content.strip()

            sections.append(
                f"""
    Source {idx}
    Type: {source}

    {content}
    """
            )

        return "\n\n".join(sections)