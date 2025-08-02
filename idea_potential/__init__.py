# Idea Potential Analysis System
# A comprehensive system to analyze and validate business ideas

from .pipeline import IdeaPotentialPipeline

def get_agent_selection():
    """
    Get user input for optional agent selection
    
    Returns:
        tuple: (use_suggester_agent, use_roadmap_agent, use_refiner_agent)
    """
    print("\n🔧 OPTIONAL AGENT SELECTION")
    print("=" * 50)
    print("The following agents are required and will always run:")
    print("  ✅ Clarifier Agent - Analyzes and refines your idea")
    print("  ✅ Research Agent - Conducts market research")
    print("  ✅ Validation Agent - Creates validation frameworks")
    print("  ✅ Report Agent - Generates the final report")
    print("\nThe following agents are optional and can be enabled:")
    print("  💡 Suggester Agent - Provides answer suggestions during interactive mode")
    print("  🗓️ Roadmap Agent - Creates development roadmaps and technical planning")
    print("  🔧 Refiner Agent - Cross-checks and validates final reports for quality")
    print("=" * 50)
    
    use_suggester_agent = False
    use_roadmap_agent = False
    use_refiner_agent = False
    
    # Ask for Suggester Agent
    print("\n💡 Would you like to enable the Suggester Agent?")
    print("   This will provide answer suggestions during interactive clarification questions.")
    suggester_choice = input("   Enable Suggester Agent? (y/n): ").strip().lower()
    use_suggester_agent = suggester_choice in ['y', 'yes', '1']
    
    # Ask for Roadmap Agent
    print("\n🗓️ Would you like to enable the Roadmap Agent?")
    print("   This will add development phases, technical requirements, and resource planning to your report.")
    roadmap_choice = input("   Enable Roadmap Agent? (y/n): ").strip().lower()
    use_roadmap_agent = roadmap_choice in ['y', 'yes', '1']
    
    # Ask for Refiner Agent
    print("\n🔧 Would you like to enable the Refiner Agent?")
    print("   This will add quality assurance, gap analysis, and refinement recommendations to your report.")
    refiner_choice = input("   Enable Refiner Agent? (y/n): ").strip().lower()
    use_refiner_agent = refiner_choice in ['y', 'yes', '1']
    
    print("\n" + "=" * 50)
    print("📋 AGENT CONFIGURATION SUMMARY:")
    print(f"  • Suggester Agent: {'✅ Enabled' if use_suggester_agent else '❌ Disabled'}")
    print(f"  • Roadmap Agent: {'✅ Enabled' if use_roadmap_agent else '❌ Disabled'}")
    print(f"  • Refiner Agent: {'✅ Enabled' if use_refiner_agent else '❌ Disabled'}")
    print("=" * 50)
    
    return use_suggester_agent, use_roadmap_agent, use_refiner_agent

def run_idea_analysis(idea: str = None, interactive: bool = False, use_suggester_agent: bool = None, use_roadmap_agent: bool = None, use_refiner_agent: bool = None):
    """
    Run the idea potential analysis system
    
    Args:
        idea (str): The business idea to analyze
        interactive (bool): Whether to run in interactive mode with clarification questions
        use_suggester_agent (bool): Whether to use the suggester agent (None for user prompt)
        use_roadmap_agent (bool): Whether to use the roadmap agent (None for user prompt)
        use_refiner_agent (bool): Whether to use the refiner agent (None for user prompt)
    
    Returns:
        dict: Analysis results
    """
    
    # Get agent selection from user if not provided
    if use_suggester_agent is None or use_roadmap_agent is None or use_refiner_agent is None:
        use_suggester_agent, use_roadmap_agent, use_refiner_agent = get_agent_selection()
    
    # Initialize pipeline with selected agents
    pipeline = IdeaPotentialPipeline(use_suggester_agent=use_suggester_agent, use_roadmap_agent=use_roadmap_agent, use_refiner_agent=use_refiner_agent)
    
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
        
        # Roadmap summary (only if enabled)
        if use_roadmap_agent:
            roadmap_summary = results.get('roadmap_summary', {})
            print(f"\n🗓️ Development Timeline: {roadmap_summary.get('overall_timeline', 'Unknown')}")
        
        # Refinement summary (only if enabled)
        if use_refiner_agent:
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
__all__ = ['run_idea_analysis', 'IdeaPotentialPipeline', 'get_agent_selection'] 