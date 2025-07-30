"""
Idea Validation Pipeline using LangGraph
Multi-agent system for brainstorming, critiquing, and validating ideas
"""

import json
import asyncio

from .pipeline import IdeaValidationPipeline


# Usage Example
async def idea_refinement_engine_main():
    """Example usage of the idea validation pipeline"""
    
    pipeline = IdeaValidationPipeline()
    
    test_idea = """
    I want to create an app that helps people manage their personal finances better. 
    I think there's a gap in the market for something that's both simple and powerful.
    """
    
    print("🚀 Starting Idea Validation Pipeline...")
    print(f"💡 User Idea: {test_idea}")
    print("\n" + "="*50 + "\n")
    
    result = await pipeline.validate_idea(test_idea, save_report=True)
    
    if result["success"]:
        print("✅ Pipeline completed successfully!")
        
        if result.get("report_filepath"):
            print(f"\n📄 Report saved to: {result['report_filepath']}")
        
        print("\n📊 FINAL VALIDATION REPORT:")
        print("="*50)
        print(result["final_report"])
        
        print("\n🔍 INTERMEDIATE ANALYSIS:")
        for key, value in result["intermediate_results"].items():
            if value:
                print(f"\n{key.upper()}:")
                print(json.dumps(value, indent=2))
    else:
        print("❌ Pipeline failed!")
        print(f"Error: {result.get('error', 'Unknown error')}")
        if result.get('errors'):
            print("Detailed errors:")
            for error in result['errors']:
                print(f"  - {error}")


if __name__ == "__main__":
    asyncio.run(idea_refinement_engine_main())