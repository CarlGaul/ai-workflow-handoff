#!/usr/bin/env python3
"""
Debug version of Qwen pregnancy discrimination benchmark
Added comprehensive error handling, timeouts, and progress indicators
"""

import json
import time
import logging
import random
import torch
import signal
import sys
from datetime import datetime
from pathlib import Path
import os
import requests

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ollama_client import OllamaClient
from config import Config

# Set up detailed logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Global timeout handler
class TimeoutError(Exception):
    pass

def timeout_handler(signum, frame):
    raise TimeoutError("Operation timed out")

class PregnancyDiscriminationBenchmarkDebug:
    def __init__(self):
        logger.info("🔧 Initializing debug benchmark...")
        
        # Test Ollama connectivity first
        logger.info("🔍 Testing Ollama connectivity...")
        try:
            response = requests.get("http://localhost:11434/api/tags", timeout=10)
            if response.status_code == 200:
                logger.info("✅ Ollama is accessible")
                models = response.json().get("models", [])
                logger.info(f"📋 Available models: {[m['name'] for m in models]}")
            else:
                logger.error(f"❌ Ollama responded with status: {response.status_code}")
                raise Exception("Ollama not responding properly")
        except Exception as e:
            logger.error(f"❌ Ollama connectivity test failed: {e}")
            raise
        
        # Initialize client with timeout
        logger.info("🔧 Creating OllamaClient...")
        try:
            self.client = OllamaClient(seed=42)
            logger.info("✅ OllamaClient created successfully")
        except Exception as e:
            logger.error(f"❌ OllamaClient creation failed: {e}")
            raise
        
        self.results = []
        self.benchmark_dir = Path("benchmarks")
        self.benchmark_dir.mkdir(exist_ok=True)
        logger.info("✅ Debug benchmark initialized")
        
    def get_simple_test_questions(self):
        """Simplified test questions for debugging"""
        return [
            {
                "category": "Simple Test",
                "question": "What is pregnancy discrimination?",
                "expected_aspects": ["discrimination", "pregnancy"]
            },
            {
                "category": "Legal Test", 
                "question": "Draft a brief memo on pregnancy discrimination rights.",
                "expected_aspects": ["rights", "legal", "memo"]
            }
        ]
    
    def get_system_prompt(self):
        """Simplified system prompt for testing"""
        return """You are a legal AI assistant specializing in employment law. 
Provide concise, accurate responses with legal citations when possible."""
    
    def test_single_response(self, question_data, temperature=0.3, timeout_seconds=60):
        """Test a single response with comprehensive error handling"""
        logger.info(f"🧪 Testing question: {question_data['category']}")
        logger.info(f"📝 Question: {question_data['question'][:50]}...")
        logger.info(f"🌡️ Temperature: {temperature}")
        
        start_time = time.time()
        
        try:
            # Set timeout for the entire operation
            signal.signal(signal.SIGALRM, timeout_handler)
            signal.alarm(timeout_seconds)
            
            logger.info("📡 Sending request to Ollama...")
            response = self.client.generate_response(
                model="qwen2.5:14b",
                prompt=question_data["question"],
                system_prompt=self.get_system_prompt(),
                temperature=temperature
            )
            
            # Cancel timeout
            signal.alarm(0)
            
            end_time = time.time()
            response_time = end_time - start_time
            
            logger.info(f"✅ Response received in {response_time:.2f} seconds")
            logger.info(f"📊 Response length: {len(response)} characters")
            
            # Basic metrics
            word_count = len(response.split())
            char_count = len(response)
            
            result = {
                "timestamp": datetime.now().isoformat(),
                "category": question_data["category"],
                "question": question_data["question"],
                "response": response,
                "response_time_seconds": response_time,
                "word_count": word_count,
                "char_count": char_count,
                "temperature": temperature,
                "model": "qwen2.5:14b",
                "status": "success"
            }
            
            logger.info(f"✅ Question completed successfully")
            return result
            
        except TimeoutError:
            logger.error(f"⏰ Timeout after {timeout_seconds} seconds")
            return {
                "timestamp": datetime.now().isoformat(),
                "category": question_data["category"],
                "question": question_data["question"],
                "error": f"Timeout after {timeout_seconds} seconds",
                "temperature": temperature,
                "model": "qwen2.5:14b",
                "status": "timeout"
            }
        except Exception as e:
            logger.error(f"❌ Error during response generation: {e}")
            return {
                "timestamp": datetime.now().isoformat(),
                "category": question_data["category"],
                "question": question_data["question"],
                "error": str(e),
                "temperature": temperature,
                "model": "qwen2.5:14b",
                "status": "error"
            }
    
    def run_debug_benchmark(self):
        """Run simplified debug benchmark"""
        logger.info("🚀 Starting debug benchmark...")
        
        questions = self.get_simple_test_questions()
        temperatures = [0.3, 0.7]  # Reduced for testing
        
        for temp in temperatures:
            logger.info(f"🌡️ Testing temperature {temp}...")
            
            for question in questions:
                logger.info(f"📋 Processing question: {question['category']}")
                result = self.test_single_response(question, temperature=temp, timeout_seconds=120)
                self.results.append(result)
                
                # Small delay between requests
                time.sleep(2)
        
        # Save results
        self.save_debug_results()
        logger.info("✅ Debug benchmark completed!")
    
    def save_debug_results(self):
        """Save debug results to file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"debug_benchmark_{timestamp}.json"
        filepath = self.benchmark_dir / filename
        
        output_data = {
            "debug_info": {
                "model": "qwen2.5:14b",
                "timestamp": datetime.now().isoformat(),
                "total_questions": len(self.results),
                "successful_responses": len([r for r in self.results if r.get("status") == "success"]),
                "failed_responses": len([r for r in self.results if r.get("status") != "success"])
            },
            "results": self.results
        }
        
        with open(filepath, 'w') as f:
            json.dump(output_data, f, indent=2)
        
        logger.info(f"💾 Results saved to {filepath}")
        
        # Print summary
        successful = [r for r in self.results if r.get("status") == "success"]
        if successful:
            avg_time = sum(r["response_time_seconds"] for r in successful) / len(successful)
            logger.info(f"📊 Summary: {len(successful)}/{len(self.results)} successful, avg time: {avg_time:.2f}s")
        else:
            logger.warning("⚠️ No successful responses recorded")

def main():
    """Run the debug benchmark"""
    try:
        benchmark = PregnancyDiscriminationBenchmarkDebug()
        benchmark.run_debug_benchmark()
    except Exception as e:
        logger.error(f"❌ Fatal error in main: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 