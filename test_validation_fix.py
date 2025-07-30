#!/usr/bin/env python3
"""
Test script to verify the validation pipeline fixes
Requires uv managed dependencies
"""

import asyncio
import sys
import os
import settings

# Add the idea_refinement_engine to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'idea_refinement_engine'))

from idea_refinement_engine.pipeline import IdeaValidationPipeline


async def test_validation_fix():
    """Test the validation pipeline with a simple idea"""
    
    print("🧪 Testing Validation Pipeline Fixes...")
    print("=" * 50)
    
    # Initialize the pipeline
    pipeline = IdeaValidationPipeline()
    
    # Test idea
    test_idea = """
    I want to create an app that helps people manage their personal finances better. 
    I think there's a gap in the market for something that's both simple and powerful.
    """
    
    print(f"💡 Testing Idea: {test_idea.strip()}")
    print("\n🚀 Starting validation...")
    
    try:
        result = await pipeline.validate_idea(test_idea, save_report=True)
        
        print(f"\n📊 Validation Result:")
        print(f"Success: {result['success']}")
        
        if result.get('errors'):
            print(f"\n❌ Errors found:")
            for error in result['errors']:
                print(f"  - {error}")
        else:
            print("\n✅ No errors found!")
        
        if result.get('final_report'):
            print(f"\n📄 Final Report Generated: {len(result['final_report'])} characters")
            if result.get('report_filepath'):
                print(f"📁 Report saved to: {result['report_filepath']}")
        else:
            print("\n⚠️ No final report generated")
            
        return result['success']
        
    except Exception as e:
        print(f"\n💥 Exception occurred: {str(e)}")
        return False


if __name__ == "__main__":
    success = asyncio.run(test_validation_fix())
    if success:
        print("\n✅ Test PASSED - Validation pipeline is working correctly!")
    else:
        print("\n❌ Test FAILED - Validation pipeline still has issues!")
    
    sys.exit(0 if success else 1) 