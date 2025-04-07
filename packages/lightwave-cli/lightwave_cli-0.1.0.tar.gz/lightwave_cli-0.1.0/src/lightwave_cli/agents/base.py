"""
Base Agent

Base class for all pydantic-ai based agents in the LightWave CLI.
"""
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field
from pydantic_ai import Agent
import os
import requests
import json


class LightWaveAgent(Agent):
    """Base agent class for all LightWave agents."""
    
    class Config:
        model_name: str = "google-gla:gemini-1.5-flash"
        api_key_env: str = "GOOGLE_API_KEY"
        temperature: float = 0.1
        max_tokens: int = 4000
    
    @property
    def api_key(self) -> str:
        """Get the API key from the appropriate environment variable."""
        env_var = self.Config.api_key_env
        api_key = os.environ.get(env_var)
        if not api_key:
            raise ValueError(f"Environment variable {env_var} not set")
        return api_key
    
    @property
    def use_mock(self) -> bool:
        """Check if mock mode is enabled."""
        return os.environ.get("AI_USE_MOCK", "").lower() in ("true", "1", "yes")
    
    def generate(self, system: str, user: str, **kwargs) -> str:
        """Generate a response using Google Gemini API or mock response if enabled."""
        # Use mock response if enabled
        if self.use_mock:
            return self._mock_generate(system, user)
            
        model = kwargs.get("model_name", self.Config.model_name)
        temperature = kwargs.get("temperature", self.Config.temperature)
        max_tokens = kwargs.get("max_tokens", self.Config.max_tokens)
        
        # Google Gemini API call
        headers = {
            "Content-Type": "application/json"
        }
        
        api_key = self.api_key
        
        # Google Gemini API endpoint
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
        
        data = {
            "contents": [
                {
                    "role": "user",
                    "parts": [
                        {"text": f"System: {system}\n\nUser: {user}"}
                    ]
                }
            ],
            "generationConfig": {
                "temperature": temperature,
                "maxOutputTokens": max_tokens,
                "topP": 0.8,
                "topK": 40
            }
        }
        
        response = requests.post(
            url,
            headers=headers,
            json=data
        )
        
        if response.status_code != 200:
            raise Exception(f"API request failed with status {response.status_code}: {response.text}")
        
        result = response.json()
        return result["candidates"][0]["content"]["parts"][0]["text"]
    
    def _mock_generate(self, system: str, user: str) -> str:
        """Generate a mock response for testing without API key."""
        if "documentation" in system.lower():
            if "what is" in user.lower() and "lightwave" in user.lower():
                return """
The LightWave ecosystem is a comprehensive development platform consisting of multiple integrated components:

1. lightwave-api-gateway: The central API gateway that routes requests to various services
2. lightwave-cli: Command-line tools for LightWave development workflows
3. lightwave-ai-services: AI services and agents for intelligent functionality
4. lightwave-design-system: Shared design components and standards
5. lightwave-eco-system-docs: Documentation for all projects
6. lightwave-shared-core: Common libraries and utilities
7. lightwave-infrastructure: Infrastructure and deployment tools
8. lightwave-monitoring: Monitoring and observability tools

The platform is designed to enable rapid development of AI-enhanced applications with consistent standards and simplified workflows.
"""
        return "This is a mock response for testing purposes. In production, this would call the Google Gemini API."


class AgentResponse(BaseModel):
    """Standard response model for agents."""
    success: bool = Field(
        ..., 
        description="Whether the operation was successful"
    )
    message: str = Field(
        ..., 
        description="Human-readable message about the operation result"
    )
    data: Optional[Dict[str, Any]] = Field(
        None, 
        description="Optional data returned by the operation"
    )
    errors: Optional[List[str]] = Field(
        None, 
        description="List of errors if any occurred"
    ) 