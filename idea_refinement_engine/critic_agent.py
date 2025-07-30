"""
Critic Agent for Idea Validation Pipeline
"""

import json
from langchain_core.prompts import ChatPromptTemplate
from .base_agent import BaseAgent
from .state import ValidationState


class CriticAgent(BaseAgent):
    """Agent 3: Performs SWOT analysis with feasibility scoring using Chain-of-Thought reasoning"""
    
    def __init__(self, llm):
        super().__init__(llm)
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """
**Role**: Devil's Advocate Analyst with Chain-of-Thought Reasoning
**Task**: Perform SWOT analysis with evidence-based reasoning using step-by-step logic

**Chain-of-Thought Process**:
1. **Step 1 - Problem Analysis**: First, analyze if the problem is real and well-defined
   - Count problem mentions vs solution details
   - Identify if this is "solution-seeking-problem"
   
2. **Step 2 - Market Assessment**: Evaluate market conditions
   - Research similar solutions
   - Assess market saturation
   - Identify competitive landscape
   
3. **Step 3 - Technical Feasibility**: Assess technical complexity
   - Break down technical requirements
   - Evaluate resource needs
   - Consider implementation timeline
   
4. **Step 4 - Operational Analysis**: Evaluate operational requirements
   - Team size needed
   - Infrastructure requirements
   - Operational complexity
   
5. **Step 5 - Risk Assessment**: Identify potential failure points
   - Logical fallacies in reasoning
   - Real-world analogs for comparison
   - Assumption validation

**Critical Rules**:  
1. For weaknesses/threats: Must cite logical fallacies OR real-world analogs  
2. Use this feasibility rubric:  
   - Technical: 1=NASA-level, 10=no-code tool  
   - Market: 1=saturated, 10=blue ocean  
   - Operational: 1=requires 50 hires, 10=solo founder  
3. Flag "solution-seeking-problem" risk with diagnostic:  
   "Problem mentions: [count] vs Solution details: [count]"  

**Output Format**:  
```json
{{
  "reasoning_steps": {{
    "step1_problem_analysis": "detailed reasoning",
    "step2_market_assessment": "detailed reasoning", 
    "step3_technical_feasibility": "detailed reasoning",
    "step4_operational_analysis": "detailed reasoning",
    "step5_risk_assessment": "detailed reasoning"
  }},
  "swot_analysis": {{
    "strengths": ["evidence-backed item", "..."],
    "weaknesses": ["evidence-backed item", "..."],
    "opportunities": ["market gap/item", "..."],
    "threats": ["competitor/risk item", "..."]
  }},
  "feasibility_scores": {{
    "technical": "1-10 integer",
    "market": "1-10 integer", 
    "operational": "1-10 integer"
  }},
  "solution_in_search_score": "0-10 integer",
  "kill_risk": "high|medium|low",
  "assumption_risks": ["assumption:risk_level:evidence"]
}}
```"""),
            ("human", "Clarified Idea: {clarified_idea}\n\nVariations: {variations}")
        ])
    
    async def run(self, state: ValidationState) -> ValidationState:
        try:
            if not state["clarified_idea"] or not state["idea_variations"]:
                state["errors"].append("Cannot critique - missing clarified idea or variations")
                return state
            
            # Ensure clarified idea has the right structure
            clarified_idea = state["clarified_idea"]
            if not isinstance(clarified_idea, dict):
                state["errors"].append("Cannot critique - clarified idea is not properly structured")
                return state
            
            # If the idea is still in clarification mode, create a basic structure
            if clarified_idea.get("status") == "needs_clarification":
                # Create a basic structure for critique
                basic_idea = {
                    "core_problem": "Problem being solved (needs clarification)",
                    "proposed_solution": "Solution approach (needs clarification)",
                    "target_users": "Target users (needs clarification)",
                    "value_proposition": "Value proposition (needs clarification)",
                    "implementation_approach": "Implementation approach (needs clarification)",
                    "known_assumptions": ["Basic assumptions"]
                }
                clarified_idea = basic_idea
                
            chain = self.prompt | self.llm
            response = await chain.ainvoke({
                "clarified_idea": json.dumps(clarified_idea),
                "variations": json.dumps(state["idea_variations"])
            })
            
            # Debug: print response for troubleshooting
            print(f"🔍 Debug: Critic response length: {len(response.content)}")
            print(f"🔍 Debug: Critic response preview: {response.content[:200]}...")
            
            result = self.parse_json_response(response.content)
            state["critique_analysis"] = result
            state["current_agent"] = "critic"
            
            return state
            
        except Exception as e:
            state["errors"].append(f"Critic error: {str(e)}")
            return state 