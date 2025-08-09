# AI Workflow Handoff Guide for Carl

## Quick Start

1. **Setup** (one-time):
   ```bash
   cd ~/Desktop/ai-workflow
   ./setup_github.sh
   # Follow the instructions to create GitHub repo
   ```

2. **With Cursor**:
   - Give Cursor tasks like: "Implement a legal document classifier"
   - Tell Cursor: "Save your code to outputs/[filename].py and a report to outputs/[filename].md"
   - When Cursor finishes: "Remind me to run the push script"

3. **Push to GitHub**:
   ```bash
   ./push-update.sh
   # or
   python3 push_to_github.py
   ```

4. **Share with Grok**:
   - Copy the raw GitHub URL: `https://raw.githubusercontent.com/CarlGaul/ai-workflow-handoff/main/outputs/[filename]`
   - Ask Grok: "Please critique this code: [URL]"

5. **Feed back to Cursor**:
   - Share Grok's feedback with Cursor
   - Have Cursor implement improvements
   - Repeat from step 3

## Example Conversation Flow

**You to Cursor:**
"Implement a function that analyzes legal contracts and extracts key terms. Save the code to outputs/contract_analyzer.py and write a report to outputs/contract_report.md"

**Cursor works and saves files**

**You run:**
```bash
./push-update.sh
```

**You to Grok:**
"Please review this contract analyzer: https://raw.githubusercontent.com/CarlGaul/ai-workflow-handoff/main/outputs/contract_analyzer.py and the report: https://raw.githubusercontent.com/CarlGaul/ai-workflow-handoff/main/outputs/contract_report.md"

**Grok provides feedback**

**You to Cursor:**
"Grok suggested these improvements: [paste feedback]. Please update the code accordingly."

## Benefits

- ✅ No more copy/paste between AI chats
- ✅ Full file context for Grok (no partial views)
- ✅ Version control for all AI work
- ✅ Reproducible results with seeds
- ✅ Organized workflow with clear handoffs

## Tips

- Use descriptive filenames: `legal_bert_classifier.py`, `document_processor.py`
- Include reports with your code: `classifier_report.md`, `processor_notes.md`
- Use the logs folder for debugging: `logs/error_log.txt`
- Keep configs separate: `configs/model_settings.json`
