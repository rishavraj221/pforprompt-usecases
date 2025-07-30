"""
Example: Using the Comprehensive Report Generator
Demonstrates how the new report system generates detailed VC-style investment memos
"""

import asyncio
import os
import sys
from pipeline import IdeaValidationPipeline


async def run_comprehensive_validation_example():
    """Run a complete idea validation with comprehensive reporting"""
    
    # Initialize the pipeline
    pipeline = IdeaValidationPipeline()
    
    # Example idea to validate
    user_idea = """
    I want to build a platform that helps small businesses automate their customer service 
    using AI chatbots. The platform would integrate with popular messaging apps like 
    WhatsApp and Facebook Messenger, and provide easy-to-use tools for businesses to 
    create and manage their chatbots without technical knowledge.
    """
    
    print("🚀 Starting Comprehensive Idea Validation")
    print("=" * 60)
    print(f"Idea: {user_idea.strip()}")
    print("=" * 60)
    
    try:
        # Run the validation pipeline
        result = await pipeline.validate_idea(user_idea, save_report=True)
        
        if result["success"]:
            print("\n✅ Validation completed successfully!")
            
            # Display tracking information
            if result.get("tracking"):
                tracking = result["tracking"]
                print(f"📊 Analysis Details:")
                print(f"   Validation ID: {tracking.get('validation_id', 'N/A')}")
                print(f"   Duration: {tracking.get('analysis_duration_minutes', 0)} minutes")
                print(f"   Start Time: {tracking.get('analysis_start_time', 'N/A')}")
            
            # Display report location
            if result.get("report_filepath"):
                print(f"\n📄 Comprehensive Report saved to: {result['report_filepath']}")
                
                # Show a preview of the report
                with open(result["report_filepath"], "r", encoding="utf-8") as f:
                    report_content = f.read()
                    print(f"\n📋 Report Preview (first 500 characters):")
                    print("-" * 40)
                    print(report_content[:500] + "...")
                    print("-" * 40)
            
            # Display intermediate results summary
            if result.get("intermediate_results"):
                intermediate = result["intermediate_results"]
                print(f"\n🔍 Analysis Summary:")
                print(f"   Clarified Idea: {'✅' if intermediate.get('clarified_idea') else '❌'}")
                print(f"   Variations Generated: {'✅' if intermediate.get('variations') else '❌'}")
                print(f"   Critique Analysis: {'✅' if intermediate.get('critique') else '❌'}")
                print(f"   Reality Check: {'✅' if intermediate.get('reality_check') else '❌'}")
                print(f"   User Validation: {'✅' if intermediate.get('user_responses') else '❌'}")
            
        else:
            print(f"\n❌ Validation failed: {result.get('error', 'Unknown error')}")
            
        # Display any errors
        if result.get("errors"):
            print(f"\n⚠️ Errors encountered:")
            for error in result["errors"]:
                print(f"   - {error}")
                
    except Exception as e:
        print(f"\n💥 Pipeline execution failed: {str(e)}")


def show_report_template_structure():
    """Show the structure of the comprehensive report template"""
    
    template_structure = """
📋 COMPREHENSIVE REPORT TEMPLATE STRUCTURE

🚀 IDEA VALIDATION REPORT
├── Header with tracking information
├── Executive Summary with verdict and confidence score
└── Key metrics dashboard

🎯 PROBLEM & SOLUTION ANALYSIS
├── Problem validation with evidence
├── Target users and pain points
├── Solution summary and value proposition
└── Solution-problem fit assessment

🏪 MARKET LANDSCAPE
├── Market opportunity indicators
├── Competitive analysis
├── Unmet needs discovery
└── Competitive edge analysis

🔍 FEASIBILITY ASSESSMENT
├── Technical feasibility (complexity, timeline, risks)
├── Market feasibility (maturity, acquisition, competition)
└── Operational feasibility (team, resources, scalability)

⚠️ CRITICAL RISKS & MITIGATION
├── Deal-breaker risks with probability/impact
└── Assumption risks with validation methods

📋 EXECUTION ROADMAP
├── Phase 1: Validation (weeks 1-4)
├── Phase 2: MVP Development (weeks 5-16)
└── Phase 3: Growth (month 4+)

🔄 PIVOT OPTIONS
├── Alternative approaches if core idea fails
└── Adjacent opportunities discovered

📊 VALIDATION DATA SOURCES
├── Community research summary
├── Sentiment analysis
└── Expert validation sources

🎯 RECOMMENDATION & NEXT STEPS
├── Primary recommendation (PURSUE/PIVOT/KILL)
├── Reasoning and justification
├── Immediate next actions
└── Success criteria for next phase

📎 APPENDICES
├── Detailed SWOT analysis
├── Brainstorming variations
└── Raw research data
"""
    
    print(template_structure)


if __name__ == "__main__":
    print("🎯 Comprehensive Report Generator Example")
    print("=" * 60)
    
    # Show the template structure
    show_report_template_structure()
    
    print("\n" + "=" * 60)
    print("Running example validation...")
    print("=" * 60)
    
    # Run the example
    asyncio.run(run_comprehensive_validation_example()) 