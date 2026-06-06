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
        collection_name="portfolio_rag",
        db_path="./qdrant_db",
    )

    retriever = PortfolioRetriever(
        vector_store=vector_store,
    )

    rag = RAGService(
        retriever=retriever,
    )

    try:

        print("\nPortfolio RAG Ready")
        print("Type 'exit' to quit.\n")

        while True:

            query = input("Question: ").strip()

            if not query:
                continue

            if query.lower() in {
                "exit",
                "quit",
            }:
                break

            answer = rag.answer(
                query=query,
                k=5,
            )

            print("\nAnswer:")
            print(answer)
            print()

    finally:
        vector_store.close()


if __name__ == "__main__":
    main()