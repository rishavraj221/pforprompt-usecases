#!/usr/bin/env python3
"""
Test script to demonstrate Reddit integration in the Reality Miner Agent
Requires uv managed dependencies: asyncpraw, textblob, vaderSentiment
"""

import asyncio
import sys
import os

# Add the idea_refinement_engine to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'idea_refinement_engine'))

from idea_refinement_engine.pipeline import IdeaValidationPipeline


async def test_reddit_integration():
    """Test the Reddit integration functionality"""
    
    print("🧪 Testing Reddit Integration...")
    print("=" * 50)
    
    # Initialize the pipeline
    pipeline = IdeaValidationPipeline()
    
    # Test idea that should have Reddit research potential
    test_idea = """
    I want to create a mobile app that helps people find and book local fitness classes.
    The app will show nearby classes, allow booking, and track fitness progress.
    Users can discover new workouts and connect with fitness communities.
    """
    
    print(f"💡 Testing Idea: {test_idea.strip()}")
    print("\n🚀 Starting validation with Reddit research...")
    
    try:
        # Test with report saving enabled
        result = await pipeline.validate_idea(test_idea, save_report=True)
        
        print(f"\n📊 Validation Result:")
        print(f"Success: {result['success']}")
        
        if result.get('report_filepath'):
            print(f"✅ Report saved successfully!")
            print(f"📁 File location: {result['report_filepath']}")
        
        # Check if reality check data includes Reddit research
        if result.get('intermediate_results', {}).get('reality_check'):
            reality_check = result['intermediate_results']['reality_check']
            
            if 'reddit_research' in reality_check:
                print(f"\n🔍 Reddit Research Found!")
                reddit_data = reality_check['reddit_research']
                
                if 'market_sentiment' in reddit_data:
                    print(f"📈 Market Sentiment: {reddit_data['market_sentiment']}")
                
                if 'market_demand' in reddit_data:
                    print(f"📊 Market Demand: {reddit_data['market_demand']}")
                
                if 'competitive_landscape' in reddit_data:
                    print(f"🏢 Competitive Landscape: {reddit_data['competitive_landscape']}")
                
                if 'existing_solutions' in reddit_data:
                    solutions = reddit_data['existing_solutions']
                    print(f"🔍 Found {len(solutions)} existing solutions/competitors")
                    for i, solution in enumerate(solutions[:3], 1):
                        print(f"  {i}. {solution.get('name', 'Unknown')} - {solution.get('user_sentiment', 'Unknown sentiment')}")
                
                if 'user_pain_points' in reddit_data:
                    pain_points = reddit_data['user_pain_points']
                    print(f"😣 Identified {len(pain_points)} user pain points")
                    for i, pain_point in enumerate(pain_points[:3], 1):
                        print(f"  {i}. {pain_point}")
            else:
                print(f"\n⚠️ No Reddit research data found in reality check")
        
        if result.get('errors'):
            print(f"\n❌ Errors found:")
            for error in result['errors']:
                print(f"  - {error}")
        
        return result['success']
        
    except Exception as e:
        print(f"\n💥 Exception occurred: {str(e)}")
        return False


if __name__ == "__main__":
    success = asyncio.run(test_reddit_integration())
    if success:
        print("\n✅ Test PASSED - Reddit integration is working!")
    else:
        print("\n❌ Test FAILED - Reddit integration has issues!")
    
    sys.exit(0 if success else 1) 