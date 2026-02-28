# AI Market Research Agent

An AI-powered market research assistant that autonomously plans, executes, and synthesizes research reports. It uses OpenAI's GPT-4.1-mini to generate structured research plans and SerpAPI for real-time web search.

Available as both a **CLI tool** and a **Streamlit web app**.

## Features

- Generates a structured multi-step research plan from a natural language goal
- Executes tasks sequentially, using web search for research-oriented tasks
- Synthesizes a final report from all completed task results
- Persists plan state to disk - resume interrupted sessions without re-running completed tasks
- Structured logging with trace context per task

## Project Structure

```
research-assistant/
├── agent/
│   ├── llm_client.py      # OpenAI client setup
│   ├── planner.py         # Generates ResearchPlan from a goal
│   ├── executor.py        # Executes tasks and synthesizes report
│   └── prompts.py         # Prompt templates
├── models/
│   └── schemas.py         # Pydantic models (Task, ResearchPlan)
├── storage/
│   └── persistence.py     # Save/load plan to data/plan.json
├── tools/
│   └── web_search.py      # SerpAPI web search tool
├── infrastructure/
│   └── logging_config.py  # Structured logging setup
├── data/
│   └── plan.json          # Persisted plan state (auto-generated)
├── main.py                # CLI entry point
├── app.py                 # Streamlit web app
└── requirements.txt
```

## Setup

**1. Clone the repository**

```bash
git clone <repo-url>
cd research-assistant
```

**2. Create and activate a virtual environment**

```bash
python -m venv venv
source venv/bin/activate        # macOS/Linux
venv\Scripts\activate           # Windows
```

**3. Install dependencies**

```bash
pip install -r requirements.txt
```

**4. Configure environment variables**

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_openai_api_key
SERPAPI_API_KEY=your_serpapi_api_key
```

- Get an OpenAI API key at [platform.openai.com](https://platform.openai.com)
- Get a SerpAPI key at [serpapi.com](https://serpapi.com)

## Usage

### CLI

```bash
python main.py
```

- Enter a research goal when prompted
- The agent generates a plan and displays it
- Press Enter to execute all tasks
- A final report is printed on completion
- If `data/plan.json` already exists, the session is resumed from where it left off

### Streamlit Web App

```bash
streamlit run app.py
```

- Enter your research goal and click **Generate Plan**
- Review the task list, then click **Execute Remaining Tasks**
- Once all tasks are complete, click **Generate Final Report**
- Use the sidebar to resume an existing plan or reset to start fresh

## How It Works

1. **Planning** - The planner sends your goal to GPT-4.1-mini and receives a structured JSON plan of research tasks.
2. **Execution** - Each task is executed in order. Tasks containing research keywords (e.g., "analyze", "market", "trend") trigger a SerpAPI web search. Results are summarized by the LLM.
3. **Persistence** - The plan is saved to `data/plan.json` after each completed task, enabling session resumption.
4. **Report synthesis** - After all tasks are complete, the agent compiles all results into a final structured report.

## Dependencies

| Package | Purpose |
|---|---|
| `openai` | LLM calls via OpenAI Responses API |
| `python-dotenv` | Load environment variables from `.env` |
| `requests` | HTTP requests to SerpAPI |
| `pydantic` | Data validation for plan/task schemas |
| `streamlit` | Web UI |