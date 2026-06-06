import streamlit as st
import openai
import json
from dotenv import load_dotenv

# Import RAG pipeline modules
from src.rag.embeddings import EmbeddingManager
from src.rag.vector_store import VectorStoreManager
from src.rag.retriever import PortfolioRetriever
from src.rag.rag_service import RAGService

# Import Calendar engine modules
from src.calendar.booking_service import (
    cal_booking_tool,
    cal_availability_tool,
    cal_cancel_tool,
    get_calendar_system_prompt,
)
from src.calendar.cal_client import (
    execute_cal_booking,
    check_cal_availability,
    cancel_cal_booking,
)

# Load environment configuration
load_dotenv()

# Streamlit Page Setup (Must be the very first Streamlit command)
st.set_page_config(
    page_title="Harsh AI Persona",
    page_icon="🤖",
    layout="wide",
)


@st.cache_resource
def initialize_rag():
    """Initializes and caches the local vector store and RAG pipeline components."""
    embedding_manager = EmbeddingManager()
    vector_store = VectorStoreManager(
        embedding_manager=embedding_manager,
        collection_name="portfolio_rag",
        db_path="./qdrant_db",
    )
    retriever = PortfolioRetriever(vector_store=vector_store)
    return RAGService(retriever=retriever)


# Instantiate core engines
rag = initialize_rag()
client = openai.OpenAI()

# --------------------------------------------------
# Sidebar Configuration
# --------------------------------------------------
with st.sidebar:
    st.title("🤖 Harsh AI Persona")
    st.markdown(
        """
Ask questions about:
- Skills & Professional Experience
- Projects (TruthLens-AI, Evident-AI)
- Technical Architecture
- **Check availability & book a meeting live**
"""
    )
    st.divider()
    st.subheader("Featured Projects")
    st.markdown(
        """
- **TruthLens-AI:** Deepfake Detection Application
- **Evident-AI:** Production-Grade RAG Pipeline
"""
    )
    st.divider()
    st.caption("Powered by OpenAI + Qdrant + Cal.com API v2")

# --------------------------------------------------
# Session State & Chat History Retention
# --------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# Redraw previous conversation entries
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --------------------------------------------------
# Execution Loop
# --------------------------------------------------
query = st.chat_input("Ask about Harsh's work or check his calendar availability...")

if query:
    # Append and present user message
    st.session_state.messages.append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.markdown(query)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):

            sources = []
            answer = ""

            # 1. Build system prompt with calendar rules + current clock
            system_instruction = (
                "You are Harsh's official AI Persona. You possess four tools:\n"
                "1. 'search_portfolio': Queries the Qdrant DB for resume and tech context.\n"
                "2. 'check_cal_availability': Reads real-time calendar open slots.\n"
                "3. 'execute_cal_booking': Confirms a calendar reservation.\n"
                "4. 'cancel_cal_booking': Cancels an existing booking by uid.\n\n"
                "CRITICAL: Always run 'check_cal_availability' before booking. "
                "Never guess dates or assume a slot is free without reading it.\n"
                + get_calendar_system_prompt()
            )

            # Build full message context for LLM
            messages = [{"role": "system", "content": system_instruction}]
            for msg in st.session_state.messages:
                messages.append({"role": msg["role"], "content": msg["content"]})

            # 2. Portfolio tool schema
            portfolio_tool = {
                "type": "function",
                "function": {
                    "name": "search_portfolio",
                    "description": "Searches Harsh's resume, projects, and technical background.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "search_query": {
                                "type": "string",
                                "description": "Specific semantic terms to retrieve context for.",
                            }
                        },
                        "required": ["search_query"],
                    },
                },
            }

            # 3. Route to model for tool evaluation
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=messages,
                tools=[cal_availability_tool, cal_booking_tool, cal_cancel_tool, portfolio_tool],
                tool_choice="auto",
            )

            response_message = response.choices[0].message

            # 4. Handle tool calls if triggered
            if response_message.tool_calls:
                messages.append(response_message)

                for tool_call in response_message.tool_calls:
                    tool_name = tool_call.function.name
                    args = json.loads(tool_call.function.arguments)

                    # Tool A: Check Available Slots
                    if tool_name == "check_cal_availability":
                        api_result = check_cal_availability(
                            start_time=args.get("start_time"),
                            end_time=args.get("end_time"),
                            timezone=args.get("timezone", "Asia/Kolkata"),
                        )

                    # Tool B: Finalize Booking
                    elif tool_name == "execute_cal_booking":
                        api_result = execute_cal_booking(
                            name=args.get("name"),
                            email=args.get("email"),
                            start_time_iso=args.get("start_time_iso"),
                            timezone=args.get("timezone", "Asia/Kolkata"),
                            notes=args.get("notes", ""),
                        )

                    # Tool C: Cancel Booking
                    elif tool_name == "cancel_cal_booking":
                        api_result = cancel_cal_booking(
                            booking_uid=args.get("booking_uid"),
                            reason=args.get("reason", "Cancelled via AI assistant"),
                        )

                    # Tool D: Portfolio RAG Search
                    elif tool_name == "search_portfolio":
                        rag_result = rag.answer(query=args.get("search_query"), k=5)
                        sources = rag_result.get("sources", [])
                        api_result = {"context": rag_result.get("answer")}

                    else:
                        api_result = {"error": f"Unknown tool: {tool_name}"}

                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "name": tool_name,
                        "content": json.dumps(api_result),
                    })

                # Second LLM call with tool results attached
                final_response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=messages,
                )
                answer = final_response.choices[0].message.content

            else:
                # Pure conversational response — no tools needed
                answer = response_message.content

        st.markdown(answer)

        # 5. Render sources expander if RAG was called
        if sources:
            with st.expander("📚 Sources Used"):
                for idx, doc in enumerate(sources, start=1):
                    source_type = doc.metadata.get("source_type", "unknown")
                    source_id = doc.metadata.get("source_id", "unknown")
                    st.markdown(
                        f"""
### Source {idx}
**Type:** {source_type} | **ID:** {source_id}
```text
{doc.page_content[:500]}
```
"""
                    )

    # Save final response to session history
    st.session_state.messages.append({"role": "assistant", "content": answer})