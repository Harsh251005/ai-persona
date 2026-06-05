from typing import List

from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings


class EmbeddingManager:
    """
    Handles embedding model creation and document embedding.
    """

    def __init__(
        self,
        model: str = "text-embedding-3-small",
    ):
        self.embedding_model = OpenAIEmbeddings(
            model=model,
        )

    @property
    def embeddings(self) -> OpenAIEmbeddings:
        return self.embedding_model

    def embed_documents(
        self,
        documents: List[Document],
    ) -> List[List[float]]:
        return self.embedding_model.embed_documents(
            [doc.page_content for doc in documents]
        )

    def embed_query(
        self,
        query: str,
    ) -> List[float]:
        return self.embedding_model.embed_query(query)