import re
import json

from agentcore.llm_providers import LLMCore, LLMProvider


def extract_json(text: str) -> str:
    text = re.sub(r"```(?:json)?|```", "", text).strip()
    
    start = text.find("[")
    if start != -1:
        depth = 0
        for i, ch in enumerate(text[start:], start):
            if ch == "[": depth += 1
            elif ch == "]": depth -= 1
            if depth == 0:
                return text[start:i+1]
    
    return text 


def generate_ideas(llm_core, provider, topic, age, lesson_goal):
    if not topic or not topic.strip():
        return {"status": "error", "error": "topic cannot be empty"}
    if not age:
        return {"status": "error", "error": "age is required"}
    if not lesson_goal or not lesson_goal.strip():
        return {"status": "error", "error": "lesson_goal cannot be empty"}
    

    system_msg = "You are a pedagogy expert who brainstorms creative, engaging lesson ideas."
    
    user_msg = f"""Generate EXACTLY 3 classroom activities for:
                Topic: {topic}
                Age: {age}
                Goal: {lesson_goal}

                Language rules:
                - Use simple, clear vocabulary appropriate for {age} students
                - Keep sentences short
                - Avoid jargon or technical terms — if unavoidable, explain them in plain language
                - Write as if explaining to the student directly, not to the teacher

                Return ONLY a JSON array of 3 objects, each with keys:
                "title", "materials", "steps", "time", "why_it_works"

                No preamble, explanation, or extra keys."""
    
    raw_output = llm_core.invoke(user_msg, system_prompt=system_msg, provider=provider)
    
    try:
        cleaned = extract_json(raw_output)
        ideas = json.loads(cleaned)
        if not isinstance(ideas, list):
            return {"status": "parse_error", "error": "Expected a JSON array", "raw": raw_output}
        
        if len(ideas) != 3:
            print(f"⚠️ Expected 3 ideas, got {len(ideas)}")
        
        return ideas
    
    except Exception as e:
        print(f"❌ JSON parse failed: {e}")
        print(f"❌ RAW OUTPUT: {raw_output}")
        return []
