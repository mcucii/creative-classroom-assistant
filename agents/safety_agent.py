# agents/safety_agent.py
import re
import json
from agentcore.llm_providers import LLMCore, LLMProvider


SYSTEM_PROMPT = """You are a child safety and educational risk assessor.
Your job is to identify hazards in classroom activities with conservative, age-calibrated judgment.
When in doubt, flag it. Be specific — vague risks are not actionable.
Never return anything other than the requested JSON object."""


RISK_TAXONOMY = """
Evaluate for these risk categories:
- physical_safety: Sharp objects, choking hazards, fire, chemicals, allergenic materials
- emotional_safety: Humiliation, exclusion, anxiety triggers, trauma-adjacent themes  
- age_appropriateness: Concepts, vocabulary, or themes beyond developmental stage
- bias_and_inclusion: Stereotypes, cultural insensitivity, exclusionary assumptions
- supervision_requirements: Steps that require adult oversight not mentioned in activity
"""


def extract_json(text: str) -> str:
    text = re.sub(r"```(?:json)?|```", "", text).strip()
    start = text.find("{")
    if start != -1:
        depth = 0
        for i, ch in enumerate(text[start:], start):
            if ch == "{": depth += 1
            elif ch == "}": depth -= 1
            if depth == 0:
                return text[start:i+1]
    return text


def check_safety(llm_core: LLMCore, provider: LLMProvider, description: str, target_age: str) -> dict:
    if not description or not description.strip():
        return {"status": "error", "error": "description cannot be empty"}
    if not target_age:
        return {"status": "error", "error": "target_age is required"}

    prompt = f"""
        Assess the classroom activity below for a {target_age} year old student group.

        {RISK_TAXONOMY}

        Return ONLY this JSON object — no preamble:
        {{
            "status": "SAFE" or "WARNING",
            "severity": "none" | "low" | "medium" | "high",
            "risks": [
                {{
                    "category": "<from taxonomy above>",
                    "description": "<specific hazard>",
                    "severity": "low" | "medium" | "high"
                }}
            ],
            "suggestions": [
                {{
                    "addresses_risk": "<category from risks list>",
                    "change": "<concrete fix>"
                }}
            ],
            "safe_to_use": true or false
        }}

        Activity:
        {description}

        Target Age: {target_age}
        """

    raw = llm_core.invoke(provider, prompt, system_prompt=SYSTEM_PROMPT)

    try:
        cleaned = extract_json(raw)
        result = json.loads(cleaned)

        required = {"status", "severity", "risks", "suggestions", "safe_to_use"}
        missing = required - result.keys()
        if missing:
            return {
                "status": "parse_error",
                "error": f"Response missing keys: {missing}",
                "raw": raw
            }

        return {"status": "ok", "assessment": result}

    except Exception as e:
        return {"status": "parse_error", "error": str(e), "raw": raw}