import streamlit as st

from src.rag.embeddings import EmbeddingManager
from src.rag.vector_store import VectorStoreManager
from src.rag.retriever import PortfolioRetriever
from src.rag.rag_service import RAGService
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="Harsh AI Persona",
    page_icon="🤖",
    layout="wide",
)

@st.cache_resource
def initialize_rag():

    embedding_manager = EmbeddingManager()

    vector_store = VectorStoreManager(
        embedding_manager=embedding_manager,
        collection_name="portfolio_rag",
        db_path="./qdrant_db",
    )

    retriever = PortfolioRetriever(
        vector_store=vector_store,
    )

    return RAGService(
        retriever=retriever,
    )


rag = initialize_rag()

st.set_page_config(
    page_title="Harsh AI Persona",
    page_icon="🤖",
    layout="wide",
)

# --------------------------------------------------
# Sidebar
# --------------------------------------------------

with st.sidebar:

    st.title("🤖 Harsh AI Persona")

    st.markdown(
        """
Ask questions about:

- Skills
- Experience
- Projects
- Education
- Technical Background
- AI Engineering Work
"""
    )

    st.divider()

    st.subheader("Projects")

    st.markdown(
        """
- TruthLens-AI
- Evident-AI
"""
    )

    st.divider()

    st.caption(
        "Powered by OpenAI + Qdrant + RAG"
    )

# --------------------------------------------------
# Session State
# --------------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

# --------------------------------------------------
# Chat History
# --------------------------------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --------------------------------------------------
# User Input
# --------------------------------------------------

query = st.chat_input(
    "Ask something about Harsh..."
)

if query:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": query,
        }
    )

    with st.chat_message("user"):
        st.markdown(query)

    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            result = rag.answer(
                query=query,
                k=5,
            )

            answer = result["answer"]
            sources = result["sources"]

        st.markdown(answer)

        with st.expander(
            "📚 Sources Used"
        ):

            for idx, doc in enumerate(
                sources,
                start=1,
            ):

                source_type = doc.metadata.get(
                    "source_type",
                    "unknown",
                )

                source_id = doc.metadata.get(
                    "source_id",
                    "unknown",
                )

                st.markdown(
                    f"""
                ### Source {idx}

                **Type:** {source_type}

                **ID:** {source_id}

                ```text
                {doc.page_content[:500]}
                """
                )

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer,
        }
    )