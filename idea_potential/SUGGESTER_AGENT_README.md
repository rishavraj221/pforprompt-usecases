# Suggester Agent

A generic agent that provides answer suggestions for any agent asking questions in the idea potential analysis system.

## Overview

The Suggester Agent is designed to enhance user experience by providing intelligent answer suggestions when agents ask questions. It can be used with any agent type (clarifier, validator, researcher, etc.) and provides context-aware suggestions based on the conversation history and agent type.

## Features

- **Generic Design**: Works with any agent type
- **Context-Aware**: Considers conversation history and agent context
- **Configurable**: Adjustable number of suggestions (default: 3)
- **History Tracking**: Maintains suggestion history for analysis
- **Easy Integration**: Simple API for integration with existing agents

## Usage

### Basic Usage

```python
from idea_potential.suggester_agent import SuggesterAgent

# Initialize the suggester agent
suggester = SuggesterAgent()

# Generate suggestions for a question
suggestions = suggester.generate_suggestions(
    question="What is your target market?",
    context={
        "idea": "A mobile app for fitness tracking",
        "target_market": "Fitness enthusiasts"
    },
    agent_type="clarifier"
)

# Access suggestions
for suggestion in suggestions.get('suggestions', []):
    print(f"- {suggestion['text']}")
    print(f"  Reason: {suggestion['reasoning']}")
```

### Integration with Clarifier Agent

The clarifier agent now automatically includes suggestions when asking questions:

```python
from idea_potential.clarifier_agent import ClarifierAgent

clarifier = ClarifierAgent()

# Analyze an idea
analysis = clarifier.analyze_initial_idea("Your idea here")

# Get questions with suggestions
question_result = clarifier.ask_next_question()

if "suggestions" in question_result:
    print("Suggested answers:")
    for i, suggestion in enumerate(question_result['suggestions'], 1):
        print(f"{i}. {suggestion['text']}")
```

### Interactive Mode

The pipeline's interactive mode now includes suggestions:

```python
from idea_potential.pipeline import IdeaPotentialPipeline

pipeline = IdeaPotentialPipeline()

# Run interactive analysis with suggestions
result = pipeline.run_interactive_analysis("Your idea here")
```

## API Reference

### SuggesterAgent Class

#### Methods

##### `generate_suggestions(question, context, agent_type="unknown", max_suggestions=3)`

Generate answer suggestions for a given question.

**Parameters:**
- `question` (str): The question being asked
- `context` (dict): Context information about the conversation/idea
- `agent_type` (str): Type of agent asking the question (e.g., 'clarifier', 'validator')
- `max_suggestions` (int): Maximum number of suggestions to generate (default: 3)

**Returns:**
- `dict`: Contains suggestions and metadata

**Example Response:**
```json
{
    "suggestions": [
        {
            "id": "suggestion_1",
            "text": "The suggested answer text",
            "reasoning": "Why this suggestion is helpful",
            "category": "specific"
        }
    ],
    "context_used": "Brief description of what context was considered",
    "agent_type": "clarifier",
    "question": "What is your target market?"
}
```

##### `get_suggestion_history()`

Get history of all suggestions made.

**Returns:**
- `list`: List of suggestion history entries

##### `clear_history()`

Clear the suggestion history.

##### `get_suggestions_for_agent(agent_type)`

Get all suggestions made for a specific agent type.

**Parameters:**
- `agent_type` (str): The agent type to filter by

**Returns:**
- `list`: List of suggestions for the specified agent type

## Integration Examples

### With Clarifier Agent

The clarifier agent automatically integrates with the suggester agent:

```python
from idea_potential.clarifier_agent import ClarifierAgent

clarifier = ClarifierAgent()

# Analyze idea
analysis = clarifier.analyze_initial_idea("A platform for remote team collaboration")

# Get questions with suggestions
question_result = clarifier.ask_next_question()

# Display suggestions
suggestions = question_result.get('suggestions', [])
for i, suggestion in enumerate(suggestions, 1):
    print(f"{i}. {suggestion['text']}")
    print(f"   Reason: {suggestion['reasoning']}")
```

### With Other Agents

You can integrate the suggester agent with any other agent:

```python
from idea_potential.suggester_agent import SuggesterAgent

suggester = SuggesterAgent()

# For validation agent
validation_suggestions = suggester.generate_suggestions(
    question="What are the main risks?",
    context={"idea": "Your idea", "target_market": "Your market"},
    agent_type="validator"
)

# For research agent
research_suggestions = suggester.generate_suggestions(
    question="Which market segments to focus on?",
    context={"idea": "Your idea", "analysis": "Your analysis"},
    agent_type="researcher"
)
```

## Configuration

The suggester agent uses the same configuration as other agents in the system. It inherits from `BaseAgent` and uses the model configuration specified in `config.py`.

## Testing

Run the test script to verify functionality:

```bash
python idea_potential/test_suggester.py
```

Run the example script to see various usage scenarios:

```bash
python idea_potential/example_with_suggestions.py
```

## Key Benefits

1. **Improved User Experience**: Users can choose from relevant suggestions or type their own answers
2. **Faster Interaction**: Reduces time spent thinking about answers
3. **Better Quality Responses**: Suggestions are context-aware and relevant
4. **Generic Design**: Can be used with any agent type
5. **History Tracking**: Maintains suggestion history for analysis and improvement

## Future Enhancements

- **Learning from User Choices**: Track which suggestions users choose most often
- **Personalized Suggestions**: Adapt suggestions based on user history
- **Multi-language Support**: Generate suggestions in different languages
- **Advanced Context Analysis**: Use more sophisticated context analysis for better suggestions 