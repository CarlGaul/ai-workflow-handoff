#!/usr/bin/env python3
"""
Fast Diagnostic Benchmark for Qwen2.5:14b
Tests 3 questions with 2 temperatures for quick baseline metrics
"""

import json
import time
import logging
import signal
import sys
import os
from datetime import datetime
from pathlib import Path
import requests

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ollama_client import OllamaClient
from config import Config

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Global timeout handler
class TimeoutError(Exception):
    pass

def timeout_handler(signum, frame):
    raise TimeoutError("Operation timed out")

# Simplified system prompt (shorter for speed)
SYSTEM_PROMPT = """You are an associate attorney specializing in pregnancy discrimination cases. 
Provide zero-hallucination responses with Bluebook citations. 
Analyze using Title VII, EEOC guidance, and NY state laws."""

# Reduced to 3 questions for diagnostic
LEGAL_QUESTIONS = [
    {
        "category": "Pregnancy Termination",
        "question": "Draft a legal memo on pregnancy discrimination under Title VII for an employee terminated after announcing pregnancy.",
        "expected_aspects": ["Title VII", "termination", "pregnancy", "discrimination"]
    },
    {
        "category": "Accommodation Denial", 
        "question": "Analyze potential claims for a pregnant worker denied reasonable accommodations, citing relevant EEOC guidance.",
        "expected_aspects": ["accommodations", "EEOC", "reasonable", "pregnancy"]
    },
    {
        "category": "NY Retaliation Case",
        "question": "Prepare a complaint outline for a pregnancy-related retaliation case in NY Supreme Court.",
        "expected_aspects": ["retaliation", "NY", "complaint", "court"]
    }
]

TEMPERATURES = [0.3, 0.7]  # Reduced to 2 for faster testing

def test_ollama_connectivity():
    """Test Ollama connectivity before starting"""
    logger.info("🔍 Testing Ollama connectivity...")
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=10)
        if response.status_code == 200:
            logger.info("✅ Ollama is accessible")
            models = response.json().get("models", [])
            logger.info(f"📋 Available models: {[m['name'] for m in models]}")
            return True
        else:
            logger.error(f"❌ Ollama responded with status: {response.status_code}")
            return False
    except Exception as e:
        logger.error(f"❌ Ollama connectivity test failed: {e}")
        return False

def generate_response(client, question_data, temperature, timeout_seconds=120):
    """Generate a single response with timeout and error handling"""
    logger.info(f"🧪 Testing: {question_data['category']} (temp: {temperature})")
    
    start_time = time.time()
    
    try:
        # Set timeout for the entire operation
        signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(timeout_seconds)
        
        logger.info("📡 Sending request to Ollama...")
        response = client.generate_response(
            model="qwen2.5:14b",
            prompt=question_data["question"],
            system_prompt=SYSTEM_PROMPT,
            temperature=temperature
        )
        
        # Cancel timeout
        signal.alarm(0)
        
        end_time = time.time()
        response_time = end_time - start_time
        
        logger.info(f"✅ Response received in {response_time:.2f} seconds")
        logger.info(f"📊 Response length: {len(response)} characters")
        
        # Calculate basic metrics
        word_count = len(response.split())
        char_count = len(response)
        
        # Count citations (Bluebook format indicators)
        citation_indicators = ["v.", "U.S.", "F.2d", "F.3d", "F.Supp.", "F.Supp.2d", "S.Ct.", "L.Ed.", "42 U.S.C.", "29 U.S.C.", "29 C.F.R.", "42 C.F.R."]
        citation_count = sum(1 for indicator in citation_indicators if indicator in response)
        
        # Check for expected aspects
        expected_aspects = question_data.get("expected_aspects", [])
        aspect_coverage = sum(1 for aspect in expected_aspects 
                            if aspect.lower() in response.lower()) / len(expected_aspects) if expected_aspects else 0
        
        return {
            "timestamp": datetime.now().isoformat(),
            "category": question_data["category"],
            "question": question_data["question"],
            "response": response,
            "response_time_seconds": response_time,
            "word_count": word_count,
            "char_count": char_count,
            "citation_count": citation_count,
            "aspect_coverage": aspect_coverage,
            "temperature": temperature,
            "model": "qwen2.5:14b",
            "status": "success"
        }
        
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

def run_diagnostic_benchmark():
    """Run the fast diagnostic benchmark"""
    logger.info("🚀 Starting fast diagnostic benchmark...")
    
    # Test connectivity first
    if not test_ollama_connectivity():
        logger.error("❌ Ollama connectivity failed - aborting")
        return None
    
    # Initialize client
    logger.info("🔧 Creating OllamaClient...")
    try:
        client = OllamaClient(seed=42)
        logger.info("✅ OllamaClient created successfully")
    except Exception as e:
        logger.error(f"❌ OllamaClient creation failed: {e}")
        return None
    
    results = []
    total_questions = len(LEGAL_QUESTIONS) * len(TEMPERATURES)
    current_question = 0
    
    for i, question in enumerate(LEGAL_QUESTIONS, 1):
        logger.info(f"📋 Processing question {i}/{len(LEGAL_QUESTIONS)}: {question['category']}")
        
        for temp in TEMPERATURES:
            current_question += 1
            logger.info(f"🌡️ Testing temperature {temp} ({current_question}/{total_questions})")
            
            result = generate_response(client, question, temp, timeout_seconds=120)
            results.append(result)
            
            # Small delay between requests
            time.sleep(2)
    
    # Save results
    save_diagnostic_results(results)
    
    # Print summary
    successful = [r for r in results if r.get("status") == "success"]
    if successful:
        avg_time = sum(r["response_time_seconds"] for r in successful) / len(successful)
        logger.info(f"📊 Summary: {len(successful)}/{len(results)} successful, avg time: {avg_time:.2f}s")
    else:
        logger.warning("⚠️ No successful responses recorded")
    
    return results

def save_diagnostic_results(results):
    """Save diagnostic results to file"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"diagnostic_benchmark_{timestamp}.json"
    
    # Create benchmarks directory if it doesn't exist
    benchmark_dir = Path("benchmarks")
    benchmark_dir.mkdir(exist_ok=True)
    filepath = benchmark_dir / filename
    
    output_data = {
        "diagnostic_info": {
            "model": "qwen2.5:14b",
            "timestamp": datetime.now().isoformat(),
            "total_questions": len(results),
            "successful_responses": len([r for r in results if r.get("status") == "success"]),
            "failed_responses": len([r for r in results if r.get("status") != "success"]),
            "test_type": "fast_diagnostic"
        },
        "results": results
    }
    
    with open(filepath, 'w') as f:
        json.dump(output_data, f, indent=2)
    
    logger.info(f"💾 Results saved to {filepath}")
    
    # Also save a summary report
    save_diagnostic_summary(timestamp, results)

def save_diagnostic_summary(timestamp, results):
    """Save a human-readable summary report"""
    filename = f"diagnostic_summary_{timestamp}.md"
    benchmark_dir = Path("benchmarks")
    filepath = benchmark_dir / filename
    
    with open(filepath, 'w') as f:
        f.write("# Fast Diagnostic Benchmark Results\n\n")
        f.write(f"**Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"**Model**: qwen2.5:14b\n")
        f.write(f"**Test Type**: Fast Diagnostic (3 questions, 2 temperatures)\n")
        f.write(f"**Total Responses**: {len(results)}\n")
        f.write(f"**Successful**: {len([r for r in results if r.get('status') == 'success'])}\n\n")
        
        # Calculate summary stats
        successful = [r for r in results if r.get("status") == "success"]
        if successful:
            avg_time = sum(r["response_time_seconds"] for r in successful) / len(successful)
            avg_words = sum(r["word_count"] for r in successful) / len(successful)
            avg_citations = sum(r["citation_count"] for r in successful) / len(successful)
            
            f.write("## Performance Summary\n\n")
            f.write(f"- **Average Response Time**: {avg_time:.2f} seconds\n")
            f.write(f"- **Average Word Count**: {avg_words:.0f} words\n")
            f.write(f"- **Average Citations**: {avg_citations:.1f}\n\n")
        
        f.write("## Detailed Results\n\n")
        for i, result in enumerate(results, 1):
            f.write(f"### {i}. {result['category']} (Temp: {result['temperature']})\n")
            f.write(f"**Question**: {result['question']}\n")
            if result.get("status") == "success":
                f.write(f"**Response Time**: {result['response_time_seconds']:.2f}s\n")
                f.write(f"**Word Count**: {result['word_count']}\n")
                f.write(f"**Citations**: {result['citation_count']}\n")
                f.write(f"**Response**: {result['response'][:200]}...\n\n")
            else:
                f.write(f"**Error**: {result.get('error', 'Unknown error')}\n\n")
    
    logger.info(f"📄 Summary report saved to {filepath}")

if __name__ == "__main__":
    try:
        logger.info("🚀 Starting diagnostic benchmark...")
        results = run_diagnostic_benchmark()
        if results:
            logger.info("✅ Diagnostic complete!")
        else:
            logger.error("❌ Diagnostic failed")
            sys.exit(1)
    except Exception as e:
        logger.error(f"❌ Main execution error: {str(e)}")
        sys.exit(1) 