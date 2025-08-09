#!/usr/bin/env python3
"""
Dependency Fix for LegalAI Application
=====================================

This script fixes the version compatibility issues between huggingface_hub, 
transformers, and sentence-transformers that were preventing the LegalAI 
application from running.

Problem:
- huggingface_hub 0.16.4 was incompatible with transformers 4.35.0
- tokenizers 0.14.1 was incompatible with newer huggingface_hub
- sentence-transformers 3.0.1 was outdated

Solution:
- Upgrade huggingface_hub to 0.34.3
- Upgrade tokenizers to 0.21.4  
- Upgrade transformers to 4.54.1
- Upgrade sentence-transformers to 5.0.0

Usage:
    python3 dependency_fix.py
"""

import subprocess
import sys
import os

def run_command(command, description):
    """Run a pip command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} completed successfully")
            return True
        else:
            print(f"❌ {description} failed:")
            print(result.stderr)
            return False
    except Exception as e:
        print(f"❌ Error during {description}: {e}")
        return False

def check_imports():
    """Test if all critical imports work"""
    print("🔍 Testing imports...")
    try:
        import transformers
        import sentence_transformers
        import huggingface_hub
        print("✅ All imports successful!")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def main():
    """Main dependency fix process"""
    print("🚀 LegalAI Dependency Fix")
    print("=" * 40)
    
    # Check if virtual environment is activated
    if not hasattr(sys, 'real_prefix') and not (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("⚠️  Warning: Virtual environment not detected")
        print("   Consider activating the virtual environment first")
    
    # Fix dependencies in order
    fixes = [
        ("pip install --upgrade huggingface-hub==0.34.3", "Upgrading huggingface-hub"),
        ("pip install --upgrade tokenizers==0.21.4", "Upgrading tokenizers"),
        ("pip install --upgrade transformers==4.54.1", "Upgrading transformers"),
        ("pip install --upgrade sentence-transformers==5.0.0", "Upgrading sentence-transformers")
    ]
    
    success_count = 0
    for command, description in fixes:
        if run_command(command, description):
            success_count += 1
    
    print(f"\n📊 Results: {success_count}/{len(fixes)} fixes applied successfully")
    
    # Test imports
    if check_imports():
        print("\n🎉 All dependencies fixed! LegalAI should now run properly.")
        print("\nNext steps:")
        print("1. Test the application: streamlit run src/main.py")
        print("2. Save this fix to ai-workflow outputs")
        print("3. Push to GitHub for Grok's review")
    else:
        print("\n❌ Some dependencies still have issues. Check the error messages above.")

if __name__ == "__main__":
    main() 