from openai import OpenAI

from src.rag.prompt_builder import PromptBuilder
from src.rag.retriever import PortfolioRetriever


class RAGService:
    """
    End-to-end RAG service.

    Query
        ↓
    Retrieval
        ↓
    Prompt Construction
        ↓
    LLM
        ↓
    Response
    """

    def __init__(
        self,
        retriever: PortfolioRetriever,
        model: str = "gpt-4.1-mini",
    ):
        self.retriever = retriever
        self.model = model
        self.client = OpenAI()

    def answer(
            self,
            query: str,
            k: int = 5,
    ) -> dict:
        documents = self.retriever.retrieve(
            query=query,
            k=k,
        )

        prompt = PromptBuilder.build_prompt(
            query=query,
            documents=documents,
        )

        response = self.client.responses.create(
            model=self.model,
            input=prompt,
        )

        return {
            "answer": response.output_text,
            "sources": documents,
        }

    def answer_with_sources(
        self,
        query: str,
        k: int = 5,
    ) -> dict:

        documents = self.retriever.retrieve(
            query=query,
            k=k,
        )

        prompt = PromptBuilder.build_prompt(
            query=query,
            documents=documents,
        )

        response = self.client.responses.create(
            model=self.model,
            input=prompt,
        )

        return {
            "answer": response.output_text,
            "sources": documents,
        }