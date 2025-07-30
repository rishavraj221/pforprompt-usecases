"""
Clarifier Agent for Idea Validation Pipeline
"""

import json
from typing import Dict, Any, List
from langchain_core.prompts import ChatPromptTemplate
from .base_agent import BaseAgent
from .state import ValidationState


class ClarifierAgent(BaseAgent):
    """Agent 1: Transforms vague ideas into structured frameworks with iterative clarification"""
    
    def __init__(self, llm):
        super().__init__(llm)
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """
**Role**: Idea Clarification Specialist  
**Task**: Transform vague ideas into structured problem-solution frameworks through iterative questioning.

**Analysis Process**:
1. Analyze the current idea for missing critical information
2. Identify the MOST IMPORTANT missing piece that would provide the biggest clarity gain
3. Ask only ONE question at a time
4. After each answer, re-evaluate if the idea is now clear enough to proceed

**Critical Information Categories** (in priority order):
1. **Core Problem**: What specific problem are you solving?
2. **Target Users**: Who exactly will use this?
3. **Proposed Solution**: How will you solve the problem?
4. **Value Proposition**: Why would users choose this over alternatives?
5. **Implementation Approach**: How will you build/deliver this?

**Decision Rules**:
- If ANY critical information is missing → Ask the highest priority missing item
- If all critical info is present but unclear → Ask for clarification on the most ambiguous part
- If idea is clear and complete → Mark as "complete"

**IMPORTANT**: After 3-5 clarifications, if the core idea is reasonably clear, mark as "complete" even if some details are missing. Don't get stuck in endless clarification loops.

**Output Format**:  
```json
{{
  "status": "complete" | "needs_clarification",
  "clarified_idea": {{
    "core_problem": "1-sentence problem statement",
    "proposed_solution": "1-sentence solution description", 
    "target_users": "comma-separated list",
    "value_proposition": "unique benefit vs alternatives",
    "implementation_approach": "how you'll build/deliver this",
    "known_assumptions": ["list", "of", "assumptions"]
  }},
  "next_question": {{
    "question": "single most important question to ask",
    "reason": "why this question is critical right now",
    "category": "core_problem|target_users|proposed_solution|value_proposition|implementation_approach"
  }}
}}
```"""),
            ("human", """
Current Idea: {user_idea}

Previous Clarifications: {previous_clarifications}
""")
        ])
    
    async def run(self, state: ValidationState) -> ValidationState:
        """Process user idea and return clarified structure"""
        try:
            # Skip clarification if validation is already complete
            if state.get("user_validation_responses") and len(state["user_validation_responses"]) > 0:
                print("\n✅ Skipping clarification - validation already completed")
                # Mark as complete to prevent further clarification
                if state["clarified_idea"]:
                    state["clarified_idea"]["status"] = "complete"
                return state
            
            # Skip clarification if analysis is already complete
            if state.get("final_report"):
                print("\n✅ Skipping clarification - analysis already completed")
                return state
            
            # Get previous clarifications if any
            previous_clarifications = state.get("clarification_history", "")
            
            chain = self.prompt | self.llm
            response = await chain.ainvoke({
                "user_idea": state["user_idea"],
                "previous_clarifications": previous_clarifications
            })
            
            result = self.parse_json_response(response.content)
            state["clarified_idea"] = result
            state["current_agent"] = "clarifier"
            
            # If needs clarification, store the next question
            if result.get("status") == "needs_clarification":
                state["next_clarification_question"] = result.get("next_question")
                # Don't add this as an error - it's a normal workflow state
                print(f"\n🤔 Idea needs clarification - generating question...")
            elif result.get("status") == "complete":
                # Clear any pending clarification question
                state["next_clarification_question"] = None
                print(f"\n✅ Idea clarification complete! Moving to next phase...")
                
            return state
            
        except Exception as e:
            state["errors"].append(f"Clarifier error: {str(e)}")
            return state 