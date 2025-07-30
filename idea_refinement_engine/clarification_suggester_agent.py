"""
Generic Suggestion Agent for Idea Validation Pipeline
"""

import json
from typing import List, Dict, Any
from langchain_core.prompts import ChatPromptTemplate
from .base_agent import BaseAgent
from .state import ValidationState


class GenericSuggestionAgent(BaseAgent):
    """Agent: Generates AI suggestions for any type of question from any agent"""
    
    def __init__(self, llm):
        super().__init__(llm)
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """
**Role**: Answer & Guidance Provider
**Task**: Generate three diverse, helpful ANSWERS or GUIDANCE for questions - NOT more questions

**CRITICAL**: You are providing ANSWERS, not asking more questions. Each suggestion should be a concrete answer or piece of guidance that helps the user respond to the question.

**WRITING STYLE**: Write all suggestions from the user's perspective using "I" and "my" instead of "you" and "your". For example, write "My app aims to solve..." instead of "Your app aims to solve...".

**Question Types**:
1. **Clarification Questions**: Provide specific, detailed answers that clarify the idea
2. **Validation Questions**: Provide concrete testing approaches and evidence-gathering methods
3. **General Questions**: Provide practical implementation guidance

**Answer Guidelines**:
1. **Diverse Perspectives**: Provide 3 different concrete answers/approaches
2. **Realistic & Specific**: Make answers concrete and actionable
3. **Varying Complexity**: Include simple, moderate, and advanced options
4. **Context-Aware**: Adapt answers based on question type and context
5. **User-Friendly**: Make answers easy to understand and implement

**Answer Types**:
- **Conservative**: Safe, proven approach or answer
- **Moderate**: Balanced approach with some innovation
- **Ambitious**: High-potential but higher-risk approach

**Context-Specific Adaptations**:
- For **Clarification Questions**: Provide specific, detailed answers that add clarity
- For **Validation Questions**: Provide concrete testing methods and validation approaches
- For **General Questions**: Provide practical implementation guidance

**Output Format**:
```json
{{
  "suggestions": [
    {{
      "question": "The question being asked",
      "question_type": "clarification|validation|general",
      "suggestions": [
        {{
          "type": "conservative",
          "suggestion": "My app aims to solve the problem of... (write from user's perspective)",
          "reasoning": "Why this answer/approach is safe and reliable"
        }},
        {{
          "type": "moderate", 
          "suggestion": "My solution addresses this by... (write from user's perspective)",
          "reasoning": "Why this answer/approach offers good risk-reward"
        }},
        {{
          "type": "ambitious",
          "suggestion": "I'm building this to revolutionize... (write from user's perspective)",
          "reasoning": "Why this answer/approach could be game-changing"
        }}
      ]
    }}
  ]
}}
```"""),
            ("human", """
Questions: {questions}
User Idea: {user_idea}
Question Context: {question_context}

Generate three diverse ANSWERS or GUIDANCE for each question. Provide concrete, helpful responses that directly address what the user needs to answer - NOT more questions to ask.
""")
        ])
    
    async def generate_suggestions(self, questions: List[str], user_idea: str, question_context: str = "general") -> Dict[str, Any]:
        """Generate AI suggestions for any type of questions"""
        try:
            print(f"🔍 Debug: Generating suggestions for {len(questions)} questions")
            print(f"🔍 Debug: Question context: {question_context}")
            print(f"🔍 Debug: User idea: {user_idea[:100]}...")
            
            chain = self.prompt | self.llm
            response = await chain.ainvoke({
                "questions": json.dumps(questions),
                "user_idea": user_idea,
                "question_context": question_context
            })
            
            print(f"🔍 Debug: Raw response: {response.content[:200]}...")
            
            result = self.parse_json_response(response.content)
            print(f"🔍 Debug: Parsed result keys: {list(result.keys()) if result else 'None'}")
            
            return result
            
        except Exception as e:
            print(f"🔍 Debug: Error in generate_suggestions: {str(e)}")
            return {
                "suggestions": [],
                "error": f"Generic suggester error: {str(e)}"
            } 