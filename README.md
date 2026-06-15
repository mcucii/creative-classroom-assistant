# Creative Classroom Assistant

A classroom activity generation toolkit that combines a FastAPI backend, Streamlit frontend, AWS-deployed AgentCore orchestration, and LLM-powered workflows to create, adapt, and safety-check lesson ideas.

Check it out: http://18.185.220.177:8501/

## Overview

This project helps teachers and curriculum designers generate creative classroom activities for different age groups using large language models. It includes:

- A Streamlit interface for brainstorming and reviewing lesson ideas
- A FastAPI service for activity generation and refinement
- An AWS-deployed AgentCore orchestration layer for runtime agent execution
- An orchestrator that adapts ideas by age and performs safety checks
- AWS Bedrock Claude integration for LLM calls

## Features

- Generate classroom activity ideas from a topic, age group, and goal
- Refine a selected idea for a specific age range
- Perform a safety assessment and return structured guidance
- Track recent activity history in the Streamlit UI

## Project Structure

- `api/main.py` - FastAPI application exposing `/invoke`, `/activities/generate`, and `/activities/refine`
- `clients/streamlit_app.py` - Streamlit UI for generating and refining classroom activities
- `agentcore/llm_providers.py` - LLM abstraction layer for Claude via AWS Bedrock
- `agentcore/orchestrator.py` - Activity orchestration and refinement workflow
- `agents/idea_agent.py` - Prompt logic for generating activity ideas
- `agents/age_adapter_agent.py` - Logic for adapting ideas to a target age group
- `agents/safety_agent.py` - Safety assessment and risk detection
- `bedrock_client.py` - helper functions for Bedrock interaction
- `Dockerfile.ui` - Streamlit UI container definition
- `Dockerfile.agents` - agent runtime container definition
- `requirements.in` / `requirements.txt` - Python dependency lists
- `start.sh` / `deploy.ps1` - local start and deployment helper scripts
- `terraform-agents/` / `terraform-ui/` - optional Terraform infrastructure definitions

## Requirements

- Python 3.11
- AWS credentials configured for Bedrock access
- `pip` installed
- Optional: Docker for containerized deployment

## Tools Used

- Python 3.11
- Streamlit for the interactive web UI
- FastAPI for the backend API service
- Uvicorn 
- AWS Bedrock / AgentCore via `boto3` for LLM execution
- Docker for containerized deployment
- Terraform for optional infrastructure provisioning
- Git for version control

## Notes

- The current implementation targets AWS Bedrock Claude.
- `clients/streamlit_app.py` is the current UI entry point for teachers.

