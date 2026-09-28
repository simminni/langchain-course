# LangChain Course

A hands-on repository for LangChain course exercises, experiments, and projects. This repository uses [`uv`](https://docs.astral.sh/uv/) for fast, deterministic Python dependency management and supports both local LLMs (via Ollama) and cloud-hosted LLMs (Google Gemini, OpenAI, etc.).

---

## 📋 Table of Contents

- [Project Structure](#-project-structure)
- [Prerequisites](#-prerequisites)
- [Getting Started](#-getting-started)
- [Environment Configuration](#-environment-configuration)
- [Running Course Scripts](#-running-course-scripts)
- [Code Quality & Formatting](#-code-quality--formatting)
- [Module Deep Dives](#-module-deep-dives)
  - [1. `hello_world.py` — Prompt Templates & LCEL](#1-hello_worldpy--prompt-templates--lcel)
  - [2. `search_agent.py` — ReAct Agents & Tool Calling](#2-search_agentpy--react-agents--tool-calling)
- [Adding New Course Modules](#-adding-new-course-modules)
- [Acknowledgements & Credits](#-acknowledgements--credits)

---

## 📂 Project Structure

```text
langchain-course/
├── .env                       # Environment variables (API keys, etc.)
├── .python-version            # Python version pin (3.14)
├── pyproject.toml             # Project dependencies and tool configurations
├── uv.lock                    # Locked dependency versions
├── README.md                  # Project documentation
├── .vscode/
│   └── settings.json          # VS Code interpreter and search paths
└── src/
    └── langchain_course/
        ├── __init__.py        # Package entrypoint
        └── hello_world.py     # Introduction to Prompts, Models, and LCEL chains
```

---

## 🛠 Prerequisites

1. **Python 3.14+** (or handled automatically via `uv`).
2. **[`uv`](https://docs.astral.sh/uv/)**: Fast Python package installer and resolver.
   ```bash
   # Install uv on macOS / Linux
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```
3. **[Ollama](https://ollama.com/)** (Optional, for local LLMs):
   - Install Ollama to run local models without external API charges.

---

## 🚀 Getting Started

### 1. Clone and Navigate

```bash
git clone https://github.com/simminni/langchain-course.git
cd langchain-course
```

### 2. Sync Dependencies

Create the virtual environment and install all dependencies in one command:

```bash
uv sync
```

### 3. Activate the Virtual Environment (Optional)

You can activate the virtual environment or run commands directly through `uv run`:

```bash
source .venv/bin/activate
```

---

## 🔐 Environment Configuration

Create a `.env` file in the project root to configure your API keys and services:

```env
# --- LLM Providers ---
# Google Gemini (Google AI Studio)
GOOGLE_API_KEY=your_google_api_key_here

# OpenAI
OPENAI_API_KEY=your_openai_api_key_here

# --- Search & Tools ---
# Tavily Search API (for agent search tools)
TAVILY_API_KEY=your_tavily_api_key_here

# --- Observability & Tracing (Optional) ---
# LangSmith (Visual monitoring & debugging LangChain runs)
LANGSMITH_TRACING=true
LANGSMITH_ENDPOINT=https://api.smith.langchain.com
LANGSMITH_API_KEY=your_langsmith_api_key_here
LANGSMITH_PROJECT=langchain-course
```

### 🔑 How to Obtain API Keys

| Service | Purpose | How to Get |
| :--- | :--- | :--- |
| **Google Gemini** | Cloud LLM inference (`ChatGoogleGenerativeAI`) | Sign in to [Google AI Studio](https://aistudio.google.com/app/apikey) and click **"Create API key"**. |
| **OpenAI** | Cloud LLM inference (`ChatOpenAI`) & embeddings | Go to [OpenAI Platform API Keys](https://platform.openai.com/api-keys) and generate a secret key. |
| **Tavily AI** | AI-optimized search engine for LangChain agents | Create a free account at [Tavily](https://app.tavily.com/) and copy your API key from the dashboard. |
| **LangSmith** *(Optional)* | Visual tracing, debugging, and prompt monitoring | Sign up at [LangSmith](https://smith.langchain.com/), navigate to **Settings > API Keys**, and create a personal API key. |

> **Note**: LangSmith observability and tracing is completely optional. If you do not configure LangSmith keys, your LangChain code will still run normally without remote trace logging.



---

## ▶️ Running Course Scripts

Execute any course script directly using `uv run`:

```bash
uv run python src/langchain_course/hello_world.py
```

---

## 🧹 Code Quality & Formatting

This project uses **Black** for code formatting and **isort** for import sorting.

```bash
# Format code with black
black .

# Sort imports with isort
isort .
```

> **Note**: Black is configured in `pyproject.toml` with `target-version = ["py314"]` to match the Python 3.14 runtime.

---

## 📖 Module Deep Dives

### 1. `hello_world.py` — Prompt Templates & LCEL

**Path**: `src/langchain_course/hello_world.py`

This module serves as the foundational introduction to core LangChain concepts:

#### Key Concepts Demonstrated

1. **Prompt Templates (`PromptTemplate`)**:
   - Decouples static prompt instructions from dynamic inputs using `{variable}` placeholders.
   - Example template takes `{information}` about a person and requests a summary + two interesting facts.

2. **LangChain Expression Language (LCEL)**:
   - Uses the pipe operator `|` to chain components together:
     ```python
     chain = summary_prompt_template | llm
     ```
   - Automatically handles input/output data flow between the prompt and the model.

3. **Interchangeable Model Backends**:
   - **Local Inference with Ollama (`ChatOllama`)**:
     - Uses local models such as `gemma3:270m` for fast, offline, and zero-cost local execution.
     - Setup required for Ollama:
       ```bash
       # Pull the local model
       ollama pull gemma3:270m

       # Verify model availability
       ollama list
       ```
   - **Cloud Inference with Google Generative AI (`ChatGoogleGenerativeAI`)**:
     - Alternative commented configuration using Google's Gemini models (`gemini-3.5-flash-lite`) via `GOOGLE_API_KEY`.

4. **Output Parsing (`StrOutputParser`)**:
   - Prepared to convert `AIMessage` objects directly into plain strings when appended to the chain:
     ```python
     chain = summary_prompt_template | llm | StrOutputParser()
     ```

#### How to Run `hello_world.py`

1. Ensure Ollama is running and the model is pulled:
   ```bash
   ollama pull gemma3:270m
   ```
2. Run the script:
   ```bash
   uv run python src/langchain_course/hello_world.py
   ```

### 2. `search_agent.py` — ReAct Agents & Tool Calling

**Path**: `src/langchain_course/search_agent.py`

Demonstrates building tool-using AI agents with LangChain and Tavily Search:

#### Key Concepts Demonstrated

1. **Agent Creation (`create_agent`)**:
   - Configures a reasoning agent with structured tools, system instructions, and LLM backends.

2. **Custom & Prebuilt Tools (`@tool`, `TavilySearch`)**:
   - Uses `TavilySearch` for live web querying.
   - Defines custom python tools like `verify_job_url` with the `@tool` decorator.

3. **Structured Response Formatting (`response_format`)**:
   - Rather than returning raw, unstructured strings, the agent uses **Pydantic** models to return predictable, strongly-typed JSON objects.
   - **Why each class and component is needed**:
     - **`Source(BaseModel)`**: Defines a clean, dedicated sub-schema for web citations (e.g. `url: str`), enabling structured attribution for every source used.
     - **`AgentResponse(BaseModel)`**: The top-level schema representing the final output payload. It bundles the synthesized narrative (`answer: str`) with the list of references (`sources: List[Source]`).
     - **`Field(description="...")`**: Injects semantic instructions into the JSON schema sent to the LLM, guiding the model on what specific data to populate in each field.
     - **`default_factory=list`**: Serves two purposes:
       1. **Mutable Safety**: Calls `list()` to dynamically create a fresh, separate empty list for every new instance, avoiding Python's shared mutable default traps.
       2. **Validation Resilience**: Makes the `sources` field optional during parsing, so if the LLM omits the `"sources"` key in its JSON payload, Pydantic initializes it cleanly to `[]` instead of raising a `ValidationError`.

#### How to Run `search_agent.py`

Ensure `TAVILY_API_KEY` and `GOOGLE_API_KEY` are set in `.env`, then run:

```bash
uv run python src/langchain_course/search_agent.py
```


---

## ➕ Adding New Course Modules

As new topics and exercises are added throughout the course, follow this structured pattern:

1. **Create the Script**:
   Add new modules under `src/langchain_course/` (e.g., `output_parsers.py`, `rag_basics.py`, `agents_and_tools.py`, `search_tavily.py`).
2. **Follow Consistent Patterns**:
   - Load environment variables with `load_dotenv()` at the top.
   - Encapsulate execution inside a `main()` function with an `if __name__ == "__main__":` guard.
   - Use LCEL chains (`prompt | model | parser`) for composability.
3. **Format**:
   Run `black .` and `isort .` before committing changes.
4. **Document**:
   Add a new section under [Module Deep Dives](#-module-deep-dives) in this `README.md` describing the module's purpose, key concepts, and run instructions.

---

## 🙏 Acknowledgements & Credits

This repository contains coursework, notes, and exercises based on the Udemy course:

- **Course**: [LangChain - Develop LLM Powered Applications with LangChain](https://www.udemy.com/course/langchain/) by [Eden Marco](https://github.com/emarco177)
- **Original Repository**: [`emarco177/langchain-course`](https://github.com/emarco177/langchain-course)

