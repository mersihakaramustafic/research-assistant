# AI Market Research Agent

An AI-powered market research assistant that autonomously plans, executes, and synthesizes research reports. It uses OpenAI's GPT-4.1-mini to generate structured research plans and SerpAPI for real-time web search.

Available as both, a **CLI tool** and a **Streamlit web app**.

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
- Use the sidebar to resume an existing plan, or reset to start fresh

## Agent Loop Architecture

The system follows a 3-stage loop:

**1. Planning Stage**

- Input: High-level research goal
- Output: Structured task plan (JSON)
- The plan is persisted to disk immediately

Only the goal is sent to the LLM during planning.

**2. Execution Stage**

- Tasks are executed sequentially
- For each task:
  - Tool selection
  - Tool results are passed to LLM
  - LLM produces structured task summary
- After each task:
  - Status is updated
  - Plan is saved to JSON file

Each task is processed independently to prevent context accumulation.

**3. Synthesis Stage**

- Completed task summaries are aggregated
- Final report is generated
- Only summaries (not raw web content) are included

This prevents prompt bloat and keeps token usage predictable.

## Tools Integrated

**SerpAPI Web Search**

- Used for market research and competitor analysis
- Returns limited structured results

**Persistence Layer (JSON-based)**

- Saves plan state after each task
- Enables resume capability
- Prevents data loss on crash

**Structured Logging**

- JSON logs
- Captures task lifecycle
- Tracks token usage
- Enables traceability

**Streamlit UI**

- Interactive goal input
- Plan visualization
- Task status tracking
- Resume and reset functionality

## Dependencies

| Package | Purpose |
|---|---|
| `openai` | LLM calls via OpenAI Responses API |
| `python-dotenv` | Load environment variables from `.env` |
| `requests` | HTTP requests to SerpAPI |
| `pydantic` | Data validation for plan/task schemas |
| `streamlit` | Web UI |

## Evaluation Scenarios
**1️. Market Overview**

Goal: Analyze the European EV market in 2025

Success Criteria:
- Structured task breakdown
- Competitor analysis included
- Trends and risks identified
- Clear final report

**2. Competitor Benchmarking**

Goal: Compare leading AI legal tech startups

Success Criteria:
- Key players identified
- Differentiation explained
- Pricing insights included

**3. Resume Capability**

Interrupt execution mid-run

Success Criteria:
- Restart resumes correctly
- No completed task is re-executed


## Future Improvements

- RAG over internal document sets
- Deployment as REST API service
- Parallel task execution
- Tool confidence scoring