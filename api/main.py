from fastapi import FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, Literal, Dict, Any, List
import uvicorn
import logging

from core.llm_providers import LLMCore, LLMProvider, DEFAULT_PROVIDER
from core.orchestrator import ActivityOrchestrator

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Classroom Assistant API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

llm_core = LLMCore()
orchestrator = ActivityOrchestrator(llm_core)


# ── Health check ──────────────────────────────────────────────────────────────

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "AgentCore API", "version": "1.0.0"}


# ── Other endpoints ───────────────────────────────────────────────────────────

class InvokeRequest(BaseModel):
    prompt: str = Field(..., description="The prompt to send to the LLM")
    provider: LLMProvider = DEFAULT_PROVIDER
    system_prompt: Optional[str] = Field(default=None)
    max_tokens: Optional[int] = Field(default=1000, ge=1, le=4096)

class InvokeResponse(BaseModel):
    response: str
    provider: str
    prompt_length: int

class GenerateIdeasRequest(BaseModel):
    topic: str
    age_group: str
    goal: str
    num_ideas: int = Field(default=3, ge=1, le=5)

class GenerateIdeasResponse(BaseModel):
    ideas: List[Dict[str, Any]]
    topic: str
    age_group: str

class RefineActivityRequest(BaseModel):
    activity: Dict[str, Any]
    age_group: str

class RefineActivityResponse(BaseModel):
    status: str
    final_plan: Optional[Dict[str, Any]] = None
    safety: Optional[Dict[str, Any]] = None
    assessment: Optional[str] = None
    stage: Optional[str] = None


@app.post("/invoke", response_model=InvokeResponse)
async def invoke(request: InvokeRequest):
    try:
        kwargs = {}
        if request.max_tokens:
            kwargs['max_tokens'] = request.max_tokens
        result = llm_core.invoke(
            prompt=request.prompt,
            provider=LLMProvider(request.provider),
            system_prompt=request.system_prompt,
            **kwargs
        )
        return InvokeResponse(
            response=result,
            provider=request.provider,
            prompt_length=len(request.prompt)
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@app.post("/activities/generate", response_model=GenerateIdeasResponse)
async def generate_activities(request: GenerateIdeasRequest):
    try:
        ideas = orchestrator.run_generate(
            topic=request.topic,
            age=request.age_group,
            goal=request.goal
        )
        return GenerateIdeasResponse(
            ideas=ideas,
            topic=request.topic,
            age_group=request.age_group
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@app.post("/activities/refine", response_model=RefineActivityResponse)
async def refine_activity(request: RefineActivityRequest):
    try:
        result = orchestrator.run_refine(
            selected_idea=request.activity,
            age=request.age_group
        )
        return RefineActivityResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@app.get("/providers")
async def get_providers():
    return {"providers": ["claude"], "default": "claude"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)