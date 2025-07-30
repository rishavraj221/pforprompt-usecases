"""
Example usage of the modular Idea Refinement Engine
"""

import asyncio
import json
from pipeline import IdeaValidationPipeline


async def example_usage():
    """Example of how to use the modular idea refinement engine"""
    
    # Initialize the pipeline
    pipeline = IdeaValidationPipeline(llm_model="gpt-4")
    
    # Example ideas to test
    test_ideas = [
        "I want to create a mobile app that helps people find local restaurants",
        "I'm thinking of building a platform for remote team collaboration",
        "I want to make an AI-powered personal finance advisor"
    ]
    
    for i, idea in enumerate(test_ideas, 1):
        print(f"\n{'='*60}")
        print(f"TESTING IDEA #{i}")
        print(f"{'='*60}")
        print(f"💡 Idea: {idea}")
        
        # Run the validation pipeline
        result = await pipeline.validate_idea(idea, save_report=True)
        
        if result["success"]:
            print("\n✅ VALIDATION COMPLETED")
            
            if result.get("report_filepath"):
                print(f"\n📄 Report saved to: {result['report_filepath']}")
            
            print("\n📊 FINAL REPORT:")
            print("-" * 40)
            print(result["final_report"])
            
            # Show intermediate results
            print("\n🔍 INTERMEDIATE ANALYSIS:")
            for key, value in result["intermediate_results"].items():
                if value:
                    print(f"\n{key.upper()}:")
                    print(json.dumps(value, indent=2, default=str))
        else:
            print("\n❌ VALIDATION FAILED")
            print(f"Error: {result.get('error', 'Unknown error')}")
            if result.get('errors'):
                print("Detailed errors:")
                for error in result['errors']:
                    print(f"  - {error}")
        
        print("\n" + "="*60 + "\n")


if __name__ == "__main__":
    asyncio.run(example_usage()) 