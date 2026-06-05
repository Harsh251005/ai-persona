# InsightForge

**InsightForge** is an AI-powered research agent that autonomously gathers, evaluates, and synthesizes information from the web into structured, citation-backed reports.

---

## 🚀 Overview

InsightForge transforms a single query into a multi-step research workflow:

* Breaks the query into focused sub-questions
* Performs parallel web searches
* Filters and ranks results for relevance
* Iteratively refines research when needed
* Generates a structured report with inline citations

Designed with **LangGraph**, it demonstrates real-world agent architecture with transparency, control, and performance optimizations.

---

## ✨ Features

* **Query Decomposition** — multi-step research planning
* **Parallel Web Search** — fast retrieval using concurrent execution
* **Relevance Ranking** — LLM-based scoring of results
* **Reflection Loop** — iterative research for deeper insights
* **Depth Control** — basic vs deep research modes
* **Inline Citations** — traceable sources in report
* **Caching** — avoids redundant API calls
* **Streaming UI** — real-time agent activity visualization
* **Export Options** — Markdown, TXT, and PDF reports
* **Custom UI** — clean, minimal, and professional Streamlit interface

---

## 🧠 Architecture

```
User Query
    ↓
Decomposition
    ↓
Parallel Web Search
    ↓
Cleaning + Ranking
    ↓
Reflection Loop (optional)
    ↓
Report Generation (with citations)
```

---

## 🛠️ Tech Stack

* **LangGraph** — agent workflow orchestration
* **OpenAI API** — reasoning & generation
* **Tavily API** — web search
* **Streamlit** — UI
* **Python** — core implementation

---

## ⚡ How It Works

1. User inputs a research query
2. System decomposes it into sub-queries
3. Executes parallel web searches
4. Cleans and ranks retrieved content
5. Evaluates if more research is needed
6. Generates a structured report with citations
7. Displays live agent activity in UI

---

## 🖥️ Run Locally

```bash
# Install dependencies
uv init
uv add langgraph openai tavily-python streamlit python-dotenv pyyaml reportlab

# Run the app
uv run streamlit run app.py
```

---

## 📄 Example Output

* Structured report with sections (Overview, Insights, etc.)
* Inline citations like [1], [2]
* Clickable source links
* Live activity trace of the agent

---

## ⚙️ Configuration

Set environment variables:

```bash
OPENAI_API_KEY=your_key
TAVILY_API_KEY=your_key
```

---

## 💡 Design Decisions

* Used **LangGraph** for explicit and controllable workflows
* Implemented **parallel search** to reduce latency
* Added **LLM-based ranking** for improved relevance
* Included **caching** to optimize cost and performance
* Designed UI for **transparency and usability**

---

## 🔮 Future Improvements

* Embedding-based ranking (faster than LLM scoring)
* Advanced caching (Redis / persistent store)
* FastAPI backend for API access
* Multi-modal research (PDFs, images, etc.)

---

## 👨‍💻 Author

**Harsh**  
*Aspiring AI Engineer*

---

