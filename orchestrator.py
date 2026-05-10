from typing import TypedDict, Optional, List, Dict, Any
from langgraph.graph import StateGraph, START, END

# Import your existing agents
from agents.idea_agent import generate_ideas
from agents.age_adapter_agent import adapt_idea
from agents.safety_agent import check_safety

MAX_RETRIES = 3

def run_generate(topic: str, age: str, goal: str):
    """Generate ideas and return the list for user selection."""
    return generate_ideas(topic, age, goal)

class RefinementState(TypedDict):
    selected_idea: Dict[str, Any]
    target_age: str
    attempt: int
    revision_notes: Optional[List[str]]
    adapted_plan: Optional[Dict[str, Any]]
    safety_assessment: Optional[Dict[str, Any]]
    status: str
    error_detail: Optional[Any]

# Nodes ( Agents)
def adapt_node(state: RefinementState):
    attempt = state.get("attempt", 0) + 1
    print(f"\n--- Graph Attempt {attempt}/{MAX_RETRIES} ---")

    adapt_result = adapt_idea(
        selected_idea=state["selected_idea"].get("title", str(state["selected_idea"])),
        target_age=state["target_age"],
        revision_notes=state.get("revision_notes")
    )

    if adapt_result.get("status") != "ok":
        return {"status": "error", "error_detail": adapt_result}

    return {
        "attempt": attempt,
        "adapted_plan": adapt_result.get("result", {}) 
    }

def safety_node(state: RefinementState):
    description_to_check = state["adapted_plan"].get("adapted_description", "")
    safety_result = check_safety(description_to_check, state["target_age"])

    if safety_result.get("status") != "ok":
        return {"status": "error", "error_detail": safety_result}

    return {"safety_assessment": safety_result["assessment"]}

def prepare_retry_node(state: RefinementState):
    assessment = state.get("safety_assessment", {})
    suggestions = [s.get("change", "") for s in assessment.get("suggestions", [])]
    print(f"Routing back to Adapter with {len(suggestions)} suggestion(s)...")
    return {"revision_notes": suggestions}



def route_after_safety(state: RefinementState) -> str:
    if state.get("status") == "error":
        return END

    assessment = state.get("safety_assessment", {})

    if assessment.get("severity") == "high":
        return "reject"

    if assessment.get("safe_to_use"):
        return "approve"

    if state["attempt"] >= MAX_RETRIES:
        return "unresolved"

    return "retry"




builder = StateGraph(RefinementState)

builder.add_node("adapt", adapt_node)
builder.add_node("check_safety", safety_node)
builder.add_node("prepare_retry", prepare_retry_node)

builder.add_edge(START, "adapt")
builder.add_edge("adapt", "check_safety")

builder.add_conditional_edges(
    "check_safety",
    route_after_safety,
    {
        "approve": END,
        "reject": END,
        "unresolved": END,
        "retry": "prepare_retry"
    }
)

builder.add_edge("prepare_retry", "adapt")

refinement_graph = builder.compile()




def run_refine(selected_idea: dict, age: str) -> dict:
    
    initial_state = {
        "selected_idea": selected_idea,
        "target_age": age,
        "attempt": 0,
        "revision_notes": None,
        "adapted_plan": None,
        "safety_assessment": None,
        "status": "processing",
        "error_detail": None
    }

    final_state = refinement_graph.invoke(initial_state)

    if final_state.get("status") == "error":
        return {
            "status": "error", 
            "stage": "graph_execution", 
            "detail": final_state.get("error_detail")
        }

    assessment = final_state.get("safety_assessment", {})

    if assessment.get("severity") == "high":
        return {
            "status": "rejected", 
            "reason": "High severity safety issue", 
            "assessment": assessment
        }

    if assessment.get("safe_to_use"):
        return {
            "status": "ok", 
            "final_plan": final_state.get("adapted_plan"), 
            "safety": assessment, 
            "attempts": final_state.get("attempt")
        }

    return {
        "status": "unresolved",
        "reason": f"Could not resolve after {MAX_RETRIES} attempts",
        "last_adapted": final_state.get("adapted_plan"),
        "last_safety": assessment
    }