from bedrock_client import invoke_model
import re
import json


def extract_json(text):
    text = re.sub(r"```json|```", "", text).strip()

    match = re.search(r"\[.*\]", text, re.DOTALL)
    if match:
        return match.group(0)

    return text

def generate_ideas(topic, age_group, lesson_goal):
    # 1. Define the specific logic/prompt here
    system_msg = "You are a pedagogy expert who brainstorms creative, engaging lesson ideas."
    user_msg = f"""Generate EXACTLY 3 classroom activities for: Topic: {topic} Age: {age_group} Goal: {lesson_goal} Return ONLY a JSON array of objects with keys: "title", "materials", "steps", "time", "why_it_works". No preamble or explanation."""

    raw_output = invoke_model(user_msg, system_prompt=system_msg)
    
    try:
        cleaned = extract_json(raw_output)
        ideas = json.loads(cleaned)
    except Exception:
        print("❌ RAW OUTPUT:", raw_output)
        return []

    return ideas[:3]