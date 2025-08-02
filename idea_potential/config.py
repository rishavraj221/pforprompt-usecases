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

# Report configuration
REPORT_OUTPUT_DIR = 'idea_potential/reports'
REPORT_TEMPLATE = 'comprehensive' 