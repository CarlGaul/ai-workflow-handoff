#!/bin/bash

echo "🚀 Setting up GitHub connection for AI Workflow..."

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "❌ Git is not installed. Please install it first."
    echo "   On Mac: brew install git"
    exit 1
fi

# Check if we're in the right directory
if [ ! -f "push-update.sh" ]; then
    echo "❌ Please run this script from the ai-workflow directory"
    exit 1
fi

echo "📝 Instructions to complete setup:"
echo ""
echo "1. Go to https://github.com/new"
echo "2. Create a new repository named 'ai-workflow-handoff'"
echo "3. Make it PUBLIC (for easy AI access)"
echo "4. DON'T add README, .gitignore, or license"
echo "5. Copy the repository URL (HTTPS)"
echo ""
echo "6. Then run these commands:"
echo "   git remote add origin YOUR_REPOSITORY_URL"
echo "   git add ."
echo "   git commit -m 'Initial setup'"
echo "   git push -u origin main"
echo ""
echo "7. Test the push script:"
echo "   ./push-update.sh"
echo ""
echo "✅ Setup complete! You can now use the AI workflow handoff system."
