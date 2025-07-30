# Reddit Integration Setup Guide

## Overview

The Reality Miner Agent now includes Reddit PRAW integration for real market research and validation. This allows the system to search Reddit for relevant posts, analyze sentiment, and identify market opportunities and pain points.

## Features

- **Real-time Reddit Research**: Searches relevant subreddits for idea validation using AsyncPRAW
- **Async-Compatible**: Properly designed for asynchronous environments
- **Sentiment Analysis**: Uses VADER + TextBlob for comprehensive sentiment scoring
- **Market Research**: Identifies existing solutions, pain points, and opportunities
- **Competitive Analysis**: Analyzes user feedback on existing products
- **Keyword Extraction**: Automatically extracts relevant keywords from user ideas

## Setup Instructions

### 1. Install Dependencies (uv managed)

The project uses `uv` for dependency management. Dependencies are already configured in `pyproject.toml`:

```bash
# Install all dependencies including Reddit integration
uv sync

# Or if you need to add dependencies manually
uv add asyncpraw textblob vaderSentiment nltk python-dotenv
```

### 2. Set Up Reddit API Credentials

1. Go to https://www.reddit.com/prefs/apps
2. Click "Create App" or "Create Another App"
3. Fill in the details:
   - **Name**: IdeaValidationBot
   - **Type**: Script
   - **Description**: Bot for idea validation research
   - **About URL**: (leave blank)
   - **Redirect URI**: http://localhost:8080

4. Note your credentials:
   - **Client ID**: The string under your app name
   - **Client Secret**: The "secret" field

### 3. Configure Environment Variables

Create a `.env` file in your project root:

```env
# Reddit API Credentials
REDDIT_CLIENT_ID=your_client_id_here
REDDIT_CLIENT_SECRET=your_client_secret_here

# OpenAI API Key
OPENAI_API_KEY=your_openai_api_key_here
```

### 4. Test the Integration

Run the test script to verify everything works:

```bash
# Using uv to run the test
uv run python test_reddit_integration.py

# Or activate the environment first
uv shell
python test_reddit_integration.py
```

## How It Works

### 1. Keyword Extraction
The system automatically extracts relevant keywords from your idea:
- Filters out common stop words
- Identifies business/tech terms
- Limits to top 10 most relevant keywords

### 2. Reddit Search Strategy
Searches multiple subreddits:
- **General**: startups, entrepreneur, smallbusiness, business
- **Tech**: technology, software, webdev, mobileapp
- **Niche**: saas, indiehackers, sidehustle

### 3. Sentiment Analysis
Uses two complementary methods:
- **VADER**: Optimized for social media text
- **TextBlob**: General-purpose sentiment analysis
- **Combined Score**: Average of both for reliability

### 4. Market Research Output
Provides comprehensive analysis:
- **Market Sentiment**: Overall market attitude
- **Existing Solutions**: Competitors and alternatives
- **User Pain Points**: Common problems and frustrations
- **Market Demand**: High/medium/low demand assessment
- **Competitive Landscape**: Market saturation analysis

## Example Output

```json
{
  "reddit_research": {
    "market_sentiment": "positive",
    "existing_solutions": [
      {
        "name": "ClassPass",
        "description": "Fitness class booking platform",
        "user_sentiment": "mixed",
        "strengths": ["wide selection", "good pricing"],
        "weaknesses": ["limited locations", "booking issues"]
      }
    ],
    "user_pain_points": [
      "difficulty finding local classes",
      "expensive membership fees",
      "lack of variety in workouts"
    ],
    "market_demand": "high",
    "competitive_landscape": "competitive"
  }
}
```

## Subreddits Searched

The system searches these subreddits for market research:

### Business & Entrepreneurship
- r/startups
- r/entrepreneur
- r/smallbusiness
- r/business

### Technology
- r/technology
- r/software
- r/webdev
- r/mobileapp

### Niche Communities
- r/productivity
- r/saas
- r/indiehackers
- r/sidehustle

## Error Handling

The system gracefully handles:
- **Missing Reddit credentials**: Falls back to basic analysis
- **API rate limits**: Implements delays between requests
- **Network issues**: Continues with available data
- **Invalid subreddits**: Skips problematic subreddits

## Performance Notes

- **Search Limit**: 50 posts per subreddit to respect rate limits
- **Rate Limiting**: 0.1 second delay between requests
- **Caching**: Results are not cached (fresh data each run)
- **Processing Time**: ~30-60 seconds for comprehensive research

## Troubleshooting

### Common Issues

1. **"AsyncPRAW not available"**
   - Install dependencies: `uv sync`
   - Or add manually: `uv add asyncpraw`

2. **"Reddit integration failed"**
   - Check your Reddit credentials in `.env`
   - Verify your Reddit app is set to "Script" type

3. **"No posts found"**
   - Try different keywords in your idea
   - Check if your idea is too niche for general subreddits

4. **Rate limit errors**
   - The system automatically handles rate limits
   - If persistent, wait a few minutes and try again

### Debug Mode

To see detailed Reddit search logs, the system prints:
- Keywords being searched
- Subreddits being scanned
- Number of relevant posts found
- Sentiment analysis results

## Running Tests with uv

```bash
# Run the Reddit integration test
uv run python test_reddit_integration.py

# Run the validation fix test
uv run python test_validation_fix.py

# Run the report saving test
uv run python test_report_saving.py

# Run the main example
uv run python -m idea_refinement_engine.example
```

## Security Notes

- **API Credentials**: Never commit your `.env` file to version control
- **Rate Limits**: The system respects Reddit's API limits
- **Data Privacy**: Only public Reddit posts are analyzed
- **User Privacy**: No personal data is collected or stored

## uv Commands Reference

```bash
# Install dependencies
uv sync

# Add a new dependency
uv add package_name

# Run a script
uv run python script.py

# Activate virtual environment
uv shell

# Update dependencies
uv lock --upgrade
``` 