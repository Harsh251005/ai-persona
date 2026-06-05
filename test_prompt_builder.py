from src.rag.embeddings import EmbeddingManager
from src.rag.vector_store import VectorStoreManager
from src.rag.retriever import PortfolioRetriever
from src.rag.prompt_builder import PromptBuilder
from dotenv import load_dotenv
load_dotenv()

embedding_manager = EmbeddingManager()

vector_store = VectorStoreManager(
    embedding_manager=embedding_manager
)

retriever = PortfolioRetriever(
    vector_store=vector_store
)

docs = retriever.retrieve(
    "What projects has Harsh worked on?"
)

prompt = PromptBuilder.build_prompt(
    query="What projects has Harsh worked on?",
    documents=docs,
)

print(prompt)

vector_store.close()