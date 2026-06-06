from src.rag.context_loader import ContextLoader
from src.rag.chunker import ContextChunker
from src.rag.embeddings import EmbeddingManager
from src.rag.vector_store import VectorStoreManager

from dotenv import load_dotenv
load_dotenv()


def main():

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

    embedding_manager = EmbeddingManager()

    vector_store = VectorStoreManager(
        embedding_manager=embedding_manager,
        collection_name="portfolio_rag",
        db_path="./qdrant_db",
    )

    try:

        print("Indexing documents...")

        vector_store.add_documents(
            chunks
        )

        print(
            f"Indexed {vector_store.count_documents()} chunks"
        )

    finally:
        vector_store.close()


if __name__ == "__main__":
    main()