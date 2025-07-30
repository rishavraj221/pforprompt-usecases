"""
Test script for the comprehensive report generator
"""

import asyncio
from report_generator import ComprehensiveReportGenerator


def test_report_generator():
    """Test the comprehensive report generator with sample data"""
    
    # Create sample state data
    sample_state = {
        "clarified_idea": {
            "core_problem": "Users struggle with AI hallucinations and inaccuracies",
            "proposed_solution": "A platform where users can share AI problems and get clarifications",
            "target_users": "AI practitioners, developers, researchers",
            "value_proposition": "Reduce AI errors through community validation",
            "implementation_approach": "Web platform with AI agent integration",
            "known_assumptions": ["Users will share problems", "Community will help", "AI agents can assist"]
        },
        "idea_variations": {
            "core_idea_summary": "AI accuracy validation platform",
            "practical_variations": [
                "Focus on specific AI models only",
                "Add automated fact-checking",
                "Include expert verification system",
                "Create educational content about AI limitations",
                "Build API for other applications"
            ],
            "wildcard_concepts": [
                "AI agents that automatically correct hallucinations",
                "Decentralized AI validation network"
            ]
        },
        "critique_analysis": {
            "swot_analysis": {
                "strengths": ["Clear problem definition", "Growing AI market", "Community-driven approach"],
                "weaknesses": ["Technical complexity", "User acquisition challenges", "Quality control"],
                "opportunities": ["AI market growth", "Educational potential", "API monetization"],
                "threats": ["Competition from big tech", "Regulatory changes", "User fatigue"]
            },
            "feasibility_scores": {
                "technical": 6,
                "market": 7,
                "operational": 5
            },
            "kill_risk": "medium",
            "assumption_risks": [
                "User engagement:high:No proven user behavior",
                "Technical complexity:medium:AI integration challenges",
                "Market size:low:Small target audience"
            ]
        },
        "reality_check": {
            "market_evidence": [
                {"source": "Reddit", "content": "Users complaining about AI hallucinations", "sentiment": "negative"},
                {"source": "Forum", "content": "Need for better AI validation tools", "sentiment": "positive"}
            ],
            "market_size_indicators": {
                "forum_mentions": 15,
                "search_volume": "Medium",
                "growth_trend": "Increasing"
            },
            "competitive_analysis": [
                {"name": "Competitor A", "strengths": ["Established user base"], "weaknesses": ["Limited AI focus"]},
                {"name": "Competitor B", "strengths": ["Technical expertise"], "weaknesses": ["Poor UX"]}
            ]
        },
        "user_validation_responses": [
            {"question": "Would you use this tool?", "response": "Yes, definitely!", "sentiment": "positive"},
            {"question": "How much would you pay?", "response": "Up to $10/month", "sentiment": "positive"},
            {"question": "What's the biggest challenge?", "response": "Getting enough users", "sentiment": "neutral"}
        ],
        "analysis_start_time": "2025-01-27T10:00:00",
        "validation_id": "VAL_20250127_100000",
        "analysis_duration_minutes": 45
    }
    
    # Create report generator
    generator = ComprehensiveReportGenerator()
    
    # Generate report
    report = generator.generate_report(sample_state, "AI hallucination validation platform")
    
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


if __name__ == "__main__":
    test_report_generator() 