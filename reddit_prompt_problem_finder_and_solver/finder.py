import praw
import re
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from collections import Counter
import time
from settings import REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET

class RedditPromptFilter:
    def __init__(self, reddit_instance):
        self.reddit = reddit_instance
        self.vader_analyzer = SentimentIntensityAnalyzer()
        
        # Configuration
        self.SUBREDDITS = ["ChatGPT", "LocalLLaMA", "PromptEngineering", "MachineLearning"]
        
        # Core problem indicators
        self.TARGET_KEYWORDS = [
            "hallucinat", "inaccur", "wrong output", "format fail", 
            "not following", "ignore", "broken", "fix prompt", 
            "improve prompt", "better results", "struggling with",
            "prompt engineering", "prompt design", "system prompt",
            "doesn't work", "not working", "failed", "error",
            "inconsistent", "unreliable", "poor quality",
            "how to prompt", "prompting technique", "better prompt",
            "prompt help", "template", "example prompt"
        ]
        
        # Negative sentiment triggers
        self.NEGATIVE_TRIGGERS = [
            "frustrat", "annoy", "ridiculous", "wtf", "sucks", "pissed",
            "terrible", "awful", "horrible", "useless", "garbage",
            "disappointed", "confused", "stuck", "lost", "help me",
            "desperate", "giving up", "can't figure", "no idea"
        ]
        
        # Solution-seeking patterns
        self.SOLUTION_PATTERNS = [
            r"how (?:do|can) (?:i|you)",
            r"what(?:'s| is) the best",
            r"any(?:one| suggestions?)",
            r"need help",
            r"looking for",
            r"tried everything",
            r"nothing works",
            r"still not working"
        ]
        
        # Quality indicators (for scoring)
        self.QUALITY_INDICATORS = {
            'problem_description': ['specific', 'example', 'tried', 'expected', 'actual'],
            'effort_shown': ['attempted', 'tested', 'experimented', 'various', 'multiple'],
            'technical_depth': ['parameters', 'temperature', 'tokens', 'model', 'api']
        }

    def preprocess_text(self, text):
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

    def calculate_sentiment_score(self, text):
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

    def count_keyword_matches(self, text, keywords):
        """Count keyword matches with partial matching"""
        text_lower = text.lower()
        matches = []
        
        for keyword in keywords:
            # Use regex for partial matching
            pattern = re.compile(r'\b\w*' + re.escape(keyword.lower()) + r'\w*\b')
            found_matches = pattern.findall(text_lower)
            matches.extend(found_matches)
        
        return len(matches), matches

    def detect_solution_seeking(self, text):
        """Detect if post is seeking solutions/help"""
        solution_score = 0
        patterns_found = []
        
        for pattern in self.SOLUTION_PATTERNS:
            if re.search(pattern, text, re.IGNORECASE):
                solution_score += 1
                patterns_found.append(pattern)
        
        # Question marks indicate questions
        question_marks = text.count('?')
        solution_score += min(question_marks, 3)  # Cap at 3
        
        return solution_score, patterns_found

    def calculate_post_quality_score(self, title, text):
        """Assess post quality and effort"""
        combined_text = f"{title} {text}".lower()
        quality_score = 0
        
        # Length indicates effort
        if len(combined_text) > 200:
            quality_score += 2
        elif len(combined_text) > 100:
            quality_score += 1
        
        # Check for quality indicators
        for category, indicators in self.QUALITY_INDICATORS.items():
            category_score = sum(1 for indicator in indicators if indicator in combined_text)
            quality_score += min(category_score, 3)  # Cap per category
        
        # Code blocks indicate technical content
        if '```' in text or '`' in text:
            quality_score += 2
        
        return quality_score

    def is_prompt_related(self, title, text):
        """Check if post is related to prompting/LLM issues"""
        combined_text = f"{title} {text}".lower()
        
        prompt_keywords = [
            'prompt', 'gpt', 'llm', 'ai', 'model', 'response', 'output',
            'generate', 'chat', 'assistant', 'instruction', 'system message'
        ]
        
        return any(keyword in combined_text for keyword in prompt_keywords)

    def analyze_post(self, post):
        """Comprehensive post analysis"""
        title = post.title or ""
        selftext = post.selftext or ""
        
        # Preprocess text
        clean_title = self.preprocess_text(title)
        clean_text = self.preprocess_text(selftext)
        combined_text = f"{clean_title} {clean_text}"
        
        # Skip if not prompt-related
        if not self.is_prompt_related(title, selftext):
            return None
        
        # Calculate sentiment
        sentiment_data = self.calculate_sentiment_score(combined_text)
        
        # Count keyword matches
        target_count, target_matches = self.count_keyword_matches(combined_text, self.TARGET_KEYWORDS)
        negative_count, negative_matches = self.count_keyword_matches(combined_text, self.NEGATIVE_TRIGGERS)
        
        # Detect solution seeking
        solution_score, solution_patterns = self.detect_solution_seeking(combined_text)
        
        # Calculate quality score
        quality_score = self.calculate_post_quality_score(title, selftext)
        
        # Calculate overall relevance score
        relevance_score = (
            target_count * 3 +  # Target keywords are most important
            negative_count * 2 +  # Negative sentiment adds weight
            solution_score * 1.5 +  # Solution seeking is important
            quality_score * 0.5 +  # Quality is a bonus
            (1 if sentiment_data['combined_sentiment'] < -0.1 else 0) * 2  # Negative sentiment
        )
        
        return {
            'post_id': post.id,
            'title': title,
            'selftext': selftext[:500] + "..." if len(selftext) > 500 else selftext,
            'subreddit': str(post.subreddit),
            'author': str(post.author) if post.author else '[deleted]',
            'score': post.score,
            'upvote_ratio': post.upvote_ratio,
            'num_comments': post.num_comments,
            'created_utc': post.created_utc,
            'url': f"https://reddit.com{post.permalink}",
            
            # Analysis results
            'relevance_score': relevance_score,
            'target_keyword_count': target_count,
            'target_matches': target_matches,
            'negative_trigger_count': negative_count,
            'negative_matches': negative_matches,
            'solution_seeking_score': solution_score,
            'solution_patterns': solution_patterns,
            'quality_score': quality_score,
            'sentiment_data': sentiment_data,
            
            # Filtering criteria
            'is_negative_sentiment': sentiment_data['combined_sentiment'] < -0.1,
            'has_frustration': negative_count > 0,
            'seeks_solution': solution_score > 0,
            'mentions_prompting': target_count > 0
        }

    def filter_posts(self, time_filter='week', limit=100, min_relevance_score=3):
        """Filter posts from multiple subreddits"""
        filtered_posts = []
        
        for subreddit_name in self.SUBREDDITS:
            print(f"Scanning r/{subreddit_name}...")
            
            try:
                subreddit = self.reddit.subreddit(subreddit_name)
                
                # Get posts from different sorting methods
                post_sources = [
                    subreddit.hot(limit=limit//4),
                    subreddit.new(limit=limit//4),
                    subreddit.top(time_filter=time_filter, limit=limit//4),
                    subreddit.rising(limit=limit//4)
                ]
                
                seen_ids = set()
                
                for posts in post_sources:
                    for post in posts:
                        if post.id in seen_ids:
                            continue
                        seen_ids.add(post.id)
                        
                        analysis = self.analyze_post(post)
                        
                        if analysis and analysis['relevance_score'] >= min_relevance_score:
                            filtered_posts.append(analysis)
                        
                        # Rate limiting
                        time.sleep(0.1)
                
            except Exception as e:
                print(f"Error scanning r/{subreddit_name}: {e}")
                continue
        
        # Sort by relevance score
        filtered_posts.sort(key=lambda x: x['relevance_score'], reverse=True)
        
        return filtered_posts

    def print_analysis_summary(self, posts):
        """Print summary of filtered posts"""
        if not posts:
            print("No posts found matching criteria.")
            return
        
        print(f"\n📊 ANALYSIS SUMMARY")
        print(f"Total filtered posts: {len(posts)}")
        print(f"Average relevance score: {sum(p['relevance_score'] for p in posts) / len(posts):.2f}")
        
        # Subreddit distribution
        subreddit_counts = Counter(p['subreddit'] for p in posts)
        print(f"\n📍 Subreddit distribution:")
        for sub, count in subreddit_counts.most_common():
            print(f"  r/{sub}: {count}")
        
        # Most common issues
        all_target_matches = []
        for post in posts:
            all_target_matches.extend(post['target_matches'])
        
        if all_target_matches:
            print(f"\n🎯 Most common issues:")
            for issue, count in Counter(all_target_matches).most_common(10):
                print(f"  {issue}: {count}")

    def print_top_posts(self, posts, top_n=10):
        """Print top filtered posts"""
        print(f"\n🔥 TOP {min(top_n, len(posts))} FILTERED POSTS:")
        
        for i, post in enumerate(posts[:top_n], 1):
            print(f"\n{i}. [{post['relevance_score']:.1f}] r/{post['subreddit']}")
            print(f"   Title: {post['title']}")
            print(f"   Author: {post['author']} | Score: {post['score']} | Comments: {post['num_comments']}")
            print(f"   Issues: {', '.join(post['target_matches'][:3])}")
            print(f"   Sentiment: {post['sentiment_data']['combined_sentiment']:.2f}")
            print(f"   URL: {post['url']}")

    def generate_markdown_report(self, posts, output_file_path):
        """Generate comprehensive markdown analysis report"""
        from datetime import datetime
        import os
        
        if not posts:
            print("No posts to generate report for.")
            return
        
        # Calculate statistics
        total_posts = len(posts)
        avg_relevance = sum(p['relevance_score'] for p in posts) / total_posts
        avg_sentiment = sum(p['sentiment_data']['combined_sentiment'] for p in posts) / total_posts
        
        # Subreddit distribution
        subreddit_counts = Counter(p['subreddit'] for p in posts)
        
        # Issue analysis
        all_target_matches = []
        all_negative_matches = []
        all_solution_patterns = []
        
        for post in posts:
            all_target_matches.extend(post['target_matches'])
            all_negative_matches.extend(post['negative_matches'])
            all_solution_patterns.extend(post['solution_patterns'])
        
        top_issues = Counter(all_target_matches).most_common(15)
        top_frustrations = Counter(all_negative_matches).most_common(10)
        top_solution_patterns = Counter(all_solution_patterns).most_common(10)
        
        # Sentiment analysis
        very_negative = len([p for p in posts if p['sentiment_data']['combined_sentiment'] < -0.3])
        negative = len([p for p in posts if -0.3 <= p['sentiment_data']['combined_sentiment'] < -0.1])
        neutral = len([p for p in posts if -0.1 <= p['sentiment_data']['combined_sentiment'] < 0.1])
        positive = len([p for p in posts if p['sentiment_data']['combined_sentiment'] >= 0.1])
        
        # Quality distribution
        high_quality = len([p for p in posts if p['quality_score'] >= 8])
        medium_quality = len([p for p in posts if 4 <= p['quality_score'] < 8])
        low_quality = len([p for p in posts if p['quality_score'] < 4])
        
        # Generate markdown content
        markdown_content = f"""# Reddit Prompting Issues Analysis Report

**Generated on:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**Analysis Period:** Recent posts from selected subreddits  
**Total Posts Analyzed:** {total_posts}

---

## 📊 Executive Summary

This report analyzes Reddit posts from AI/ML communities to identify users struggling with prompting and LLM outputs. The analysis uses advanced sentiment analysis, keyword matching, and behavioral pattern recognition to surface high-value opportunities for prompting assistance.

### Key Metrics
- **Average Relevance Score:** {avg_relevance:.2f}/10
- **Average Sentiment Score:** {avg_sentiment:.2f} (negative indicates frustration)
- **Posts with Negative Sentiment:** {very_negative + negative} ({((very_negative + negative)/total_posts)*100:.1f}%)
- **Solution-Seeking Posts:** {len([p for p in posts if p['seeks_solution']])} ({(len([p for p in posts if p['seeks_solution']])/total_posts)*100:.1f}%)

---

## 🎯 Subreddit Distribution

| Subreddit | Posts | Percentage |
|-----------|--------|------------|
"""
        
        for subreddit, count in subreddit_counts.most_common():
            percentage = (count / total_posts) * 100
            markdown_content += f"| r/{subreddit} | {count} | {percentage:.1f}% |\n"
        
        markdown_content += f"""
---

## 🔍 Issue Categories Analysis

### Most Common Problems Identified

| Issue Type | Frequency | Description |
|------------|-----------|-------------|
"""
        
        for issue, count in top_issues:
            percentage = (count / len(all_target_matches)) * 100 if all_target_matches else 0
            markdown_content += f"| {issue} | {count} ({percentage:.1f}%) | Problem keyword detected in posts |\n"
        
        markdown_content += f"""
### Frustration Indicators

| Frustration Type | Frequency | Emotional Intensity |
|------------------|-----------|-------------------|
"""
        
        for frustration, count in top_frustrations:
            percentage = (count / len(all_negative_matches)) * 100 if all_negative_matches else 0
            markdown_content += f"| {frustration} | {count} ({percentage:.1f}%) | High negative sentiment |\n"
        
        markdown_content += f"""
---

## 📈 Sentiment Analysis Breakdown

| Sentiment Category | Count | Percentage | Description |
|-------------------|--------|------------|-------------|
| Very Negative (<-0.3) | {very_negative} | {(very_negative/total_posts)*100:.1f}% | Highly frustrated users |
| Negative (-0.3 to -0.1) | {negative} | {(negative/total_posts)*100:.1f}% | Mildly frustrated users |
| Neutral (-0.1 to 0.1) | {neutral} | {(neutral/total_posts)*100:.1f}% | Neutral tone |
| Positive (>0.1) | {positive} | {(positive/total_posts)*100:.1f}% | Positive/satisfied users |

---

## 💡 Solution-Seeking Patterns

| Pattern Type | Frequency | Example Context |
|--------------|-----------|-----------------|
"""
        
        for pattern, count in top_solution_patterns:
            percentage = (count / len(all_solution_patterns)) * 100 if all_solution_patterns else 0
            markdown_content += f"| {pattern} | {count} ({percentage:.1f}%) | Question/help-seeking pattern |\n"
        
        markdown_content += f"""
---

## 📋 Post Quality Assessment

| Quality Level | Count | Percentage | Characteristics |
|---------------|--------|------------|-----------------|
| High Quality (8+) | {high_quality} | {(high_quality/total_posts)*100:.1f}% | Detailed, technical, shows effort |
| Medium Quality (4-7) | {medium_quality} | {(medium_quality/total_posts)*100:.1f}% | Moderate detail and effort |
| Low Quality (<4) | {low_quality} | {(low_quality/total_posts)*100:.1f}% | Brief, lacking context |

---

## 🔥 Top Priority Posts for Intervention

*Posts ranked by relevance score - highest potential for prompting assistance*

"""
        
        # Add top posts
        for i, post in enumerate(posts[:200], 1):
            # Format timestamp
            post_date = datetime.fromtimestamp(post['created_utc']).strftime('%Y-%m-%d %H:%M')
            
            # Truncate text for readability
            preview_text = post['selftext'][:200] + "..." if len(post['selftext']) > 200 else post['selftext']
            
            # Key issues identified
            key_issues = ', '.join(post['target_matches'][:3]) if post['target_matches'] else 'None specified'
            
            markdown_content += f"""
### {i}. [{post['relevance_score']:.1f}/10] {post['title']}

**Subreddit:** r/{post['subreddit']}  
**Author:** u/{post['author']}  
**Posted:** {post_date}  
**Engagement:** {post['score']} points, {post['num_comments']} comments  
**Upvote Ratio:** {post['upvote_ratio']:.2f}

**🎯 Relevance Score:** {post['relevance_score']:.1f}/10  
**😟 Sentiment Score:** {post['sentiment_data']['combined_sentiment']:.2f} ({'Negative' if post['sentiment_data']['combined_sentiment'] < -0.1 else 'Neutral/Positive'})  
**🔧 Quality Score:** {post['quality_score']}/15  

**Key Issues Identified:** {key_issues}  
**Frustration Indicators:** {', '.join(post['negative_matches'][:3]) if post['negative_matches'] else 'None'}  
**Solution-Seeking Score:** {post['solution_seeking_score']}

**Post Preview:**
> {preview_text}

**🔗 [View Full Post]({post['url']})**

**Analysis Flags:**
- {'✅' if post['mentions_prompting'] else '❌'} Mentions prompting/LLM issues
- {'✅' if post['has_frustration'] else '❌'} Shows frustration indicators  
- {'✅' if post['seeks_solution'] else '❌'} Actively seeking solutions
- {'✅' if post['is_negative_sentiment'] else '❌'} Negative sentiment detected

---
"""
        
        # Add detailed statistics section
        markdown_content += f"""
## 📊 Detailed Analytics

### Keyword Distribution Analysis

#### Target Keywords (Problem Indicators)
"""
        
        for keyword in ["hallucinat", "inaccur", "wrong output", "not following", "broken", "fix prompt"]:
            count = sum(1 for matches in [p['target_matches'] for p in posts] for match in matches if keyword in match)
            if count > 0:
                markdown_content += f"- **{keyword}**: {count} occurrences\n"
        
        markdown_content += f"""
#### Negative Sentiment Keywords
"""
        
        for keyword in ["frustrat", "annoy", "ridiculous", "sucks", "terrible", "useless"]:
            count = sum(1 for matches in [p['negative_matches'] for p in posts] for match in matches if keyword in match)
            if count > 0:
                markdown_content += f"- **{keyword}**: {count} occurrences\n"
        
        markdown_content += f"""
### Engagement Metrics

- **Average Post Score:** {sum(p['score'] for p in posts) / total_posts:.1f}
- **Average Comments:** {sum(p['num_comments'] for p in posts) / total_posts:.1f}
- **Average Upvote Ratio:** {sum(p['upvote_ratio'] for p in posts) / total_posts:.2f}

### Most Engaged Posts (by comments)

"""
        
        # Sort by comments for engagement analysis
        most_commented = sorted(posts, key=lambda x: x['num_comments'], reverse=True)[:5]
        
        for i, post in enumerate(most_commented, 1):
            markdown_content += f"{i}. **{post['title']}** - {post['num_comments']} comments ([Link]({post['url']}))\n"
        
        markdown_content += f"""
---

## 🎯 Recommendations

### High-Priority Intervention Opportunities

1. **Focus on High-Frustration Posts**: {very_negative + negative} posts show negative sentiment
2. **Target Solution Seekers**: {len([p for p in posts if p['seeks_solution']])} posts actively seeking help
3. **Quality Content First**: Prioritize {high_quality} high-quality posts for maximum impact

### Common Prompting Issues to Address

Based on the analysis, users frequently struggle with:
"""
        
        # Add top 5 issues as recommendations
        for issue, count in top_issues[:5]:
            markdown_content += f"- **{issue.title()}** ({count} mentions)\n"
        
        markdown_content += f"""
### Subreddit Strategy

- **r/{subreddit_counts.most_common(1)[0][0]}**: Highest volume ({subreddit_counts.most_common(1)[0][1]} posts) - primary target
- Focus on posts with relevance scores above {avg_relevance:.1f}
- Prioritize posts with negative sentiment (<-0.1) for immediate assistance

---

## 📁 Data Export Summary

- **Total Posts Filtered:** {total_posts}
- **Date Range:** Recent posts (within analysis timeframe)
- **Filtering Criteria:** Relevance score ≥ minimum threshold
- **Analysis Methods:** VADER + TextBlob sentiment analysis, regex pattern matching

*This report was generated automatically by the Reddit Prompting Issues Filter tool.*
"""
        
        # Write to file
        try:
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
            
            with open(output_file_path, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
            
            print(f"\n✅ Detailed analysis report generated: {output_file_path}")
            print(f"📄 Report contains {total_posts} filtered posts with comprehensive analysis")
            
        except Exception as e:
            print(f"❌ Error writing report to {output_file_path}: {e}")
            # Fallback - print to console
            print("\n" + "="*50)
            print("MARKDOWN REPORT (couldn't write to file):")
            print("="*50)
            print(markdown_content[:2000] + "... [truncated]")


# Usage example
def fetch_reddit_posts(report_file_path="reddit_prompting_analysis_report.md"):
    # Initialize Reddit instance (you need to set up your credentials)
    reddit = praw.Reddit(
        client_id=REDDIT_CLIENT_ID,
        client_secret=REDDIT_CLIENT_SECRET,
        user_agent="Repulsive_Appeal6381"
    )
    
    # Create filter instance
    filter_bot = RedditPromptFilter(reddit)
    
    # Filter posts
    print("🔍 Starting Reddit post filtering...")
    filtered_posts = filter_bot.filter_posts(
        time_filter='week',  # 'hour', 'day', 'week', 'month', 'year', 'all'
        limit=200,  # Posts per subreddit per sorting method
        min_relevance_score=4  # Minimum score to include
    )
    
    # Print console summary
    filter_bot.print_analysis_summary(filtered_posts)
    filter_bot.print_top_posts(filtered_posts, top_n=15)
    
    # Generate detailed markdown report
    filter_bot.generate_markdown_report(filtered_posts, report_file_path)
    
    return filtered_posts