import os
from dotenv import load_dotenv

load_dotenv()

# Import from existing settings
import sys
sys.path.append('..')
from settings import OPENAI_API_KEY, REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET

# Model Configuration for each agent
MODEL_CONFIG = {
    'clarifier': 'gpt-4o-mini',  # Fast, cost-effective for Q&A
    'research': 'gpt-4o',        # More capable for research analysis
    'validation': 'gpt-4o',      # Complex analysis
    'roadmap': 'gpt-4o',         # Strategic thinking
    'report': 'gpt-4o',          # Detailed report generation
    'refiner': 'gpt-4o'          # Final refinement
}

# Reddit subreddits for research (focused on business, entrepreneurship, startups)
RESEARCH_SUBREDDITS = [
    'entrepreneur',
    'startups', 
    'smallbusiness',
    'business',
    'marketing',
    'productivity',
    'technology',
    'webdev',
    'programming',
    'SaaS'
]

# Analysis parameters
MAX_REDDIT_POSTS = 50  # Per subreddit
MIN_RELEVANCE_SCORE = 3
TIME_FILTER = 'month'  # 'hour', 'day', 'week', 'month', 'year', 'all'

# Chunking configuration for large datasets
CHUNK_SIZE = 20  # Number of posts per chunk for LLM analysis
MAX_CHUNKS = 10  # Maximum number of chunks to process
LARGE_DATASET_THRESHOLD = 20  # Threshold to trigger chunking

# Quantitative analysis parameters
MIN_ENGAGEMENT_SCORE = 5  # Minimum score for high engagement posts
MIN_COMMENTS_THRESHOLD = 3  # Minimum comments for high engagement
SENTIMENT_THRESHOLDS = {
    'positive': 0.1,
    'negative': -0.1,
    'neutral_lower': -0.1,
    'neutral_upper': 0.1
}

# Report configuration
REPORT_OUTPUT_DIR = 'idea_potential/reports'
REPORT_TEMPLATE = 'comprehensive' 