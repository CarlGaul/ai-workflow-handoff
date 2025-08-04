#!/usr/bin/env python3
import requests
import json
import sys
import os
import time

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import Config

class OllamaClient:
    def __init__(self, base_url: str = None):
        self.base_url = base_url or Config.OLLAMA_BASE_URL
        self.timeout = 300
        self.session = requests.Session()

    def generate_response(self, model: str, prompt: str, system_prompt: str = "", stream: bool = False):
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
                    "temperature": 0.7,
                    "top_p": 0.9,
                    "num_predict": 2048
                }
            }
            
            print(f"🔍 DEBUG: Sending request to {self.base_url}/api/chat")
            print(f"🔍 DEBUG: Model: {model}")
            print(f"🔍 DEBUG: Stream: {stream}")
            
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
                return result.get("message", {}).get("content", "")
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Ollama request failed: {e}")
            return "Sorry, I'm having trouble connecting to the AI model. Please make sure Ollama is running."
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            return "Sorry, an unexpected error occurred while processing your request."

    def is_available(self) -> bool:
        """Check if Ollama is running and accessible"""
        try:
            response = self.session.get(f"{self.base_url}/api/tags", timeout=10) 
            if response.status_code == 200:
                data = response.json()
                return True
            return False
        except requests.exceptions.RequestException as e:
            print(f"❌ DEBUG: Ollama not available: {e}")
            return False
