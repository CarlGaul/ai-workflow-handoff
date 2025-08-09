#!/usr/bin/env python3
"""
Fixed Qwen pregnancy discrimination benchmark
Incorporates timeout handling, error handling, and progress indicators
"""

import json
import time
import logging
import random
import torch
import signal
import sys
import requests
from datetime import datetime
from pathlib import Path
import os

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ollama_client import OllamaClient
from config import Config

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Global timeout handler
class TimeoutError(Exception):
    pass

def timeout_handler(signum, frame):
    raise TimeoutError("Operation timed out")

class PregnancyDiscriminationBenchmark:
    def __init__(self):
        logger.info("🔧 Initializing pregnancy discrimination benchmark...")
        
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
        
        # Initialize client
        logger.info("🔧 Creating OllamaClient...")
        try:
            self.client = OllamaClient(seed=42)  # Fixed seed for reproducibility
            logger.info("✅ OllamaClient created successfully")
        except Exception as e:
            logger.error(f"❌ OllamaClient creation failed: {e}")
            raise
        
        self.results = []
        self.benchmark_dir = Path("benchmarks")
        self.benchmark_dir.mkdir(exist_ok=True)
        logger.info("✅ Benchmark initialized")
        
    def get_pregnancy_discrimination_questions(self):
        """Comprehensive set of pregnancy discrimination legal drafting questions"""
        return [
            {
                "category": "Legal Memo",
                "question": "Draft a legal memo analyzing the basic rights of pregnant employees under the Pregnancy Discrimination Act. Include specific citations to relevant cases and statutes from the database.",
                "expected_aspects": ["PDA coverage", "equal treatment", "reasonable accommodations", "bluebook citations"]
            },
            {
                "category": "Accommodation Analysis",
                "question": "Analyze the legal requirements for reasonable accommodations for pregnant employees. Cite specific cases and regulations from the database that establish these requirements.",
                "expected_aspects": ["light duty", "breaks", "modified work", "ADA integration", "case citations"]
            },
            {
                "category": "FMLA Brief",
                "question": "Draft a brief section on FMLA rights for pregnant employees and new parents. Include specific citations to FMLA regulations and relevant case law from the database.",
                "expected_aspects": ["12 weeks", "job protection", "health benefits", "eligibility", "statute citations"]
            },
            {
                "category": "Lactation Rights Memo",
                "question": "Prepare a legal memo on lactation accommodation requirements in the workplace. Cite specific federal laws and regulations from the database.",
                "expected_aspects": ["break time", "private space", "pump access", "federal law", "regulation citations"]
            },
            {
                "category": "Discrimination Case Analysis",
                "question": "Analyze common examples of pregnancy discrimination in the workplace. Cite specific cases from the database that illustrate these patterns.",
                "expected_aspects": ["hiring bias", "promotion denial", "termination", "harassment", "case citations"]
            },
            {
                "category": "Remedies Brief",
                "question": "Draft a brief on legal remedies available for pregnancy discrimination victims. Include specific citations to cases and statutes establishing these remedies.",
                "expected_aspects": ["EEOC filing", "damages", "reinstatement", "attorney fees", "bluebook format"]
            },
            {
                "category": "NY State Law Analysis",
                "question": "Analyze how New York State law protects pregnant employees beyond federal law. Cite specific NY statutes and cases from the database.",
                "expected_aspects": ["NYSHRL", "additional protections", "state agencies", "local laws", "state citations"]
            },
            {
                "category": "Documentation Guide",
                "question": "Draft a legal guide on documentation pregnant employees should keep to protect their rights. Cite relevant cases and regulations from the database.",
                "expected_aspects": ["medical records", "communications", "performance reviews", "timeline", "legal citations"]
            }
        ]
    
    def get_system_prompt(self):
        """Legal AI system prompt for associate attorney role with database reliance"""
        return """You are an associate attorney specializing in pregnancy discrimination and employment law. 

CRITICAL REQUIREMENTS:
1. You must rely EXCLUSIVELY on the local database of cases, statutes, and legal documents
2. You must provide Bluebook-formatted citations to specific documents in the database
3. You must NOT hallucinate or reference documents not in the database
4. You must act as a legal professional drafting memos, briefs, and legal advice
5. You must be 100% confidential and accurate

CITATION REQUIREMENTS:
- Use Bluebook format for all citations
- Cite specific cases, statutes, and regulations from the database
- Include pinpoint citations when referencing specific sections
- Format: Case names in italics, statute citations with proper abbreviations

RESPONSE FORMAT:
- Professional legal writing style
- Clear legal analysis
- Specific citations to database documents
- Practical legal advice
- Zero hallucination - only cite what exists in the database

Focus on the Pregnancy Discrimination Act, FMLA, ADA, and relevant state laws as documented in your local legal database."""
    
    def benchmark_single_question(self, question_data, temperature=0.3, timeout_seconds=180):
        """Benchmark a single question with timing and quality metrics"""
        logger.info(f"🧪 Testing: {question_data['category']}")
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
            
            # Calculate response metrics
            word_count = len(response.split())
            char_count = len(response)
            
            # Check for expected aspects (basic content validation)
            expected_aspects = question_data.get("expected_aspects", [])
            aspect_coverage = sum(1 for aspect in expected_aspects 
                                if aspect.lower() in response.lower()) / len(expected_aspects) if expected_aspects else 0
            
            # Count citations (Bluebook format indicators)
            citation_indicators = ["v.", "U.S.", "F.2d", "F.3d", "F.Supp.", "F.Supp.2d", "S.Ct.", "L.Ed.", "42 U.S.C.", "29 U.S.C.", "29 C.F.R.", "42 C.F.R."]
            citation_count = sum(1 for indicator in citation_indicators if indicator in response)
            
            # Check for legal document references
            legal_terms = ["case", "statute", "regulation", "holding", "court", "plaintiff", "defendant", "jurisdiction"]
            legal_analysis_score = sum(1 for term in legal_terms if term.lower() in response.lower()) / len(legal_terms)
            
            result = {
                "timestamp": datetime.now().isoformat(),
                "category": question_data["category"],
                "question": question_data["question"],
                "response": response,
                "response_time_seconds": response_time,
                "word_count": word_count,
                "char_count": char_count,
                "aspect_coverage": aspect_coverage,
                "citation_count": citation_count,
                "legal_analysis_score": legal_analysis_score,
                "temperature": temperature,
                "model": "qwen2.5:14b"
            }
            
            logger.info(f"✅ {question_data['category']}: {response_time:.2f}s, {word_count} words, {aspect_coverage:.2f} coverage, {citation_count} citations, {legal_analysis_score:.2f} legal score")
            
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
            logger.error(f"❌ Error benchmarking question: {e}")
            return {
                "timestamp": datetime.now().isoformat(),
                "category": question_data["category"],
                "question": question_data["question"],
                "error": str(e),
                "temperature": temperature,
                "model": "qwen2.5:14b",
                "status": "error"
            }
    
    def run_full_benchmark(self, temperatures=[0.3, 0.7, 1.0]):
        """Run full benchmark across multiple temperatures"""
        logger.info("🚀 Starting Qwen pregnancy discrimination benchmark...")
        
        questions = self.get_pregnancy_discrimination_questions()
        
        for temp in temperatures:
            logger.info(f"🌡️ Testing temperature {temp}...")
            
            for i, question in enumerate(questions, 1):
                logger.info(f"📋 Processing question {i}/{len(questions)}: {question['category']}")
                result = self.benchmark_single_question(question, temperature=temp, timeout_seconds=180)
                self.results.append(result)
                
                # Small delay between requests
                time.sleep(2)
        
        # Calculate summary statistics
        self.calculate_summary_stats()
        
        # Save results
        self.save_results()
        
        logger.info("Benchmark completed!")
    
    def calculate_summary_stats(self):
        """Calculate summary statistics from benchmark results"""
        successful_results = [r for r in self.results if "error" not in r]
        
        if not successful_results:
            logger.warning("No successful benchmark results to analyze")
            return
        
        # Group by temperature
        temp_groups = {}
        for result in successful_results:
            temp = result["temperature"]
            if temp not in temp_groups:
                temp_groups[temp] = []
            temp_groups[temp].append(result)
        
        # Calculate stats per temperature
        self.summary_stats = {}
        for temp, results in temp_groups.items():
            response_times = [r["response_time_seconds"] for r in results]
            word_counts = [r["word_count"] for r in results]
            aspect_coverages = [r["aspect_coverage"] for r in results]
            citation_counts = [r["citation_count"] for r in results]
            legal_scores = [r["legal_analysis_score"] for r in results]
            
            self.summary_stats[temp] = {
                "avg_response_time": sum(response_times) / len(response_times),
                "avg_word_count": sum(word_counts) / len(word_counts),
                "avg_aspect_coverage": sum(aspect_coverages) / len(aspect_coverages),
                "avg_citation_count": sum(citation_counts) / len(citation_counts),
                "avg_legal_analysis_score": sum(legal_scores) / len(legal_scores),
                "total_questions": len(results),
                "min_response_time": min(response_times),
                "max_response_time": max(response_times)
            }
    
    def save_results(self):
        """Save benchmark results to file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"qwen_pregnancy_benchmark_{timestamp}.json"
        filepath = self.benchmark_dir / filename
        
        output_data = {
            "benchmark_info": {
                "model": "qwen2.5:14b",
                "timestamp": datetime.now().isoformat(),
                "total_questions": len(self.results),
                "summary_stats": getattr(self, 'summary_stats', {})
            },
            "results": self.results
        }
        
        with open(filepath, 'w') as f:
            json.dump(output_data, f, indent=2)
        
        logger.info(f"Results saved to {filepath}")
        
        # Also save a summary report
        self.save_summary_report(timestamp)
    
    def save_summary_report(self, timestamp):
        """Save a human-readable summary report"""
        filename = f"qwen_pregnancy_benchmark_summary_{timestamp}.md"
        filepath = self.benchmark_dir / filename
        
        with open(filepath, 'w') as f:
            f.write("# Qwen Pregnancy Discrimination Benchmark Results\n\n")
            f.write(f"**Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"**Model**: qwen2.5:14b\n")
            f.write(f"**Total Questions**: {len(self.results)}\n\n")
            
            if hasattr(self, 'summary_stats'):
                f.write("## Summary Statistics\n\n")
                for temp, stats in self.summary_stats.items():
                    f.write(f"### Temperature {temp}\n")
                    f.write(f"- Average Response Time: {stats['avg_response_time']:.2f} seconds\n")
                    f.write(f"- Average Word Count: {stats['avg_word_count']:.0f} words\n")
                    f.write(f"- Average Aspect Coverage: {stats['avg_aspect_coverage']:.2f}\n")
                    f.write(f"- Questions Tested: {stats['total_questions']}\n\n")
            
            f.write("## Detailed Results\n\n")
            for i, result in enumerate(self.results, 1):
                f.write(f"### {i}. {result['category']}\n")
                f.write(f"**Question**: {result['question']}\n")
                if "error" not in result:
                    f.write(f"**Response Time**: {result['response_time_seconds']:.2f}s\n")
                    f.write(f"**Word Count**: {result['word_count']}\n")
                    f.write(f"**Aspect Coverage**: {result['aspect_coverage']:.2f}\n")
                    f.write(f"**Response**: {result['response'][:200]}...\n\n")
                else:
                    f.write(f"**Error**: {result['error']}\n\n")
        
        logger.info(f"Summary report saved to {filepath}")

def main():
    """Run the benchmark"""
    try:
        benchmark = PregnancyDiscriminationBenchmark()
        benchmark.run_full_benchmark()
    except Exception as e:
        logger.error(f"❌ Fatal error in main: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 