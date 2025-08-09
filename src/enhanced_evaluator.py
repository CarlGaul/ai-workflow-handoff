#!/usr/bin/env python3
"""
Enhanced Evaluator for Legal AI Benchmarking
Implements new evaluation metrics and scoring system
"""
import re
import torch
import numpy as np
import logging
from typing import Dict, List, Tuple, Any
from dataclasses import dataclass

# Setup logging
logger = logging.getLogger(__name__)

@dataclass
class EnhancedMetrics:
    """Enhanced metrics for legal memo evaluation"""
    response_time: float
    word_count: int
    citation_count: int
    aspect_coverage: float
    legal_analysis_score: float
    response_completeness: float  # New: 1-10 for full memo delivery
    alignment_to_question: float  # New: How well it matches the question focus
    zero_hallucination_compliance: float  # Enhanced scoring
    accuracy: float  # Rule-based scoring
    citations: float  # Citation quality
    clarity: float  # Response clarity
    explaining: float  # Explanation quality
    comprehensiveness: float  # Coverage completeness

class EnhancedEvaluator:
    """Enhanced evaluation with new metrics and reproducible scoring"""
    
    def __init__(self):
        # Set fixed seed for reproducibility
        torch.manual_seed(42)
        np.random.seed(42)
        
        # Define evaluation weights (no structure penalties)
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
        """Evaluate if response is a complete memo (1-10 scale)"""
        
        if not response:
            return 1.0
        
        score = 0.0
        
        # Check for memo structure (3 points)
        has_memo_structure = any([
            'To:' in response and 'From:' in response and 'Subject:' in response,
            '**To:**' in response and '**From:**' in response and '**Subject:**' in response,
            'Memo' in response[:100]
        ])
        
        if has_memo_structure:
            score += 3.0
        
        # Check for legal analysis components (3 points)
        has_analysis = any([
            'Analysis' in response,
            'Introduction' in response,
            'Conclusion' in response,
            'legal authority' in response.lower(),
            'citation' in response.lower()
        ])
        
        if has_analysis:
            score += 3.0
        
        # Check for citations (2 points)
        has_citations = bool(re.search(r'\d+ U\.S\.C\.|\(\d{4}\)|v\.|, \d+ F\.', response))
        if has_citations:
            score += 2.0
        
        # Check for substantial content (2 points)
        if len(response) > 500:
            score += 2.0
        elif len(response) > 300:
            score += 1.0
        
        return min(10.0, score)
    
    def evaluate_alignment_to_question(self, response: str, question: str, category: str) -> float:
        """Evaluate how well response aligns with the question focus (1-10 scale)"""
        
        if not response or not question:
            return 1.0
        
        # Extract key terms from question and category
        question_lower = question.lower()
        category_lower = category.lower()
        
        # Define expected content based on category
        expected_content = {
            'legal memo': ['pregnancy discrimination act', 'pda', 'title vii', 'equal treatment'],
            'accommodation analysis': ['reasonable accommodation', 'light duty', 'ada', 'modified work'],
            'fmla brief': ['fmla', 'family medical leave', '12 weeks', 'job protection'],
            'lactation rights memo': ['lactation', 'breastfeeding', 'pump', 'break time', 'private space'],
            'discrimination case analysis': ['discrimination', 'harassment', 'termination', 'case examples'],
            'remedies brief': ['damages', 'injunctive relief', 'attorney fees', 'back pay'],
            'ny state law analysis': ['new york', 'ny', 'state law', 'human rights', 'enhanced rights'],
            'documentation guide': ['documentation', 'evidence', 'timeline', 'practical advice'],
            'pda memo': ['pregnancy discrimination act', 'pda', 'title vii', 'equal treatment'],
            'fmla accommodations': ['fmla', 'family medical leave', 'reasonable accommodation', 'light duty'],
            'ny law': ['new york', 'ny', 'state law', 'human rights', 'enhanced rights'],
            'remedies': ['damages', 'injunctive relief', 'attorney fees', 'back pay']
        }
        
        # Check for expected content
        score = 0.0
        expected_terms = expected_content.get(category_lower, [])
        
        for term in expected_terms:
            if term in response.lower():
                score += 1.0
        
        # Check for federal vs local focus
        if 'federal' in question_lower and 'federal' in response.lower():
            score += 1.0
        if 'new york' in question_lower and 'new york' in response.lower():
            score += 1.0
        
        # Check for specific legal concepts mentioned in question
        question_terms = question_lower.split()
        legal_terms = ['pregnancy', 'discrimination', 'accommodation', 'fmla', 'lactation', 'remedies']
        for term in legal_terms:
            if term in question_terms and term in response.lower():
                score += 0.5
        
        # Normalize to 1-10 scale
        max_possible = len(expected_terms) + 2  # +2 for federal/local alignment
        normalized_score = min(10.0, (score / max_possible) * 10.0)
        
        return normalized_score
    
    def evaluate_zero_hallucination_compliance(self, response: str, context: str) -> float:
        """Enhanced zero-hallucination compliance scoring"""
        
        if not response:
            return 1.0
        
        score = 0.0
        
        # Extract citations from response
        citation_patterns = [
            r'\d+ U\.S\.C\. \§ \d+',  # Federal statutes
            r'\(\d{4}\)',  # Year citations
            r'v\. [A-Z]',  # Case names
            r', \d+ F\.',  # Federal cases
            r'NY Slip Op',  # NY cases
        ]
        
        citations_found = []
        for pattern in citation_patterns:
            citations_found.extend(re.findall(pattern, response))
        
        # Check for "No relevant DB info" when appropriate
        has_fallback = 'no relevant db info' in response.lower()
        
        # Calculate compliance score
        if citations_found:
            score += 4.0  # Citations present
        if has_fallback:
            score += 2.0  # Proper fallback handling
        if 'database' in response.lower() or 'db context' in response.lower():
            score += 2.0  # References database
        if len(response) > 200:  # Substantial response
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
    
    def calculate_comprehensive_score(self, metrics: EnhancedMetrics) -> float:
        """Calculate comprehensive score from all metrics (no structure penalties)"""
        
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
        response_completeness = self.evaluate_response_completeness(response)
        alignment_to_question = self.evaluate_alignment_to_question(response, question, category)
        zero_hallucination_compliance = self.evaluate_zero_hallucination_compliance(response, context)
        accuracy = self.evaluate_accuracy(response, question)
        citations = self.evaluate_citations(response)
        clarity = self.evaluate_clarity(response)
        explaining = self.evaluate_explaining(response)
        aspect_coverage = self.evaluate_comprehensiveness(response, expected_aspects)
        
        # Create metrics object
        metrics = EnhancedMetrics(
            response_time=response_time,
            word_count=len(response.split()),
            citation_count=len(re.findall(r'\d+ U\.S\.C\.|\(\d{4}\)|v\.|, \d+ F\.', response)),
            aspect_coverage=aspect_coverage / 10.0,  # Normalize to 0-1
            legal_analysis_score=0.0,  # Legacy metric
            response_completeness=response_completeness,
            alignment_to_question=alignment_to_question,
            zero_hallucination_compliance=zero_hallucination_compliance,
            accuracy=accuracy,
            citations=citations,
            clarity=clarity,
            explaining=explaining,
            comprehensiveness=aspect_coverage
        )
        
        # Calculate comprehensive score
        comprehensive_score = self.calculate_comprehensive_score(metrics)
        
        return {
            'metrics': metrics.__dict__,
            'comprehensive_score': comprehensive_score,
            'evaluation_breakdown': {
                'response_completeness': response_completeness,
                'alignment_to_question': alignment_to_question,
                'zero_hallucination_compliance': zero_hallucination_compliance,
                'accuracy': accuracy,
                'citations': citations,
                'clarity': clarity,
                'explaining': explaining,
                'comprehensiveness': aspect_coverage
            },
            'enhanced_evaluation': True
        }
    
    def generate_evaluation_summary(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate summary statistics for benchmark results"""
        
        if not results:
            return {}
        
        # Calculate averages
        avg_scores = {}
        for metric in ['response_completeness', 'alignment_to_question', 'zero_hallucination_compliance', 
                      'accuracy', 'citations', 'clarity', 'explaining', 'comprehensiveness', 'comprehensive_score']:
            values = [r.get('metrics', {}).get(metric, 0) for r in results]
            avg_scores[f'avg_{metric}'] = sum(values) / len(values) if values else 0
        
        # Planning detection statistics
        planning_detected = sum(1 for r in results if r.get('planning_detected', False))
        planning_rate = planning_detected / len(results) if results else 0
        
        # Model performance comparison
        model_performance = {}
        for result in results:
            model = result.get('model', 'unknown')
            if model not in model_performance:
                model_performance[model] = []
            model_performance[model].append(result.get('comprehensive_score', 0))
        
        # Calculate model averages
        for model, scores in model_performance.items():
            model_performance[model] = sum(scores) / len(scores) if scores else 0
        
        return {
            'total_results': len(results),
            'average_scores': avg_scores,
            'planning_detection_rate': planning_rate,
            'model_performance': model_performance,
            'enhanced_evaluation': True
        }
