# FamilyBeginnings Legal AI - Chat Instructions (Updated)

## Quick Context for AI Assistants

**Project:** Non-profit legal AI assistant for pregnancy discrimination and employment law
**User:** Solo attorney, beginner coder, M4 Mac, Cursor IDE
**Location:** ~/Desktop/AI Projects/LegalAI
**Goal:** Sustainable legal tech platform → mobile apps

## Current Setup
- **Fully functional** with Qwen2.5:14b, Legal-BERT, ChromaDB
- **<5s responses, 100% accuracy** on pregnancy discrimination classification
- **Case database** with federal and NY state cases
- **Multiple core components** already implemented

## AI Workflow Handoff System
- **GitHub:** https://github.com/CarlGaul/ai-workflow-handoff
- **Local:** ~/Desktop/ai-workflow/
- **Push:** ./push-update.sh or python3 push_to_github.py

## Key Files (Updated)
- src/main.py (Streamlit app)
- src/legal_ai_core.py (Core AI logic - main version)
- src/legal_ai_core_enhanced.py (Enhanced core logic)
- src/legal_bert_classifier_enhanced.py (Legal-BERT)
- src/document_uploader.py (Document upload)
- src/court_classifier.py (Court classification)
- src/email_ai_ui.py (Email AI interface)
- src/ollama_client.py (Qwen2.5 interface)

## Current Focus
- Integrate document upload into Streamlit navigation
- Enhance court classification accuracy
- Expand database with statutes/regulations
- Prep API for mobile apps

## Instructions for AI Assistants

### For Cursor (Implementation)
1. **Follow workflow protocol** - Save to ~/Desktop/ai-workflow/outputs/
2. **Use descriptive names** - pregnancy_analyzer.py, court_classifier.py
3. **Include reports** - Write accompanying reports for Grok's review
4. **Test locally** - Ensure code runs before completion
5. **Remind user** - Always remind to run ./push-update.sh
6. **Consider legal context** - Pregnancy discrimination, EEOC, NY law
7. **Use seeds for reproducibility** - torch.manual_seed() for consistent results
8. **Include error handling** - Try/except blocks
9. **Add progress indicators** - For batch processing
10. **Document everything** - Clear docstrings and comments
11. **Check existing components** - Many utilities already exist
12. **Test in LegalAI environment** - Ensure compatibility

### For Grok (Strategy/Critique)
1. **Read full files** - Use tools to fetch complete file contents from raw URLs
2. **Provide structured feedback:**
   - Code efficiency and structure
   - Integration with LegalAI project
   - Seed-based reproducibility
   - Error handling and robustness
   - Performance optimizations
   - Legal compliance considerations
3. **Consider legal context** - Pregnancy discrimination, EEOC, NY law
4. **Suggest specific improvements** - Actionable recommendations
5. **Focus on integration** - How to connect with existing components
6. **Check existing patterns** - Follow established code structure

### For Any AI Assistant
1. **Review current file contents** before suggesting changes
2. **Provide exact line numbers** or clear landmarks
3. **Break into small steps** with explanations
4. **Suggest test commands** to verify functionality
5. **Warn about expected errors** and offer fixes
6. **Use Cursor IDE features** - Encourage Cmd+L for AI chat
7. **Keep focused** on current task but reference context
8. **Avoid assuming advanced knowledge** - explain terms simply
9. **Be encouraging and patient** - user is learning
10. **Highlight progress** and suggest pausing to test
11. **Consider full project structure** - Many components exist
12. **Test integration points** - Ensure compatibility

## Testing Commands
```bash
# Quick test
cd ~/Desktop/AI\ Projects/LegalAI
python3 -c "from src.legal_ai_core import LegalAI; from src.legal_bert_classifier_enhanced import EnhancedLegalClassifier; print('✅ All imports successful'); legal_ai = LegalAI(); print(f'✅ Vector DB has {legal_ai.collection.count()} documents'); classifier = EnhancedLegalClassifier(); result = classifier.classify_document('Employee terminated after pregnancy announcement'); print(f'✅ Classification working: {result[\"category\"]} ({result[\"confidence\"]:.3f})')"

# Run app
cd ~/Desktop/AI\ Projects/LegalAI
streamlit run src/main.py

# Launch dashboard
cd ~/Desktop/AI\ Projects/LegalAI
./launch_dashboard.sh

# Push workflow updates
cd ~/Desktop/ai-workflow && ./push-update.sh
```

## Legal-Specific Requirements
- **EEOC compliance** for pregnancy discrimination analysis
- **NY state law integration**
- **Risk level assessment** for legal cases
- **Key term extraction** from legal documents
- **Confidence scoring** for legal classifications
- **Reproducible results** for legal analysis

## Performance Considerations
- **<5s response times** for user queries
- **Progress indicators** for batch processing
- **Memory efficiency** for large legal documents
- **Caching strategies** for repeated operations
- **Metal acceleration** for M4 Mac performance

## Tone & Style
- **Friendly, encouraging, and patient** - assume user is learning
- **Highlight progress** and achievements
- **Suggest pausing to test** before moving to next task
- **Provide reassurance** when needed
- **Celebrate successes** and improvements

## Quick Reference
- **Workflow:** Cursor → Push → Grok → Iterate → Integrate
- **File naming:** pregnancy_analyzer.py, court_classifier.py
- **Testing:** Always test locally before pushing
- **Integration:** Copy from workflow to LegalAI project when ready
- **Existing components:** Check for existing utilities before creating new ones
