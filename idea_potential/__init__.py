# Idea Potential Analysis System
# A comprehensive system to analyze and validate business ideas

from .pipeline import IdeaPotentialPipeline

def run_idea_analysis(idea: str = None, interactive: bool = False):
    """
    Run the idea potential analysis system
    
    Args:
        idea (str): The business idea to analyze
        interactive (bool): Whether to run in interactive mode with clarification questions
    
    Returns:
        dict: Analysis results
    """
    
    # Initialize pipeline
    pipeline = IdeaPotentialPipeline()
    
    # Get idea from user if not provided
    if not idea:
        print("\n📝 Please enter your business idea:")
        idea = input("> ").strip()
        
        if not idea:
            print("❌ No idea provided. Exiting.")
            return {"error": "No idea provided"}
    
    try:
        if interactive:
            # Run interactive analysis
            results = pipeline.run_interactive_analysis(idea)
        else:
            # Run standard analysis
            results = pipeline.start_analysis(idea)
        
        if "error" in results:
            print(f"\n❌ Analysis failed: {results['error']}")
            return results
        
        # Display summary
        print("\n" + "=" * 50)
        print("📊 ANALYSIS SUMMARY")
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
        
        print("\n✅ Analysis complete! Check the idea_potential/reports directory for detailed results.")
        
        return results
        
    except KeyboardInterrupt:
        print("\n\n⚠️ Analysis interrupted by user.")
        return {"error": "Analysis interrupted by user"}
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return {"error": f"Unexpected error: {e}"}

# Export the main function
__all__ = ['run_idea_analysis', 'IdeaPotentialPipeline'] 