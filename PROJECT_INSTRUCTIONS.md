# FamilyBeginnings Legal AI - Project Instructions

## Project Overview
**FamilyBeginnings Legal AI** - A non-profit legal AI assistant specializing in pregnancy discrimination and employment law for expecting/new parents. Goal: Sustainable legal tech platform, eventually spinning off into mobile apps. Current phase: Database organization and feature expansion (Phase 4).

## User Context
- **Role:** Solo attorney, novice coder learning in spare time
- **Tech Approach:** Local AI for privacy, zero-hallucination responses, real case citations
- **Goals:** Add document upload functionality, enhance court classification, expand database (NY statutes, federal laws, EEOC guidance), prep for mobile app API endpoints
- **Skill Level:** Beginner, needs step-by-step guidance with exact file locations, line numbers, minimal assumptions about coding knowledge
- **Hardware:** M4 MacBook Air, 24GB RAM, macOS 24.5.0, Python 3.13.5
- **IDE:** Cursor IDE (preferred for AI assistance and debugging)

## Project Setup
**Location:** ~/Desktop/LegalAI

**File Structure:**
```
~/Desktop/LegalAI/
├── src/
│   ├── main.py                              # Streamlit app entry point
│   ├── config.py                           # System configuration
│   ├── legal_ai_core.py                    # Core AI logic
│   ├── legal_bert_classifier_enhanced.py   # Legal-BERT classification
│   ├── ollama_client.py                    # Qwen2.5 interface
│   ├── court_classifier.py                 # Court classification
│   ├── document_uploader.py                # Document upload logic
│   └── [support files]
├── database/cases/nys/supreme_court/       # 30+ PDF legal cases
├── vector_database/                        # ChromaDB embeddings
└── requirements.txt
```

**Dependencies (all installed):**
- streamlit==1.46.1
- sentence-transformers==5.0.0
- chromadb==1.0.15
- transformers==4.53.2
- torch==2.7.1
- PyPDF2==3.0.1
- ollama (Qwen2.5:14b)
- coremltools==8.3.0

**Config:** Qwen2.5:14b model, Legal-BERT, ChromaDB, Metal acceleration enabled, 222 case chunks ingested.

## AI Workflow Handoff System
**GitHub Repository:** https://github.com/CarlGaul/ai-workflow-handoff
**Local Workspace:** ~/Desktop/ai-workflow/
**Push Scripts:** ./push-update.sh or python3 push_to_github.py

### Workflow Protocol
1. **Cursor (Implementation):** Saves to ~/Desktop/ai-workflow/outputs/[filename].py
2. **Push to GitHub:** Run ./push-update.sh
3. **Grok (Strategy/Critique):** Reviews via raw GitHub URLs
4. **Iterate:** Feed Grok's feedback back to Cursor
5. **Integrate:** Copy polished code to ~/Desktop/LegalAI/src/

## Current Status
- **Fully functional** with Qwen2.5:14b, Legal-BERT, ChromaDB
- **<5s responses, 100% accuracy** on pregnancy discrimination classification
- **In Progress:** Enhance court classification, integrate document upload into Streamlit navigation
- **Next:** Expand database with statutes/regulations, prep API for mobile apps

## Key Files
- src/main.py (Streamlit app entry point)
- src/config.py (System configuration)
- src/legal_ai_core.py (Core AI logic)
- src/legal_bert_classifier_enhanced.py (Legal-BERT classification)
- src/document_uploader.py (Document upload logic)

## Testing Commands
**Quick Test:**
```bash
cd ~/Desktop/LegalAI
python3 -c "from src.legal_ai_core import LegalAI; from src.legal_bert_classifier_enhanced import EnhancedLegalClassifier; print('✅ All imports successful'); legal_ai = LegalAI(); print(f'✅ Vector DB has {legal_ai.collection.count()} documents'); classifier = EnhancedLegalClassifier(); result = classifier.classify_document('Employee terminated after pregnancy announcement'); print(f'✅ Classification working: {result[\"category\"]} ({result[\"confidence\"]:.3f})')"
```

**Run App:**
```bash
cd ~/Desktop/LegalAI
streamlit run src/main.py
```

## Current Task Focus
- Integrate document upload into src/main.py (Streamlit navigation)
- Next steps: Enhance src/document_uploader.py, improve court classification accuracy, expand database

## Instructions for AI Assistants

### For Cursor (Implementation)
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

### For Grok (Strategy/Critique)
1. **Read full files** - Use tools to fetch complete file contents from raw URLs
2. **Provide structured feedback:**
   - Code efficiency and structure
   - Integration with LegalAI project
   - Seed-based reproducibility for legal analysis
   - Error handling and robustness
   - Performance optimizations
   - Legal compliance considerations
3. **Consider legal context** - Pregnancy discrimination, EEOC compliance, NY law
4. **Suggest specific improvements** - Actionable, detailed recommendations
5. **Focus on integration** - How to connect with existing LegalAI components
6. **Consider performance** - Efficiency for large legal document processing
7. **Review error handling** - Robustness for real-world legal document processing
8. **Check reproducibility** - Seed-based consistency for legal analysis

### For Any AI Assistant
1. **Always review current file contents** before suggesting changes
2. **Provide exact line numbers** or clear "before/after" landmarks
3. **Break instructions into small steps** with explanations
4. **Suggest specific test commands** to verify functionality
5. **Warn about expected errors** and offer fixes
6. **Use Cursor IDE features** - Encourage Cmd+L for AI chat
7. **Keep responses focused** on current task but reference context
8. **Avoid assuming advanced coding knowledge** - explain terms simply
9. **Be encouraging and patient** - user is learning
10. **Highlight progress** and suggest pausing to test

## Legal-Specific Requirements
- **EEOC compliance** for pregnancy discrimination analysis
- **NY state law integration**
- **Risk level assessment** for legal cases
- **Key term extraction** from legal documents
- **Confidence scoring** for legal classifications
- **Reproducible results** for legal analysis

## Performance Considerations
- **Progress indicators** for batch processing
- **Memory efficiency** for large legal documents
- **Caching strategies** for repeated operations
- **Parallel processing** where appropriate
- **<5s response times** for user queries

## Integration Guidelines
- **Copy from workflow** to LegalAI project when ready
- **Test in LegalAI environment** before deployment
- **Update main.py** to import new modules
- **Consider ChromaDB integration** for vector storage
- **Prepare for mobile app API** endpoints

## File Naming Conventions
- **Descriptive:** pregnancy_discrimination_analyzer.py
- **Consistent:** Use underscores, not hyphens
- **Specific:** Include purpose in filename
- **Organized:** Group related files with same prefix

## Quick Reference Commands
```bash
# Push workflow updates
cd ~/Desktop/ai-workflow && ./push-update.sh

# Test in LegalAI
cd ~/Desktop/LegalAI && python3 src/[filename].py

# Run LegalAI app
cd ~/Desktop/LegalAI && streamlit run src/main.py

# Copy from workflow to project
cp ~/Desktop/ai-workflow/outputs/[filename].py ~/Desktop/LegalAI/src/
```

## Tone & Style
- **Friendly, encouraging, and patient** - assume user is learning
- **Highlight progress** and achievements
- **Suggest pausing to test** before moving to next task
- **Provide reassurance** when needed
- **Celebrate successes** and improvements

This protocol ensures consistent, efficient AI collaboration for legal AI development with focus on pregnancy discrimination analysis and employment law.
