import boto3, json, os
from dotenv import load_dotenv
from botocore.config import Config

load_dotenv()
my_config = Config(
    retries = {
        'max_attempts': 10,
        'mode': 'adaptive'
    }
)

bedrock = boto3.client(
    'bedrock-runtime', 
    region_name='eu-central-1',
    config=my_config
) 


def generate_activities(topic, age_group, lesson_goal):
    prompt = f"""Generate EXACTLY 3 classroom activities for: Topic: {topic} Age: {age_group} Goal: {lesson_goal} Return ONLY a JSON array of objects with keys: "title", "materials", "steps", "time", "why_it_works". No preamble or explanation."""

    body = json.dumps({
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "text": prompt
                    }
                ]
            }
        ],
        "inferenceConfig": {
            "maxTokens": 1024,
            "temperature": 0.7,
            "topP": 0.9
        }
    })

    response = bedrock.invoke_model(
        modelId='eu.amazon.nova-2-lite-v1:0',
        body=body,
        contentType='application/json',
        accept='application/json'
    )

    #response = bedrock.invoke_model(
    # modelId='anthropic.claude-3-sonnet-20240229-v1:0',
    #body=json.dumps({
    #    "anthropic_version": "bedrock-2023-05-31",
    #    "max_tokens": 300,
    #    "messages": [{"role": "user", "content": prompt}],
    #    "temperature": 0.3
    #    })
    #)

    return json.loads(response['body'].read())['content'][0]['text']
'''


def generate_activities(topic, age_group, lesson_goal):
    prompt = f"""
    Generate EXACTLY 3 classroom activities for topic: {topic}, 
    age: {age_group}, goal: {lesson_goal}. 
    Each: Title, Materials, Steps (3-6 bullets), Time, Why it works.
    JSON only. Classroom-safe.
    """
    
    response = bedrock.invoke_model(
        modelId='anthropic.claude-opus-4-7',
        body=json.dumps({
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 2000,
            "messages": [{"role": "user", "content": prompt}]
        })
    )
    return json.loads(response['body'].read())['content'][0]['text']

'''