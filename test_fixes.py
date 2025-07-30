#!/usr/bin/env python3
"""
Simple test script to verify the interactive validation fixes
"""

import asyncio
from idea_refinement_engine.pipeline import IdeaValidationPipeline
import settings

async def test_fixes():
    """Test the fixed pipeline"""
    print("🧪 Testing fixed pipeline...")
    
    # Initialize pipeline
    pipeline = IdeaValidationPipeline()
    
    # Test idea
    test_idea = "I built an app where users can share the problems with their prompt and llm hallucinations, it is at very initial stage and i want to engage it with the ai agents which will look for open source community forums and prepare the difficult questions for me to answer"
    
    try:
        # Run validation
        result = await pipeline.validate_idea(test_idea)
        
        print("\n✅ Test completed!")
        print(f"Success: {result['success']}")
        print(f"Errors: {result.get('intermediate_results', {}).get('errors', [])}")
        
        if result['success']:
            print("\n📄 Final Report Preview:")
            report = result.get('final_report', 'No report generated')
            print(report[:500] + "..." if len(report) > 500 else report)
        
    except Exception as e:
        print(f"❌ Test failed with error: {str(e)}")

if __name__ == "__main__":
    asyncio.run(test_fixes()) 