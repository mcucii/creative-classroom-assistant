import boto3, json, os
from dotenv import load_dotenv

load_dotenv()
bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')

def generate_activities(topic, age_group, lesson_goal):
    prompt = f"""
    Generate EXACTLY 3 classroom activities for topic: {topic}, 
    age: {age_group}, goal: {lesson_goal}. 
    Each: Title, Materials, Steps (3-6 bullets), Time, Why it works.
    JSON only. Classroom-safe.
    """
    
    response = bedrock.invoke_model(
        modelId='anthropic.claude-sonnet-4.6-v1:0',
        body=json.dumps({
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 2000,
            "messages": [{"role": "user", "content": prompt}]
        })
    )
    return json.loads(response['body'].read())['content'][0]['text']