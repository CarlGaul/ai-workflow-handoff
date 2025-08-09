# AI Collaboration Protocol for Carl's LegalAI Development

## System Overview
This protocol enables seamless collaboration between Cursor (implementation) and Grok (strategy/critique) for legal AI development, eliminating copy/paste and ensuring full file context.

## Infrastructure
- **GitHub Repository:** https://github.com/CarlGaul/ai-workflow-handoff
- **Local Workspace:** ~/Desktop/ai-workflow/
- **Push Scripts:** ./push-update.sh or python3 push_to_github.py

## Workflow Instructions

### For Cursor (Implementation Agent)
1. **Receive Task:** User provides development task
2. **Save Outputs:** Always save to specific files in ~/Desktop/ai-workflow/
   - Code: `outputs/[descriptive_name].py`
   - Reports: `outputs/[descriptive_name]_report.md`
   - Configs: `configs/[descriptive_name].json`
3. **Use Descriptive Names:** pregnancy_analyzer.py, court_classifier.py, etc.
4. **Include Reports:** Always write accompanying reports with implementation details
5. **Test Locally:** Run code before pushing
6. **Remind User:** "Please run ./push-update.sh to push to GitHub"

### For Grok (Strategy/Critique Agent)
1. **Receive Raw URLs:** User shares https://raw.githubusercontent.com/CarlGaul/ai-workflow-handoff/main/outputs/[filename]
2. **Read Full Files:** Use tools to fetch complete file contents
3. **Provide Detailed Feedback:**
   - Code efficiency and structure
   - Integration with LegalAI project
   - Seed-based reproducibility for legal analysis
   - Error handling and robustness
   - Performance optimizations
4. **Suggest Improvements:** Specific, actionable recommendations
5. **Consider Legal Context:** Pregnancy discrimination, EEOC compliance, NY law

### For User (Carl)
1. **Task Cursor:** "Implement [feature]. Save to outputs/[filename].py"
2. **Push to GitHub:** Run ./push-update.sh when Cursor finishes
3. **Share with Grok:** Copy raw URLs and request feedback
4. **Feed Back to Cursor:** Share Grok's suggestions for implementation
5. **Iterate:** Repeat until satisfied, then copy to LegalAI project

## File Structure Standards
```
outputs/
├── [feature_name].py              # Main implementation
├── [feature_name]_report.md       # Analysis report
└── [feature_name]_test.py         # Test cases

configs/
├── [feature_name]_config.json     # Configuration
└── [feature_name]_settings.json   # Settings

logs/
└── [feature_name]_debug.log       # Debug information
```

## Naming Conventions
- **Descriptive:** pregnancy_discrimination_analyzer.py
- **Consistent:** Use underscores, not hyphens
- **Specific:** Include purpose in filename
- **Organized:** Group related files with same prefix

## Integration with LegalAI Project
- Copy polished code from ~/Desktop/ai-workflow/outputs/ to ~/Desktop/LegalAI/src/
- Copy configs to ~/Desktop/LegalAI/configs/
- Test in LegalAI environment
- Update main.py to import new modules

## Seed-Based Reproducibility
- Always use torch.manual_seed() for Legal-BERT operations
- Log seeds in configs for debugging
- Ensure consistent results across runs for legal analysis

## Error Handling Standards
- Try/except blocks for file operations
- Log errors to logs/ folder
- Graceful degradation for legal document processing
- User-friendly error messages

## Performance Considerations
- Progress indicators for batch processing
- Efficient memory usage for large legal documents
- Caching for repeated operations
- Parallel processing where appropriate

## Legal-Specific Requirements
- EEOC compliance considerations
- NY state law integration
- Pregnancy discrimination detection
- Risk level assessment
- Key term extraction from legal documents

## Quick Reference Commands
```bash
# Push updates
cd ~/Desktop/ai-workflow && ./push-update.sh

# Test locally
python3 outputs/[filename].py

# Copy to LegalAI project
cp outputs/[filename].py ~/Desktop/LegalAI/src/
cp configs/[filename].json ~/Desktop/LegalAI/configs/

# Run LegalAI
cd ~/Desktop/LegalAI && streamlit run src/main.py
```

## Example Workflow
1. User: "Create pregnancy discrimination classifier"
2. Cursor: Saves to outputs/pregnancy_classifier.py + report
3. User: Runs ./push-update.sh
4. User: Shares raw URL with Grok
5. Grok: Provides detailed feedback and suggestions
6. User: Feeds back to Cursor for improvements
7. User: Copies final version to LegalAI project

This protocol ensures consistent, efficient AI collaboration for legal AI development.
