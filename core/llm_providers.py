import boto3
import json
import os
from dotenv import load_dotenv
from botocore.config import Config
from google import genai
from google.genai import types

from typing import Optional
from enum import Enum

load_dotenv()

class LLMProvider(str, Enum):
    CLAUDE = "claude"
    GEMINI = "gemini"

DEFAULT_PROVIDER = LLMProvider(os.getenv("LLM_PROVIDER", "gemini"))

    
class LLMCore:
    """Core LLM invocation logic - provider-agnostic interface"""
    
    def __init__(self):
        self._bedrock = None
        self._gemini = None


    @property
    def bedrock(self):
        if self._bedrock is None:
            my_config = Config(retries={'max_attempts': 10, 'mode': 'adaptive'})
            self._bedrock = boto3.client(
                'bedrock-runtime',
                region_name=os.getenv('AWS_REGION', 'eu-central-1'),
                config=my_config
            )
        return self._bedrock

    @property
    def gemini(self):
        if self._gemini is None:
            self._gemini = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        return self._gemini
        
    def invoke_claude(
        self, 
        user_prompt: str, 
        system_prompt: Optional[str] = None,
        max_tokens: int = 1000,
        model_id: str = "global.anthropic.claude-sonnet-4-5-20250929-v1:0"
    ) -> str:
        """Invoke Claude via AWS Bedrock"""

        messages = [
            {
                "role": "user", 
                "content": [{"type": "text", "text": user_prompt}]
            }
        ]
        body_obj = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": max_tokens,
            "system": [{"type": "text", "text": system_prompt}] if system_prompt else [],
            "messages": messages
        }
        
        body = json.dumps(body_obj)
        response = self.bedrock.invoke_model(
            body=body, 
            modelId=model_id
        )
        response_body = json.loads(response.get("body").read())
        return response_body["content"][0]["text"]


    def invoke_gemini(
        self,
        user_prompt: str,
        system_prompt: Optional[str] = None,
        max_tokens: int = 1000,
        model_id: str = os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite"),
    ) -> str:
        """Invoke Gemini via Google AI Studio API"""
        response = self.gemini.models.generate_content(
            model=model_id,
            contents=user_prompt,
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                max_output_tokens=max_tokens,
                thinking_config=types.ThinkingConfig(thinking_level="low"),
            ),
        )
        return response.text
    
    
    def invoke(
        self,
        prompt: str,
        provider: LLMProvider = DEFAULT_PROVIDER,
        system_prompt: Optional[str] = None,
        **kwargs
    ) -> str:
        """Unified invoke interface, routes to the chosen provider."""
        if provider == LLMProvider.CLAUDE:
            return self.invoke_claude(user_prompt=prompt, system_prompt=system_prompt, **kwargs)
        if provider == LLMProvider.GEMINI:
            return self.invoke_gemini(user_prompt=prompt, system_prompt=system_prompt, **kwargs)
        raise ValueError(f"Unknown provider: {provider}")