from src.rag.embeddings import EmbeddingManager
from src.rag.vector_store import VectorStoreManager
from src.rag.retriever import PortfolioRetriever
from src.rag.rag_service import RAGService

from dotenv import load_dotenv
load_dotenv()


def main():

    embedding_manager = EmbeddingManager()

    vector_store = VectorStoreManager(
        embedding_manager=embedding_manager,
    )

    retriever = PortfolioRetriever(
        vector_store=vector_store,
    )

    rag = RAGService(
        retriever=retriever,
    )

    try:

        while True:

            query = input("\nQuestion: ")

            if query.lower() in {
                "quit",
                "exit",
            }:
                break

            answer = rag.answer(query)

            print("\nAnswer:")
            print(answer)

    finally:
        vector_store.close()


if __name__ == "__main__":
    main()