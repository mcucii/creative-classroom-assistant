# agents/age_adapter_agent.py
from bedrock_client import invoke_model

def adapt_idea(selected_idea, target_age):
    prompt = f"""
    Act as an expert teacher. Adapt the following lesson idea for {target_age} students.
    Make the language, tone, and complexity perfectly suited for this age group.
    
    Idea: {selected_idea}
    
    Provide a structured activity plan.
    """
    return invoke_model(prompt)