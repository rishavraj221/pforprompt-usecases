"""
Test the comprehensive report generator with realistic sample data
"""

from report_generator import ComprehensiveReportGenerator


def test_report_generator():
    """Test the comprehensive report generator with realistic sample data"""
    
    # Realistic sample state data that matches actual agent outputs
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
        "validation_questions": {
            "questions": [
                "Would you pay $20/month for an AI prompt optimization tool?",
                "How often do you struggle with prompt debugging?",
                "What's your biggest frustration with current prompt engineering tools?",
                "Would you prefer a standalone tool or IDE integration?"
            ]
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
                    },
                    {
                        "source": "Stack Overflow",
                        "discussion": "Best practices for prompt engineering",
                        "pain_points": ["Lack of standardization", "Difficulty measuring performance"],
                        "sentiment": "neutral"
                    }
                ],
                "market_trends": [
                    "Growing demand for AI development tools",
                    "Increasing focus on prompt engineering",
                    "Rise of specialized AI tools",
                    "Shift toward developer productivity"
                ]
            },
            "reddit_analysis": {
                "total_posts": 45,
                "subreddits_analyzed": ["MachineLearning", "OpenAI", "ArtificialIntelligence"],
                "sentiment_distribution": {
                    "positive": 30,
                    "neutral": 10,
                    "negative": 5
                }
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
            },
            {
                "question": "Would you prefer a standalone tool or IDE integration?",
                "response": "IDE integration would be ideal, but I'd use a standalone tool if it's powerful enough.",
                "sentiment": "positive"
            }
        ],
        "analysis_start_time": "2025-01-27T10:00:00",
        "validation_id": "VAL_20250127_100000",
        "analysis_duration_minutes": 45
    }
    
    # Create report generator
    generator = ComprehensiveReportGenerator()
    
    # Generate report
    report = generator.generate_report(sample_state, "AI-powered prompt engineering assistant")
    
    # Print the report
    print("Generated Report:")
    print("=" * 80)
    print(report)
    print("=" * 80)
    
    # Save to file for inspection
    with open("test_report_output.md", "w", encoding="utf-8") as f:
        f.write(report)
    
    print(f"\nReport saved to test_report_output.md")
    print(f"Report length: {len(report)} characters")
    
    # Verify key sections are present
    required_sections = [
        "🚀 IDEA VALIDATION REPORT",
        "📊 EXECUTIVE SUMMARY",
        "📈 Key Metrics Dashboard",
        "🎯 PROBLEM & SOLUTION ANALYSIS",
        "🏪 MARKET LANDSCAPE",
        "🔍 FEASIBILITY ASSESSMENT",
        "⚠️ CRITICAL RISKS & MITIGATION",
        "📋 EXECUTION ROADMAP",
        "🔄 PIVOT OPTIONS",
        "📊 VALIDATION DATA SOURCES",
        "🎯 RECOMMENDATION & NEXT STEPS",
        "📎 APPENDICES"
    ]
    
    missing_sections = []
    for section in required_sections:
        if section not in report:
            missing_sections.append(section)
    
    if missing_sections:
        print(f"\n⚠️ Missing sections: {missing_sections}")
    else:
        print(f"\n✅ All required sections present")
    
    # Check for mock data
    mock_indicators = ["[X]", "[Action 1]", "[Specific task]", "[Cost estimate]", "[X]%", "$[X]"]
    found_mock = []
    for indicator in mock_indicators:
        if indicator in report:
            found_mock.append(indicator)
    
    if found_mock:
        print(f"\n⚠️ Found mock data indicators: {found_mock}")
    else:
        print(f"\n✅ No mock data found")


if __name__ == "__main__":
    test_report_generator() 