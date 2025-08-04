#!/usr/bin/env python3
"""
AI Workflow GitHub Push Script
Automates pushing changes to GitHub for AI handoff workflow
"""

import subprocess
import datetime
import sys

def push_to_github(message=None):
    """Push changes to GitHub with optional custom message"""
    if not message:
        message = f"Auto-update: {datetime.datetime.now()}"
    
    try:
        # Add all changes
        subprocess.run(["git", "add", "."], check=True)
        print("✅ Added all changes")
        
        # Commit with message
        subprocess.run(["git", "commit", "-m", message], check=True)
        print("✅ Committed changes")
        
        # Push to main branch
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("✅ Successfully pushed to GitHub!")
        
        print("\n📁 Share raw URLs with Grok for feedback:")
        print("   https://raw.githubusercontent.com/CarlGaul/ai-workflow-handoff/main/outputs/[filename]")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error during git operation: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    # Use command line argument as message if provided
    custom_message = sys.argv[1] if len(sys.argv) > 1 else None
    push_to_github(custom_message)
