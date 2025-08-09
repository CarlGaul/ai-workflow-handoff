# Cursor Project Instructions for FamilyBeginnings Legal AI

## Project Context
**FamilyBeginnings Legal AI** - Non-profit legal AI assistant for pregnancy discrimination and employment law.

## User Profile
- Solo attorney, beginner coder, M4 Mac, Cursor IDE
- Learning in spare time, needs step-by-step guidance
- Hardware: M4 MacBook Air, 24GB RAM, macOS 24.5.0, Python 3.13.5

## Project Location
~/Desktop/AI Projects/LegalAI/

## AI Workflow Handoff System
- GitHub: https://github.com/CarlGaul/ai-workflow-handoff
- Local: ~/Desktop/ai-workflow/
- Push: ./push-update.sh or python3 push_to_github.py

## Key Files
- src/main.py (Streamlit app)
- src/legal_ai_core.py (Core AI logic)
- src/legal_bert_classifier_enhanced.py (Legal-BERT)
- src/document_uploader.py (Document upload)
- src/court_classifier.py (Court classification)
- src/email_ai_ui.py (Email AI interface)

## Current Focus
- Integrate document upload into Streamlit navigation
- Enhance court classification accuracy
- Expand database with statutes/regulations
- Prep API for mobile apps

## Instructions for Cursor
1. **Follow AI workflow handoff protocol** - Save to ~/Desktop/ai-workflow/outputs/
2. **Use descriptive filenames** - pregnancy_analyzer.py, court_classifier.py
3. **Include reports** - Always write accompanying reports for Grok's review
4. **Test locally** - Ensure code runs before completion
5. **Remind user** - Always remind to run ./push-update.sh
6. **Consider legal context** - Pregnancy discrimination, EEOC compliance, NY law
7. **Use seeds for reproducibility** - torch.manual_seed() for consistent results
8. **Include error handling** - Try/except blocks for file operations
9. **Add progress indicators** - For batch processing operations
10. **Document everything** - Clear docstrings and comments
11. **Check existing components** - Many utilities already exist in LegalAI
12. **Test in LegalAI environment** - Ensure compatibility with current setup

## Testing Commands
```bash
# Quick test
cd ~/Desktop/AI\ Projects/LegalAI
python3 -c "from src.legal_ai_core import LegalAI; from src.legal_bert_classifier_enhanced import EnhancedLegalClassifier; print('✅ All imports successful'); legal_ai = LegalAI(); print(f'✅ Vector DB has {legal_ai.collection.count()} documents'); classifier = EnhancedLegalClassifier(); result = classifier.classify_document('Employee terminated after pregnancy announcement'); print(f'✅ Classification working: {result[\"category\"]} ({result[\"confidence\"]:.3f})')"

# Run app
cd ~/Desktop/AI\ Projects/LegalAI
streamlit run src/main.py

# Push workflow updates
cd ~/Desktop/ai-workflow && ./push-update.sh
```

## Legal-Specific Requirements
- EEOC compliance for pregnancy discrimination analysis
- NY state law integration
- Risk level assessment for legal cases
- Key term extraction from legal documents
- Confidence scoring for legal classifications
- Reproducible results for legal analysis

## Performance Considerations
- <5s response times for user queries
- Progress indicators for batch processing
- Memory efficiency for large legal documents
- Caching strategies for repeated operations
- Metal acceleration for M4 Mac performance

## Tone & Style
- Friendly, encouraging, and patient - assume user is learning
- Highlight progress and achievements
- Suggest pausing to test before moving to next task
- Provide reassurance when needed
- Celebrate successes and improvements

## Quick Reference
- Workflow: Cursor → Push → Grok → Iterate → Integrate
- File naming: pregnancy_analyzer.py, court_classifier.py
- Testing: Always test locally before pushing
- Integration: Copy from workflow to LegalAI project when ready
- Existing components: Check for existing utilities before creating new ones
