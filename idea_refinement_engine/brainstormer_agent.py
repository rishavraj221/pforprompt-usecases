"""
Brainstormer Agent for Idea Validation Pipeline
"""

import json
from langchain_core.prompts import ChatPromptTemplate
from .base_agent import BaseAgent
from .state import ValidationState


class BrainstormerAgent(BaseAgent):
    """Agent 2: Generates idea variations and extensions"""
    
    def __init__(self, llm):
        super().__init__(llm)
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """
**Role**: Divergent Thinking Engine  
**Task**: Generate 5 practical variations and 2 radical extensions of the core idea  
**Constraints**:  
- Variations must maintain core problem-solving intent  
- Wildcards must include "What if [constraint removed]?" framing  
- FORBIDDEN: Critiques, feasibility analysis  

**Output Format**:  
```json
{{
  "core_idea_summary": "max 15-word summary",
  "practical_variations": ["var1", "var2", "var3", "var4", "var5"],
  "wildcard_concepts": ["radical1", "radical2"],
  "trigger_questions": ["How might we combine X with Y?", "What if Z constraint disappeared?"]
}}
```"""),
            ("human", "Clarified Idea: {clarified_idea}")
        ])
    
    async def run(self, state: ValidationState) -> ValidationState:
        try:
            if not state["clarified_idea"]:
                state["errors"].append("Cannot brainstorm - missing clarified idea")
                return state
            
            # Handle case where idea is still being clarified
            clarified_idea = state["clarified_idea"]
            if clarified_idea.get("status") == "needs_clarification":
                # Use the user's original idea for brainstorming
                user_idea = state["user_idea"]
                # Create a basic structure for brainstorming
                basic_idea = {
                    "core_problem": "Problem being solved",
                    "proposed_solution": "Solution approach", 
                    "target_users": "Target users",
                    "value_proposition": "Value proposition",
                    "implementation_approach": "Implementation approach",
                    "known_assumptions": ["Basic assumptions"]
                }
                clarified_idea = basic_idea
                
            chain = self.prompt | self.llm
            response = await chain.ainvoke({
                "clarified_idea": json.dumps(clarified_idea)
            })
            
            result = self.parse_json_response(response.content)
            state["idea_variations"] = result
            state["current_agent"] = "brainstormer"
            
            return state
            
        except Exception as e:
            state["errors"].append(f"Brainstormer error: {str(e)}")
            return state 