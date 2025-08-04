# AI Instructions for FamilyBeginnings Legal AI

## For Any AI Assistant

**Project:** Non-profit legal AI assistant for pregnancy discrimination and employment law
**User:** Solo attorney, beginner coder, M4 Mac, Cursor IDE
**Location:** ~/Desktop/AI Projects/LegalAI
**Goal:** Sustainable legal tech platform → mobile apps

## AI Workflow Handoff System
- **GitHub:** https://github.com/CarlGaul/ai-workflow-handoff
- **Local:** ~/Desktop/ai-workflow/
- **Push:** ./push-update.sh or python3 push_to_github.py

## Key Files
- src/main.py (Streamlit app)
- src/legal_ai_core.py (Core AI logic)
- src/legal_bert_classifier_enhanced.py (Legal-BERT)
- src/document_uploader.py (Document upload)
- src/court_classifier.py (Court classification)

## Instructions for Implementation (Cursor)
1. Follow AI workflow handoff protocol - Save to ~/Desktop/ai-workflow/outputs/
2. Use descriptive filenames - pregnancy_analyzer.py, court_classifier.py
3. Include reports for strategy review
4. Test locally before completion
5. Remind user to run ./push-update.sh
6. Consider legal context - Pregnancy discrimination, EEOC, NY law
7. Use seeds for reproducibility - torch.manual_seed()
8. Include error handling - Try/except blocks
9. Check existing components before creating new ones

## Instructions for Strategy/Critique (Grok)
1. Read full files from raw GitHub URLs
2. Provide structured feedback on code efficiency, integration, reproducibility
3. Consider legal context - Pregnancy discrimination, EEOC, NY law
4. Suggest specific improvements and next steps
5. Focus on integration with existing LegalAI components

## Testing Commands
```bash
cd ~/Desktop/AI\ Projects/LegalAI && streamlit run src/main.py
cd ~/Desktop/ai-workflow && ./push-update.sh
```

## Tone & Style
- Friendly, encouraging, patient - assume user is learning
- Highlight progress and suggest pausing to test
- Provide step-by-step guidance with exact file locations
- Avoid assuming advanced coding knowledge
