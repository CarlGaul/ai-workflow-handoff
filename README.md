# AI Workflow Handoff System

This repository serves as a shared interface between different AI tools (like Cursor and Grok) for collaborative development workflows.

## Directory Structure

- `prompts/` - Input prompts and task descriptions
- `outputs/` - AI-generated code, reports, and results
- `configs/` - Configuration files and settings
- `logs/` - Error messages, notes, and debugging info

## Workflow

1. **Cursor writes outputs** to specific files in the `outputs/` directory
2. **Push script** automatically uploads changes to GitHub
3. **Share raw URLs** with Grok for feedback and critique
4. **Grok analyzes** the files and provides suggestions
5. **Feed feedback** back to Cursor for improvements

## Usage

### For Cursor:
- Save outputs to `outputs/[filename].py` or `outputs/[filename].md`
- Don't manage git directly - just write files locally
- Remind user to run push script when done

### For Grok:
- Share raw GitHub URLs like: `https://raw.githubusercontent.com/CarlGaul/ai-workflow-handoff/main/outputs/[filename]`
- Grok can read full file contents and provide detailed feedback

### Push Scripts:
- Bash: `./push-update.sh`
- Python: `python3 push_to_github.py [optional_message]`

## Example Workflow

1. Task Cursor: "Implement document upload for legal AI"
2. Cursor saves to `outputs/document_uploader.py`
3. Run: `./push-update.sh`
4. Share with Grok: "Feedback on https://raw.githubusercontent.com/.../outputs/document_uploader.py"
5. Grok provides critique and suggestions
6. Feed feedback back to Cursor

## Seeds for Reproducibility

For legal AI systems, use fixed seeds for classification stages and varied seeds for reasoning:

```python
import torch
torch.manual_seed(42)  # Fixed seed for consistent classification
```

This ensures reproducible results across multiple runs.
