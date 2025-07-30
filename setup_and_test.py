#!/usr/bin/env python3
"""
Setup and test script for the Idea Refinement Engine with Reddit integration
Uses uv for dependency management
"""

import subprocess
import sys
import os
from pathlib import Path


def run_command(command, description):
    """Run a command and handle errors"""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False


def check_dependencies():
    """Check if required dependencies are available"""
    print("\n🔍 Checking dependencies...")
    
    required_packages = ['asyncpraw', 'textblob', 'vaderSentiment']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package} is available")
        except ImportError:
            print(f"❌ {package} is missing")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n⚠️ Missing packages: {', '.join(missing_packages)}")
        print("Run: uv sync")
        return False
    
    return True


def check_env_file():
    """Check if .env file exists with required variables"""
    env_file = Path('.env')
    if not env_file.exists():
        print("\n⚠️ .env file not found")
        print("Create .env file with:")
        print("REDDIT_CLIENT_ID=your_client_id")
        print("REDDIT_CLIENT_SECRET=your_client_secret")
        print("OPENAI_API_KEY=your_openai_api_key")
        return False
    
    print("✅ .env file found")
    return True


def run_tests():
    """Run all test scripts"""
    test_scripts = [
        "test_validation_fix.py",
        "test_report_saving.py", 
        "test_reddit_integration.py"
    ]
    
    print("\n🧪 Running tests...")
    
    for script in test_scripts:
        if Path(script).exists():
            print(f"\n📋 Running {script}...")
            success = run_command(f"uv run python {script}", f"Running {script}")
            if not success:
                print(f"❌ {script} failed")
                return False
        else:
            print(f"⚠️ {script} not found, skipping")
    
    return True


def main():
    """Main setup and test function"""
    print("🚀 Idea Refinement Engine Setup and Test")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not Path('pyproject.toml').exists():
        print("❌ pyproject.toml not found. Make sure you're in the project root directory.")
        return False
    
    # Step 1: Install dependencies
    if not run_command("uv sync", "Installing dependencies"):
        return False
    
    # Step 2: Check dependencies
    if not check_dependencies():
        return False
    
    # Step 3: Check environment file
    env_ok = check_env_file()
    if not env_ok:
        print("\n⚠️ Environment not fully configured, but continuing with tests...")
    
    # Step 4: Run tests
    if not run_tests():
        return False
    
    print("\n🎉 Setup and tests completed successfully!")
    print("\n📚 Next steps:")
    print("1. Configure your .env file with Reddit and OpenAI credentials")
    print("2. Run: uv run python -m idea_refinement_engine.example")
    print("3. Check the generated reports in idea_refinement_engine/reports/")
    
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 