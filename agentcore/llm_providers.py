"""
LLM Provider abstraction layer
Supports AWS Bedrock (Claude) and Google GenAI (Gemini)
"""
import boto3
import json
import os
from dotenv import load_dotenv
from botocore.config import Config
from google import genai
from typing import Optional, Literal, Dict, Any
from enum import Enum

load_dotenv()

class LLMProvider(str, Enum):
    CLAUDE = "claude"

class LLMCore:
    """Core LLM invocation logic - provider-agnostic interface"""
    
    def __init__(self):
        # AWS Bedrock setup
        my_config = Config(retries={'max_attempts': 10, 'mode': 'adaptive'})
        self.bedrock = boto3.client(
            'bedrock-runtime', 
            region_name=os.getenv('AWS_REGION', 'eu-central-1'),
            config=my_config
        )
        
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
    
    
    def invoke(
        self,
        prompt: str,
        provider: LLMProvider = LLMProvider.CLAUDE,
        system_prompt: Optional[str] = None,
        **kwargs
    ) -> str:
        """
        Unified invoke interface. `prompt` is the first positional argument; `provider`
        may be provided as a keyword (defaults to Claude). For Claude we forward to
        `invoke_claude` which expects `user_prompt` and an optional `system_prompt`.
        """
        if provider == LLMProvider.CLAUDE:
            return self.invoke_claude(user_prompt=prompt, system_prompt=system_prompt, **kwargs)
        else:
            raise ValueError(f"Unknown provider: {provider}")