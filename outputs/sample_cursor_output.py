# Sample Cursor Output
# This file demonstrates how Cursor would save its work

import os
import json
from typing import Dict, List

class DocumentProcessor:
    """Sample legal document processor created by Cursor"""
    
    def __init__(self, config_path: str = None):
        self.config = self._load_config(config_path)
        self.seed = 42  # Fixed seed for reproducibility
        
    def _load_config(self, config_path: str) -> Dict:
        """Load configuration from file"""
        if config_path and os.path.exists(config_path):
            with open(config_path, 'r') as f:
                return json.load(f)
        return {"model": "legal-bert", "confidence_threshold": 0.8}
    
    def process_document(self, document_text: str) -> Dict:
        """Process a legal document and return analysis"""
        # This is where Cursor would implement the actual processing logic
        return {
            "document_type": "contract",
            "confidence": 0.95,
            "key_terms": ["liability", "indemnification"],
            "risk_level": "medium"
        }
    
    def batch_process(self, documents: List[str]) -> List[Dict]:
        """Process multiple documents"""
        results = []
        for doc in documents:
            results.append(self.process_document(doc))
        return results

# Example usage
if __name__ == "__main__":
    processor = DocumentProcessor()
    sample_doc = "This agreement is between Party A and Party B..."
    result = processor.process_document(sample_doc)
    print(f"Analysis result: {result}")
