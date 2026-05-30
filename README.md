# Creative Classroom Assistant

A classroom activity generation toolkit that combines a FastAPI backend, Streamlit frontend, and LLM-powered orchestration to create, adapt, and safety-check lesson ideas.

## 🚀 Overview

This project helps teachers and curriculum designers generate creative classroom activities for different age groups using large language models. It includes:

- A FastAPI service for activity generation and refinement
- A Streamlit interface for brainstorming and reviewing lesson ideas
- An orchestrator that adapts ideas by age and performs safety checks
- AWS Bedrock Claude integration for LLM calls

## ✨ Features

- Generate three classroom activity ideas from a topic, age group, and goal
- Refine a selected idea for a specific age range
- Perform a safety assessment and return concrete revision suggestions


## 📁 Project Structure

- `api/main.py` - FastAPI application exposing `/invoke`, `/activities/generate`, and `/activities/refine`
- `clients/streamlit_app.py` - Streamlit UI for generating ideas and refining selected activities
- `agentcore/llm_providers.py` - LLM abstraction layer for Claude via AWS Bedrock
- `agentcore/orchestrator.py` - Activity orchestration and refinement workflow
- `agents/idea_agent.py` - Prompt logic for generating activity ideas
- `agents/age_adapter_agent.py` - Logic for adapting ideas to a target age group
- `agents/safety_agent.py` - Safety assessment and risk detection
- `Dockerfile` - Container image definition
- `requirements.in` / `requirements.txt` - Python dependency lists
- `terraform/` - Infrastructure definitions for deployment

## 🧩 Requirements

- Python 3.11
- AWS credentials configured for Bedrock access
- `pip` installed
- Optional: Docker for containerized deployment

## �️ Tools Used

This project is built with and uses the following tools:

- Python 3.11
- `pip` for dependency installation
- FastAPI for the backend API service
- Streamlit for the interactive web UI
- Uvicorn as the ASGI server
- Docker for containerized deployment
- AWS Bedrock / Claude via `boto3` for LLM execution
- Terraform for optional infrastructure provisioning
- Git for version control

## �🔧 Setup

1. Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/Scripts/activate   # Windows PowerShell: .venv\Scripts\Activate.ps1
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Configure environment variables in a `.env` file or your shell:

```env
AWS_REGION=eu-central-1
AWS_ACCESS_KEY_ID=YOUR_AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY=YOUR_AWS_SECRET_ACCESS_KEY
```

4. Start the app:

```bash
bash start.sh
```

This launches:

- FastAPI backend on `http://0.0.0.0:8080`
- Streamlit UI on `http://0.0.0.0:8501`

## ⚙️ Running Without `start.sh`

To run services separately:

```bash
uvicorn api.main:app --host 0.0.0.0 --port 8080
python -m streamlit run clients/streamlit_app.py --server.port 8501 --server.address 0.0.0.0
```

## 📡 API Endpoints

- `GET /health` — health check
- `POST /invoke` — generic LLM invocation
- `POST /activities/generate` — generate classroom activity ideas
- `POST /activities/refine` — refine a selected idea and run a safety assessment

### Example: Generate Activities

```json
POST /activities/generate
{
  "topic": "Water Cycle",
  "age_group": "8-10",
  "goal": "experiment",
  "provider": "claude",
  "num_ideas": 3
}
```

## 🧠 How It Works

1. The Streamlit app collects a topic, age group, and goal.
2. The orchestrator calls `idea_agent.generate_ideas()` to create activity options.
3. When an idea is selected, the orchestrator adapts it for the target age using `age_adapter_agent.py`.
4. The adapted plan is safety-checked using `safety_agent.py`.

## 🛠 Notes

- The current implementation uses AWS Bedrock Claude via `agentcore/llm_providers.py`.
- The system expects structured JSON output from the LLM prompts and includes parsing fallback logic.

## 📦 Docker

Build and run with Docker:

```bash
docker build -t creative-classroom-assistant .
docker run -p 8501:8501 -p 8080:8080 creative-classroom-assistant
```
