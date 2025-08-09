#!/usr/bin/env python3
"""
Enhanced Benchmarking System - Updated for Speed & Modularity
Addresses GPT-OSS planning issues and implements config-driven approach
"""
import re
import json
import torch
import numpy as np
import logging
from typing import Dict, List, Tuple, Any
from dataclasses import dataclass
from pathlib import Path

# Ensure src directory exists
Path(__file__).parent.mkdir(parents=True, exist_ok=True)

from config import Config

# Setup logging
logger = logging.getLogger(__name__)

@dataclass
class BenchmarkMetrics:
    """Updated metrics for legal memo evaluation"""
    response_time: float
    word_count: int
    citation_count: int
    aspect_coverage: float
    legal_analysis_score: float
    response_completeness: float  # Word count proxy: <300=5, 300-800=10, >800=7
    alignment_to_question: float  # Key terms match percentage
    zero_hallucination_compliance: float  # Citations and fallbacks
    accuracy: float  # Rule-based scoring
    citations: float  # Citation quality
    clarity: float  # Response clarity
    explaining: float  # Explanation quality
    comprehensiveness: float  # Coverage completeness

class EnhancedPromptEngineer:
    """Model-specific prompt engineering with uniform base prompt"""
    
    @staticmethod
    def get_enhanced_prompt(model: str, temperature: float, context: str) -> str:
        """Generate enhanced prompt with truncation and model tweaks"""
        
        # Use uniform base prompt from config
        base_prompt = Config.SYSTEM_PROMPT
        
        # Add general model tweaks (no temp-specific)
        if model == "gpt-oss:20b-q6":
            base_prompt += "\n\nCRITICAL: Skip internal thoughts—avoid phrases like 'We need to', 'Let me craft', or 'I'll produce'. Output only the complete final memo."
        elif model == "qwen2.5:14b":
            base_prompt += "\n\nOUTPUT FORMAT: Provide complete memo with proper legal structure and citations."
        elif model == "llama3.1:8b":
            base_prompt += "\n\nCOMPLETENESS REQUIREMENT: Ensure the memo is complete and professional in format."
        
        # Intelligent context truncation (2000 token limit)
        truncated_context = EnhancedPromptEngineer._truncate_context(context, Config.PROMPT_MAX_TOKENS)
        
        logger.info(f"Generated enhanced prompt for {model} (temp: {temperature}), context length: {len(truncated_context)} chars")
        
        return f"{base_prompt}\n\nDB Context:\n{truncated_context}"
    
    @staticmethod
    def _truncate_context(context: str, max_tokens: int) -> str:
        """Intelligently truncate context to stay within token limit"""
        
        # Rough token estimation (1 token ≈ 4 characters)
        estimated_tokens = len(context) // 4
        
        if estimated_tokens <= max_tokens:
            return context
        
        logger.info(f"Truncating context from {estimated_tokens} to {max_tokens} tokens")
        
        # Truncate intelligently by keeping most relevant parts
        lines = context.split('\n')
        truncated_lines = []
        current_tokens = 0
        
        # Priority keywords to preserve
        priority_keywords = ['pregnancy discrimination', 'PDA', 'FMLA', 'Title VII', '42 U.S.C.', '29 U.S.C.']
        
        # First pass: keep lines with priority keywords
        for line in lines:
            line_tokens = len(line) // 4
            if any(keyword.lower() in line.lower() for keyword in priority_keywords):
                if current_tokens + line_tokens <= max_tokens:
                    truncated_lines.append(line)
                    current_tokens += line_tokens
        
        # Second pass: add remaining lines if space allows
        for line in lines:
            if line not in truncated_lines:
                line_tokens = len(line) // 4
                if current_tokens + line_tokens <= max_tokens:
                    truncated_lines.append(line)
                    current_tokens += line_tokens
                else:
                    break
        
        return '\n'.join(truncated_lines)

class ResponsePostProcessor:
    """Enhanced post-processing with retry logic and planning detection"""
    
    def __init__(self):
        # Enhanced planning detection patterns
        self.planning_patterns = [
            r'<\|start\|>.*?<\|message\|>',  # Ollama tags
            r'<\|assistant\|>.*?<\|message\|>',
            r'<\|system\|>.*?<\|message\|>',
            r'Let me (craft|produce|create|analyze|think).*?(?=\n\n|\n[A-Z])',
            r'I\'ll (craft|produce|create|analyze).*?(?=\n\n|\n[A-Z])',
            r'Here\'s my (analysis|response|memo).*?(?=\n\n|\n[A-Z])',
            r'First, let me.*?(?=\n\n|\n[A-Z])',
            r'To answer this.*?(?=\n\n|\n[A-Z])',
            r'I\'m going to.*?(?=\n\n|\n[A-Z])',
            r'Let me create.*?(?=\n\n|\n[A-Z])',
            r'We need to.*?(?=\n\n|\n[A-Z])',
            r'Let me start.*?(?=\n\n|\n[A-Z])',
            r'I\'ll begin.*?(?=\n\n|\n[A-Z])',
            r'Let me write.*?(?=\n\n|\n[A-Z])',
            r'I\'ll draft.*?(?=\n\n|\n[A-Z])',
            r'Let me analyze.*?(?=\n\n|\n[A-Z])',
            r'I\'m going to.*?(?=\n\n|\n[A-Z])'
        ]
        
        # Unicode and special character patterns
        self.unicode_patterns = [
            r'<\|end\|>',
            r'<\|im_end\|>',
            r'<\|im_start\|>',
            r'<\|endoftext\|>',
            r'<\|eot\|>',
            r'<\|eos\|>'
        ]
    
    def extract_final_content(self, response: str) -> str:
        """Extract final memo content, removing planning and unicode artifacts"""
        
        if not response:
            return ""
        
        # Remove unicode artifacts first
        cleaned_response = response
        for pattern in self.unicode_patterns:
            cleaned_response = re.sub(pattern, '', cleaned_response, flags=re.IGNORECASE)
        
        # Remove non-ASCII characters that might cause issues
        cleaned_response = re.sub(r'[^\x00-\x7F]+', '', cleaned_response)
        
        # Remove planning patterns
        for pattern in self.planning_patterns:
            cleaned_response = re.sub(pattern, '', cleaned_response, flags=re.IGNORECASE | re.DOTALL)
        
        # Find memo content
        memo_indicators = [
            r'To:.*?From:.*?Date:.*?Subject:',
            r'\*\*To:\*\*.*?\*\*From:\*\*.*?\*\*Date:\*\*.*?\*\*Subject:\*\*',
            r'Memo\s*To:',
            r'\*\*Memo\*\*\s*To:',
        ]
        
        memo_start = -1
        for indicator in memo_indicators:
            match = re.search(indicator, cleaned_response, re.IGNORECASE | re.DOTALL)
            if match:
                memo_start = match.start()
                break
        
        # If no memo structure, look for legal content
        if memo_start == -1:
            legal_indicators = [
                r'Pregnancy Discrimination Act',
                r'Title VII',
                r'FMLA',
                r'legal authority',
                r'citation',
                r'statute',
                r'regulation'
            ]
            
            for indicator in legal_indicators:
                match = re.search(indicator, cleaned_response, re.IGNORECASE)
                if match:
                    memo_start = max(0, match.start() - 100)
                    break
        
        # Extract content
        if memo_start >= 0:
            cleaned_response = cleaned_response[memo_start:]
        
        # Clean up formatting
        cleaned_response = re.sub(r'\n{3,}', '\n\n', cleaned_response)
        cleaned_response = re.sub(r'^\s+', '', cleaned_response)
        cleaned_response = cleaned_response.strip()
        
        return cleaned_response
    
    def detect_planning_content(self, response: str) -> bool:
        """Detect if response contains planning content (no penalty scoring)"""
        
        if not response:
            return False
        
        response_lower = response.lower()
        
        # Check for planning keywords
        planning_keywords = [
            'planning', 'craft', 'produce', 'let me', 'i\'ll', 'here\'s my',
            'first, let me', 'to answer this', 'let me think', 'i will',
            'let me create', 'i\'m going to', 'let me analyze', 'we need to',
            'let me start', 'i\'ll begin', 'let me write', 'i\'ll draft'
        ]
        
        for keyword in planning_keywords:
            if keyword in response_lower:
                logger.info(f"Planning keyword detected: {keyword}")
                return True
        
        # Check for Ollama tags
        ollama_patterns = [
            r'<\|start\|>.*?<\|message\|>',
            r'<\|assistant\|>.*?<\|message\|>',
            r'<\|system\|>.*?<\|message\|>'
        ]
        
        for pattern in ollama_patterns:
            if re.search(pattern, response, re.DOTALL):
                logger.info(f"Ollama tag detected: {pattern}")
                return True
        
        return False
    
    def process_with_retries(self, response: str, max_retries: int = 2) -> str:
        """Process response with retry logic if planning detected"""
        
        final_content = self.extract_final_content(response)
        attempts = 0
        
        # Check if planning was detected
        while self.detect_planning_content(response) and attempts < max_retries:
            attempts += 1
            logger.info(f"Planning detected, retry attempt {attempts}/{max_retries}")
            
            # Retry processing with more aggressive cleaning
            final_content = self.extract_final_content(final_content)
            
            # Check if planning is still detected in the cleaned content
            if not self.detect_planning_content(final_content):
                logger.info(f"Planning successfully removed after {attempts} attempts")
                break
        
        if attempts > 0:
            logger.info(f"Final processing completed after {attempts} retry attempts")
        
        return final_content

class EnhancedEvaluator:
    """Updated evaluator without structure penalties"""
    
    def __init__(self):
        # Set fixed seed for reproducibility
        torch.manual_seed(42)
        np.random.seed(42)
        
        # Updated weights (no structure penalties)
        self.weights = {
            'completeness': 0.25,
            'alignment': 0.15,
            'zero_hallucination': 0.20,
            'accuracy': 0.15,
            'citations': 0.10,
            'clarity': 0.10,
            'aspect_coverage': 0.05
        }
    
    def evaluate_response_completeness(self, response: str) -> float:
        """Evaluate completeness based on word count"""
        
        word_count = len(response.split())
        
        if word_count < 300:
            return 5.0
        elif 300 <= word_count <= 800:
            return 10.0
        else:  # > 800
            return 7.0
    
    def evaluate_alignment_to_question(self, response: str, question: str, category: str) -> float:
        """Evaluate alignment based on key terms match percentage"""
        
        if not response or not question:
            return 0.0
        
        # Define expected content by category
        expected_content = {
            'pda memo': ['pregnancy discrimination act', 'pda', 'title vii', 'equal treatment'],
            'fmla accommodations': ['fmla', 'family medical leave', 'reasonable accommodation', 'light duty'],
            'ny law': ['new york', 'ny', 'state law', 'human rights', 'enhanced rights'],
            'remedies': ['damages', 'injunctive relief', 'attorney fees', 'back pay', 'compensatory']
        }
        
        expected_terms = expected_content.get(category.lower(), [])
        if not expected_terms:
            return 0.0
        
        response_lower = response.lower()
        matched_terms = sum(1 for term in expected_terms if term in response_lower)
        
        return (matched_terms / len(expected_terms)) * 10.0
    
    def evaluate_zero_hallucination_compliance(self, response: str, context: str) -> float:
        """Evaluate zero-hallucination compliance"""
        
        if not response:
            return 0.0
        
        score = 0.0
        
        # Check for citations
        citation_patterns = [
            r'\d+ U\.S\.C\. \§ \d+',
            r'\(\d{4}\)',
            r'v\. [A-Z]',
            r', \d+ F\.',
            r'NY Slip Op'
        ]
        
        citations_found = []
        for pattern in citation_patterns:
            citations_found.extend(re.findall(pattern, response))
        
        if citations_found:
            score += 5.0
        
        # Check for fallback handling
        if 'no relevant db info' in response.lower():
            score += 3.0
        
        # Check for database references
        if 'database' in response.lower() or 'db context' in response.lower():
            score += 2.0
        
        return min(10.0, score)
    
    def evaluate_accuracy(self, response: str, question: str) -> float:
        """Rule-based accuracy evaluation"""
        
        if not response:
            return 0.0
        
        score = 0.0
        response_lower = response.lower()
        
        # Check for legal accuracy indicators
        legal_terms = [
            'pregnancy discrimination', 'title vii', 'fmla', 'ada',
            'reasonable accommodation', 'statute', 'regulation', 'case law'
        ]
        
        legal_term_count = sum(1 for term in legal_terms if term in response_lower)
        score += min(5.0, legal_term_count)
        
        # Check for proper legal analysis
        if 'legal authority' in response_lower or 'citation' in response_lower:
            score += 3.0
        
        # Check for professional tone
        if 'memo' in response_lower or 'analysis' in response_lower:
            score += 2.0
        
        return min(10.0, score)
    
    def evaluate_citations(self, response: str) -> float:
        """Evaluate citation quality"""
        
        citation_count = len(re.findall(r'\d+ U\.S\.C\.|\(\d{4}\)|v\.|, \d+ F\.', response))
        
        if citation_count >= 3:
            return 10.0
        elif citation_count >= 2:
            return 7.0
        elif citation_count >= 1:
            return 5.0
        else:
            return 0.0
    
    def evaluate_clarity(self, response: str) -> float:
        """Evaluate response clarity"""
        
        if not response:
            return 0.0
        
        score = 0.0
        
        # Check for clear structure
        if 'introduction' in response.lower() or 'analysis' in response.lower() or 'conclusion' in response.lower():
            score += 4.0
        
        # Check for good paragraph structure
        if response.count('\n\n') >= 3:
            score += 3.0
        
        # Check for professional language
        professional_indicators = ['legal', 'authority', 'statute', 'regulation']
        professional_count = sum(1 for indicator in professional_indicators if indicator in response.lower())
        score += min(3.0, professional_count)
        
        return min(10.0, score)
    
    def evaluate_explaining(self, response: str) -> float:
        """Evaluate explanation quality"""
        
        if not response:
            return 0.0
        
        score = 0.0
        
        # Check for explanatory language
        explaining_indicators = ['because', 'therefore', 'thus', 'as a result', 'consequently']
        explaining_count = sum(1 for indicator in explaining_indicators if indicator in response.lower())
        score += min(5.0, explaining_count)
        
        # Check for detailed analysis
        if len(response) > 400:
            score += 3.0
        
        # Check for legal reasoning
        if 'legal authority' in response.lower() or 'citation' in response.lower():
            score += 2.0
        
        return min(10.0, score)
    
    def evaluate_comprehensiveness(self, response: str, expected_aspects: List[str]) -> float:
        """Evaluate comprehensiveness based on aspect coverage"""
        
        if not response or not expected_aspects:
            return 0.0
        
        response_lower = response.lower()
        covered_aspects = sum(1 for aspect in expected_aspects if aspect.lower() in response_lower)
        
        return (covered_aspects / len(expected_aspects)) * 10.0 if expected_aspects else 0.0
    
    def calculate_comprehensive_score(self, metrics: BenchmarkMetrics) -> float:
        """Calculate comprehensive score with updated weights"""
        
        score = (
            metrics.response_completeness * self.weights['completeness'] +
            metrics.alignment_to_question * self.weights['alignment'] +
            metrics.zero_hallucination_compliance * self.weights['zero_hallucination'] +
            metrics.accuracy * self.weights['accuracy'] +
            metrics.citations * self.weights['citations'] +
            metrics.clarity * self.weights['clarity'] +
            metrics.aspect_coverage * self.weights['aspect_coverage']
        )
        
        return max(0.0, min(10.0, score))
    
    def evaluate_benchmark_result(self, response: str, question: str, category: str, 
                                context: str, expected_aspects: List[str], 
                                response_time: float) -> Dict[str, Any]:
        """Complete evaluation of a benchmark result"""
        
        # Calculate all metrics
        completeness = self.evaluate_response_completeness(response)
        alignment = self.evaluate_alignment_to_question(response, question, category)
        zero_hallucination = self.evaluate_zero_hallucination_compliance(response, context)
        accuracy = self.evaluate_accuracy(response, question)
        citations = self.evaluate_citations(response)
        clarity = self.evaluate_clarity(response)
        explaining = self.evaluate_explaining(response)
        comprehensiveness = self.evaluate_comprehensiveness(response, expected_aspects)
        
        # Create metrics object
        metrics = BenchmarkMetrics(
            response_time=response_time,
            word_count=len(response.split()),
            citation_count=len(re.findall(r'\d+ U\.S\.C\.|\(\d{4}\)|v\.|, \d+ F\.', response)),
            aspect_coverage=comprehensiveness / 10.0,  # Normalize to 0-1
            legal_analysis_score=0.0,  # Legacy metric
            response_completeness=completeness,
            alignment_to_question=alignment,
            zero_hallucination_compliance=zero_hallucination,
            accuracy=accuracy,
            citations=citations,
            clarity=clarity,
            explaining=explaining,
            comprehensiveness=comprehensiveness
        )
        
        # Calculate comprehensive score
        comprehensive_score = self.calculate_comprehensive_score(metrics)
        
        return {
            'metrics': metrics.__dict__,
            'comprehensive_score': comprehensive_score,
            'evaluation_breakdown': {
                'completeness': completeness,
                'alignment': alignment,
                'zero_hallucination': zero_hallucination,
                'accuracy': accuracy,
                'citations': citations,
                'clarity': clarity,
                'explaining': explaining,
                'comprehensiveness': comprehensiveness
            },
            'enhanced_evaluation': True
        }

class BenchmarkEnhancements:
    """Main class for implementing enhanced benchmarking"""
    
    def __init__(self):
        self.prompt_engineer = EnhancedPromptEngineer()
        self.post_processor = ResponsePostProcessor()
        self.evaluator = EnhancedEvaluator()
    
    def process_benchmark_response(self, response: str, question: str, category: str, 
                                 context: str, response_time: float) -> Dict[str, Any]:
        """Process a benchmark response with enhanced evaluation"""
        
        # Post-process with retries
        final_content = self.post_processor.process_with_retries(response, max_retries=Config.RETRY_ATTEMPTS)
        
        # Detect planning content (no penalty)
        planning_detected = self.post_processor.detect_planning_content(response)
        
        # Get expected aspects for the category
        expected_aspects = self._get_expected_aspects(category)
        
        # Evaluate with updated metrics
        evaluation_result = self.evaluator.evaluate_benchmark_result(
            final_content, question, category, context, expected_aspects, response_time
        )
        
        return {
            'original_response': response,
            'final_content': final_content,
            'planning_detected': planning_detected,
            'processing_notes': {
                'content_extracted': len(final_content) != len(response),
                'planning_detected': planning_detected,
                'retries_applied': planning_detected
            },
            **evaluation_result
        }
    
    def get_enhanced_prompt(self, model: str, temperature: float, context: str) -> str:
        """Get enhanced prompt with truncation"""
        return self.prompt_engineer.get_enhanced_prompt(model, temperature, context)
    
    def _get_expected_aspects(self, category: str) -> List[str]:
        """Get expected aspects for a given category"""
        aspect_mapping = {
            'pda memo': ['pda coverage', 'equal treatment', 'reasonable accommodations', 'bluebook citations'],
            'fmla accommodations': ['fmla rights', 'reasonable accommodation', 'light duty', 'job protection'],
            'ny law': ['ny protections', 'state statutes', 'local laws', 'enhanced rights'],
            'remedies': ['damages', 'injunctive relief', 'attorney fees', 'back pay']
        }
        return aspect_mapping.get(category.lower(), [])
