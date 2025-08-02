# from reddit_prompt_problem_finder_and_solver.finder import fetch_reddit_posts

# if __name__ == "__main__":

#     report_file_path = "/Users/rishavraj/Downloads/Codes/pforprompts-usecases/reddit_prompt_problem_finder_and_solver/analysis/3.md"

#     fetch_reddit_posts(report_file_path=report_file_path)

"""
Main entry point for the pforprompts-usecases project
"""

import asyncio
import json
import sys
from idea_refinement_engine.pipeline import IdeaValidationPipeline
from idea_potential import run_idea_analysis
from settings import OPENAI_API_KEY


async def run_idea_refinement_engine():
    """Run the idea refinement engine"""
    
    # Initialize the pipeline
    pipeline = IdeaValidationPipeline(llm_model="gpt-4")
    
    # Example ideas to test
    test_ideas = [
        "I built an app where users can share the problems with their prompt and llm hallucinations, it is at very initial stage and i want to engage it with the ai agents which will look for open source community forums and prepare the difficult questions for me to answer",
    ]
    
    for i, idea in enumerate(test_ideas, 1):
        print(f"\n{'='*60}")
        print(f"TESTING IDEA #{i}")
        print(f"{'='*60}")
        print(f"💡 Idea: {idea}")
        
        # Run the validation pipeline
        result = await pipeline.validate_idea(idea)
        
        if result["success"]:
            print("\n✅ VALIDATION COMPLETED")
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


def run_idea_potential_analysis():
    """Run the idea potential analysis system"""
    
    print("🎯 Idea Potential Analysis System")
    print("=" * 50)
    
    # Check for command line arguments
    if len(sys.argv) > 1:
        if sys.argv[1] == "--interactive" or sys.argv[1] == "-i":
            # Interactive mode
            run_idea_analysis(interactive=True)
        else:
            # Idea provided as argument
            idea = " ".join(sys.argv[1:])
            run_idea_analysis(idea=idea)
    else:
        # Get idea from user input
        run_idea_analysis()


def show_menu():
    """Show the main menu"""
    
    print("🚀 pforprompts-usecases")
    print("=" * 50)
    print("Choose an analysis system:")
    print("1. Idea Refinement Engine (async)")
    print("2. Idea Potential Analysis System")
    print("3. Idea Potential Analysis (Interactive)")
    print("4. Exit")
    print("=" * 50)
    
    choice = input("Enter your choice (1-4): ").strip()
    
    if choice == "1":
        print("\n🔄 Running Idea Refinement Engine...")
        asyncio.run(run_idea_refinement_engine())
    elif choice == "2":
        print("\n🎯 Running Idea Potential Analysis...")
        run_idea_potential_analysis()
    elif choice == "3":
        print("\n🎯 Running Interactive Idea Potential Analysis...")
        run_idea_analysis(interactive=True)
    elif choice == "4":
        print("👋 Goodbye!")
        return False
    else:
        print("❌ Invalid choice. Please try again.")
    
    return True


if __name__ == "__main__":
    # Check if command line arguments are provided
    # if len(sys.argv) > 1:
    #     # Direct execution with arguments
    #     if sys.argv[1] in ["--idea-potential", "--ip"]:
    #         # Run idea potential analysis
    #         if len(sys.argv) > 2 and sys.argv[2] in ["--interactive", "-i"]:
    #             run_idea_analysis(interactive=True)
    #         else:
    #             idea = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else None
    #             run_idea_analysis(idea=idea)
    #     elif sys.argv[1] in ["--idea-refinement", "--ir"]:
    #         # Run idea refinement engine
    #         asyncio.run(run_idea_refinement_engine())
    #     else:
    #         # Default to idea potential analysis with provided idea
    #         idea = " ".join(sys.argv[1:])
    #         run_idea_analysis(idea=idea)

#     idea = """
# i have an idea to build a platform like stackoverflow for developers, only for their struggle in prompts, llm hallucinations, which can be fixed by tweaking prompt, so community will help user refine prompt to get the expected answer
# """

    idea = "building agentic os"

    run_idea_analysis(
        idea=idea,
        interactive=True,
    )

    # from datetime import datetime
    # from idea_potential.generate_comprehensive_reports import main

    # json_file_path = "idea_potential/reports/idea_analysis_results_20250802_180619.json"
    # output_file_path = f"idea_potential/reports/idea_analysis_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    # main(json_file_path, output_file_path)

    # else:
    #     # Interactive menu
    #     while show_menu():
    #         pass 