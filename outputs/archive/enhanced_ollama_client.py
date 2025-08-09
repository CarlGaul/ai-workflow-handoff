#!/usr/bin/env python3
import requests
import json
import sys
import os
import time
import logging
import random
import torch

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import Config

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class OllamaClient:
    def __init__(self, base_url: str = None, seed: int = None):
        self.base_url = base_url or Config.OLLAMA_BASE_URL
        self.timeout = 300
        self.session = requests.Session()
        
        # Set seeds for reproducibility
        if seed is not None:
            self.seed = seed
            random.seed(seed)
            if torch.cuda.is_available():
                torch.cuda.manual_seed(seed)
            torch.manual_seed(seed)
        else:
            self.seed = random.randint(1, 1000000)
            random.seed(self.seed)
            if torch.cuda.is_available():
                torch.cuda.manual_seed(self.seed)
            torch.manual_seed(self.seed)
        
        logger.info(f"OllamaClient initialized with seed: {self.seed}")

    def generate_response(self, model: str, prompt: str, system_prompt: str = "", stream: bool = False, temperature: float = 0.7):
        """Generate response from Ollama using chat API"""
        try:
            # Build messages array
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})
            
            payload = {
                "model": model,
                "messages": messages,
                "stream": stream,
                "options": {
                    "temperature": temperature,
                    "top_p": 0.9,
                    "num_predict": 2048,
                    "seed": self.seed
                }
            }
            
            logger.info(f"Generating response with model: {model}, temperature: {temperature}, stream: {stream}")
            
            response = self.session.post(
                f"{self.base_url}/api/chat",
                json=payload,
                timeout=self.timeout,
                stream=stream
            )
            response.raise_for_status()
            
            if stream:
                # For streaming, return a generator
                def generate_chunks():
                    for line in response.iter_lines():
                        if line:
                            try:
                                chunk = json.loads(line.decode('utf-8'))
                                if "content" in chunk.get("message", {}):
                                    yield chunk["message"]["content"]
                                if chunk.get("done"):
                                    break
                            except json.JSONDecodeError:
                                continue
                
                return generate_chunks()
            else:
                # For non-streaming, return the response directly
                result = response.json()
                content = result.get("message", {}).get("content", "")
                logger.info(f"Generated response length: {len(content)} characters")
                return content
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Ollama request failed: {e}")
            return "Sorry, I'm having trouble connecting to the AI model. Please make sure Ollama is running."
        except Exception as e:
            logger.error(f"Unexpected error in generate_response: {e}")
            return "Sorry, an unexpected error occurred while processing your request."

    def generate_multiple_responses(self, model: str, prompt: str, system_prompt: str = "", 
                                  temperatures: list = [0.3, 0.7, 1.0], max_responses: int = 3):
        """Generate multiple responses with different temperatures for comparison"""
        try:
            logger.info(f"Generating {len(temperatures)} responses with temperatures: {temperatures}")
            
            responses = []
            for i, temp in enumerate(temperatures[:max_responses]):
                logger.info(f"Generating response {i+1}/{len(temperatures[:max_responses])} with temperature {temp}")
                
                response = self.generate_response(
                    model=model,
                    prompt=prompt,
                    system_prompt=system_prompt,
                    stream=False,
                    temperature=temp
                )
                
                responses.append({
                    "temperature": temp,
                    "response": response,
                    "response_number": i + 1
                })
                
                # Small delay between requests to avoid overwhelming the server
                time.sleep(0.5)
            
            logger.info(f"Successfully generated {len(responses)} responses")
            return responses
            
        except Exception as e:
            logger.error(f"Error in generate_multiple_responses: {e}")
            return [{"temperature": 0.7, "response": "Error generating multiple responses", "response_number": 1}]

    def is_available(self) -> bool:
        """Check if Ollama is running and accessible"""
        try:
            response = self.session.get(f"{self.base_url}/api/tags", timeout=10) 
            if response.status_code == 200:
                data = response.json()
                logger.info("Ollama is available and responding")
                return True
            logger.warning(f"Ollama responded with status code: {response.status_code}")
            return False
        except requests.exceptions.RequestException as e:
            logger.error(f"Ollama not available: {e}")
            return False

    def get_model_info(self, model: str) -> dict:
        """Get information about a specific model"""
        try:
            response = self.session.get(f"{self.base_url}/api/show", params={"name": model}, timeout=10)
            if response.status_code == 200:
                return response.json()
            else:
                logger.warning(f"Could not get model info for {model}: {response.status_code}")
                return {}
        except Exception as e:
            logger.error(f"Error getting model info: {e}")
            return {}

# Test function for development
if __name__ == "__main__":
    client = OllamaClient(seed=42)
    
    if client.is_available():
        print("✅ Ollama is available")
        
        # Test single response
        response = client.generate_response(
            model="qwen2.5:14b",
            prompt="What is pregnancy discrimination?",
            system_prompt="You are a legal AI assistant specializing in employment law.",
            temperature=0.7
        )
        print(f"Single response: {response[:100]}...")
        
        # Test multiple responses
        responses = client.generate_multiple_responses(
            model="qwen2.5:14b",
            prompt="What is pregnancy discrimination?",
            system_prompt="You are a legal AI assistant specializing in employment law.",
            temperatures=[0.3, 0.7, 1.0]
        )
        
        for resp in responses:
            print(f"\nTemperature {resp['temperature']}: {resp['response'][:100]}...")
    else:
        print("❌ Ollama is not available")
