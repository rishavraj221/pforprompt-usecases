# Idea Potential Analysis System

A comprehensive AI-powered system to analyze and validate business ideas through market research, validation frameworks, and strategic planning. This system uses a pipeline of specialized AI agents to thoroughly evaluate business ideas and provide actionable insights.

## 🎯 Overview

The Idea Potential Analysis System is designed to help entrepreneurs, innovators, and business professionals validate their ideas through a systematic, AI-driven approach. It combines market research, validation frameworks, strategic planning, and comprehensive reporting to provide a complete picture of a business idea's potential.

### Key Features

- **Multi-Agent Pipeline**: Six specialized AI agents working in sequence
- **Market Research**: Automated Reddit analysis for real-time market insights
- **Validation Frameworks**: Comprehensive validation matrices and SWOT analysis
- **Strategic Planning**: Development roadmaps and priority matrices
- **Comprehensive Reporting**: Detailed markdown reports with actionable insights
- **Interactive Mode**: Guided analysis with clarification questions

## 🏗️ Architecture

### System Flow

```
Raw Idea Input → Clarifier Agent → Research Agent → Validation Agent → Roadmap Agent → Report Agent → Refiner Agent → Final Report
```

### Agent Pipeline

1. **Clarifier Agent** (`clarifier_agent.py`)
   - Analyzes initial idea and asks targeted questions
   - Refines idea description and identifies target market
   - Uses GPT-4o-mini for cost-effective Q&A

2. **Research Agent** (`research_agent.py`)
   - Conducts market research using Reddit data
   - Analyzes sentiment, engagement, and market trends
   - Identifies pain points and market opportunities
   - Uses GPT-4o for complex analysis

3. **Validation Agent** (`validation_agent.py`)
   - Creates comprehensive validation frameworks
   - Generates validation matrices and SWOT analysis
   - Assesses market, technical, financial, and competitive risks
   - Uses GPT-4o for strategic analysis

4. **Roadmap Agent** (`roadmap_agent.py`)
   - Builds development roadmaps and priority matrices
   - Creates 4-phase development timeline
   - Plans resource allocation and milestones
   - Uses GPT-4o for strategic planning

5. **Report Agent** (`report_agent.py`)
   - Generates comprehensive analysis reports
   - Creates executive summaries and detailed analysis
   - Formats data into structured markdown reports
   - Uses GPT-4o for detailed report generation

6. **Refiner Agent** (`refiner_agent.py`)
   - Cross-checks and validates final reports
   - Identifies gaps and inconsistencies
   - Provides refinement recommendations
   - Uses GPT-4o for quality assurance

## 🚀 Quick Start

### Prerequisites

1. **Python 3.8+**
2. **OpenAI API Key** - Get from [OpenAI Platform](https://platform.openai.com/)
3. **Reddit API Credentials** - Get from [Reddit Apps](https://www.reddit.com/prefs/apps)

### Installation

The project uses `uv` for dependency management. All dependencies are configured in `pyproject.toml`.

```bash
# Clone the repository
git clone <repository-url>
cd pforprompts-usecases

# Install dependencies
uv sync
```

### Environment Setup

Create a `.env` file in the root directory:

```env
OPENAI_API_KEY=your_openai_api_key_here
REDDIT_CLIENT_ID=your_reddit_client_id_here
REDDIT_CLIENT_SECRET=your_reddit_client_secret_here
```

## 📖 Usage Examples

### Example 1: Basic Idea Analysis

```python
from idea_potential import run_idea_analysis

# Analyze a business idea
idea = "A mobile app that helps people find local farmers markets"
results = run_idea_analysis(idea=idea)

# Access results
print(f"Recommendation: {results['executive_summary']['recommendation']}")
print(f"Confidence: {results['executive_summary']['confidence_level']}")
print(f"Validation Score: {results['validation_summary']['overall_score']}/10")
```

### Example 2: Interactive Analysis

```python
from idea_potential import run_idea_analysis

# Run interactive analysis with clarification questions
results = run_idea_analysis(interactive=True)
```

### Example 3: Direct Pipeline Usage

```python
from idea_potential.pipeline import IdeaPotentialPipeline

# Initialize pipeline
pipeline = IdeaPotentialPipeline()

# Run complete analysis
results = pipeline.start_analysis("Your business idea here")

# Access individual step results
clarification = pipeline.get_step_data('clarification')
research = pipeline.get_step_data('research')
validation = pipeline.get_step_data('validation')
```

### Example 4: Command Line Usage

```bash
# Basic analysis
uv run main.py "A mobile app that helps people find local farmers markets"

# Interactive mode
uv run main.py --idea-potential --interactive

# Direct idea potential analysis
uv run main.py --idea-potential "Your idea here"
```

## 📊 Output Structure

### Report Files

The system generates two types of output files in the `idea_potential/reports/` directory:

1. **Markdown Report** (`{IdeaNameInCamelCase}_ddmmyy_hhmm.md`)
   - Comprehensive analysis report
   - Executive summary
   - Detailed market, technical, and financial analysis
   - Strategic recommendations

2. **JSON Results** (`idea_analysis_results_YYYYMMDD_HHMMSS.json`)
   - Complete analysis data
   - All agent outputs
   - Structured data for further processing

### Example Output Structure

```json
{
  "idea_summary": "A mobile app that helps people find local farmers markets",
  "target_market": "Urban consumers interested in local, organic food",
  "executive_summary": {
    "recommendation": "PROCEED_WITH_CAUTION",
    "confidence_level": "medium",
    "key_findings": [
      "Strong market need identified",
      "Moderate competition landscape",
      "Technical feasibility confirmed"
    ]
  },
  "validation_summary": {
    "overall_score": 7.5,
    "risk_level": "medium"
  },
  "research_summary": {
    "posts_analyzed": 45,
    "market_validation": "Positive sentiment, clear pain points"
  },
  "roadmap_summary": {
    "overall_timeline": "42 weeks",
    "phases": ["Validation", "MVP Development", "Market Entry", "Scaling"]
  },
  "refinement_summary": {
    "quality_score": 8.5,
    "authenticity": "high"
  },
  "report_filepath": "idea_potential/reports/AMobileAppThatHelpsPeopleFindLocalFarmersMarkets_251224_1430.md"
}
```

## 🔧 Configuration

### Model Configuration

Edit `idea_potential/config.py` to customize model choices:

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

### Reddit Research Configuration

Customize subreddits for research:

```python
SUBREDDIT_CATEGORIES = {
    'business': ['business', 'entrepreneur', 'startups', 'smallbusiness'],
    'technology': ['technology', 'programming', 'webdev', 'AI'],
    'finance': ['finance', 'personalfinance', 'investing'],
    # Add more categories as needed
}
```

## 📈 Example Analysis Results

### Executive Summary Example

```
📋 Recommendation: PROCEED_WITH_CAUTION
📋 Confidence Level: medium

🔍 Key Findings:
  • Strong market need identified (83 posts analyzed)
  • Moderate competition landscape
  • Technical feasibility confirmed
  • Financial viability requires validation
  • Clear pain points: difficulty finding local markets
```

### Validation Summary Example

```
✅ Validation Score: 7.5/10
✅ Risk Level: medium

📊 Validation Matrix:
  Market Validation: 8/10
  Technical Feasibility: 7/10
  Financial Viability: 6/10
  Competitive Landscape: 7/10
  Customer Adoption: 8/10
```

### Research Summary Example

```
📊 Research Results:
  • Posts Analyzed: 83
  • Subreddits: 9 different communities
  • Sentiment: 68.7% positive, 30.1% negative
  • Engagement Rate: 1092.02
  • Market Validation: Positive sentiment, clear pain points
```

## 🛠️ Customization

### Adding New Research Sources

1. Create a new research agent class inheriting from `BaseAgent`
2. Implement required methods: `conduct_research()`, `analyze_data()`
3. Update the pipeline to include the new agent

```python
class CustomResearchAgent(BaseAgent):
    def conduct_research(self, clarification_data):
        # Your custom research logic
        pass
    
    def analyze_data(self, research_data):
        # Your custom analysis logic
        pass
```

### Customizing Validation Frameworks

1. Modify validation agent prompts in `validation_agent.py`
2. Add new validation criteria to the validation matrix
3. Update the validation scoring system

### Extending Report Sections

1. Modify report agent prompts in `report_agent.py`
2. Add new analysis sections to the markdown template
3. Update the report generator in `generate_comprehensive_reports.py`

## 🧪 Testing

### Running System Tests

```bash
cd idea_potential
python test_system.py
```

### Testing Individual Agents

```python
from idea_potential.clarifier_agent import ClarifierAgent
from idea_potential.research_agent import ResearchAgent

# Test clarifier agent
clarifier = ClarifierAgent()
result = clarifier.analyze_initial_idea("Test idea")

# Test research agent
research = ResearchAgent()
result = research.conduct_research(clarification_data)
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

Add debug logging by modifying agent classes:

```python
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class CustomAgent(BaseAgent):
    def process(self, data):
        logger.debug(f"Processing data: {data}")
        # Your processing logic
```

## 📚 API Reference

### Main Functions

#### `run_idea_analysis(idea=None, interactive=False)`

Main entry point for idea analysis.

**Parameters:**
- `idea` (str, optional): The business idea to analyze
- `interactive` (bool): Whether to run in interactive mode

**Returns:**
- `dict`: Complete analysis results

#### `IdeaPotentialPipeline`

Main pipeline class for orchestrating the analysis.

**Methods:**
- `start_analysis(idea)`: Run complete analysis pipeline
- `run_interactive_analysis(idea)`: Run analysis with user interaction
- `get_step_data(step)`: Get data from specific pipeline step
- `get_pipeline_status()`: Get current pipeline status

### Agent Classes

#### `ClarifierAgent`
- `analyze_initial_idea(idea)`: Analyze and clarify the initial idea

#### `ResearchAgent`
- `conduct_research(clarification_data)`: Conduct market research
- `analyze_data(research_data)`: Analyze research findings

#### `ValidationAgent`
- `create_validation_matrix(clarification_data, research_data)`: Create validation framework
- `generate_swot_analysis(data)`: Generate SWOT analysis

#### `RoadmapAgent`
- `create_roadmap(clarification_data, validation_data)`: Create development roadmap
- `generate_priority_matrix(data)`: Generate priority matrix

#### `ReportAgent`
- `generate_report(clarification_data, research_data, validation_data, roadmap_data)`: Generate comprehensive report

#### `RefinerAgent`
- `refine_report(report_data, clarification_data, research_data, validation_data)`: Refine and validate report

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

*The Idea Potential Analysis System helps you validate your business ideas through comprehensive AI-driven analysis, market research, and strategic planning.* 