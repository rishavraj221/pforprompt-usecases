"""
Example Comprehensive Report Generation
Demonstrates the improved report generator with realistic data
"""

import asyncio
from pipeline import IdeaValidationPipeline
from report_generator import ComprehensiveReportGenerator


async def run_comprehensive_validation_example():
    """Run a complete validation example with comprehensive reporting"""
    
    print("🚀 Running Comprehensive Idea Validation Example")
    print("=" * 60)
    
    # Example idea for testing
    test_idea = "AI-powered prompt engineering assistant that helps developers debug and optimize their LLM prompts"
    
    try:
        # Initialize pipeline
        pipeline = IdeaValidationPipeline()
        
        print(f"\n📝 Analyzing Idea: {test_idea}")
        print("\n🔄 Running validation pipeline...")
        
        # Run validation with comprehensive reporting
        result = await pipeline.validate_idea(test_idea, save_report=True)
        
        if result["success"]:
            print(f"\n✅ Validation completed successfully!")
            print(f"📊 Report saved to: {result['report_filepath']}")
            print(f"⏱️ Analysis duration: {result['tracking']['analysis_duration_minutes']} minutes")
            print(f"🆔 Validation ID: {result['tracking']['validation_id']}")
            
            # Show intermediate results
            if result.get("intermediate_results"):
                print(f"\n📋 Intermediate Results:")
                for agent, status in result["intermediate_results"].items():
                    print(f"  • {agent}: {status}")
            
            # Show any errors
            if result.get("errors"):
                print(f"\n⚠️ Errors encountered:")
                for error in result["errors"]:
                    print(f"  • {error}")
            
            # Show final report preview
            if result.get("final_report"):
                print(f"\n📄 Report Preview (first 500 chars):")
                preview = result["final_report"][:500] + "..." if len(result["final_report"]) > 500 else result["final_report"]
                print(preview)
                
        else:
            print(f"\n❌ Validation failed: {result.get('error', 'Unknown error')}")
            
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


def demonstrate_improved_report_generator():
    """Demonstrate the improved report generator with realistic data"""
    
    print("🔧 Demonstrating Improved Report Generator")
    print("=" * 50)
    
    # Create realistic sample data
    sample_state = {
        "user_idea": "AI-powered prompt engineering assistant that helps developers debug and optimize their LLM prompts",
        "clarified_idea": {
            "status": "complete",
            "core_problem": "Developers struggle to debug and optimize LLM prompts effectively",
            "proposed_solution": "AI-powered assistant that analyzes prompts and suggests improvements",
            "target_users": "Software developers, AI engineers, prompt engineers",
            "value_proposition": "Faster prompt debugging and optimization with AI-powered insights",
            "implementation_approach": "Web-based platform with API integration",
            "known_assumptions": [
                "Developers will pay for prompt optimization tools",
                "AI can effectively analyze and improve prompts",
                "Market exists for specialized prompt engineering tools"
            ]
        },
        "idea_variations": {
            "practical_variations": [
                "Browser extension for real-time prompt analysis",
                "VS Code plugin for prompt debugging",
                "API service for prompt optimization",
                "Collaborative prompt workspace",
                "Prompt template marketplace"
            ],
            "wildcard_concepts": [
                "AI that writes prompts for you based on requirements",
                "Prompt version control with git-like functionality",
                "Prompt performance analytics dashboard",
                "Cross-platform prompt sharing platform",
                "Prompt optimization as a service"
            ]
        },
        "critique_analysis": {
            "swot_analysis": {
                "strengths": [
                    "Addresses real developer pain point",
                    "AI-powered insights provide unique value",
                    "Growing market for AI development tools",
                    "Scalable SaaS business model"
                ],
                "weaknesses": [
                    "Requires significant AI/ML expertise",
                    "High development complexity",
                    "Need for large training dataset",
                    "Competition from established players"
                ],
                "opportunities": [
                    "Growing demand for AI development tools",
                    "Potential for enterprise partnerships",
                    "Expansion to other AI development areas",
                    "Integration with existing developer tools"
                ],
                "threats": [
                    "Large tech companies entering the space",
                    "Rapidly evolving AI landscape",
                    "Difficulty in maintaining competitive advantage",
                    "Potential regulatory challenges"
                ]
            },
            "feasibility_scores": {
                "technical": 6,
                "market": 7,
                "operational": 5
            },
            "assumption_risks": [
                "Market size sufficient for sustainable business: high",
                "AI can effectively analyze prompts: medium",
                "Developers will pay for this tool: medium",
                "Technical complexity manageable: high"
            ],
            "kill_risk": "low"
        },
        "reality_check": {
            "market_size_indicators": {
                "forum_mentions": 45,
                "search_volume": "High",
                "growth_trend": "Growing"
            },
            "web_research": {
                "existing_solutions": [
                    {
                        "name": "PromptPerfect",
                        "website": "https://promptperfect.com",
                        "strengths": ["User-friendly interface", "Multiple model support"],
                        "weaknesses": ["Limited customization", "High pricing"],
                        "pricing": "$29/month",
                        "user_sentiment": "positive"
                    },
                    {
                        "name": "PromptBase",
                        "website": "https://promptbase.com",
                        "strengths": ["Large prompt library", "Community features"],
                        "weaknesses": ["No optimization tools", "Quality varies"],
                        "pricing": "Free + premium",
                        "user_sentiment": "neutral"
                    }
                ],
                "forum_insights": [
                    {
                        "source": "Reddit r/MachineLearning",
                        "discussion": "Prompt engineering challenges in production",
                        "pain_points": ["Debugging complex prompts", "Optimizing for cost", "Maintaining consistency"],
                        "sentiment": "negative"
                    }
                ],
                "market_trends": [
                    "Growing demand for AI development tools",
                    "Increasing focus on prompt engineering",
                    "Rise of specialized AI tools"
                ]
            },
            "reddit_analysis": {
                "total_posts": 45,
                "subreddits_analyzed": ["MachineLearning", "OpenAI", "ArtificialIntelligence"]
            }
        },
        "user_validation_responses": [
            {
                "question": "Would you pay $20/month for an AI prompt optimization tool?",
                "response": "Yes, absolutely! I spend hours debugging prompts and would love a tool to help with this.",
                "sentiment": "positive"
            },
            {
                "question": "How often do you struggle with prompt debugging?",
                "response": "Almost daily. It's the most time-consuming part of my AI development workflow.",
                "sentiment": "negative"
            },
            {
                "question": "What's your biggest frustration with current prompt engineering tools?",
                "response": "Most tools are too basic or too expensive. Need something in between.",
                "sentiment": "neutral"
            }
        ],
        "analysis_start_time": "2025-01-27T10:00:00",
        "validation_id": "VAL_20250127_100000",
        "analysis_duration_minutes": 45
    }
    
    # Generate report using improved generator
    generator = ComprehensiveReportGenerator()
    report = generator.generate_report(sample_state, "AI-powered prompt engineering assistant")
    
    print("\n📊 Generated Report Preview:")
    print("=" * 60)
    
    # Show key sections
    sections = report.split("\n\n")
    for i, section in enumerate(sections[:5]):  # Show first 5 sections
        print(f"\n{section}")
        if i < 4:  # Don't print separator after last section
            print("-" * 40)
    
    print(f"\n... (report continues with {len(sections)-5} more sections)")
    
    # Save complete report
    with open("example_comprehensive_report.md", "w", encoding="utf-8") as f:
        f.write(report)
    
    print(f"\n✅ Complete report saved to: example_comprehensive_report.md")
    print(f"📏 Report length: {len(report)} characters")
    
    # Analyze report quality
    print(f"\n🔍 Report Quality Analysis:")
    
    # Check for mock data
    mock_indicators = ["[X]", "[Action 1]", "[Specific task]", "[Cost estimate]", "[X]%", "$[X]"]
    found_mock = [indicator for indicator in mock_indicators if indicator in report]
    
    if found_mock:
        print(f"⚠️ Found mock data indicators: {found_mock}")
    else:
        print("✅ No mock data found - all content is data-driven")
    
    # Check metrics calculation
    if "Problem Validation|7/10" in report or "Problem Validation|8/10" in report:
        print("✅ Problem validation score calculated from real data")
    else:
        print("⚠️ Problem validation score may be using default values")
    
    # Check competitive analysis
    if "PromptPerfect" in report or "PromptBase" in report:
        print("✅ Competitive analysis includes real competitor data")
    else:
        print("⚠️ Competitive analysis may be generic")
    
    # Check user validation
    if "Yes, absolutely!" in report or "Almost daily" in report:
        print("✅ User validation responses included in report")
    else:
        print("⚠️ User validation responses may be missing")


if __name__ == "__main__":
    print("🎯 Comprehensive Report Generation Examples")
    print("=" * 50)
    
    # Show template structure
    show_report_template_structure()
    
    print("\n" + "=" * 50)
    
    # Demonstrate improved generator
    demonstrate_improved_report_generator()
    
    print("\n" + "=" * 50)
    
    # Run full pipeline example (optional)
    print("\n🚀 To run a full pipeline example, uncomment the following line:")
    print("# asyncio.run(run_comprehensive_validation_example())") 