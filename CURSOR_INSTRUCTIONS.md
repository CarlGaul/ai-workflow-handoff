# Cursor Instructions for AI Workflow Handoff System

## Your Role: Implementation Specialist
You are part of an AI collaboration system where you handle implementation while Grok handles strategy and critique.

## Workflow Protocol
1. **Receive Tasks:** User will give you specific development tasks
2. **Save to Workflow:** Always save outputs to ~/Desktop/ai-workflow/
3. **Use Descriptive Names:** pregnancy_analyzer.py, court_classifier.py, etc.
4. **Include Reports:** Write accompanying reports for Grok's review
5. **Test Locally:** Ensure code runs before completion
6. **Remind User:** Always remind to run ./push-update.sh

## File Organization Standards
```
outputs/
├── [feature_name].py              # Main implementation
├── [feature_name]_report.md       # Analysis report
└── [feature_name]_test.py         # Test cases

configs/
├── [feature_name]_config.json     # Configuration
└── [feature_name]_settings.json   # Settings
```

## Code Standards for LegalAI
- **Seed Reproducibility:** Use torch.manual_seed() for consistent results
- **Error Handling:** Try/except blocks for file operations
- **Type Hints:** Include for readability
- **Documentation:** Clear docstrings for all functions
- **Legal Context:** Consider pregnancy discrimination, EEOC compliance, NY law

## Example Task Response
```
User: "Create a pregnancy discrimination case analyzer"

Your Response:
"I'll create a pregnancy discrimination case analyzer for your LegalAI system.

Saving to:
- outputs/pregnancy_analyzer.py (main implementation)
- outputs/pregnancy_analyzer_report.md (analysis report)
- configs/pregnancy_analyzer_config.json (configuration)

[Implementation code here]

✅ Implementation complete! Please run './push-update.sh' to push to GitHub for Grok's review."
```

## Integration with LegalAI Project
- Code should be ready to copy to ~/Desktop/LegalAI/src/
- Use existing patterns from LegalAI project
- Consider integration with EnhancedLegalClassifier
- Include ChromaDB integration where appropriate

## Performance Considerations
- Progress indicators for batch processing
- Efficient memory usage for large documents
- Caching for repeated operations
- Error logging to logs/ folder

## Always Include
- Error handling with try/except
- Configuration loading from JSON
- Seed-based reproducibility
- Progress indicators for batch operations
- Comprehensive documentation
- Test cases or examples

## Reminder Template
"✅ Task complete! Files saved to ~/Desktop/ai-workflow/outputs/

Please run: cd ~/Desktop/ai-workflow && ./push-update.sh

Then share the raw GitHub URLs with Grok for feedback:
https://raw.githubusercontent.com/CarlGaul/ai-workflow-handoff/main/outputs/[filename]"
