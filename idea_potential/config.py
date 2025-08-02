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

# Dynamic subreddit mapping based on idea categories
SUBREDDIT_CATEGORIES = {
    # AI/ML/Technology
    'ai': ['artificial', 'MachineLearning', 'OpenAI', 'ChatGPT', 'AI', 'artificialintelligence', 'deeplearning', 'datascience'],
    'machine_learning': ['MachineLearning', 'deeplearning', 'datascience', 'MLjobs', 'learnmachinelearning'],
    'programming': ['programming', 'learnprogramming', 'webdev', 'javascript', 'Python', 'reactjs', 'node'],
    'technology': ['technology', 'tech', 'gadgets', 'Futurology', 'science'],
    
    # Business/Startup
    'business': ['business', 'entrepreneur', 'startups', 'smallbusiness', 'SaaS', 'marketing'],
    'entrepreneurship': ['entrepreneur', 'startups', 'smallbusiness', 'SaaS', 'entrepreneurship'],
    'startups': ['startups', 'entrepreneur', 'SaaS', 'smallbusiness', 'startup'],
    
    # Developer/Engineering
    'development': ['programming', 'webdev', 'javascript', 'Python', 'reactjs', 'node', 'learnprogramming'],
    'software_engineering': ['programming', 'softwareengineering', 'webdev', 'cscareerquestions'],
    'web_development': ['webdev', 'javascript', 'reactjs', 'node', 'frontend', 'backend'],
    
    # Creative/Design
    'design': ['design', 'graphic_design', 'UI_Design', 'UX_Design', 'web_design'],
    'creative': ['design', 'graphic_design', 'UI_Design', 'UX_Design', 'creative'],
    
    # Finance/Economics
    'finance': ['finance', 'personalfinance', 'investing', 'wallstreetbets', 'stocks'],
    'cryptocurrency': ['cryptocurrency', 'bitcoin', 'ethereum', 'cryptomarkets'],
    
    # Health/Wellness
    'health': ['health', 'fitness', 'nutrition', 'mentalhealth', 'medicine'],
    'fitness': ['fitness', 'bodybuilding', 'running', 'yoga', 'nutrition'],
    
    # Education/Learning
    'education': ['education', 'learnprogramming', 'learnmachinelearning', 'learnpython', 'learnjavascript'],
    'learning': ['learnprogramming', 'learnmachinelearning', 'learnpython', 'learnjavascript', 'education'],
    
    # Gaming/Entertainment
    'gaming': ['gaming', 'pcgaming', 'PS5', 'XboxSeriesX', 'NintendoSwitch'],
    'entertainment': ['movies', 'television', 'music', 'books', 'gaming'],
    
    # Lifestyle/Personal
    'lifestyle': ['lifestyle', 'productivity', 'selfimprovement', 'personalfinance', 'fitness'],
    'productivity': ['productivity', 'selfimprovement', 'getmotivated', 'lifestyle'],
    
    # Marketplace/E-commerce
    'marketplace': ['ecommerce', 'shopify', 'amazon', 'ebay', 'etsy'],
    'ecommerce': ['ecommerce', 'shopify', 'amazon', 'ebay', 'etsy', 'dropshipping'],
    
    # Community/Social
    'community': ['community', 'social', 'discussion', 'askreddit', 'casualconversation'],
    'social_media': ['socialmedia', 'marketing', 'instagram', 'facebook', 'twitter'],
    
    # Tools/Utilities
    'tools': ['tools', 'productivity', 'software', 'programming', 'technology'],
    'utilities': ['tools', 'productivity', 'software', 'programming'],
    
    # Prompt Engineering Specific
    'prompt_engineering': ['artificial', 'MachineLearning', 'OpenAI', 'ChatGPT', 'AI', 'programming', 'datascience'],
    'llm': ['artificial', 'MachineLearning', 'OpenAI', 'ChatGPT', 'AI', 'datascience'],
    'language_models': ['artificial', 'MachineLearning', 'OpenAI', 'ChatGPT', 'AI', 'datascience'],
    
    # Forum/Community Platform
    'forum': ['community', 'discussion', 'askreddit', 'casualconversation', 'social'],
    'platform': ['programming', 'webdev', 'technology', 'startups', 'SaaS'],
    
    # Marketplace/Exchange
    'marketplace_platform': ['ecommerce', 'startups', 'SaaS', 'programming', 'webdev'],
    'exchange': ['cryptocurrency', 'finance', 'investing', 'programming', 'technology']
}

# Keyword to category mapping for better subreddit selection
KEYWORD_CATEGORY_MAPPING = {
    # AI/ML Keywords
    'ai': 'ai', 'artificial intelligence': 'ai', 'machine learning': 'machine_learning', 'ml': 'machine_learning',
    'deep learning': 'machine_learning', 'neural network': 'machine_learning', 'data science': 'machine_learning',
    'chatgpt': 'ai', 'openai': 'ai', 'gpt': 'ai', 'llm': 'llm', 'large language model': 'llm',
    'language model': 'llm', 'prompt': 'prompt_engineering', 'prompt engineering': 'prompt_engineering',
    'prompting': 'prompt_engineering', 'prompt optimization': 'prompt_engineering',
    
    # Development Keywords
    'developer': 'development', 'programming': 'development', 'coding': 'development', 'software': 'software_engineering',
    'web development': 'web_development', 'frontend': 'web_development', 'backend': 'web_development',
    'javascript': 'web_development', 'python': 'development', 'react': 'web_development', 'node': 'web_development',
    
    # Business Keywords
    'business': 'business', 'startup': 'startups', 'entrepreneur': 'entrepreneurship', 'saas': 'business',
    'marketplace': 'marketplace_platform', 'platform': 'platform', 'forum': 'forum', 'community': 'community',
    'exchange': 'exchange', 'trading': 'exchange', 'market': 'marketplace_platform',
    
    # Technology Keywords
    'technology': 'technology', 'tech': 'technology', 'software': 'software_engineering', 'app': 'development',
    'application': 'development', 'tool': 'tools', 'utility': 'utilities', 'api': 'development',
    
    # Creative Keywords
    'design': 'design', 'ui': 'design', 'ux': 'design', 'creative': 'creative', 'graphic': 'design',
    
    # Finance Keywords
    'finance': 'finance', 'investment': 'finance', 'trading': 'finance', 'cryptocurrency': 'cryptocurrency',
    'bitcoin': 'cryptocurrency', 'crypto': 'cryptocurrency',
    
    # Health Keywords
    'health': 'health', 'fitness': 'fitness', 'wellness': 'health', 'medical': 'health',
    
    # Education Keywords
    'education': 'education', 'learning': 'learning', 'course': 'education', 'tutorial': 'learning',
    
    # Gaming Keywords
    'gaming': 'gaming', 'game': 'gaming', 'video game': 'gaming', 'entertainment': 'entertainment',
    
    # Lifestyle Keywords
    'lifestyle': 'lifestyle', 'productivity': 'productivity', 'personal': 'lifestyle',
    
    # E-commerce Keywords
    'ecommerce': 'ecommerce', 'shopify': 'ecommerce', 'amazon': 'ecommerce', 'online store': 'ecommerce',
    'dropshipping': 'ecommerce', 'selling': 'ecommerce',
    
    # Social Keywords
    'social': 'social_media', 'social media': 'social_media', 'instagram': 'social_media', 'facebook': 'social_media',
    'twitter': 'social_media', 'community': 'community', 'discussion': 'community', 'forum': 'forum'
}

# Fallback subreddits for when no specific category is found
FALLBACK_SUBREDDITS = [
    'entrepreneur',
    'startups', 
    'smallbusiness',
    'business',
    'technology',
    'programming',
    'webdev',
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