"""
Cerebras AI service for model inference
"""

import asyncio
import json
import logging
from typing import Dict, Any, Optional, AsyncGenerator
from cerebras.cloud.sdk import Cerebras
from app.core.config import settings
from app.core.exceptions import CerebrasAPIError

logger = logging.getLogger(__name__)


class CerebrasService:
    """Service for interacting with Cerebras AI models"""
    
    def __init__(self):
        self.client = Cerebras(api_key=settings.CEREBRAS_API_KEY)
        self.default_model = settings.DEFAULT_MODEL
        self.max_tokens = settings.MAX_TOKENS
        self.temperature = settings.TEMPERATURE
        self.top_p = settings.TOP_P
    
    async def generate_completion(
        self,
        prompt: str,
        model: Optional[str] = None,
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
        top_p: Optional[float] = None,
        stream: bool = False
    ) -> Dict[str, Any]:
        """Generate completion using Cerebras model"""
        try:
            model = model or self.default_model
            max_tokens = max_tokens or self.max_tokens
            temperature = temperature or self.temperature
            top_p = top_p or self.top_p
            
            # Prepare messages
            messages = [
                {
                    "role": "system",
                    "content": "You are a helpful AI assistant powered by Cerebras models."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
            
            if stream:
                return await self._stream_completion(
                    messages=messages,
                    model=model,
                    max_tokens=max_tokens,
                    temperature=temperature,
                    top_p=top_p
                )
            else:
                return await self._generate_completion(
                    messages=messages,
                    model=model,
                    max_tokens=max_tokens,
                    temperature=temperature,
                    top_p=top_p
                )
                
        except Exception as e:
            logger.error(f"Cerebras API error: {e}")
            raise CerebrasAPIError(str(e))
    
    async def _generate_completion(
        self,
        messages: list,
        model: str,
        max_tokens: int,
        temperature: float,
        top_p: float
    ) -> Dict[str, Any]:
        """Generate non-streaming completion"""
        try:
            response = self.client.chat.completions.create(
                messages=messages,
                model=model,
                max_completion_tokens=max_tokens,
                temperature=temperature,
                top_p=top_p,
                stream=False
            )
            
            return {
                "content": response.choices[0].message.content,
                "model": model,
                "tokens_used": getattr(response.usage, 'total_tokens', 0),
                "finish_reason": response.choices[0].finish_reason
            }
            
        except Exception as e:
            logger.error(f"Cerebras completion error: {e}")
            raise CerebrasAPIError(f"Completion generation failed: {str(e)}")
    
    async def _stream_completion(
        self,
        messages: list,
        model: str,
        max_tokens: int,
        temperature: float,
        top_p: float
    ) -> AsyncGenerator[Dict[str, Any], None]:
        """Generate streaming completion"""
        try:
            stream = self.client.chat.completions.create(
                messages=messages,
                model=model,
                max_completion_tokens=max_tokens,
                temperature=temperature,
                top_p=top_p,
                stream=True
            )
            
            for chunk in stream:
                if chunk.choices[0].delta.content:
                    yield {
                        "content": chunk.choices[0].delta.content,
                        "model": model,
                        "finish_reason": None
                    }
            
            # Send final chunk
            yield {
                "content": "",
                "model": model,
                "finish_reason": "stop"
            }
            
        except Exception as e:
            logger.error(f"Cerebras streaming error: {e}")
            raise CerebrasAPIError(f"Streaming generation failed: {str(e)}")
    
    async def generate_agent_response(
        self,
        agent_prompt: str,
        context: Optional[Dict[str, Any]] = None,
        model: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Generate response for a specific agent"""
        try:
            # Build context-aware prompt
            full_prompt = self._build_agent_prompt(agent_prompt, context)
            
            # Generate completion
            response = await self.generate_completion(
                prompt=full_prompt,
                model=model,
                **kwargs
            )
            
            return {
                "response": response["content"],
                "tokens_used": response["tokens_used"],
                "model": response["model"],
                "context": context
            }
            
        except Exception as e:
            logger.error(f"Agent response generation error: {e}")
            raise CerebrasAPIError(f"Agent response generation failed: {str(e)}")
    
    def _build_agent_prompt(self, prompt: str, context: Optional[Dict[str, Any]] = None) -> str:
        """Build context-aware prompt for agent"""
        if not context:
            return prompt
        
        context_str = json.dumps(context, indent=2)
        return f"""
Context Information:
{context_str}

Task:
{prompt}

Please provide a response based on the context and task requirements.
"""
    
    async def get_available_models(self) -> list:
        """Get list of available Cerebras models"""
        try:
            # This would typically call a models endpoint
            # For now, return the known models
            return [
                "llama-4-maverick-17b-128e-instruct",
                "llama-3-8b-instruct",
                "llama-3-70b-instruct",
                "llama-2-7b-chat",
                "llama-2-13b-chat",
                "llama-2-70b-chat"
            ]
        except Exception as e:
            logger.error(f"Error getting available models: {e}")
            return []
    
    async def validate_model(self, model: str) -> bool:
        """Validate if model is available"""
        try:
            available_models = await self.get_available_models()
            return model in available_models
        except Exception as e:
            logger.error(f"Error validating model: {e}")
            return False


# Global Cerebras service instance
cerebras_service = CerebrasService()