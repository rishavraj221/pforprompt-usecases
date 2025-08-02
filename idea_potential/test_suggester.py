#!/usr/bin/env python3
"""
Test script for the Suggester Agent functionality
"""

from idea_potential.suggester_agent import SuggesterAgent
from idea_potential.clarifier_agent import ClarifierAgent

def test_suggester_agent():
    """Test the suggester agent with different scenarios"""
    
    print("🧪 Testing Suggester Agent")
    print("=" * 50)
    
    # Initialize suggester agent
    suggester = SuggesterAgent()
    
    # Test 1: Basic suggestion generation
    print("\n📝 Test 1: Basic suggestion generation")
    print("-" * 30)
    
    question = "What is your target market for this idea?"
    context = {
        "idea": "A mobile app for remote team collaboration",
        "analysis": "This is a B2B SaaS product targeting remote teams",
        "target_market": "Remote teams and distributed organizations"
    }
    
    result = suggester.generate_suggestions(
        question=question,
        context=context,
        agent_type="clarifier"
    )
    
    if "error" not in result:
        print(f"✅ Generated {len(result.get('suggestions', []))} suggestions")
        for i, suggestion in enumerate(result.get('suggestions', []), 1):
            print(f"   {i}. {suggestion['text']}")
            print(f"      💭 {suggestion['reasoning']}")
    else:
        print(f"❌ Error: {result['error']}")
    
    # Test 2: Test with clarifier agent integration
    print("\n📝 Test 2: Clarifier agent integration")
    print("-" * 30)
    
    clarifier = ClarifierAgent()
    
    # Analyze an idea
    idea = "A platform that connects local farmers with consumers for direct food sales"
    analysis = clarifier.analyze_initial_idea(idea)
    
    if "error" not in analysis:
        print(f"✅ Analyzed idea: {analysis.get('idea_summary', 'Unknown')}")
        
        # Get first question with suggestions
        question_result = clarifier.ask_next_question()
        
        if "error" not in question_result:
            print(f"❓ Question: {question_result['question']}")
            print(f"💡 Reason: {question_result['reason']}")
            
            suggestions = question_result.get('suggestions', [])
            if suggestions:
                print(f"\n💡 Generated {len(suggestions)} suggestions:")
                for i, suggestion in enumerate(suggestions, 1):
                    print(f"   {i}. {suggestion['text']}")
                    print(f"      💭 {suggestion['reasoning']}")
            else:
                print("⚠️ No suggestions generated")
        else:
            print(f"❌ Error getting question: {question_result['error']}")
    else:
        print(f"❌ Error analyzing idea: {analysis['error']}")
    
    # Test 3: Test suggestion history
    print("\n📝 Test 3: Suggestion history")
    print("-" * 30)
    
    history = suggester.get_suggestion_history()
    print(f"📊 Total suggestions made: {len(history)}")
    
    for entry in history:
        print(f"   - {entry['agent_type']}: {entry['question'][:50]}...")
    
    # Test 4: Test with different agent types
    print("\n📝 Test 4: Different agent types")
    print("-" * 30)
    
    validation_question = "What are the main risks associated with this idea?"
    validation_context = {
        "idea": "A subscription-based pet food delivery service",
        "analysis": "This is a consumer-facing e-commerce business",
        "target_market": "Pet owners in urban areas"
    }
    
    validation_result = suggester.generate_suggestions(
        question=validation_question,
        context=validation_context,
        agent_type="validator"
    )
    
    if "error" not in validation_result:
        print(f"✅ Generated {len(validation_result.get('suggestions', []))} suggestions for validator")
        for i, suggestion in enumerate(validation_result.get('suggestions', []), 1):
            print(f"   {i}. {suggestion['text']}")
    else:
        print(f"❌ Error: {validation_result['error']}")
    
    print("\n✅ Suggester agent tests completed!")

if __name__ == "__main__":
    test_suggester_agent() 