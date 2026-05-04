import boto3, json, os
from dotenv import load_dotenv
from botocore.config import Config
from google import genai
from google import genai         # This is the correct modern import
from google.genai import types

load_dotenv()

# Configuration
my_config = Config(retries={'max_attempts': 10, 'mode': 'adaptive'})
bedrock = boto3.client('bedrock-runtime', region_name='eu-central-1', config=my_config)
client_gemini = genai.Client(api_key='AIzaSyCD2x18mFsf9ynZwLR2RJdmmET7nUtrgb0')

# 1. AWS Bedrock (Claude)
def invoke_model(prompt, system_prompt="You are a creative classroom assistant."):
    body = json.dumps({
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 1000,
        "system": system_prompt,
        "messages": [{"role": "user", "content": prompt}]
    })

    model_id = "eu.anthropic.claude-haiku-4-5-20251001-v1:0"

    
    response = bedrock.invoke_model(
        body=body, 
        modelId = model_id
    )

    response_body = json.loads(response.get("body").read())
    return response_body["content"][0]["text"]

# 2. Google GenAI (Gemini)
# def invoke_gemini(prompt, system_prompt="You are a creative classroom assistant."):
#     response = client_gemini.models.generate_content(
#         model="gemini-2.0-flash",
#         contents=prompt,
#         config=genai.types.GenerateContentConfig(system_instruction=system_prompt)
#     )
#     return response.text

# Usage
# print(invoke_claude("Explain photosynthesis"))
# print(invoke_gemini("Explain gravity"))
