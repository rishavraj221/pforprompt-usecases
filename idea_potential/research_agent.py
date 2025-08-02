import praw
import re
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from collections import Counter
import time
from typing import Dict, List, Any
from idea_potential.base_agent import BaseAgent
from idea_potential.config import (REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, RESEARCH_SUBREDDITS, 
                                   MAX_REDDIT_POSTS, MIN_RELEVANCE_SCORE, TIME_FILTER, CHUNK_SIZE, 
                                   LARGE_DATASET_THRESHOLD, MIN_ENGAGEMENT_SCORE, MIN_COMMENTS_THRESHOLD)

class ResearchAgent(BaseAgent):
    """Agent responsible for gathering market intelligence from Reddit"""
    
    def __init__(self):
        super().__init__('research')
        self.reddit = None
        self.vader_analyzer = SentimentIntensityAnalyzer()
        self.research_data = {}
        self.references = []  # Track all Reddit references
        
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
    
    def chunk_large_dataset(self, posts: List[Dict[str, Any]], max_chunk_size: int = CHUNK_SIZE) -> List[List[Dict[str, Any]]]:
        """Break large Reddit datasets into manageable chunks for LLM analysis"""
        chunks = []
        for i in range(0, len(posts), max_chunk_size):
            chunk = posts[i:i + max_chunk_size]
            chunks.append(chunk)
        return chunks
    
    def analyze_chunk_with_references(self, chunk: List[Dict[str, Any]], idea_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze a chunk of Reddit posts with reference tracking"""
        
        # Prepare chunk data with references
        chunk_data = []
        chunk_references = []
        
        for post in chunk:
            try:
                # Ensure we have a valid URL
                url = post.get('url', '')
                if not url and 'permalink' in post:
                    url = f"https://reddit.com{post['permalink']}"
                elif not url:
                    url = f"https://reddit.com/r/{post.get('subreddit', 'unknown')}/comments/{post.get('post_id', 'unknown')}/"
                
                post_data = {
                    'title': post.get('title', 'Unknown'),
                    'content': post.get('selftext', '')[:500],  # Limit content length
                    'score': post.get('score', 0),
                    'comments_count': post.get('num_comments', 0),
                    'sentiment': post.get('sentiment_data', {'compound': 0}),
                    'url': url,
                    'subreddit': post.get('subreddit', 'unknown'),
                    'created_utc': post.get('created_utc', 0)
                }
                chunk_data.append(post_data)
                chunk_references.append({
                    'url': url,
                    'title': post.get('title', 'Unknown'),
                    'subreddit': post.get('subreddit', 'unknown'),
                    'score': post.get('score', 0),
                    'comments': post.get('num_comments', 0)
                })
            except Exception as e:
                print(f"Warning: Error processing post in chunk: {e}")
                continue
        
        # Check if we have valid data
        if not chunk_data:
            return {"error": "No valid posts in chunk"}
        
        prompt = f"""
        Analyze this chunk of Reddit posts for market insights related to this business idea:

        IDEA: {idea_data.get('refined_idea', 'Unknown')}
        TARGET MARKET: {idea_data.get('target_market', 'Unknown')}

        REDDIT POSTS TO ANALYZE:
        {chunk_data}

        Provide analysis in JSON format:
        {{
            "quantitative_metrics": {{
                "total_posts": {len(chunk_data)},
                "avg_score": "average post score",
                "avg_comments": "average comments per post",
                "engagement_rate": "engagement calculation",
                "sentiment_breakdown": {{
                    "positive": "count",
                    "neutral": "count", 
                    "negative": "count"
                }}
            }},
            "user_feedback": {{
                "common_complaints": ["list of complaints"],
                "expressed_needs": ["list of needs"],
                "pain_points": ["list of pain points"],
                "feature_requests": ["list of feature requests"],
                "user_sentiment": "overall sentiment analysis"
            }},
            "market_insights": {{
                "trends_identified": ["list of trends"],
                "opportunities": ["list of opportunities"],
                "challenges": ["list of challenges"]
            }},
            "references": {chunk_references}
        }}
        """
        
        messages = [
            {"role": "system", "content": "You are an expert market analyst specializing in Reddit data analysis and business idea validation."},
            {"role": "user", "content": prompt}
        ]
        
        response = self.call_llm(messages, temperature=0.3)
        result = self.parse_json_response(response)
        
        if result:
            # Add references to global tracking
            self.references.extend(chunk_references)
            return result
        
        return {"error": "Failed to analyze chunk"}
    
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
        print(f"research search keywords result: {result}")
        
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
        """Main method to conduct comprehensive market research with chunking and quantitative analysis"""
        
        # Generate search keywords
        keywords = self.generate_search_keywords(idea_data)
        
        # Search Reddit posts
        posts = self.search_reddit_posts(keywords)
        
        # Check if dataset is large and needs chunking
        if len(posts) > LARGE_DATASET_THRESHOLD:
            print(f"Large dataset detected ({len(posts)} posts). Breaking into chunks for better analysis...")
            chunks = self.chunk_large_dataset(posts, max_chunk_size=CHUNK_SIZE)
            
            all_chunk_insights = []
            quantitative_metrics = {
                'total_posts': len(posts),
                'chunks_analyzed': len(chunks),
                'avg_score': 0,
                'avg_comments': 0,
                'engagement_rate': 0,
                'sentiment_breakdown': {'positive': 0, 'neutral': 0, 'negative': 0}
            }
            
            # Analyze each chunk
            for i, chunk in enumerate(chunks):
                print(f"Analyzing chunk {i+1}/{len(chunks)}...")
                try:
                    chunk_insights = self.analyze_chunk_with_references(chunk, idea_data)
                    
                    if 'error' not in chunk_insights:
                        all_chunk_insights.append(chunk_insights)
                        
                        # Aggregate quantitative metrics
                        if 'quantitative_metrics' in chunk_insights:
                            qm = chunk_insights['quantitative_metrics']
                            quantitative_metrics['avg_score'] += qm.get('avg_score', 0)
                            quantitative_metrics['avg_comments'] += qm.get('avg_comments', 0)
                            if 'sentiment_breakdown' in qm:
                                for sentiment, count in qm['sentiment_breakdown'].items():
                                    quantitative_metrics['sentiment_breakdown'][sentiment] += count
                    else:
                        print(f"Warning: Chunk {i+1} analysis failed: {chunk_insights['error']}")
                except Exception as e:
                    print(f"Error analyzing chunk {i+1}: {e}")
                    continue
            
            # Calculate averages
            if len(all_chunk_insights) > 0:
                quantitative_metrics['avg_score'] /= len(all_chunk_insights)
                quantitative_metrics['avg_comments'] /= len(all_chunk_insights)
                quantitative_metrics['engagement_rate'] = (quantitative_metrics['avg_score'] + quantitative_metrics['avg_comments']) / 2
            
            # Combine insights from all chunks
            if all_chunk_insights:
                combined_insights = self.combine_chunk_insights(all_chunk_insights, quantitative_metrics)
            else:
                print("Warning: All chunks failed. Falling back to original analysis method.")
                combined_insights = self.analyze_market_insights(posts, idea_data)
            
        else:
            # For smaller datasets, use the original method
            combined_insights = self.analyze_market_insights(posts, idea_data)
        
        # Store research data with references
        self.research_data = {
            'keywords_used': keywords,
            'posts_collected': posts,
            'insights': combined_insights,
            'references': self.references,
            'quantitative_data': self.calculate_comprehensive_metrics(posts)
        }
        
        return self.research_data
    
    def combine_chunk_insights(self, chunk_insights: List[Dict[str, Any]], quantitative_metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Combine insights from multiple chunks into a comprehensive analysis"""
        
        # Aggregate user feedback
        all_complaints = []
        all_needs = []
        all_pain_points = []
        all_feature_requests = []
        
        for chunk in chunk_insights:
            if 'user_feedback' in chunk:
                uf = chunk['user_feedback']
                all_complaints.extend(uf.get('common_complaints', []))
                all_needs.extend(uf.get('expressed_needs', []))
                all_pain_points.extend(uf.get('pain_points', []))
                all_feature_requests.extend(uf.get('feature_requests', []))
        
        # Remove duplicates and get top items
        all_complaints = list(set(all_complaints))[:10]
        all_needs = list(set(all_needs))[:10]
        all_pain_points = list(set(all_pain_points))[:10]
        all_feature_requests = list(set(all_feature_requests))[:10]
        
        # Aggregate market insights
        all_trends = []
        all_opportunities = []
        all_challenges = []
        
        for chunk in chunk_insights:
            if 'market_insights' in chunk:
                mi = chunk['market_insights']
                all_trends.extend(mi.get('trends_identified', []))
                all_opportunities.extend(mi.get('opportunities', []))
                all_challenges.extend(mi.get('challenges', []))
        
        # Remove duplicates
        all_trends = list(set(all_trends))[:10]
        all_opportunities = list(set(all_opportunities))[:10]
        all_challenges = list(set(all_challenges))[:10]
        
        return {
            'quantitative_metrics': quantitative_metrics,
            'user_feedback': {
                'common_complaints': all_complaints,
                'expressed_needs': all_needs,
                'pain_points': all_pain_points,
                'feature_requests': all_feature_requests,
                'user_sentiment': 'Aggregated from multiple chunks'
            },
            'market_insights': {
                'trends_identified': all_trends,
                'opportunities': all_opportunities,
                'challenges': all_challenges
            },
            'posts_analyzed': quantitative_metrics['total_posts'],
            'chunks_analyzed': quantitative_metrics['chunks_analyzed']
        }
    
    def calculate_comprehensive_metrics(self, posts: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate comprehensive quantitative metrics from Reddit posts"""
        
        if not posts:
            return {}
        
        scores = [post.get('score', 0) for post in posts]
        comments = [post.get('num_comments', 0) for post in posts]
        sentiments = [post.get('sentiment_data', {}).get('compound', 0) for post in posts]
        
        # Calculate metrics
        total_posts = len(posts)
        avg_score = sum(scores) / total_posts if scores else 0
        avg_comments = sum(comments) / total_posts if comments else 0
        engagement_rate = (avg_score + avg_comments) / 2
        
        # Sentiment breakdown
        positive = len([s for s in sentiments if s > 0.1])
        neutral = len([s for s in sentiments if -0.1 <= s <= 0.1])
        negative = len([s for s in sentiments if s < -0.1])
        
        # Top performing posts
        top_posts = sorted(posts, key=lambda x: x.get('score', 0), reverse=True)[:5]
        
        # Subreddit distribution
        subreddit_counts = Counter([post.get('subreddit', 'unknown') for post in posts])
        
        # High engagement posts using config thresholds
        high_engagement_posts = [
            p for p in posts 
            if p.get('score', 0) > MIN_ENGAGEMENT_SCORE or p.get('num_comments', 0) > MIN_COMMENTS_THRESHOLD
        ]
        
        return {
            'total_posts_analyzed': total_posts,
            'average_score': round(avg_score, 2),
            'average_comments': round(avg_comments, 2),
            'engagement_rate': round(engagement_rate, 2),
            'sentiment_distribution': {
                'positive': positive,
                'neutral': neutral,
                'negative': negative,
                'total': total_posts,
                'positive_percentage': round((positive / total_posts) * 100, 1) if total_posts > 0 else 0,
                'neutral_percentage': round((neutral / total_posts) * 100, 1) if total_posts > 0 else 0,
                'negative_percentage': round((negative / total_posts) * 100, 1) if total_posts > 0 else 0
            },
            'top_performing_posts': [
                {
                    'title': post.get('title', ''),
                    'score': post.get('score', 0),
                    'comments': post.get('num_comments', 0),
                    'url': post.get('url', ''),  # Use the already constructed URL
                    'subreddit': post.get('subreddit', '')
                } for post in top_posts
            ],
            'subreddit_distribution': dict(subreddit_counts.most_common(10)),
            'high_engagement_posts': len(high_engagement_posts),
            'engagement_percentage': round((len(high_engagement_posts) / total_posts) * 100, 1) if total_posts > 0 else 0
        } 