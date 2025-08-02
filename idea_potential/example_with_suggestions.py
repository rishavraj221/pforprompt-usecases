#!/usr/bin/env python3
"""
Example demonstrating the Suggester Agent with different agent types
"""

from idea_potential.suggester_agent import SuggesterAgent
from idea_potential.clarifier_agent import ClarifierAgent
from idea_potential.validation_agent import ValidationAgent

def example_clarifier_with_suggestions():
    """Example of using suggester agent with clarifier agent"""
    
    print("🎯 Example: Clarifier Agent with Suggestions")
    print("=" * 50)
    
    clarifier = ClarifierAgent()
    suggester = SuggesterAgent()
    
    # Analyze an idea
    idea = "An AI-powered personal fitness coach that creates custom workout plans"
    print(f"📝 Idea: {idea}")
    
    analysis = clarifier.analyze_initial_idea(idea)
    
    if "error" not in analysis:
        print(f"✅ Analysis: {analysis.get('idea_summary', 'Unknown')}")
        
        # Get questions with suggestions
        questions = analysis.get('critical_questions', [])
        
        for i, question_data in enumerate(questions, 1):
            print(f"\n❓ Question {i}: {question_data['question']}")
            print(f"💡 Why this matters: {question_data['reason']}")
            
            # Generate suggestions for this question
            context = {
                "idea": analysis.get('idea_summary', ''),
                "analysis": analysis.get('analysis', ''),
                "critical_questions": questions,
                "current_question_index": i - 1
            }
            
            suggestions = suggester.generate_suggestions(
                question=question_data['question'],
                context=context,
                agent_type="clarifier"
            )
            
            if "error" not in suggestions:
                print(f"\n💡 Suggested answers:")
                for j, suggestion in enumerate(suggestions.get('suggestions', []), 1):
                    print(f"   {j}. {suggestion['text']}")
                    print(f"      💭 {suggestion['reasoning']}")
                print(f"   {len(suggestions.get('suggestions', [])) + 1}. Type your own answer")
            else:
                print(f"⚠️ No suggestions available: {suggestions['error']}")
            
            print("-" * 40)

def example_validation_with_suggestions():
    """Example of using suggester agent with validation agent"""
    
    print("\n🎯 Example: Validation Agent with Suggestions")
    print("=" * 50)
    
    validator = ValidationAgent()
    suggester = SuggesterAgent()
    
    # Mock validation data
    clarification_data = {
        "refined_idea": "A mobile app for finding and booking local fitness classes",
        "target_market": "Fitness enthusiasts aged 25-45 in urban areas",
        "value_propositions": ["Convenient booking", "Verified reviews", "Class variety"],
        "potential_challenges": ["Market saturation", "High customer acquisition costs"]
    }
    
    research_data = {
        "market_size": "Large and growing fitness market",
        "competition": "Established players like ClassPass and Mindbody",
        "pain_points": ["Inconvenient booking process", "Unreliable class quality", "Limited options"]
    }
    
    # Generate validation questions
    validation_questions = [
        "What is your unique value proposition compared to existing solutions?",
        "How do you plan to acquire your first 1000 customers?",
        "What are the main technical challenges you anticipate?",
        "How will you differentiate from competitors like ClassPass?"
    ]
    
    print(f"📝 Idea: {clarification_data['refined_idea']}")
    print(f"🎯 Target Market: {clarification_data['target_market']}")
    
    for i, question in enumerate(validation_questions, 1):
        print(f"\n❓ Validation Question {i}: {question}")
        
        # Generate suggestions for validation questions
        context = {
            "idea": clarification_data['refined_idea'],
            "target_market": clarification_data['target_market'],
            "value_propositions": clarification_data['value_propositions'],
            "potential_challenges": clarification_data['potential_challenges'],
            "research_data": research_data
        }
        
        suggestions = suggester.generate_suggestions(
            question=question,
            context=context,
            agent_type="validator"
        )
        
        if "error" not in suggestions:
            print(f"\n💡 Suggested answers:")
            for j, suggestion in enumerate(suggestions.get('suggestions', []), 1):
                print(f"   {j}. {suggestion['text']}")
                print(f"      💭 {suggestion['reasoning']}")
            print(f"   {len(suggestions.get('suggestions', [])) + 1}. Type your own answer")
        else:
            print(f"⚠️ No suggestions available: {suggestions['error']}")
        
        print("-" * 40)

def example_generic_suggester():
    """Example of using suggester agent generically"""
    
    print("\n🎯 Example: Generic Suggester Agent")
    print("=" * 50)
    
    suggester = SuggesterAgent()
    
    # Example questions from different agent types
    questions_and_contexts = [
        {
            "agent_type": "researcher",
            "question": "What specific market segments should we focus on?",
            "context": {
                "idea": "A B2B SaaS platform for project management",
                "analysis": "Targeting small to medium businesses",
                "target_market": "SMBs with 10-500 employees"
            }
        },
        {
            "agent_type": "roadmap_builder",
            "question": "What should be the first milestone in your development roadmap?",
            "context": {
                "idea": "A mobile app for food delivery",
                "analysis": "MVP should focus on core delivery functionality",
                "target_market": "Urban consumers aged 18-45"
            }
        },
        {
            "agent_type": "critic",
            "question": "What are the biggest risks to your business model?",
            "context": {
                "idea": "A subscription-based content platform",
                "analysis": "High customer churn risk in content platforms",
                "target_market": "Content creators and consumers"
            }
        }
    ]
    
    for i, qc in enumerate(questions_and_contexts, 1):
        print(f"\n📝 Example {i}: {qc['agent_type'].title()} Agent")
        print(f"❓ Question: {qc['question']}")
        
        suggestions = suggester.generate_suggestions(
            question=qc['question'],
            context=qc['context'],
            agent_type=qc['agent_type']
        )
        
        if "error" not in suggestions:
            print(f"\n💡 Suggested answers:")
            for j, suggestion in enumerate(suggestions.get('suggestions', []), 1):
                print(f"   {j}. {suggestion['text']}")
                print(f"      💭 {suggestion['reasoning']}")
        else:
            print(f"⚠️ No suggestions available: {suggestions['error']}")
        
        print("-" * 40)

def main():
    """Run all examples"""
    
    print("🚀 Suggester Agent Examples")
    print("=" * 50)
    
    # Example 1: Clarifier with suggestions
    example_clarifier_with_suggestions()
    
    # Example 2: Validation with suggestions
    example_validation_with_suggestions()
    
    # Example 3: Generic suggester
    example_generic_suggester()
    
    print("\n✅ All examples completed!")
    print("\n💡 Key Features:")
    print("   - Generic suggester agent that works with any agent type")
    print("   - Context-aware suggestions based on conversation history")
    print("   - Configurable number of suggestions (default: 3)")
    print("   - Suggestion history tracking")
    print("   - Easy integration with existing agents")

if __name__ == "__main__":
    main() 