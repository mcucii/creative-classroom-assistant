# agents/safety_agent.py
from bedrock_client import invoke_model

def check_safety(adapted_text, target_age):
    prompt = f"""
    Act as a School Safety Officer. Review the following activity for {target_age} students.
    Check for:
    1. Inappropriate language or themes.
    2. Physical dangers.
    3. Potential biases.
    
    Activity: {adapted_text}
    
    Start your response with '✅ SAFE' or '⚠️ WARNING', followed by a 1-sentence explanation.
    """
    return invoke_model(prompt)