# agents/age_adapter_agent.py
from bedrock_client import invoke_model

AGE_PROFILES = {
    "5-7":   "Play-based learning, tactile activities, 10-15 min attention spans. Simple sentences.",
    "8-10":  "Structured tasks, guided discovery, 20-25 min spans. Can handle multi-step instructions.",
    "11-12": "Collaborative projects, beginning abstract thought, 30 min spans.",
    "12-14": "Social interaction, abstract reasoning, autonomy, debate and reflection.",
    "15-17": "Critical thinking, real-world connections, independent research, peer discussion.",
}

def get_age_profile(age):
    profile = AGE_PROFILES.get(age)
    if profile:
        return profile, True
    return "General student population. Adjust complexity based on context.", False


def adapt_idea(selected_idea: str, target_age: str, revision_notes=None) -> dict:
    profile, found = get_age_profile(target_age)

    if not found:
        print(f"[age_adapter] Warning: no profile for age '{target_age}', using fallback")

    revision_section = ""
    if revision_notes:
        revision_section = f"\nRevision notes from safety check — please address these:\n" + "\n".join(f"- {r}" for r in revision_notes)

    prompt = f"""
        Role: Expert Pedagogical Designer.
        Context: Students aged {target_age}. {profile}
        Task: Adapt the idea below for this age group.
        Constraint: Use vocabulary appropriate for age {target_age}.
        {revision_section}

        Idea: {selected_idea}

        Respond in this exact JSON format:
        {{
            "title": "Activity name",
            "duration_minutes": 20,
            "adapted_description": "Full description of the adapted activity",
            "materials": ["item1", "item2"],
            "vocabulary_level": "brief note on language complexity used"
        }}
    """

    raw = invoke_model(prompt)

    try:
        import json, re
        cleaned = re.sub(r"```(?:json)?|```", "", raw).strip()
        return {"status": "ok", "age": target_age, "result": json.loads(cleaned)}
    except Exception as e:
        return {"status": "parse_error", "age": target_age, "raw": raw, "error": str(e)}

