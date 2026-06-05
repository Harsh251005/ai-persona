# main.py

from src.rag.context_loader import ContextLoader
from src.rag.chunker import ContextChunker
from src.rag.embeddings import EmbeddingManager
from src.rag.vector_store import VectorStoreManager
from dotenv import load_dotenv

load_dotenv()


def main() -> None:
    print("Loading documents...")

    documents = ContextLoader(
        context_dir="context_data"
    ).load_all()

    print(f"Loaded {len(documents)} documents")

    print("Chunking documents...")

    chunks = ContextChunker().chunk_documents(
        documents
    )

    print(f"Created {len(chunks)} chunks")

    print("Initializing embeddings...")

    embedding_manager = EmbeddingManager()

    print("Initializing vector store...")

    vector_store = VectorStoreManager(
        embedding_manager=embedding_manager,
        collection_name="portfolio_rag",
        db_path="./qdrant_db",
    )

    try:
        print("Indexing chunks...")

        vector_store.add_documents(
            chunks
        )

        print(
            f"Indexed {vector_store.count_documents()} chunks"
        )

        print("\nTesting retrieval...\n")

        results = vector_store.similarity_search_with_score(
            query="What is evidentai and show it's latest commits",
            k=10,
        )

        for doc, score in results:
            print(score)
            print(doc.metadata)
            print("-" * 150)
            print(doc.page_content)
            print("-" * 150)

        from collections import Counter

        counter = Counter()

        for chunk in chunks:
            counter[chunk.metadata["source_type"]] += 1

        print(counter)

    finally:
        vector_store.close()


if __name__ == "__main__":
    main()