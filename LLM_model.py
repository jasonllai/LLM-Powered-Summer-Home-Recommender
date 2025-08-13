import requests
import json
import os
import time
import logging
from typing import List, Dict, Any, Optional, Union
from dataclasses import dataclass, field
from abc import ABC, abstractmethod

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class ModelConfig:
    """Configuration for LLM model settings to ensure reproducibility"""
    model: str = "google/gemini-2.0-flash-exp:free"
    temperature: float = 0.1  # Lower temperature for more reproducible outputs
    max_tokens: Optional[int] = None
    top_p: float = 1.0
    frequency_penalty: float = 0.0
    presence_penalty: float = 0.0
    seed: Optional[int] = 42  # For reproducibility when supported
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert config to dictionary for API call"""
        config = {
            "model": self.model,
            "temperature": self.temperature,
            "top_p": self.top_p,
            "frequency_penalty": self.frequency_penalty,
            "presence_penalty": self.presence_penalty,
        }
        if self.max_tokens:
            config["max_tokens"] = self.max_tokens
        if self.seed:
            config["seed"] = self.seed
        return config


@dataclass
class Message:
    """Represents a single message in the conversation"""
    role: str  # "user", "assistant", or "system"
    content: Union[str, List[Dict[str, Any]]]
    
    def to_dict(self) -> Dict[str, Any]:
        return {"role": self.role, "content": self.content}


class LLMClient:
    """
    Improved LLM API client with better reproducibility and error handling
    """
    
    def __init__(self, api_key: Optional[str] = None, base_url: str = "https://openrouter.ai/api/v1"):
        self.api_key = api_key or os.getenv("OPENROUTER_API_KEY")
        self.base_url = base_url
        self.session = requests.Session()
        
        if not self.api_key:
            raise ValueError("API key must be provided either as parameter or OPENROUTER_API_KEY environment variable")
        
        # Set default headers
        self.session.headers.update({
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "LLM-Summer-Home-Recommender",  # Optional: helps with rate limits
        })
    
    def create_text_message(self, content: str, role: str = "user") -> Message:
        """Create a simple text message"""
        return Message(role=role, content=content)
    
    def create_multimodal_message(self, text: str, image_url: str, role: str = "user") -> Message:
        """Create a message with both text and image"""
        content = [
            {"type": "text", "text": text},
            {"type": "image_url", "image_url": {"url": image_url}}
        ]
        return Message(role=role, content=content)
    
    def chat_completion(
        self,
        messages: List[Message],
        config: Optional[ModelConfig] = None,
        max_retries: int = 3,
        retry_delay: float = 1.0
    ) -> Dict[str, Any]:
        """
        Send chat completion request with retry logic and error handling
        
        Args:
            messages: List of Message objects
            config: ModelConfig for API parameters
            max_retries: Number of retry attempts
            retry_delay: Delay between retries in seconds
            
        Returns:
            API response as dictionary
        """
        if not messages:
            raise ValueError("At least one message must be provided")
        
        config = config or ModelConfig()
        
        # Prepare request payload
        payload = {
            **config.to_dict(),
            "messages": [msg.to_dict() for msg in messages]
        }
        
        url = f"{self.base_url}/chat/completions"
        
        for attempt in range(max_retries + 1):
            try:
                logger.info(f"Making API request (attempt {attempt + 1}/{max_retries + 1})")
                response = self.session.post(url, json=payload, timeout=60)
                
                if response.status_code == 200:
                    return response.json()
                elif response.status_code == 429:  # Rate limit
                    if attempt < max_retries:
                        wait_time = retry_delay * (2 ** attempt)  # Exponential backoff
                        logger.warning(f"Rate limited. Waiting {wait_time} seconds...")
                        time.sleep(wait_time)
                        continue
                    else:
                        raise Exception(f"Rate limited after {max_retries} retries")
                else:
                    logger.error(f"API error: {response.status_code} - {response.text}")
                    response.raise_for_status()
                    
            except requests.exceptions.RequestException as e:
                if attempt < max_retries:
                    logger.warning(f"Request failed: {e}. Retrying in {retry_delay} seconds...")
                    time.sleep(retry_delay)
                    continue
                else:
                    raise Exception(f"Request failed after {max_retries} retries: {e}")
        
        raise Exception("Unexpected error in chat completion")
    
    def simple_prompt(self, prompt: str, config: Optional[ModelConfig] = None) -> str:
        """
        Simple interface for single text prompts
        
        Args:
            prompt: The text prompt to send
            config: Optional model configuration
            
        Returns:
            The response text content
        """
        message = self.create_text_message(prompt)
        response = self.chat_completion([message], config)
        
        try:
            return response["choices"][0]["message"]["content"]
        except (KeyError, IndexError) as e:
            logger.error(f"Unexpected response format: {response}")
            raise Exception(f"Failed to extract content from response: {e}")


# Example usage and testing functions
def main():
    """Example usage of the improved LLM client"""
    try:
        # Initialize client
        client = LLMClient()
        
        # Example 1: Simple text prompt
        print("=== Simple Text Prompt ===")
        config = ModelConfig(temperature=0.1)  # Low temperature for reproducibility
        
        prompt = "Explain the benefits of renewable energy in exactly 3 bullet points."
        response = client.simple_prompt(prompt, config)
        print(f"Response: {response}\n")
        
        # Example 2: Multi-message conversation
        print("=== Multi-message Conversation ===")
        messages = [
            client.create_text_message("You are a helpful assistant specializing in vacation rentals.", "system"),
            client.create_text_message("What factors should I consider when choosing a summer home rental?")
        ]
        
        response = client.chat_completion(messages, config)
        print(f"Response: {response['choices'][0]['message']['content']}\n")
        
        # Example 3: Image analysis (if you have an image URL)
        print("=== Image Analysis Example ===")
        image_message = client.create_multimodal_message(
            "Describe this location for a vacation rental listing.",
            "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/2560px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg"
        )
        
        response = client.chat_completion([image_message], config)
        print(f"Image analysis: {response['choices'][0]['message']['content']}")
        
    except Exception as e:
        logger.error(f"Error in main: {e}")


if __name__ == "__main__":
    main()
