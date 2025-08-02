#!/usr/bin/env python3
"""
Test script for the Idea Potential Analysis System
"""

import os
import sys

def test_configuration():
    """Test if configuration is properly set up"""
    
    print("🔧 Testing Configuration...")
    
    try:
        # Import from existing settings
        sys.path.append('..')
        from settings import OPENAI_API_KEY, REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET
        
        # Check OpenAI API key
        if not OPENAI_API_KEY:
            print("❌ OPENAI_API_KEY not found in settings")
            return False
        else:
            print("✅ OPENAI_API_KEY configured")
        
        # Check Reddit credentials
        if not REDDIT_CLIENT_ID or not REDDIT_CLIENT_SECRET:
            print("⚠️ Reddit credentials not configured (research functionality will be limited)")
        else:
            print("✅ Reddit credentials configured")
        
        return True
        
    except ImportError as e:
        print(f"❌ Failed to import settings: {e}")
        return False

def test_imports():
    """Test if all modules can be imported"""
    
    print("\n📦 Testing Imports...")
    
    try:
        from base_agent import BaseAgent
        print("✅ BaseAgent imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import BaseAgent: {e}")
        return False
    
    try:
        from clarifier_agent import ClarifierAgent
        print("✅ ClarifierAgent imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import ClarifierAgent: {e}")
        return False
    
    try:
        from research_agent import ResearchAgent
        print("✅ ResearchAgent imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import ResearchAgent: {e}")
        return False
    
    try:
        from validation_agent import ValidationAgent
        print("✅ ValidationAgent imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import ValidationAgent: {e}")
        return False
    
    try:
        from roadmap_agent import RoadmapAgent
        print("✅ RoadmapAgent imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import RoadmapAgent: {e}")
        return False
    
    try:
        from report_agent import ReportAgent
        print("✅ ReportAgent imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import ReportAgent: {e}")
        return False
    
    try:
        from refiner_agent import RefinerAgent
        print("✅ RefinerAgent imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import RefinerAgent: {e}")
        return False
    
    try:
        from pipeline import IdeaPotentialPipeline
        print("✅ IdeaPotentialPipeline imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import IdeaPotentialPipeline: {e}")
        return False
    
    try:
        from idea_potential import run_idea_analysis
        print("✅ run_idea_analysis imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import run_idea_analysis: {e}")
        return False
    
    return True

def test_agent_initialization():
    """Test if agents can be initialized"""
    
    print("\n🤖 Testing Agent Initialization...")
    
    try:
        from clarifier_agent import ClarifierAgent
        clarifier = ClarifierAgent()
        print("✅ ClarifierAgent initialized successfully")
    except Exception as e:
        print(f"❌ Failed to initialize ClarifierAgent: {e}")
        return False
    
    try:
        from research_agent import ResearchAgent
        research = ResearchAgent()
        print("✅ ResearchAgent initialized successfully")
    except Exception as e:
        print(f"❌ Failed to initialize ResearchAgent: {e}")
        return False
    
    try:
        from validation_agent import ValidationAgent
        validator = ValidationAgent()
        print("✅ ValidationAgent initialized successfully")
    except Exception as e:
        print(f"❌ Failed to initialize ValidationAgent: {e}")
        return False
    
    try:
        from roadmap_agent import RoadmapAgent
        roadmap = RoadmapAgent()
        print("✅ RoadmapAgent initialized successfully")
    except Exception as e:
        print(f"❌ Failed to initialize RoadmapAgent: {e}")
        return False
    
    try:
        from report_agent import ReportAgent
        report = ReportAgent()
        print("✅ ReportAgent initialized successfully")
    except Exception as e:
        print(f"❌ Failed to initialize ReportAgent: {e}")
        return False
    
    try:
        from refiner_agent import RefinerAgent
        refiner = RefinerAgent()
        print("✅ RefinerAgent initialized successfully")
    except Exception as e:
        print(f"❌ Failed to initialize RefinerAgent: {e}")
        return False
    
    try:
        from pipeline import IdeaPotentialPipeline
        pipeline = IdeaPotentialPipeline()
        print("✅ IdeaPotentialPipeline initialized successfully")
    except Exception as e:
        print(f"❌ Failed to initialize IdeaPotentialPipeline: {e}")
        return False
    
    return True

def test_basic_functionality():
    """Test basic functionality without making API calls"""
    
    print("\n🧪 Testing Basic Functionality...")
    
    try:
        from clarifier_agent import ClarifierAgent
        clarifier = ClarifierAgent()
        
        # Test input validation
        result = clarifier.validate_input("")
        if result == False:
            print("✅ Input validation working correctly")
        else:
            print("❌ Input validation not working correctly")
            return False
        
        # Test with valid input
        result = clarifier.validate_input("A valid business idea")
        if result == True:
            print("✅ Valid input validation working correctly")
        else:
            print("❌ Valid input validation not working correctly")
            return False
        
        print("✅ Basic functionality tests passed")
        return True
        
    except Exception as e:
        print(f"❌ Basic functionality test failed: {e}")
        return False

def test_directory_structure():
    """Test if required directories exist"""
    
    print("\n📁 Testing Directory Structure...")
    
    # Check if reports directory exists or can be created
    try:
        os.makedirs('idea_potential/reports', exist_ok=True)
        print("✅ Reports directory ready")
    except Exception as e:
        print(f"❌ Failed to create reports directory: {e}")
        return False
    
    return True

def run_all_tests():
    """Run all tests"""
    
    print("🧪 Idea Potential Analysis System - System Tests")
    print("=" * 50)
    
    tests = [
        ("Configuration", test_configuration),
        ("Imports", test_imports),
        ("Agent Initialization", test_agent_initialization),
        ("Basic Functionality", test_basic_functionality),
        ("Directory Structure", test_directory_structure)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🔍 Running {test_name} test...")
        if test_func():
            print(f"✅ {test_name} test passed")
            passed += 1
        else:
            print(f"❌ {test_name} test failed")
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The system is ready to use.")
        return True
    else:
        print("⚠️ Some tests failed. Please check the configuration and dependencies.")
        return False

def main():
    success = run_all_tests()
    
    if success:
        print("\n🚀 You can now run the system with:")
        print("   uv run main.py")
        print("   uv run main.py \"Your business idea here\"")
        print("   uv run main.py --idea-potential --interactive")
    else:
        print("\n❌ Please fix the issues before running the system.")
        sys.exit(1) 