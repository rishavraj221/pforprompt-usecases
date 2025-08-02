#!/usr/bin/env python3
"""
Example usage of the Idea Potential Analysis System
"""

from idea_potential.pipeline import IdeaPotentialPipeline

def run_example():
    """Run an example analysis"""
    
    # Example business idea
    idea = "A mobile app that helps small businesses manage their inventory and track sales in real-time"
    
    print("🎯 Idea Potential Analysis System - Example")
    print("=" * 50)
    print(f"📝 Example Idea: {idea}")
    print("=" * 50)
    
    # Initialize pipeline
    pipeline = IdeaPotentialPipeline()
    
    try:
        # Start analysis
        print("\n🚀 Starting analysis...")
        results = pipeline.start_analysis(idea)
        
        if "error" in results:
            print(f"\n❌ Analysis failed: {results['error']}")
            return
        
        # Display results
        print("\n" + "=" * 50)
        print("📊 ANALYSIS RESULTS")
        print("=" * 50)
        
        print(f"🎯 Idea: {results.get('idea_summary', 'Unknown')}")
        print(f"🎯 Target Market: {results.get('target_market', 'Unknown')}")
        
        # Executive summary
        exec_summary = results.get('executive_summary', {})
        print(f"\n📋 Recommendation: {exec_summary.get('recommendation', 'Unknown').upper()}")
        print(f"📋 Confidence Level: {exec_summary.get('confidence_level', 'Unknown')}")
        
        # Key findings
        print(f"\n🔍 Key Findings:")
        for finding in exec_summary.get('key_findings', []):
            print(f"  • {finding}")
        
        # Validation summary
        val_summary = results.get('validation_summary', {})
        print(f"\n✅ Validation Score: {val_summary.get('overall_score', 'Unknown')}/10")
        print(f"✅ Risk Level: {val_summary.get('risk_level', 'Unknown')}")
        
        # Research summary
        research_summary = results.get('research_summary', {})
        print(f"\n📊 Research Results:")
        print(f"  • Posts Analyzed: {research_summary.get('posts_analyzed', 0)}")
        print(f"  • Market Validation: {research_summary.get('market_validation', 'Unknown')}")
        
        # Roadmap summary
        roadmap_summary = results.get('roadmap_summary', {})
        print(f"\n🗓️ Development Timeline: {roadmap_summary.get('overall_timeline', 'Unknown')}")
        
        # Refinement summary
        refinement_summary = results.get('refinement_summary', {})
        print(f"\n🔧 Report Quality: {refinement_summary.get('quality_score', 'Unknown')}/10")
        print(f"🔧 Authenticity: {refinement_summary.get('authenticity', 'Unknown')}")
        
        # File locations
        print(f"\n📁 Report saved to: {results.get('report_filepath', 'Not saved')}")
        
        print("\n✅ Example analysis complete!")
        print("📁 Check the reports directory for detailed results.")
        
    except Exception as e:
        print(f"\n❌ Example analysis failed: {e}")
        import traceback
        traceback.print_exc()

def run_interactive_example():
    """Run an interactive example"""
    
    print("🎯 Idea Potential Analysis System - Interactive Example")
    print("=" * 50)
    
    # Example idea
    idea = "A subscription service that delivers healthy meal kits to busy professionals"
    
    print(f"📝 Example Idea: {idea}")
    print("\nThis example will show the clarification process...")
    
    # Initialize pipeline
    pipeline = IdeaPotentialPipeline()
    
    try:
        # Step 1: Clarify the idea
        print("\n🔍 Step 1: Clarifying the idea...")
        clarification_result = pipeline.clarify_idea(idea)
        
        if "error" in clarification_result:
            print(f"❌ Clarification failed: {clarification_result['error']}")
            return
        
        # Show the questions that would be asked
        questions = clarification_result.get('critical_questions', [])
        
        if questions:
            print(f"\n📋 The system would ask {len(questions)} critical questions:")
            
            for i, question_data in enumerate(questions, 1):
                print(f"\n❓ Question {i}: {question_data['question']}")
                print(f"💡 Why this matters: {question_data['reason']}")
                print(f"📂 Category: {question_data['category']}")
        
        print("\n✅ Clarification example complete!")
        print("💡 In interactive mode, you would answer these questions.")
        
    except Exception as e:
        print(f"\n❌ Interactive example failed: {e}")

if __name__ == "__main__":
    import sys
    
    if "--interactive" in sys.argv or "-i" in sys.argv:
        run_interactive_example()
    else:
        run_example() 