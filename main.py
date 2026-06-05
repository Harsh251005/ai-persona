from src.rag.context_loader import ContextLoader
from src.rag.chunker import ContextChunker

documents = ContextLoader(
    "context_data"
).load_all()

chunker = ContextChunker()

chunks = chunker.chunk_documents(
    documents
)

print(f"Documents: {len(documents)}")
print(f"Chunks: {len(chunks)}")