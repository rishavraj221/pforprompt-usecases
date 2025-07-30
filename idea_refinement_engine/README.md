# Idea Refinement Engine

A modular multi-agent system for brainstorming, critiquing, and validating ideas using LangGraph.

## Architecture

The codebase has been refactored into a clean, modular structure:

```
idea_refinement_engine/
├── __init__.py              # Package exports
├── main.py                  # Main entry point
├── pipeline.py              # Main pipeline orchestrator
├── state.py                 # State management classes
├── base_agent.py            # Base agent class
├── clarifier_agent.py       # Agent 1: Idea clarification
├── brainstormer_agent.py    # Agent 2: Idea variations
├── critic_agent.py          # Agent 3: SWOT analysis
├── questioner_agent.py      # Agent 4: Validation questions
├── reality_miner_agent.py   # Agent 5: Real-world evidence
├── synthesizer_agent.py     # Agent 6: Final report
├── example.py               # Usage examples
└── README.md               # This file
```

## Components

### Core Classes

- **`IdeaValidationPipeline`**: Main orchestrator that manages the agent workflow
- **`ValidationState`**: TypedDict for state management between agents
- **`BaseAgent`**: Abstract base class with common functionality

### Agent Classes

1. **`ClarifierAgent`**: Transforms vague ideas into structured frameworks
2. **`BrainstormerAgent`**: Generates idea variations and extensions
3. **`CriticAgent`**: Performs SWOT analysis with feasibility scoring
4. **`QuestionerAgent`**: Generates validation-focused questions
5. **`RealityMinerAgent`**: Analyzes real-world evidence (mock implementation)
6. **`SynthesizerAgent`**: Creates final investment-ready report

## Usage

### Basic Usage

```python
import asyncio
from idea_refinement_engine import IdeaValidationPipeline

async def validate_idea():
    pipeline = IdeaValidationPipeline()
    result = await pipeline.validate_idea("Your idea here")
    
    if result["success"]:
        print(result["final_report"])
    else:
        print(f"Error: {result.get('error')}")

# Run the validation
asyncio.run(validate_idea())
```

### Advanced Usage

```python
from idea_refinement_engine import (
    IdeaValidationPipeline,
    ClarifierAgent,
    BrainstormerAgent,
    # ... other agents
)

# Create custom pipeline with specific agents
pipeline = IdeaValidationPipeline(llm_model="gpt-4")
result = await pipeline.validate_idea("Your idea")
```

## Agent Workflow

1. **Clarifier**: Transforms vague ideas into structured problem-solution frameworks
2. **Brainstormer**: Generates 5 practical variations and 2 radical extensions
3. **Critic**: Performs SWOT analysis with feasibility scoring
4. **Questioner**: Generates validation questions based on risks
5. **Reality Miner**: Analyzes real-world evidence (currently mocked)
6. **Synthesizer**: Creates final investment memo

## State Management

The `ValidationState` TypedDict tracks:
- User's original idea
- Clarified idea structure
- Idea variations
- Critique analysis
- Validation questions
- Reality check data
- Final report
- Current agent and iteration count
- Error tracking

## Error Handling

Each agent includes comprehensive error handling:
- JSON parsing errors
- Missing required data
- LLM response validation
- State validation

## Dependencies

- `langgraph`: Workflow orchestration
- `langchain_openai`: LLM integration
- `langchain_core`: Core LangChain components

## Running Examples

```bash
# Run the main example
python idea_refinement_engine/main.py

# Run the extended example
python idea_refinement_engine/example.py
```

## Extending the System

To add new agents:

1. Create a new agent class inheriting from `BaseAgent`
2. Implement the `run()` method
3. Add the agent to the pipeline in `pipeline.py`
4. Update the workflow graph as needed

## Benefits of Modular Structure

- **Maintainability**: Each agent is isolated and easily testable
- **Extensibility**: Easy to add new agents or modify existing ones
- **Reusability**: Agents can be used independently
- **Clarity**: Clear separation of concerns
- **Testing**: Each component can be unit tested separately 