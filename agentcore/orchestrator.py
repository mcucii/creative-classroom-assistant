from typing import TypedDict, Optional, List, Dict, Any
from langgraph.graph import StateGraph, START, END

from agents.idea_agent import generate_ideas
from agents.age_adapter_agent import adapt_idea
from agents.safety_agent import check_safety

from agentcore.llm_providers import LLMCore, LLMProvider


class RefinementState(TypedDict):
    selected_idea: Dict[str, Any]
    target_age: str
    attempt: int
    revision_notes: Optional[List[str]]
    adapted_plan: Optional[Dict[str, Any]]
    safety_assessment: Optional[Dict[str, Any]]
    status: str
    error_detail: Optional[Any]


 
class ActivityOrchestrator:
    def __init__(
        self,
        llm_core: LLMCore,
        provider: LLMProvider
    ):
        self.llm_core = llm_core
        self.provider = provider
        self.refinement_graph = self._build_graph()
        self.MAX_RETRIES = 3


    def _build_graph(self):
        builder = StateGraph(RefinementState)
        builder.add_node("adapt", self.adapt_node)
        builder.add_node("check_safety", self.safety_node)
        builder.add_node("prepare_retry", self.prepare_retry_node)

        builder.add_edge(START, "adapt")
        builder.add_edge("adapt", "check_safety")

        builder.add_conditional_edges(
            "check_safety",
            self.route_after_safety,
            {
                "approve": END,
                "reject": END,
                "unresolved": END,
                "retry": "prepare_retry"
            }
        )

        builder.add_edge("prepare_retry", "adapt")
        return builder.compile()
    

    def adapt_node(self, state: RefinementState):
        attempt = state.get("attempt", 0) + 1
        selected_idea = state.get("selected_idea", {})
        idea_title = (
            selected_idea.get("title")
            if isinstance(selected_idea, dict)
            else str(selected_idea)
        )

        adapt_result = adapt_idea(
            llm_core=self.llm_core,
            provider=self.provider,
            selected_idea=idea_title,
            target_age=state["target_age"],
            revision_notes=state.get("revision_notes")
        )

        if adapt_result.get("status") != "ok":
            return {
                "status": "error",
                "error_detail": adapt_result
            }

        return {
            "attempt": attempt,
            "adapted_plan": adapt_result.get("result", {})
        }
    

    def safety_node(self, state: RefinementState):
        adapted_plan = state.get("adapted_plan") or {}
        description_to_check = adapted_plan.get("adapted_description", "")
        safety_result = check_safety(llm_core=self.llm_core, provider=self.provider, description=description_to_check, target_age=state["target_age"])
        if safety_result.get("status") != "ok":
            return {"status": "error", "error_detail": safety_result}
        return {"safety_assessment": safety_result["assessment"]}

    def prepare_retry_node(self, state: RefinementState):
        assessment = state.get("safety_assessment", {})
        suggestions = [s.get("change", "") for s in assessment.get("suggestions", [])]
        print(f"Routing back to Adapter with {len(suggestions)} suggestion(s)...")
        return {"revision_notes": suggestions}


    def route_after_safety(self, state: RefinementState) -> str:
        if state.get("status") == "error":
            return END

        assessment = state.get("safety_assessment", {})
        if assessment.get("severity") == "high":
            return "reject"

        if assessment.get("safe_to_use"):
            return "approve"

        if state["attempt"] >= self.MAX_RETRIES:
            return "unresolved"

        return "retry"


    def run_generate(self, topic: str, age: str, goal: str):
        return generate_ideas(
            llm_core=self.llm_core,
            provider=self.provider,
            topic=topic,
            age=age,
            lesson_goal=goal
        )
    
    def run_refine(self, selected_idea: dict, age: str):
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

        result = self.refinement_graph.invoke(initial_state)


        final_status = result.get("status")
        assessment = result.get("safety_assessment") or {}
        if final_status == "error":
            status_mapping = "error"
        elif assessment.get("severity") == "high":
            status_mapping = "rejected"
        elif result.get("attempt", 0) >= self.MAX_RETRIES and not assessment.get("safe_to_use"):
            status_mapping = "unresolved"
        else:
            status_mapping = "ok"

        return {
            "status": status_mapping,
            "final_plan": result.get("adapted_plan"),
            "safety": result.get("safety_assessment"),
            "attempts": result.get("attempt"),
            "error": result.get("error_detail")
        }



