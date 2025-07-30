#!/usr/bin/env python3
"""
Test script to demonstrate report saving functionality
Requires uv managed dependencies
"""

import asyncio
import sys
import os

# Add the idea_refinement_engine to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'idea_refinement_engine'))

from idea_refinement_engine.pipeline import IdeaValidationPipeline


async def test_report_saving():
    """Test the report saving functionality"""
    
    print("🧪 Testing Report Saving Functionality...")
    print("=" * 50)
    
    # Initialize the pipeline
    pipeline = IdeaValidationPipeline()
    
    # Test idea
    test_idea = """
    I want to create a mobile app that helps people find and book local fitness classes.
    The app will show nearby classes, allow booking, and track fitness progress.
    """
    
    print(f"💡 Testing Idea: {test_idea.strip()}")
    print("\n🚀 Starting validation with report saving...")
    
    try:
        # Test with report saving enabled
        result = await pipeline.validate_idea(test_idea, save_report=True)
        
        print(f"\n📊 Validation Result:")
        print(f"Success: {result['success']}")
        
        if result.get('report_filepath'):
            print(f"✅ Report saved successfully!")
            print(f"📁 File location: {result['report_filepath']}")
            
            # Check if file exists and show its size
            if os.path.exists(result['report_filepath']):
                file_size = os.path.getsize(result['report_filepath'])
                print(f"📏 File size: {file_size} bytes")
                
                # Show first few lines of the report
                with open(result['report_filepath'], 'r', encoding='utf-8') as f:
                    first_lines = f.readlines()[:10]
                    print(f"\n📄 Report preview (first 10 lines):")
                    print("-" * 40)
                    for line in first_lines:
                        print(line.rstrip())
                    print("-" * 40)
            else:
                print("❌ File was not created!")
        else:
            print("⚠️ No report filepath returned")
        
        if result.get('errors'):
            print(f"\n❌ Errors found:")
            for error in result['errors']:
                print(f"  - {error}")
        
        return result['success'] and result.get('report_filepath') is not None
        
    except Exception as e:
        print(f"\n💥 Exception occurred: {str(e)}")
        return False


if __name__ == "__main__":
    success = asyncio.run(test_report_saving())
    if success:
        print("\n✅ Test PASSED - Report saving is working correctly!")
    else:
        print("\n❌ Test FAILED - Report saving has issues!")
    
    sys.exit(0 if success else 1) 