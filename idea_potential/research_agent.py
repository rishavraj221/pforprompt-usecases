import praw
import re
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from collections import Counter
import time
from typing import Dict, List, Any
from idea_potential.base_agent import BaseAgent
from idea_potential.config import REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, RESEARCH_SUBREDDITS, MAX_REDDIT_POSTS, MIN_RELEVANCE_SCORE, TIME_FILTER

class ResearchAgent(BaseAgent):
    """Agent responsible for gathering market intelligence from Reddit"""
    
    def __init__(self):
        super().__init__('research')
        self.reddit = None
        self.vader_analyzer = SentimentIntensityAnalyzer()
        self.research_data = {}
        
        # Initialize Reddit client
        if REDDIT_CLIENT_ID and REDDIT_CLIENT_SECRET:
            try:
                self.reddit = praw.Reddit(
                    client_id=REDDIT_CLIENT_ID,
                    client_secret=REDDIT_CLIENT_SECRET,
                    user_agent="IdeaPotentialAnalyzer/1.0"
                )
            except Exception as e:
                print(f"Failed to initialize Reddit client: {e}")
    
    def generate_search_keywords(self, idea_data: Dict[str, Any]) -> List[str]:
        """Generate relevant search keywords from the clarified idea"""
        
        prompt = f"""
        Based on this business idea, generate 10-15 relevant search keywords for Reddit research:

        IDEA: {idea_data.get('refined_idea', 'Unknown')}
        TARGET MARKET: {idea_data.get('target_market', 'Unknown')}
        VALUE PROPOSITIONS: {idea_data.get('value_propositions', [])}

        Generate keywords that would help find:
        1. People discussing similar problems
        2. Market needs and pain points
        3. Existing solutions and their limitations
        4. Customer feedback and complaints
        5. Industry trends and discussions

        Return as JSON array of strings:
        ["keyword1", "keyword2", "keyword3", ...]
        """
        
        messages = [
            {"role": "system", "content": "You are an expert at identifying relevant search terms for market research."},
            {"role": "user", "content": prompt}
        ]
        
        response = self.call_llm(messages, temperature=0.3)
        result = self.parse_json_response(response)
        
        if isinstance(result, list):
            self.log_activity("Generated search keywords", len(result))
            return result
        
        # Fallback keywords
        return ["business", "startup", "entrepreneur", "problem", "solution"]
    
    def search_reddit_posts(self, keywords: List[str]) -> List[Dict[str, Any]]:
        """Search Reddit posts using the generated keywords"""
        if not self.reddit:
            return []
        
        all_posts = []
        
        for subreddit_name in RESEARCH_SUBREDDITS:
            try:
                subreddit = self.reddit.subreddit(subreddit_name)
                
                for keyword in keywords[:5]:  # Limit keywords to avoid rate limiting
                    print(f"Searching r/{subreddit_name} for '{keyword}'...")
                    
                    # Search posts
                    search_results = subreddit.search(keyword, limit=MAX_REDDIT_POSTS//len(keywords), time_filter=TIME_FILTER)
                    
                    for post in search_results:
                        post_data = self.analyze_post_relevance(post, keyword)
                        if post_data and post_data['relevance_score'] >= MIN_RELEVANCE_SCORE:
                            all_posts.append(post_data)
                    
                    time.sleep(1)  # Rate limiting
                    
            except Exception as e:
                print(f"Error searching r/{subreddit_name}: {e}")
                continue
        
        # Remove duplicates and sort by relevance
        unique_posts = self.remove_duplicate_posts(all_posts)
        unique_posts.sort(key=lambda x: x['relevance_score'], reverse=True)
        
        self.log_activity("Collected Reddit posts", len(unique_posts))
        return unique_posts
    
    def analyze_post_relevance(self, post, keyword: str) -> Dict[str, Any]:
        """Analyze a Reddit post for relevance to the idea"""
        title = post.title or ""
        selftext = post.selftext or ""
        combined_text = f"{title} {selftext}".lower()
        
        # Skip if post is too short
        if len(combined_text) < 50:
            return None
        
        # Calculate keyword relevance
        keyword_matches = sum(1 for word in keyword.lower().split() if word in combined_text)
        
        # Calculate sentiment
        sentiment_data = self.calculate_sentiment_score(combined_text)
        
        # Calculate relevance score
        relevance_score = (
            keyword_matches * 3 +
            (1 if sentiment_data['compound'] < -0.1 else 0) * 2 +  # Negative sentiment indicates problems
            min(post.num_comments, 10) * 0.5 +  # Engagement
            min(post.score, 50) * 0.3  # Upvotes
        )
        
        return {
            'post_id': post.id,
            'title': title,
            'selftext': selftext[:500] + "..." if len(selftext) > 500 else selftext,
            'subreddit': str(post.subreddit),
            'author': str(post.author) if post.author else '[deleted]',
            'score': post.score,
            'num_comments': post.num_comments,
            'created_utc': post.created_utc,
            'url': f"https://reddit.com{post.permalink}",
            'keyword': keyword,
            'relevance_score': relevance_score,
            'sentiment_data': sentiment_data,
            'is_problem_discussion': sentiment_data['compound'] < -0.1,
            'engagement_level': 'high' if post.num_comments > 10 else 'medium' if post.num_comments > 3 else 'low'
        }
    
    def calculate_sentiment_score(self, text: str) -> Dict[str, float]:
        """Calculate sentiment score using VADER"""
        scores = self.vader_analyzer.polarity_scores(text)
        return {
            'compound': scores['compound'],
            'neg': scores['neg'],
            'pos': scores['pos'],
            'neu': scores['neu']
        }
    
    def remove_duplicate_posts(self, posts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Remove duplicate posts based on post ID"""
        seen_ids = set()
        unique_posts = []
        
        for post in posts:
            if post['post_id'] not in seen_ids:
                seen_ids.add(post['post_id'])
                unique_posts.append(post)
        
        return unique_posts
    
    def analyze_market_insights(self, posts: List[Dict[str, Any]], idea_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze collected posts to extract market insights"""
        
        if not posts:
            return {"error": "No posts to analyze"}
        
        # Prepare data for analysis
        all_text = " ".join([f"{p['title']} {p['selftext']}" for p in posts])
        problem_posts = [p for p in posts if p['is_problem_discussion']]
        high_engagement_posts = [p for p in posts if p['engagement_level'] == 'high']
        
        # Extract common themes
        themes = self.extract_common_themes(posts)
        
        # Analyze sentiment distribution
        sentiment_analysis = self.analyze_sentiment_distribution(posts)
        
        # Identify pain points
        pain_points = self.identify_pain_points(problem_posts)
        
        # Generate insights
        prompt = f"""
        Analyze this market research data and provide insights about the business idea:

        IDEA: {idea_data.get('refined_idea', 'Unknown')}
        TARGET MARKET: {idea_data.get('target_market', 'Unknown')}

        MARKET DATA SUMMARY:
        - Total posts analyzed: {len(posts)}
        - Problem discussion posts: {len(problem_posts)}
        - High engagement posts: {len(high_engagement_posts)}
        - Common themes: {themes[:5]}
        - Pain points: {pain_points[:5]}
        - Sentiment analysis: {sentiment_analysis}

        Provide insights in JSON format:
        {{
            "market_validation": "Assessment of market need",
            "pain_points_identified": ["List of key pain points"],
            "competition_analysis": "Analysis of existing solutions",
            "customer_sentiment": "Overall customer sentiment",
            "opportunity_assessment": "Market opportunity assessment",
            "risks_and_challenges": ["List of potential risks"],
            "recommendations": ["List of recommendations"]
        }}
        """
        
        messages = [
            {"role": "system", "content": "You are an expert market analyst specializing in business idea validation."},
            {"role": "user", "content": prompt}
        ]
        
        response = self.call_llm(messages, temperature=0.3)
        result = self.parse_json_response(response)
        
        if result:
            result['posts_analyzed'] = len(posts)
            result['problem_posts_count'] = len(problem_posts)
            result['high_engagement_count'] = len(high_engagement_posts)
            self.log_activity("Generated market insights")
        
        return result or {"error": "Failed to analyze market insights"}
    
    def extract_common_themes(self, posts: List[Dict[str, Any]]) -> List[str]:
        """Extract common themes from posts"""
        all_text = " ".join([f"{p['title']} {p['selftext']}" for p in posts])
        
        # Simple keyword extraction (in a real system, you'd use more sophisticated NLP)
        words = re.findall(r'\b\w+\b', all_text.lower())
        word_freq = Counter(words)
        
        # Filter out common words
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'can', 'this', 'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them'}
        
        filtered_words = [(word, count) for word, count in word_freq.items() 
                         if word not in stop_words and len(word) > 3 and count > 2]
        
        return [word for word, count in sorted(filtered_words, key=lambda x: x[1], reverse=True)[:10]]
    
    def analyze_sentiment_distribution(self, posts: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze sentiment distribution across posts"""
        sentiments = [p['sentiment_data']['compound'] for p in posts]
        
        negative = len([s for s in sentiments if s < -0.1])
        neutral = len([s for s in sentiments if -0.1 <= s <= 0.1])
        positive = len([s for s in sentiments if s > 0.1])
        
        return {
            'negative': negative,
            'neutral': neutral,
            'positive': positive,
            'total': len(sentiments),
            'avg_sentiment': sum(sentiments) / len(sentiments) if sentiments else 0
        }
    
    def identify_pain_points(self, problem_posts: List[Dict[str, Any]]) -> List[str]:
        """Identify common pain points from problem discussion posts"""
        pain_keywords = [
            'problem', 'issue', 'difficult', 'hard', 'challenge', 'struggle',
            'frustrated', 'annoyed', 'confused', 'stuck', 'need help',
            'broken', 'doesn\'t work', 'not working', 'failed', 'error'
        ]
        
        pain_points = []
        for post in problem_posts:
            text = f"{post['title']} {post['selftext']}".lower()
            for keyword in pain_keywords:
                if keyword in text:
                    pain_points.append(keyword)
        
        return list(set(pain_points))  # Remove duplicates
    
    def conduct_research(self, idea_data: Dict[str, Any]) -> Dict[str, Any]:
        """Main method to conduct comprehensive market research"""
        
        # Generate search keywords
        keywords = self.generate_search_keywords(idea_data)
        
        # Search Reddit posts
        posts = self.search_reddit_posts(keywords)
        
        # Analyze market insights
        insights = self.analyze_market_insights(posts, idea_data)
        
        # Store research data
        self.research_data = {
            'keywords_used': keywords,
            'posts_collected': posts,
            'insights': insights
        }
        
        return self.research_data 