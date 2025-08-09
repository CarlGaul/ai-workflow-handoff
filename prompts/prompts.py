#!/usr/bin/env python3
"""
Prompt Templates for Legal AI Benchmarking
Uniform templates with model-specific tweaks
"""
import sys
import os
from typing import Dict, List
from pathlib import Path

# Add src to path for config import
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from config import Config

class PromptTemplates:
    """Uniform prompt templates with model tweaks"""
    
    @staticmethod
    def get_base_prompt() -> str:
        """Get the base system prompt from config"""
        return Config.SYSTEM_PROMPT
    
    @staticmethod
    def get_model_tweak(model: str) -> str:
        """Get model-specific tweaks (no temperature-specific)"""
        tweaks = {
            "gpt-oss:20b-q6": "\n\nCRITICAL: Skip internal thoughts—avoid phrases like 'We need to', 'Let me craft', or 'I'll produce'. Output only the complete final memo.",
            "qwen2.5:14b": "\n\nOUTPUT FORMAT: Provide complete memo with proper legal structure and citations.",
            "llama3.1:8b": "\n\nCOMPLETENESS REQUIREMENT: Ensure the memo is complete and professional in format."
        }
        return tweaks.get(model, "")
    
    @staticmethod
    def truncate_context(context: str, max_tokens: int = 2000) -> str:
        """Intelligently truncate context to stay within token limit"""
        
        # Rough token estimation (1 token ≈ 4 characters)
        estimated_tokens = len(context) // 4
        
        if estimated_tokens <= max_tokens:
            return context
        
        # Priority keywords to preserve
        priority_keywords = [
            'pregnancy discrimination', 'PDA', 'FMLA', 'Title VII', 
            '42 U.S.C.', '29 U.S.C.', 'reasonable accommodation',
            'New York', 'NY', 'damages', 'injunctive relief'
        ]
        
        # Truncate intelligently by keeping most relevant parts
        lines = context.split('\n')
        truncated_lines = []
        current_tokens = 0
        
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
    
    @staticmethod
    def build_prompt(model: str, context: str, max_tokens: int = 2000) -> str:
        """Build complete prompt with model tweaks and context truncation"""
        
        base_prompt = PromptTemplates.get_base_prompt()
        model_tweak = PromptTemplates.get_model_tweak(model)
        truncated_context = PromptTemplates.truncate_context(context, max_tokens)
        
        return f"{base_prompt}{model_tweak}\n\nDB Context:\n{truncated_context}"
    
    @staticmethod
    def get_benchmark_scenarios() -> List[Dict[str, str]]:
        """Get the 4 core benchmark scenarios"""
        return [
            {
                "category": "PDA Memo",
                "question": "Draft a legal memo analyzing the basic rights of pregnant employees under the Pregnancy Discrimination Act. Include specific citations to relevant cases and statutes from the database.",
                "expected_aspects": ["PDA coverage", "equal treatment", "reasonable accommodations", "bluebook citations"]
            },
            {
                "category": "FMLA Accommodations", 
                "question": "Analyze the legal requirements for reasonable accommodations for pregnant employees under FMLA. Cite specific cases and regulations from the database that establish these requirements.",
                "expected_aspects": ["FMLA rights", "reasonable accommodation", "light duty", "job protection"]
            },
            {
                "category": "NY Law",
                "question": "Analyze how New York State law protects pregnant employees beyond federal law. Cite specific NY statutes and cases from the database.",
                "expected_aspects": ["NY protections", "state statutes", "local laws", "enhanced rights"]
            },
            {
                "category": "Remedies",
                "question": "Draft a brief on legal remedies available for pregnancy discrimination victims. Include specific citations to cases and statutes establishing these remedies.",
                "expected_aspects": ["damages", "injunctive relief", "attorney fees", "back pay"]
            }
        ]
