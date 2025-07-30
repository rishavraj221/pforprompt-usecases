"""
Questioner Agent for Idea Validation Pipeline
"""

import json
from langchain_core.prompts import ChatPromptTemplate
from .base_agent import BaseAgent
from .state import ValidationState


class QuestionerAgent(BaseAgent):
    """Agent 4: Generates validation-focused questions using Few-Shot Learning"""
    
    def __init__(self, llm):
        super().__init__(llm)
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """
**Role**: Validation Gap Identifier with Few-Shot Learning
**Task**: Generate ONLY questions that resolve critical uncertainties

**Few-Shot Examples**:

**Example 1 - Technical Risk**:
Input: "AI-powered customer service chatbot"
Question: "How to validate that the AI can handle 95% of customer queries without human intervention?"
Linked Risk: "Technical feasibility - AI complexity"
Test Method: "prototype"

**Example 2 - Market Risk**:
Input: "Subscription-based meal planning app"
Question: "How to confirm users will pay $15/month when free alternatives exist?"
Linked Risk: "Market willingness to pay"
Test Method: "survey"

**Example 3 - Operational Risk**:
Input: "B2B SaaS for small businesses"
Question: "How to validate that small businesses have budget for $500/month software?"
Linked Risk: "Customer acquisition cost vs LTV"
Test Method: "data analysis"

**Strict Filters**:  
1. Every question must map to:  
   - Weakness/Threat from SWOT OR  
   - Assumption with risk≥medium OR  
   - Feasibility score≤5  
2. Format: "How to [action] regarding [specific issue]?"  
3. Max 5 questions prioritized by kill_risk  

**Output Format**:  
```json
{{
  "validation_questions": [
    {{
      "question": "How to validate [specific assumption]?",
      "linked_risk": "SWOT weakness / Assumption",
      "test_method": "survey|prototype|data analysis"
    }}
  ]
}}
```"""),
            ("human", "Critique Analysis: {critique}")
        ])
        
        # New prompt for generating next question based on previous responses
        self.next_question_prompt = ChatPromptTemplate.from_messages([
            ("system", """
**Role**: Adaptive Question Generator
**Task**: Generate the NEXT most important validation question based on previous responses

**Context**: You have access to previous questions asked and user responses. Use this to:
1. Avoid asking redundant questions
2. Build upon previous answers
3. Focus on the most critical remaining uncertainty
4. Adapt the question based on what you've learned
5. Consider the user's development stage (MVP vs production)
6. Focus on MVP-level validation for early-stage ideas

**Previous Questions and Responses**:
{previous_qa}

**Remaining Critical Uncertainties**:
- Technical feasibility gaps
- Market validation needs  
- Operational challenges
- Risk mitigation requirements

**Rules**:
1. Ask only ONE question at a time
2. Make it the most critical remaining uncertainty
3. Build on previous responses when possible
4. MAXIMUM 5 questions total - stop after 5 questions
5. Focus on MVP-level questions if user is building an MVP
6. If all major uncertainties are addressed, return "complete"

**Output Format**:
```json
{{
  "status": "continue" | "complete",
  "next_question": {{
    "question": "How to validate [specific remaining uncertainty]?",
    "linked_risk": "SWOT weakness / Assumption",
    "test_method": "survey|prototype|data analysis",
    "reasoning": "Why this question is critical now based on previous responses"
  }}
}}
```"""),
            ("human", """
Critique Analysis: {critique}
Previous Q&A: {previous_qa}
Current Question Index: {question_index}
User Idea: {user_idea}

Generate the next most critical validation question. Focus on MVP-level concerns if this appears to be an early-stage idea.
""")
        ])
    
    async def run(self, state: ValidationState) -> ValidationState:
        """Generate initial set of validation questions"""
        try:
            if not state["critique_analysis"]:
                state["errors"].append("Cannot generate questions - missing critique analysis")
                return state
                
            chain = self.prompt | self.llm
            response = await chain.ainvoke({
                "critique": json.dumps(state["critique_analysis"])
            })
            
            result = self.parse_json_response(response.content)
            state["validation_questions"] = result
            state["current_agent"] = "questioner"
            
            return state
            
        except Exception as e:
            state["errors"].append(f"Questioner error: {str(e)}")
            return state
    
    async def generate_next_question(self, state: ValidationState, previous_responses: list) -> dict:
        """Generate the next validation question based on previous responses"""
        try:
            if not state["critique_analysis"]:
                return {"status": "complete", "error": "Missing critique analysis"}
            
            # Ensure previous_responses is a list
            if previous_responses is None:
                previous_responses = []
            
            # Check if we've reached the maximum questions
            if len(previous_responses) >= 5:
                return {"status": "complete", "reason": "Maximum 5 questions reached"}
            
            # Format previous Q&A for context
            previous_qa = []
            for resp in previous_responses:
                if isinstance(resp, dict) and 'question' in resp and 'response' in resp:
                    previous_qa.append(f"Q: {resp['question']}\nA: {resp['response']}")
            
            previous_qa_text = "\n\n".join(previous_qa) if previous_qa else "No previous questions asked yet."
            
            chain = self.next_question_prompt | self.llm
            response = await chain.ainvoke({
                "critique": json.dumps(state["critique_analysis"]),
                "previous_qa": previous_qa_text,
                "question_index": len(previous_responses) + 1,
                "user_idea": state["user_idea"]
            })
            
            result = self.parse_json_response(response.content)
            return result
            
        except Exception as e:
            return {"status": "complete", "error": f"Next question generation error: {str(e)}"} 