from agents.idea_agent import generate_ideas
from agents.age_adapter_agent import adapt_idea
from agents.safety_agent import check_safety

def run_generate(topic, age_group, lesson_goal):
    return generate_ideas(topic, age_group, lesson_goal)

def run_refine(selected_idea, target_age):
    adapted = adapt_idea(selected_idea, target_age)
    safety = check_safety(adapted, target_age)
    return adapted, safety