"""
Reality Miner Agent for Idea Validation Pipeline
Enhanced with Reddit PRAW integration for real market research
"""

import json
import re
import time
import asyncio
from typing import List, Dict, Any
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from collections import Counter

from langchain_core.prompts import ChatPromptTemplate
from .base_agent import BaseAgent
from .state import ValidationState

# Try to import AsyncPRAW, but don't fail if not available
try:
    import asyncpraw
    ASYNCPRAW_AVAILABLE = True
except ImportError:
    ASYNCPRAW_AVAILABLE = False
    print("⚠️ AsyncPRAW not available. Install with: uv add asyncpraw")


class RealityMinerAgent(BaseAgent):
    """Agent 5: Analyzes real-world evidence from Reddit and user validation with PRAW integration"""
    
    def __init__(self, llm):
        super().__init__(llm)
        
        # Initialize sentiment analyzers
        self.vader_analyzer = SentimentIntensityAnalyzer()
        
        # Reddit configuration
        self.reddit = None
        if ASYNCPRAW_AVAILABLE:
            try:
                import settings
                # Note: We'll initialize the async Reddit instance in the run method
                # since we need it to be async-compatible
                self.reddit_config = {
                    "client_id": settings.REDDIT_CLIENT_ID,
                    "client_secret": settings.REDDIT_CLIENT_SECRET,
                    "user_agent": "IdeaValidationBot/1.0"
                }
                print("✅ Reddit AsyncPRAW integration configured")
            except Exception as e:
                print(f"⚠️ Reddit integration failed: {e}")
                self.reddit_config = None
        
        # Subreddits for idea validation (general + specific)
        self.GENERAL_SUBREDDITS = [
            "startups", "entrepreneur", "smallbusiness", "business", 
            "productivity", "technology", "software", "webdev",
            "mobileapp", "saas", "indiehackers", "sidehustle"
        ]
        
        # Keywords for market research
        self.MARKET_KEYWORDS = [
            "problem", "issue", "frustrated", "annoying", "difficult",
            "looking for", "need help", "suggestion", "alternative",
            "best", "recommend", "review", "experience", "opinion",
            "worth it", "value", "cost", "price", "free", "paid",
            "feature", "missing", "wish", "would love", "hate",
            "love", "great", "terrible", "awesome", "sucks"
        ]
        
        # Solution-seeking patterns
        self.SOLUTION_PATTERNS = [
            r"looking for.*app",
            r"need.*solution",
            r"anyone.*recommend",
            r"best.*for",
            r"alternative.*to",
            r"problem.*with",
            r"issue.*using",
            r"frustrated.*with",
            r"wish.*had",
            r"missing.*feature"
        ]
        
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """
**Role**: Reality Check Specialist with Web Browsing Capabilities
**Task**: Analyze user validation responses and forum data to assess idea feasibility

**Web Research Instructions**:
1. Search for existing solutions in the market
2. Find forum discussions about similar problems
3. Look for competitor analysis and reviews
4. Research market size and trends
5. Find real user complaints and pain points

**Analysis Framework**:
1. User Validation Analysis: Review user responses to validation questions
2. Web Research Analysis: Incorporate findings from web searches
3. Risk Assessment: Identify high-risk areas based on user responses and market research
4. Feasibility Score: Rate idea feasibility (1-10) based on evidence
5. Recommendations: Suggest next steps or pivots

**Output Format**:
```json
{{
  "web_research": {{
    "existing_solutions": [
      {{
        "name": "Competitor Name",
        "website": "URL",
        "strengths": ["list"],
        "weaknesses": ["list"],
        "pricing": "price info",
        "user_sentiment": "positive/negative/neutral"
      }}
    ],
    "forum_insights": [
      {{
        "source": "Reddit/HN/etc",
        "discussion": "summary",
        "pain_points": ["list"],
        "sentiment": "positive/negative/neutral"
      }}
    ],
    "market_trends": ["list of trends"]
  }},
  "user_validation_analysis": {{
    "high_risk_areas": ["list of concerns"],
    "confidence_indicators": ["positive signals"],
    "feasibility_score": 7,
    "key_insights": ["main takeaways"]
  }},
  "overall_assessment": {{
    "feasibility_score": 7,
    "risk_level": "medium",
    "recommendations": ["next steps"],
    "pivot_suggestions": ["alternative approaches"]
  }}
}}
```"""),
            ("human", """
Validation Questions: {validation_questions}
User Responses: {user_responses}
Clarified Idea: {clarified_idea}
""")
        ])
    
    def preprocess_text(self, text: str) -> str:
        """Clean and normalize text for analysis"""
        if not text:
            return ""
        
        # Remove URLs, mentions, markdown formatting
        text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)
        text = re.sub(r'u/\w+', '', text)
        text = re.sub(r'r/\w+', '', text)
        text = re.sub(r'\*\*?(.+?)\*\*?', r'\1', text)  # Remove markdown bold
        text = re.sub(r'`(.+?)`', r'\1', text)  # Remove code blocks
        text = re.sub(r'\n+', ' ', text)  # Replace newlines with spaces
        
        return text.lower().strip()
    
    def calculate_sentiment_score(self, text: str) -> Dict[str, float]:
        """Calculate comprehensive sentiment score"""
        # VADER sentiment (better for social media text)
        vader_scores = self.vader_analyzer.polarity_scores(text)
        
        # TextBlob sentiment
        blob = TextBlob(text)
        textblob_polarity = blob.sentiment.polarity
        textblob_subjectivity = blob.sentiment.subjectivity
        
        # Combined sentiment score
        combined_sentiment = (vader_scores['compound'] + textblob_polarity) / 2
        
        return {
            'vader_compound': vader_scores['compound'],
            'vader_neg': vader_scores['neg'],
            'vader_pos': vader_scores['pos'],
            'textblob_polarity': textblob_polarity,
            'textblob_subjectivity': textblob_subjectivity,
            'combined_sentiment': combined_sentiment
        }
    
    def extract_keywords_from_idea(self, idea: str) -> List[str]:
        """Extract relevant keywords from the user's idea for Reddit search"""
        # Simple keyword extraction - in production, use NLP
        words = re.findall(r'\b\w+\b', idea.lower())
        
        # Filter for meaningful words (exclude common words)
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'can', 'this', 'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them'}
        
        keywords = [word for word in words if len(word) > 3 and word not in stop_words]
        
        # Add common business/tech terms
        business_terms = ['app', 'platform', 'tool', 'service', 'product', 'solution', 'market', 'users', 'customers', 'business', 'startup', 'company']
        keywords.extend([term for term in business_terms if term in idea.lower()])
        
        return list(set(keywords))[:10]  # Limit to top 10 keywords
    
    async def search_reddit_for_idea_validation(self, idea: str, limit: int = 50) -> List[Dict[str, Any]]:
        """Search Reddit for posts related to the user's idea using AsyncPRAW"""
        if not self.reddit_config:
            print("⚠️ Reddit not available, skipping Reddit research")
            return []
        
        try:
            keywords = self.extract_keywords_from_idea(idea)
            print(f"🔍 Searching Reddit with keywords: {keywords[:5]}...")
            
            relevant_posts = []
            
            # Initialize async Reddit instance
            async with asyncpraw.Reddit(**self.reddit_config) as reddit:
                for subreddit_name in self.GENERAL_SUBREDDITS[:5]:  # Limit to top 5 subreddits
                    try:
                        subreddit = await reddit.subreddit(subreddit_name)
                        
                        # Search for posts containing our keywords
                        for keyword in keywords[:3]:  # Use top 3 keywords
                            search_results = subreddit.search(keyword, limit=limit//len(keywords), sort='relevance', time_filter='year')
                            
                            async for post in search_results:
                                # Analyze post relevance
                                title = post.title or ""
                                selftext = post.selftext or ""
                                combined_text = f"{title} {selftext}"
                                
                                # Calculate relevance score
                                relevance_score = 0
                                for kw in keywords:
                                    if kw.lower() in combined_text.lower():
                                        relevance_score += 1
                                
                                if relevance_score > 0:
                                    # Calculate sentiment
                                    clean_text = self.preprocess_text(combined_text)
                                    sentiment_data = self.calculate_sentiment_score(clean_text)
                                    
                                    # Check for solution-seeking patterns
                                    solution_seeking = any(re.search(pattern, combined_text, re.IGNORECASE) for pattern in self.SOLUTION_PATTERNS)
                                    
                                    post_data = {
                                        'post_id': post.id,
                                        'title': title,
                                        'selftext': selftext[:300] + "..." if len(selftext) > 300 else selftext,
                                        'subreddit': str(post.subreddit),
                                        'author': str(post.author) if post.author else '[deleted]',
                                        'score': post.score,
                                        'upvote_ratio': post.upvote_ratio,
                                        'num_comments': post.num_comments,
                                        'created_utc': post.created_utc,
                                        'url': f"https://reddit.com{post.permalink}",
                                        'relevance_score': relevance_score,
                                        'sentiment_data': sentiment_data,
                                        'solution_seeking': solution_seeking,
                                        'keywords_matched': [kw for kw in keywords if kw.lower() in combined_text.lower()]
                                    }
                                    
                                    relevant_posts.append(post_data)
                                
                                # Rate limiting - use asyncio.sleep instead of time.sleep
                                await asyncio.sleep(0.1)
                    
                    except Exception as e:
                        print(f"⚠️ Error searching r/{subreddit_name}: {e}")
                        continue
            
            # Sort by relevance score
            relevant_posts.sort(key=lambda x: x['relevance_score'], reverse=True)
            
            print(f"✅ Found {len(relevant_posts)} relevant Reddit posts")
            return relevant_posts[:20]  # Return top 20 posts
            
        except Exception as e:
            print(f"❌ Reddit search failed: {e}")
            return []
    
    async def run(self, state: ValidationState) -> ValidationState:
        try:
            # Check if we have at least some validation data
            user_responses = state.get("user_validation_responses", [])
            if user_responses is None:
                user_responses = []
            
            # If we have user responses, we can proceed even without validation questions
            if not user_responses:
                state["errors"].append("Cannot analyze reality - missing user validation responses")
                return state
            
            # Get the user's original idea for Reddit research
            user_idea = state.get("user_idea", "")
            
            # Perform Reddit research
            print("\n🔍 Performing Reddit market research...")
            reddit_posts = await self.search_reddit_for_idea_validation(user_idea)
            
            # Prepare Reddit research data for LLM analysis
            reddit_research_data = {
                "total_posts_found": len(reddit_posts),
                "posts": reddit_posts[:10],  # Top 10 posts for analysis
                "subreddit_distribution": Counter(post['subreddit'] for post in reddit_posts).most_common(5),
                "sentiment_summary": {
                    "positive_posts": len([p for p in reddit_posts if p['sentiment_data']['combined_sentiment'] > 0.1]),
                    "negative_posts": len([p for p in reddit_posts if p['sentiment_data']['combined_sentiment'] < -0.1]),
                    "neutral_posts": len([p for p in reddit_posts if -0.1 <= p['sentiment_data']['combined_sentiment'] <= 0.1]),
                    "average_sentiment": sum(p['sentiment_data']['combined_sentiment'] for p in reddit_posts) / len(reddit_posts) if reddit_posts else 0
                },
                "solution_seeking_posts": len([p for p in reddit_posts if p['solution_seeking']]),
                "top_keywords": list(set([kw for post in reddit_posts for kw in post['keywords_matched']]))[:10]
            }
            
            # Update the prompt to include Reddit research
            enhanced_prompt = ChatPromptTemplate.from_messages([
                ("system", """
**Role**: Reality Check Specialist with Reddit Market Research
**Task**: Analyze user validation responses and Reddit market data to assess idea feasibility

**Reddit Research Analysis**:
- Analyze market sentiment from Reddit posts
- Identify existing solutions and user pain points
- Assess market demand and competition
- Evaluate user feedback and feature requests

**Analysis Framework**:
1. User Validation Analysis: Review user responses to validation questions
2. Reddit Market Research: Incorporate findings from Reddit posts
3. Risk Assessment: Identify high-risk areas based on user responses and market research
4. Feasibility Score: Rate idea feasibility (1-10) based on evidence
5. Recommendations: Suggest next steps or pivots

**Output Format**:
```json
{{
  "reddit_research": {{
    "market_sentiment": "positive/negative/neutral",
    "existing_solutions": [
      {{
        "name": "Competitor/Alternative",
        "description": "What it does",
        "user_sentiment": "positive/negative/neutral",
        "strengths": ["list"],
        "weaknesses": ["list"]
      }}
    ],
    "user_pain_points": ["list of identified problems"],
    "market_demand": "high/medium/low",
    "competitive_landscape": "saturated/competitive/opportunity"
  }},
  "user_validation_analysis": {{
    "high_risk_areas": ["list of concerns"],
    "confidence_indicators": ["positive signals"],
    "feasibility_score": 7,
    "key_insights": ["main takeaways"]
  }},
  "overall_assessment": {{
    "feasibility_score": 7,
    "risk_level": "medium",
    "recommendations": ["next steps"],
    "pivot_suggestions": ["alternative approaches"]
  }}
}}
```"""),
                ("human", """
Validation Questions: {validation_questions}
User Responses: {user_responses}
Clarified Idea: {clarified_idea}
Reddit Research: {reddit_research}
""")
            ])
            
            chain = enhanced_prompt | self.llm
            response = await chain.ainvoke({
                "validation_questions": json.dumps(state.get("validation_questions", {})),
                "user_responses": json.dumps(state["user_validation_responses"]),
                "clarified_idea": json.dumps(state["clarified_idea"]),
                "reddit_research": json.dumps(reddit_research_data)
            })
            
            result = self.parse_json_response(response.content)
            state["reality_check"] = result
            state["current_agent"] = "reality_miner"
            
            return state
            
        except Exception as e:
            state["errors"].append(f"Reality Miner error: {str(e)}")
            return state 