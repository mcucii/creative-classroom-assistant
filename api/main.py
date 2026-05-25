"""
FastAPI API Service for AgentCore
Exposes /invoke endpoint and activity-specific endpoints
"""
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, Literal, Dict, Any, List
import uvicorn
import logging

from agentcore.llm_providers import LLMCore, LLMProvider
from agentcore.orchestrator import ActivityOrchestrator

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI
app = FastAPI(
    title="AgentCore API",
    description="API service for classroom activity generation and refinement",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
llm_core = LLMCore()
orchestrator = ActivityOrchestrator(llm_core, provider=LLMProvider.CLAUDE)


# ═══════════════════════════════════════════════════════════════════════════
# Request/Response Models
# ═══════════════════════════════════════════════════════════════════════════

class InvokeRequest(BaseModel):
    """Generic LLM invocation request"""
    prompt: str = Field(..., description="The prompt to send to the LLM")
    provider: Literal["claude", "gemini"] = Field(
        default="claude",
        description="LLM provider to use"
    )
    system_prompt: Optional[str] = Field(
        default=None,
        description="Custom system prompt (optional)"
    )
    max_tokens: Optional[int] = Field(
        default=1000,
        description="Maximum tokens for response",
        ge=1,
        le=4096
    )


class InvokeResponse(BaseModel):
    """Generic LLM invocation response"""
    response: str
    provider: str
    prompt_length: int


class GenerateIdeasRequest(BaseModel):
    """Request for generating classroom activity ideas"""
    topic: str = Field(..., description="Subject matter (e.g., 'Water Cycle')")
    age_group: str = Field(..., description="Age range (e.g., '8-10')")
    goal: str = Field(..., description="What students should do (e.g., 'experiment')")
    provider: Literal["claude", "gemini"] = Field(default="claude")
    num_ideas: int = Field(default=3, ge=1, le=5)


class GenerateIdeasResponse(BaseModel):
    """Response containing generated activity ideas"""
    ideas: List[Dict[str, Any]]
    topic: str
    age_group: str


class RefineActivityRequest(BaseModel):
    """Request for refining a classroom activity"""
    activity: Dict[str, Any] = Field(..., description="The activity to refine")
    age_group: str = Field(..., description="Target age group")
    provider: Literal["claude", "gemini"] = Field(default="claude")


class RefineActivityResponse(BaseModel):
    """Response containing refined activity and safety assessment"""
    status: str
    final_plan: Optional[Dict[str, Any]] = None
    safety: Optional[Dict[str, Any]] = None
    assessment: Optional[str] = None
    stage: Optional[str] = None


# ═══════════════════════════════════════════════════════════════════════════
# Endpoints
# ═══════════════════════════════════════════════════════════════════════════

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "AgentCore API",
        "version": "1.0.0"
    }


@app.post("/invoke", response_model=InvokeResponse)
async def invoke(request: InvokeRequest):
    """
    Generic LLM invocation endpoint
    
    Use this for raw LLM calls when you need direct access to Claude/Gemini
    """
    try:
        logger.info(f"Invoking {request.provider} with prompt length: {len(request.prompt)}")
        
        kwargs = {}
        if request.provider == "claude" and request.max_tokens:
            kwargs['max_tokens'] = request.max_tokens
        
        result = llm_core.invoke(
            prompt=request.prompt,
            provider=LLMProvider(request.provider),
            system_prompt=request.system_prompt,
            **kwargs
        )
        
        logger.info(f"Successfully invoked {request.provider}")
        
        return InvokeResponse(
            response=result,
            provider=request.provider,
            prompt_length=len(request.prompt)
        )
        
    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Internal error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to invoke LLM: {str(e)}"
        )


@app.post("/activities/generate", response_model=GenerateIdeasResponse)
async def generate_activities(request: GenerateIdeasRequest):
    """
    Generate classroom activity ideas
    
    This is the main endpoint for the "Generate Ideas" functionality
    """
    try:
        logger.info(
            f"Generating {request.num_ideas} ideas for topic='{request.topic}', "
            f"age={request.age_group}, goal='{request.goal}'"
        )
        
        ideas = orchestrator.generate_ideas(
            topic=request.topic,
            age_group=request.age_group,
            goal=request.goal,
            provider=LLMProvider(request.provider),
            num_ideas=request.num_ideas
        )
        
        logger.info(f"Successfully generated {len(ideas)} ideas")
        
        return GenerateIdeasResponse(
            ideas=ideas,
            topic=request.topic,
            age_group=request.age_group
        )
        
    except Exception as e:
        logger.error(f"Error generating activities: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate activities: {str(e)}"
        )


@app.post("/activities/refine", response_model=RefineActivityResponse)
async def refine_activity(request: RefineActivityRequest):
    """
    Refine and safety-check a classroom activity
    
    This is the main endpoint for the "Select & Refine" functionality
    """
    try:
        logger.info(
            f"Refining activity: {request.activity.get('title', 'Untitled')} "
            f"for age group {request.age_group}"
        )
        
        result = orchestrator.refine_activity(
            activity=request.activity,
            age_group=request.age_group,
            provider=LLMProvider(request.provider)
        )
        
        logger.info(f"Refinement complete with status: {result.get('status')}")
        
        return RefineActivityResponse(**result)
        
    except Exception as e:
        logger.error(f"Error refining activity: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to refine activity: {str(e)}"
        )


@app.get("/providers")
async def get_providers():
    """List available LLM providers"""
    return {
        "providers": ["claude", "gemini"],
        "default": "claude"
    }


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8080,
        reload=True
    )