# core/llm_providers.py
import boto3
import json
import os
from dotenv import load_dotenv
from botocore.config import Config
from google import genai
from typing import Optional, Literal
from enum import Enum

load_dotenv()

class LLMProvider(str, Enum):
    CLAUDE = "claude"
    GEMINI = "gemini"

class LLMCore:
    def __init__(self):
        # AWS Bedrock setup
        my_config = Config(retries={'max_attempts': 10, 'mode': 'adaptive'})
        self.bedrock = boto3.client(
            'bedrock-runtime', 
            region_name='eu-central-1', 
            config=my_config
        )
        
        # Gemini setup
        self.client_gemini = genai.Client(
            api_key=os.getenv('GEMINI_API_KEY', 'AIzaSyCD2x18mFsf9ynZwLR2RJdmmET7nUtrgb0')
        )
        
        self.default_system_prompt = "You are a creative classroom assistant."
    
    def invoke_claude(
        self, 
        prompt: str, 
        system_prompt: Optional[str] = None,
        max_tokens: int = 1000
    ) -> str:
        """Invoke Claude via AWS Bedrock"""
        body = json.dumps({
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": max_tokens,
            "system": system_prompt or self.default_system_prompt,
            "messages": [{"role": "user", "content": prompt}]
        })
        
        model_id = "eu.anthropic.claude-haiku-4-5-20251001-v1:0"
        
        response = self.bedrock.invoke_model(
            body=body, 
            modelId=model_id
        )
        
        response_body = json.loads(response.get("body").read())
        return response_body["content"][0]["text"]
    
    def invoke_gemini(
        self, 
        prompt: str, 
        system_prompt: Optional[str] = None
    ) -> str:
        """Invoke Gemini via Google GenAI"""
        response = self.client_gemini.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt,
            config=genai.types.GenerateContentConfig(
                system_instruction=system_prompt or self.default_system_prompt
            )
        )
        return response.text
    
    def invoke(
        self, 
        prompt: str,
        provider: LLMProvider = LLMProvider.CLAUDE,
        system_prompt: Optional[str] = None,
        **kwargs
    ) -> str:
        """Unified invoke method"""
        if provider == LLMProvider.CLAUDE:
            return self.invoke_claude(prompt, system_prompt, **kwargs)
        elif provider == LLMProvider.GEMINI:
            return self.invoke_gemini(prompt, system_prompt)
        else:
            raise ValueError(f"Unknown provider: {provider}")