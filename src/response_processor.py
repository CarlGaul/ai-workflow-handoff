#!/usr/bin/env python3
"""
Response Post-Processor for Legal AI Benchmarking
Handles extraction of final content and detection of planning processes
"""
import re
import logging
from typing import Tuple, List, Dict, Any

# Setup logging
logger = logging.getLogger(__name__)

class ResponsePostProcessor:
    """Post-processes AI responses to extract final content and detect planning"""
    
    def __init__(self):
        # Enhanced planning detection patterns
        self.planning_patterns = [
            r'<\|start\|>.*?<\|message\|>',  # Ollama tags
            r'<\|assistant\|>.*?<\|message\|>',
            r'<\|system\|>.*?<\|message\|>',
            r'Let me (craft|produce|create|analyze|think).*?(?=\n\n|\n[A-Z])',
            r'I\'ll (craft|produce|create|analyze).*?(?=\n\n|\n[A-Z])',
            r'Here\'s my (analysis|response|memo).*?(?=\n\n|\n[A-Z])',
            r'Let me think.*?(?=\n\n|\n[A-Z])',
            r'First, let me.*?(?=\n\n|\n[A-Z])',
            r'To answer this.*?(?=\n\n|\n[A-Z])',
            r'I\'m going to.*?(?=\n\n|\n[A-Z])',
            r'Let me create.*?(?=\n\n|\n[A-Z])',
            r'Let me analyze.*?(?=\n\n|\n[A-Z])',
            r'Let me start.*?(?=\n\n|\n[A-Z])',
            r'I\'ll begin.*?(?=\n\n|\n[A-Z])',
            r'Let me write.*?(?=\n\n|\n[A-Z])',
            r'I\'ll draft.*?(?=\n\n|\n[A-Z])',
            r'We need to.*?(?=\n\n|\n[A-Z])',
            r'Let me produce.*?(?=\n\n|\n[A-Z])',
            r'I will create.*?(?=\n\n|\n[A-Z])',
            r'Let me develop.*?(?=\n\n|\n[A-Z])'
        ]
        
        # Memo structure indicators
        self.memo_indicators = [
            r'To:.*?From:.*?Date:.*?Subject:',
            r'\*\*To:\*\*.*?\*\*From:\*\*.*?\*\*Date:\*\*.*?\*\*Subject:\*\*',
            r'Memo\s*To:',
            r'\*\*Memo\*\*\s*To:',
        ]
        
        # Planning keywords for detection
        self.planning_keywords = [
            'planning', 'craft', 'produce', 'let me', 'i\'ll', 'here\'s my',
            'first, let me', 'to answer this', 'let me think', 'i will',
            'let me create', 'i\'m going to', 'let me analyze', 'i\'m going to',
            'let me start', 'i\'ll begin', 'let me write', 'i\'ll draft',
            'we need to', 'let me produce', 'i will create', 'let me develop'
        ]
    
    def extract_final_content(self, response: str) -> str:
        """Extract final memo content, removing planning and internal thoughts"""
        
        if not response:
            return ""
        
        # Remove unicode artifacts first
        cleaned_response = response
        
        # Remove unicode and special characters
        unicode_patterns = [
            r'<\|end\|>',
            r'<\|im_end\|>',
            r'<\|im_start\|>',
            r'<\|endoftext\|>',
            r'<\|eot\|>',
            r'<\|eos\|>'
        ]
        
        for pattern in unicode_patterns:
            cleaned_response = re.sub(pattern, '', cleaned_response, flags=re.IGNORECASE)
        
        # Remove non-ASCII characters that might cause issues
        cleaned_response = re.sub(r'[^\x00-\x7F]+', '', cleaned_response)
        
        # Remove common planning indicators
        for pattern in self.planning_patterns:
            cleaned_response = re.sub(pattern, '', cleaned_response, flags=re.IGNORECASE | re.DOTALL)
        
        # Find the actual memo content
        memo_start = -1
        for indicator in self.memo_indicators:
            match = re.search(indicator, cleaned_response, re.IGNORECASE | re.DOTALL)
            if match:
                memo_start = match.start()
                break
        
        # If no memo structure found, try to find professional content
        if memo_start == -1:
            # Look for legal content indicators
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
                    memo_start = max(0, match.start() - 100)  # Start 100 chars before
                    break
        
        # Extract content from memo start
        if memo_start >= 0:
            cleaned_response = cleaned_response[memo_start:]
        
        # Clean up any remaining artifacts
        cleaned_response = re.sub(r'\n{3,}', '\n\n', cleaned_response)  # Remove excessive newlines
        cleaned_response = re.sub(r'^\s+', '', cleaned_response)  # Remove leading whitespace
        cleaned_response = cleaned_response.strip()
        
        return cleaned_response
    
    def detect_planning_content(self, response: str) -> bool:
        """Detect planning content and return detection status (no penalty scoring)"""
        
        if not response:
            return False
        
        response_lower = response.lower()
        
        # Check for planning keywords
        for keyword in self.planning_keywords:
            if keyword in response_lower:
                logger.info(f"Planning keyword detected: {keyword}")
                return True
        
        # Check for Ollama tags
        ollama_tag_patterns = [
            r'<\|start\|>.*?<\|message\|>',
            r'<\|assistant\|>.*?<\|message\|>',
            r'<\|system\|>.*?<\|message\|>'
        ]
        
        for pattern in ollama_tag_patterns:
            if re.search(pattern, response, re.DOTALL):
                logger.info(f"Ollama tag detected: {pattern}")
                return True
        
        # Check for meta-commentary
        meta_patterns = [
            r'let me (craft|produce|create|analyze)',
            r'i\'ll (craft|produce|create|analyze)',
            r'here\'s my (analysis|response|memo)',
            r'let me think',
            r'first, let me',
            r'to answer this',
            r'we need to',
            r'i\'m going to'
        ]
        
        for pattern in meta_patterns:
            if re.search(pattern, response_lower):
                logger.info(f"Meta-commentary detected: {pattern}")
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
    
    def validate_memo_structure(self, response: str) -> Dict[str, Any]:
        """Validate if response has proper memo structure"""
        
        validation = {
            'has_memo_structure': False,
            'has_to_from_subject': False,
            'has_sections': False,
            'has_citations': False,
            'structure_score': 0.0
        }
        
        # Check for memo header
        header_patterns = [
            r'To:.*?From:.*?Subject:',
            r'\*\*To:\*\*.*?\*\*From:\*\*.*?\*\*Subject:\*\*',
            r'Memo\s*To:',
            r'\*\*Memo\*\*\s*To:'
        ]
        
        for pattern in header_patterns:
            if re.search(pattern, response, re.IGNORECASE | re.DOTALL):
                validation['has_to_from_subject'] = True
                validation['has_memo_structure'] = True
                break
        
        # Check for sections
        sections = ['Introduction', 'Analysis', 'Conclusion']
        found_sections = 0
        for section in sections:
            if section in response:
                found_sections += 1
        
        validation['has_sections'] = found_sections >= 2
        if found_sections >= 2:
            validation['structure_score'] += 0.5
        
        # Check for citations
        citation_patterns = [
            r'\d+ U\.S\.C\.',
            r'\(\d{4}\)',
            r'v\. [A-Z]',
            r', \d+ F\.',
            r'NY Slip Op'
        ]
        
        for pattern in citation_patterns:
            if re.search(pattern, response):
                validation['has_citations'] = True
                validation['structure_score'] += 0.3
                break
        
        # Add score for memo structure
        if validation['has_memo_structure']:
            validation['structure_score'] += 0.2
        
        validation['structure_score'] = min(1.0, validation['structure_score'])
        
        return validation
    
    def calculate_content_quality(self, response: str) -> Dict[str, float]:
        """Calculate content quality metrics"""
        
        quality_metrics = {
            'completeness': 0.0,
            'professionalism': 0.0,
            'legal_accuracy': 0.0,
            'citation_quality': 0.0
        }
        
        if not response:
            return quality_metrics
        
        # Completeness (based on length and structure)
        word_count = len(response.split())
        if word_count > 500:
            quality_metrics['completeness'] = 1.0
        elif word_count > 300:
            quality_metrics['completeness'] = 0.7
        elif word_count > 150:
            quality_metrics['completeness'] = 0.4
        else:
            quality_metrics['completeness'] = 0.1
        
        # Professionalism (based on structure and tone)
        structure_validation = self.validate_memo_structure(response)
        quality_metrics['professionalism'] = structure_validation['structure_score']
        
        # Legal accuracy (based on legal terms and citations)
        legal_terms = [
            'pregnancy discrimination', 'title vii', 'fmla', 'ada',
            'reasonable accommodation', 'statute', 'regulation', 'case law'
        ]
        
        legal_term_count = sum(1 for term in legal_terms if term in response.lower())
        quality_metrics['legal_accuracy'] = min(1.0, legal_term_count / 5.0)
        
        # Citation quality
        citation_count = len(re.findall(r'\d+ U\.S\.C\.|\(\d{4}\)|v\.|, \d+ F\.', response))
        quality_metrics['citation_quality'] = min(1.0, citation_count / 3.0)
        
        return quality_metrics
    
    def process_response(self, response: str, question: str, category: str) -> Dict[str, Any]:
        """Complete response processing pipeline"""
        
        # Extract final content
        final_content = self.extract_final_content(response)
        
        # Detect planning content
        planning_detected = self.detect_planning_content(response)
        
        # Validate structure
        structure_validation = self.validate_memo_structure(final_content)
        
        # Calculate quality metrics
        quality_metrics = self.calculate_content_quality(final_content)
        
        return {
            'original_response': response,
            'final_content': final_content,
            'planning_detected': planning_detected,
            'detected_phrases': [],  # No penalty scoring
            'structure_validation': structure_validation,
            'quality_metrics': quality_metrics,
            'content_extracted': len(final_content) != len(response),
            'word_count': len(final_content.split()),
            'processing_notes': {
                'content_extracted': len(final_content) != len(response),
                'planning_detected': planning_detected,
                'structure_validated': structure_validation['has_memo_structure']
            }
        }
