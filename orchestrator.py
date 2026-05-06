from agents.idea_agent import generate_ideas
from agents.age_adapter_agent import adapt_idea
from agents.safety_agent import check_safety

MAX_RETRIES = 3


def run_generate(topic: str, age: str, goal: str):
    """Generate ideas and return the list for user selection."""
    return generate_ideas(topic, age, goal)


def run_refine(selected_idea: dict, age: str) -> dict:
    """Adapt + safety check a single selected idea, with retries."""
    revision_context = None
    assessment = None
    adapt_result = None

    for attempt in range(1, MAX_RETRIES + 1):
        print(f"\n--- Attempt {attempt}/{MAX_RETRIES} ---")

        adapt_result = adapt_idea(
            selected_idea=selected_idea.get("title", str(selected_idea)),
            target_age=age,
            revision_notes=revision_context
        )

        if adapt_result.get("status") != "ok":
            return {"status": "error", "stage": "adapt", "attempt": attempt, "detail": adapt_result}

        adapted_description = adapt_result["result"]["adapted_description"]

        safety_result = check_safety(adapted_description, age)

        if safety_result.get("status") != "ok":
            return {"status": "error", "stage": "safety", "attempt": attempt, "detail": safety_result}

        assessment = safety_result["assessment"]

        if assessment["severity"] == "high":
            return {"status": "rejected", "reason": "High severity safety issue", "assessment": assessment}

        if assessment["safe_to_use"]:
            return {"status": "ok", "final_plan": adapt_result["result"], "safety": assessment, "attempts": attempt}

        revision_context = [s["change"] for s in assessment.get("suggestions", [])]
        print(f"⚠️  Retrying with {len(revision_context)} suggestion(s): {revision_context}")

    return {
        "status": "unresolved",
        "reason": f"Could not resolve after {MAX_RETRIES} attempts",
        "last_adapted": adapt_result,
        "last_safety": assessment
    }