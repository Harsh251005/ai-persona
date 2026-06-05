from dotenv import load_dotenv
from src.rag.context_loader import ContextLoader
from src.rag.chunker import ContextChunker

load_dotenv()

documents = ContextLoader(
    "context_data"
).load_all()

chunker = ContextChunker()

chunks = chunker.chunk_documents(
    documents
)

print(f"Documents: {len(documents)}")
print(f"Chunks: {len(chunks)}")

from src.rag.embeddings import EmbeddingManager

embedding_manager = EmbeddingManager()

query_embedding = embedding_manager.embed_query(
    "What projects has Harsh built?"
)

print(query_embedding)