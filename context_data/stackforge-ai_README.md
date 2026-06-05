# 🤖 StackForge AI

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)
![LangGraph](https://img.shields.io/badge/LangGraph-Latest-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

**An autonomous multi-agent system that intelligently generates complete web projects using AI orchestration**

[Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [Architecture](#-architecture)

</div>

---

## 🌟 Overview

StackForge AI is a sophisticated multi-agent system that automates the entire web development workflow. It leverages Google's Gemini AI and LangGraph to coordinate three specialized agents—**Planner**, **Architect**, and **Coder**—that work together to transform a simple text description into a fully functional website.

### ✨ Key Highlights

- 🧠 **Intelligent Planning**: Research-driven content strategy with web search integration
- 🏗️ **Smart Architecture**: Automated system design and implementation roadmapping
- 💻 **Code Generation**: Real-time file creation with tool-augmented AI
- 🎨 **Beautiful UI**: Glassmorphic interface with live terminal output
- 🔄 **Real-time Updates**: Watch agents work with live status indicators
- 🎯 **Production Ready**: Clean code structure, error handling, and logging

---

## 🎯 Features

### 🤖 Multi-Agent System
- **Planner Agent**: Conducts web research, analyzes trends, and creates content strategy
- **Architect Agent**: Designs system architecture and generates implementation plans
- **Coder Agent**: Implements code with file operations and image retrieval tools

### 🎨 Modern UI/UX
- **Glassmorphism Design**: Clean, professional interface with subtle glass effects
- **Live Terminal Output**: Real-time backend activity mirrored to frontend
- **Agent Status Cards**: Visual indicators showing current agent state (Idle/Working/Complete)
- **Live Indicator**: Pulsing green badge showing active execution
- **Auto-scrolling Terminal**: Smooth terminal experience with color-coded logs

### 🔧 Technical Features
- **LangGraph Orchestration**: State-based workflow management
- **Tool Integration**: Web search (Tavily), file operations, image retrieval
- **Structured Output**: Type-safe data models using Pydantic
- **Error Handling**: Comprehensive error catching and logging
- **Extensible Architecture**: Easy to add new agents or tools

---

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- Google AI API Key (Gemini)
- Tavily API Key (for web search)

### Step 1: Clone the Repository
```bash
git clone https://github.com/Harsh251005/stackforge-ai.git
cd stackforge-ai
```

### Step 2: Install Dependencies
```bash
uv sync
```

### Step 3: Environment Setup
Create a `.env` file in the root directory:
```env
GOOGLE_API_KEY=your_google_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
PEXELS_API_KEY=your_pexels_api_key_here
```

### Step 4: Project Structure
```
StackForge AI/
├── main.py                 # Streamlit UI application
├── orchestrator/
│   ├── agents.py           # Agent implementations
│   ├── graph.py            # LangGraph workflow
│   ├── states.py           # State definitions
│   ├── tools.py            # Tool functions
│   └── prompts.py          # System prompts
├── generated_projects/     # Output directory
├── .python-version         # Python Version being used
├── pyproject.toml          # Details about the dependencies
├── README.md               # Descrption about the project
├── .env
└── uv.lock
```

---

## 🚀 Usage

### Running the Application
```bash
streamlit run main.py
```

The application will open in your browser at `http://localhost:8501`

### Basic Workflow

1. **Enter Project Description**
   ```
   Create a portfolio website for an AI developer named <Your Name> who has skills in ML, DL, GenAI, Agentic AI. Create a dark themed UI with vibrant color combinations.
   ```

2. **Click Execute** 🚀
   - Watch the Planner agent research and strategize
   - See the Architect design the system architecture
   - Observe the Coder implement files in real-time

3. **View Output**
   - Generated files appear in `generated_projects/[project_name]/`
   - Live terminal shows all backend activity
   - Agent cards update in real-time

### Example Projects

**E-commerce Site**
```
Create a modern e-commerce site for selling handmade jewelry 
with product galleries and a shopping cart
```

**Portfolio Website**
```
Build a creative portfolio website for a photographer with 
image galleries and contact form
```

**Landing Page**
```
Design a SaaS landing page with pricing tiers, testimonials, 
and call-to-action sections
```

---

## 🏗️ Architecture

### System Flow
```
User Input → Planner Agent → Architect Agent → Coder Agent → Generated Project
               ↓                ↓                  ↓
           Web Search       Design Spec      File Operations
           Research         Tech Stack       Image Retrieval
```

### Agent Details

#### 🧠 Planner Agent
- **Purpose**: Strategic planning and content research
- **Tools**: Tavily Web Search
- **Output**: Structured plan with sections and content strategy
- **Prompt**: Research-focused with market analysis

#### 📐 Architect Agent
- **Purpose**: Technical architecture and implementation planning
- **Tools**: None (pure reasoning)
- **Output**: Step-by-step implementation plan with file specifications
- **Prompt**: Design-focused with component breakdown

#### 👨‍💻 Coder Agent
- **Purpose**: Code generation and file management
- **Tools**: 
  - `create_project_folder`: Initialize project structure
  - `create_file`: Create new files
  - `write_file`: Write content to files
  - `update_file`: Modify existing files
  - `read_file`: Read file contents
  - `list_project_files`: List all project files
  - `get_relevant_image`: Fetch images from Pexels
- **Output**: Complete web project with HTML/CSS/JS
- **Prompt**: Implementation-focused with coding best practices

---

## 🛠️ Technologies Used

| Technology | Purpose |
|------------|---------|
| **Streamlit** | Web interface and real-time updates |
| **LangGraph** | Agent orchestration and workflow |
| **Google Gemini** | Large language model (gemini-2.5-flash) |
| **LangChain** | LLM framework and tool integration |
| **Tavily** | Web search API |
| **Pexels** | Stock image retrieval |
| **Pydantic** | Data validation and structured output |

---

## 📝 Configuration

### Customizing Agents

Edit `orchestrator/prompts.py` to modify agent behavior:

### Adding New Tools

1. Define tool in `orchestrator/tools.py`:

2. Add to Coder agent in `orchestrator/agents.py`:
```python
coder_tools = [create_file, write_file, my_custom_tool]
```

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Google** for Gemini API
- **Tavily** for web search capabilities
- **Pexels** for stock images
- **LangChain** team for the excellent framework
- **Streamlit** for the amazing UI framework

---

## 👩‍💻 Author
**Harsh Dharnidharka**  
[GitHub](https://github.com/Harsh251005) | [LinkedIn](https://www.linkedin.com/in/harsh-dharnidharka/)
---

<div align="center">

**⭐ Star this repo if you find it helpful!**

</div>