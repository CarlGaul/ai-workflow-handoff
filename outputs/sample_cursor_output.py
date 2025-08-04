# Sample Cursor Output - Updated with Grok Feedback
# This file demonstrates how Cursor would save its work, now with efficiency improvements, better seed handling, and error handling

import os
import json
from typing import Dict, List
import torch  # For seed reproducibility - import at top

class DocumentProcessor:
    """Sample legal document processor created by Cursor, enhanced for Legal AI integration"""

    def __init__(self, config_path: str = None):
        self.config = self._load_config(config_path)
        self.seed = self.config.get('seed', 42)  # Pull from config if available, default 42
        torch.manual_seed(self.seed)  # Set seed here for all torch-based operations (e.g., Legal-BERT)

    def _load_config(self, config_path: str) -> Dict:
        """Load configuration from file with error handling"""
        try:
            if config_path and os.path.exists(config_path):
                with open(config_path, 'r') as f:
                    return json.load(f)
            return {"model": "legal-bert", "confidence_threshold": 0.8}
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Config load error: {e}. Using defaults.")
            return {"model": "legal-bert", "confidence_threshold": 0.8}

    def process_document(self, document_text: str) -> Dict:
        """Process a legal document and return analysis, integrating with Legal-BERT"""
        if not document_text.strip():  # Simple check for empty input
            raise ValueError("Document text cannot be empty")

        # Placeholder for real integration: Call your EnhancedLegalClassifier
        # Assuming it's imported or available - in real use, add: from src.legal_bert_classifier_enhanced import EnhancedLegalClassifier
        # classifier = EnhancedLegalClassifier()
        # result = classifier.classify_document(document_text)
        # For now, simulate with hardcoded, but filter by confidence from config
        simulated_result = {
            "document_type": "contract",  # Would be result['category']
            "confidence": 0.95,  # Would be result['confidence']
            "key_terms": ["liability", "indemnification", "pregnancy discrimination"],  # Add legal-specific
            "risk_level": "medium"
        }

        if simulated_result['confidence'] < self.config['confidence_threshold']:
            simulated_result['risk_level'] = "low"  # Example dynamic use of config

        return simulated_result

    def batch_process(self, documents: List[str]) -> List[Dict]:
        """Process multiple documents with progress indicator for efficiency"""
        results = []
        for i, doc in enumerate(documents, 1):
            print(f"Processing document {i}/{len(documents)}...")  # Simple progress
            try:
                results.append(self.process_document(doc))
            except ValueError as e:
                print(f"Error on document {i}: {e}")
                results.append({"error": str(e)})
        return results

# Example usage
if __name__ == "__main__":
    processor = DocumentProcessor(config_path="configs/processor_config.json")  # Use the config file
    sample_doc = "Employee terminated after pregnancy announcement under NY law."
    result = processor.process_document(sample_doc)
    print(f"Analysis result: {result}")
