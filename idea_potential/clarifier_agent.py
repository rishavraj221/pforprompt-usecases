from idea_potential.base_agent import BaseAgent
from idea_potential.suggester_agent import SuggesterAgent
from typing import Dict, List, Optional, Any
from idea_potential.structured_outputs import (
    IdeaAnalysisResponse, ClarificationSummaryResponse, UserPersona
)

class ClarifierAgent(BaseAgent):
    """Agent responsible for clarifying and understanding the user's idea through targeted questions"""
    
    def __init__(self):
        super().__init__('clarifier')
        self.questions_asked = []
        self.user_responses = []
        self.idea_context = {}
        self.suggester = SuggesterAgent()
        
    def analyze_initial_idea(self, idea: str) -> Dict[str, Any]:
        """Analyze the initial idea and determine what questions to ask"""
        if not self.validate_input(idea):
            return {"error": "Invalid idea input"}
            
        prompt = f"""
        You are an expert business analyst and idea validator. Your job is to analyze a business idea and determine the most critical questions to ask to understand its potential.

        IDEA: {idea}

        Analyze this idea and identify the 3 most critical questions that need to be answered to properly evaluate its potential. Focus on:
        1. Target market and customer pain points
        2. Value proposition and differentiation
        3. Feasibility and resources needed

        Please respond with valid JSON format containing:
        - analysis: Brief analysis of the idea
        - critical_questions: Array of 3 questions with question, reason, and category fields
        - idea_summary: One sentence summary of the idea

        For the category field, use exactly one of these values:
        - "market" for questions about target market, customers, or market validation
        - "value_proposition" for questions about value proposition, differentiation, or competitive advantage
        - "feasibility" for questions about technical feasibility, resources, or implementation
        """
        
        messages = [
            {"role": "system", "content": "You are a business analyst expert at asking the right questions to validate ideas."},
            {"role": "user", "content": prompt}
        ]
        
        try:
            # Try structured output first
            result = self.call_llm_structured(messages, IdeaAnalysisResponse, temperature=0.3)
            
            if result:
                self.idea_context = {
                    "analysis": result.analysis,
                    "critical_questions": [q.dict() for q in result.critical_questions],
                    "idea_summary": result.idea_summary
                }
                self.log_activity("Analyzed initial idea", result.idea_summary)
                return self.idea_context
                
        except Exception as e:
            print(f"Error analyzing initial idea with structured output: {e}")
        
        # Fallback to regular LLM call
        response = self.call_llm(messages, temperature=0.3)
        result = self.parse_json_response(response)
        
        if result:
            # Ensure the result has the expected structure
            if "critical_questions" in result:
                # Convert category values to proper enum values if needed
                for question in result.get("critical_questions", []):
                    if "category" in question:
                        category = question["category"]
                        if isinstance(category, str):
                            category_lower = category.lower()
                            if "market" in category_lower or "target" in category_lower:
                                question["category"] = "market"
                            elif "value" in category_lower or "proposition" in category_lower:
                                question["category"] = "value_proposition"
                            elif "feasibility" in category_lower or "resources" in category_lower:
                                question["category"] = "feasibility"
            
            self.idea_context = result
            self.log_activity("Analyzed initial idea", result.get("idea_summary"))
        
        return result or {"error": "Failed to analyze idea"}
    
    def ask_next_question(self, user_response: str = None) -> Dict[str, Any]:
        """Ask the next critical question based on previous responses"""
        
        # Add user response to context if provided
        if user_response:
            self.user_responses.append(user_response)
        
        # If we haven't analyzed the idea yet, return error
        if not self.idea_context:
            return {"error": "No idea analyzed yet"}
        
        # Determine if we need more questions
        if len(self.user_responses) >= len(self.idea_context.get("critical_questions", [])):
            return self.generate_clarification_summary()
        
        # Get the next question
        current_question_index = len(self.user_responses)
        questions = self.idea_context.get("critical_questions", [])
        
        if current_question_index < len(questions):
            next_question = questions[current_question_index]
            self.questions_asked.append(next_question)
            
            # Generate suggestions for this question
            context = {
                "idea": self.idea_context.get("idea_summary", ""),
                "analysis": self.idea_context.get("analysis", ""),
                "critical_questions": self.idea_context.get("critical_questions", []),
                "user_responses": self.user_responses,
                "current_question_index": current_question_index
            }
            
            suggestions = self.suggester.generate_suggestions(
                question=next_question["question"],
                context=context,
                agent_type="clarifier"
            )
            
            return {
                "question": next_question["question"],
                "reason": next_question["reason"],
                "category": next_question["category"],
                "question_number": current_question_index + 1,
                "total_questions": len(questions),
                "status": "asking",
                "suggestions": suggestions.get("suggestions", []) if "error" not in suggestions else []
            }
        
        return {"error": "No more questions to ask"}
    
    def generate_clarification_summary(self) -> Dict[str, Any]:
        """Generate a summary of all clarifications made with detailed user personas"""
        
        # First, develop detailed user personas
        user_personas = self.develop_user_personas()
        
        prompt = f"""
        Based on the following idea and user responses, create a comprehensive summary of the clarified idea:

        ORIGINAL IDEA: {self.idea_context.get("idea_summary", "Unknown")}
        
        QUESTIONS ASKED AND ANSWERS:
        """
        
        for i, (question, response) in enumerate(zip(self.questions_asked, self.user_responses)):
            prompt += f"\nQ{i+1}: {question['question']}\nA{i+1}: {response}\n"
        
        prompt += f"""
        USER PERSONAS DEVELOPED:
        {user_personas}

        Create a comprehensive summary that includes:
        1. Refined idea description
        2. Target market identification with detailed user personas
        3. Key value propositions
        4. Potential challenges
        5. Next steps for validation

        Return as JSON:
        {{
            "refined_idea": "Clear description of the idea after clarification",
            "target_market": "Identified target market",
            "user_personas": {user_personas},
            "value_propositions": ["List of key value propositions"],
            "potential_challenges": ["List of potential challenges"],
            "validation_priorities": ["List of what needs to be validated"],
            "status": "clarified"
        }}
        """
        
        messages = [
            {"role": "system", "content": "You are an expert at synthesizing information into clear business insights."},
            {"role": "user", "content": prompt}
        ]
        
        response = self.call_llm(messages, temperature=0.3)
        result = self.parse_json_response(response)
        
        if result:
            result["status"] = "clarified"
            self.log_activity("Generated clarification summary")
        
        return result or {"error": "Failed to generate clarification summary"}
    
    def develop_user_personas(self) -> Dict[str, Any]:
        """Develop detailed user personas for the business idea"""
        
        prompt = f"""
        Develop detailed user personas for this business idea:

        IDEA: {self.idea_context.get("idea_summary", "Unknown")}
        TARGET MARKET: {self.idea_context.get("analysis", "Unknown")}
        USER RESPONSES: {self.user_responses}

        Create 3-5 detailed user personas that represent the target market. For each persona, include:

        Return as JSON:
        {{
            "primary_personas": [
                {{
                    "name": "Persona name",
                    "role": "Job title/role",
                    "age_range": "Age range",
                    "experience_level": "Experience level",
                    "company_size": "Company size they work for",
                    "industry": "Industry they work in",
                    "goals": ["List of primary goals"],
                    "pain_points": ["List of pain points"],
                    "motivations": ["List of motivations"],
                    "frustrations": ["List of frustrations"],
                    "tech_savviness": "high|medium|low",
                    "budget": "budget_range",
                    "decision_making_factors": ["List of factors that influence decisions"],
                    "daily_workflow": "Description of typical daily workflow",
                    "tools_they_use": ["List of current tools they use"],
                    "challenges_they_face": ["List of specific challenges"],
                    "success_metrics": ["How they measure success"],
                    "communication_preferences": ["How they prefer to communicate"],
                    "learning_style": "How they prefer to learn new things",
                    "quote": "A representative quote from this persona"
                }}
            ],
            "secondary_personas": [
                {{
                    "name": "Persona name",
                    "role": "Job title/role",
                    "relationship_to_primary": "How they relate to primary personas",
                    "influence_level": "high|medium|low",
                    "goals": ["List of goals"],
                    "pain_points": ["List of pain points"],
                    "motivations": ["List of motivations"]
                }}
            ],
            "persona_insights": {{
                "common_characteristics": ["Characteristics shared across personas"],
                "key_differences": ["Key differences between personas"],
                "unified_needs": ["Needs that all personas share"],
                "persona_priorities": ["Priority order for addressing personas"]
            }}
        }}
        """
        
        messages = [
            {"role": "system", "content": "You are an expert in user research and persona development with deep understanding of various industries and user types."},
            {"role": "user", "content": prompt}
        ]
        
        response = self.call_llm(messages, temperature=0.4)
        result = self.parse_json_response(response)
        
        if result:
            self.log_activity("Developed user personas")
            return result
        
        return {"error": "Failed to develop user personas"}
    
    def get_clarification_status(self) -> Dict[str, Any]:
        """Get current status of clarification process"""
        return {
            "questions_asked": len(self.questions_asked),
            "responses_received": len(self.user_responses),
            "total_questions": len(self.idea_context.get("critical_questions", [])),
            "status": "complete" if len(self.user_responses) >= len(self.idea_context.get("critical_questions", [])) else "in_progress"
        } 