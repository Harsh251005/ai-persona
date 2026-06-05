from src.rag.context_loader import ContextLoader

loader = ContextLoader(
    context_dir="context_data"
)

documents = loader.load_all()

print(f"Loaded {len(documents)} documents")