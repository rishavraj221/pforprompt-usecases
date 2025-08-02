# Idea Potential Analysis System

A comprehensive AI-powered system to analyze and validate business ideas through market research, validation frameworks, and strategic planning.

## 🎯 Overview

This system uses a pipeline of specialized AI agents to thoroughly analyze business ideas:

1. **Clarifier Agent** - Asks critical questions to understand the idea
2. **Research Agent** - Gathers market intelligence from Reddit
3. **Validation Agent** - Creates validation matrices and SWOT analysis
4. **Roadmap Agent** - Builds development roadmaps and priority matrices
5. **Report Agent** - Generates comprehensive analysis reports
6. **Refiner Agent** - Cross-checks and validates the final report

## 🚀 Quick Start

### Prerequisites

1. **Python 3.8+**
2. **OpenAI API Key** - Get from [OpenAI Platform](https://platform.openai.com/)
3. **Reddit API Credentials** - Get from [Reddit Apps](https://www.reddit.com/prefs/apps)

### Installation

The project uses `uv` for dependency management. All dependencies are already configured in `pyproject.toml`.

### Environment Setup

Ensure your `.env` file in the root directory contains:
```env
OPENAI_API_KEY=your_openai_api_key_here
REDDIT_CLIENT_ID=your_reddit_client_id_here
REDDIT_CLIENT_SECRET=your_reddit_client_secret_here
```

### Usage

#### Interactive Menu
```bash
uv run main.py
```

#### Direct Idea Analysis
```bash
uv run main.py "Your business idea here"
```

#### Interactive Mode (with clarification questions)
```bash
uv run main.py --idea-potential --interactive
```

#### Command Line Options
```bash
# Run idea potential analysis
uv run main.py --idea-potential "Your idea here"

# Run interactive idea potential analysis
uv run main.py --idea-potential --interactive

# Run idea refinement engine
uv run main.py --idea-refinement
```

#### Example
```bash
uv run main.py "A mobile app that helps people find local farmers markets"
```

## 📋 System Flow

```
A[Raw Idea Input] --> B{Idea Clarifier Agent}
B -->|1-3 Critical Questions| U[User]
U -->|Answers| B
B --> C[Smart Research Agent]
C --> D[Validation Matrix Generator]
D --> E[Priority Roadmap Builder]
E --> F[Report Builder]
F --> G[Report Refiner Agent]
```

## 🤖 Agent Details

### 1. Clarifier Agent
- **Model**: GPT-4o-mini
- **Purpose**: Asks targeted questions to understand the idea
- **Output**: Refined idea description, target market, value propositions

### 2. Research Agent
- **Model**: GPT-4o
- **Purpose**: Gathers market intelligence from Reddit
- **Features**: 
  - Searches relevant subreddits
  - Analyzes sentiment and engagement
  - Identifies pain points and market needs
- **Output**: Market insights, pain points, competition analysis

### 3. Validation Agent
- **Model**: GPT-4o
- **Purpose**: Creates comprehensive validation frameworks
- **Output**: 
  - Validation matrix (market, technical, financial, competitive, customer adoption)
  - SWOT analysis
  - Risk assessment

### 4. Roadmap Agent
- **Model**: GPT-4o
- **Purpose**: Creates development roadmaps and priority matrices
- **Output**: 
  - 4-phase development roadmap
  - Priority matrix for tasks
  - Resource planning
  - Milestone timeline

### 5. Report Agent
- **Model**: GPT-4o
- **Purpose**: Generates comprehensive analysis reports
- **Output**: 
  - Executive summary
  - Market analysis
  - Technical analysis
  - Financial analysis
  - Risk assessment
  - Strategic recommendations
  - Implementation roadmap
  - Success metrics

### 6. Refiner Agent
- **Model**: GPT-4o
- **Purpose**: Cross-checks and validates the final report
- **Features**:
  - Validates authenticity and consistency
  - Cross-checks claims against research data
  - Identifies gaps and improvements
  - Provides refinement recommendations

## 📊 Output Files

The system generates output files in the `idea_potential/reports/` directory:

1. **Markdown Report** (`{IdeaNameInCamelCase}_ddmmyy_hhmm.md`)
   - Comprehensive analysis report
   - Executive summary
   - Detailed market, technical, and financial analysis
   - Strategic recommendations

2. **JSON Results** (`idea_analysis_results_YYYYMMDD_HHMMSS.json`)
   - Complete analysis data
   - All agent outputs
   - Structured data for further processing

### Example Filename
- Idea: "A mobile app that helps people find local farmers markets"
- Filename: `AMobileAppThatHelpsPeopleFindLocalFarmersMarkets_251224_1430.md`

## 🔧 Configuration

### Model Configuration
Edit `idea_potential/config.py` to customize model choices for each agent:

```python
MODEL_CONFIG = {
    'clarifier': 'gpt-4o-mini',  # Fast, cost-effective for Q&A
    'research': 'gpt-4o',        # More capable for research analysis
    'validation': 'gpt-4o',      # Complex analysis
    'roadmap': 'gpt-4o',         # Strategic thinking
    'report': 'gpt-4o',          # Detailed report generation
    'refiner': 'gpt-4o'          # Final refinement
}
```

### Reddit Configuration
Customize subreddits for research in `idea_potential/config.py`:

```python
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
```

## 📈 Example Output

### Executive Summary
```
📋 Recommendation: PROCEED_WITH_CAUTION
📋 Confidence Level: medium

🔍 Key Findings:
  • Strong market need identified
  • Moderate competition landscape
  • Technical feasibility confirmed
  • Financial viability requires validation
```

### Validation Summary
```
✅ Validation Score: 7.5/10
✅ Risk Level: medium
```

### Research Summary
```
📊 Research Results:
  • Posts Analyzed: 45
  • Market Validation: Positive sentiment, clear pain points
```

## 🛠️ Customization

### Adding New Research Sources
1. Create a new research agent class
2. Implement the required methods
3. Update the pipeline to include the new agent

### Customizing Validation Frameworks
1. Modify the validation agent prompts
2. Add new validation criteria
3. Update the validation matrix structure

### Extending Report Sections
1. Modify the report agent prompts
2. Add new analysis sections
3. Update the markdown template

## 🧪 Testing

Run the system tests:
```bash
cd idea_potential
python test_system.py
```

## 🔍 Troubleshooting

### Common Issues

1. **OpenAI API Errors**
   - Check your API key in `.env`
   - Ensure sufficient API credits
   - Verify API key permissions

2. **Reddit API Errors**
   - Verify Reddit credentials in `.env`
   - Check Reddit API rate limits
   - Ensure proper user agent string

3. **Import Errors**
   - Ensure you're running from the project root
   - Check that all dependencies are installed via `uv`
   - Verify Python version (3.8+ required)

### Debug Mode
Add debug logging by modifying agent classes to include more detailed logging.

## 📝 License

This project is open source. Feel free to modify and distribute according to your needs.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📞 Support

For issues and questions:
1. Check the troubleshooting section
2. Review the configuration options
3. Open an issue with detailed error information

---

**Built with ❤️ for entrepreneurs and innovators** 