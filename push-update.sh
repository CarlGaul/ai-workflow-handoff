#!/bin/bash

# AI Workflow Push Script
# This script automates pushing changes to GitHub for AI handoff workflow

echo "🤖 AI Workflow: Pushing updates to GitHub..."

# Add all changes
git add .

# Commit with timestamp
git commit -m "Workflow update: $(date)"

# Push to main branch
git push origin main

echo "✅ Successfully pushed to GitHub!"
echo "📁 Share raw URLs with Grok for feedback:"
echo "   https://raw.githubusercontent.com/CarlGaul/ai-workflow-handoff/main/outputs/[filename]"
