# Quick Reference: AI Workflow Handoff System

## 🚀 One-Liner Commands

### After Cursor Finishes Work
```bash
cd ~/Desktop/ai-workflow && ./push-update.sh
```

### Test Code Locally
```bash
python3 outputs/[filename].py
```

### Copy to LegalAI Project
```bash
cp outputs/[filename].py ~/Desktop/LegalAI/src/
cp configs/[filename].json ~/Desktop/LegalAI/configs/
```

## 📁 File Organization
```
outputs/
├── [feature].py              # Main implementation
├── [feature]_report.md       # Analysis report
└── [feature]_test.py         # Test cases

configs/
├── [feature]_config.json     # Configuration
└── [feature]_settings.json   # Settings
```

## 🔄 Workflow Steps
1. **Task Cursor:** "Implement [feature]. Save to outputs/[filename].py"
2. **Push:** `./push-update.sh`
3. **Share with Grok:** Raw URL from GitHub
4. **Feed Back:** Share Grok's suggestions with Cursor
5. **Iterate:** Repeat until satisfied
6. **Integrate:** Copy to LegalAI project

## 📋 Example Tasks for Cursor
- "Create pregnancy discrimination classifier. Save to outputs/pregnancy_classifier.py"
- "Improve court case analyzer. Save to outputs/enhanced_court_analyzer.py"
- "Add PDF processing to document uploader. Save to outputs/pdf_processor.py"
- "Create risk assessment module. Save to outputs/risk_assessor.py"

## 🔗 Raw URL Format
```
https://raw.githubusercontent.com/CarlGaul/ai-workflow-handoff/main/outputs/[filename]
```

## 📊 Status Check
```bash
ls outputs/          # See what Cursor created
git status          # Check what's changed
./push-update.sh    # Push latest changes
```

## 🎯 Integration Commands
```bash
# Copy polished code to LegalAI
cp outputs/[filename].py ~/Desktop/LegalAI/src/

# Test in LegalAI environment
cd ~/Desktop/LegalAI && python3 src/[filename].py

# Run LegalAI app
cd ~/Desktop/LegalAI && streamlit run src/main.py
```

## 📝 Naming Conventions
- Use underscores: `pregnancy_analyzer.py`
- Be descriptive: `court_classifier.py`
- Include purpose: `risk_assessor.py`
- Group related files: `pregnancy_analyzer.py`, `pregnancy_analyzer_report.md`

## 🔧 Troubleshooting
- **Push fails:** Check git credentials
- **Code won't run:** Test locally first
- **Grok can't read:** Use raw URLs, not repo pages
- **Integration issues:** Check file paths and imports

## 🚀 Pro Tips
- Always include reports with code files
- Test locally before pushing
- Use descriptive filenames
- Keep configs separate from implementation
- Log errors to logs/ folder
- Use seeds for reproducible results
