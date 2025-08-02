from idea_potential.base_agent import BaseAgent
from idea_potential.suggester_agent import SuggesterAgent
from typing import Dict, List, Optional, Any

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

        Return your response as JSON with this structure:
        {{
            "analysis": "Brief analysis of the idea",
            "critical_questions": [
                {{
                    "question": "The question text",
                    "reason": "Why this question is critical",
                    "category": "market|value_proposition|feasibility"
                }}
            ],
            "idea_summary": "One sentence summary of the idea"
        }}
        """
        
        messages = [
            {"role": "system", "content": "You are a business analyst expert at asking the right questions to validate ideas."},
            {"role": "user", "content": prompt}
        ]
        
        response = self.call_llm(messages, temperature=0.3)
        result = self.parse_json_response(response)
        
        if result:
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
        """Generate a summary of all clarifications made"""
        
        prompt = f"""
        Based on the following idea and user responses, create a comprehensive summary of the clarified idea:

        ORIGINAL IDEA: {self.idea_context.get("idea_summary", "Unknown")}
        
        QUESTIONS ASKED AND ANSWERS:
        """
        
        for i, (question, response) in enumerate(zip(self.questions_asked, self.user_responses)):
            prompt += f"\nQ{i+1}: {question['question']}\nA{i+1}: {response}\n"
        
        prompt += """
        Create a comprehensive summary that includes:
        1. Refined idea description
        2. Target market identification
        3. Key value propositions
        4. Potential challenges
        5. Next steps for validation

        Return as JSON:
        {
            "refined_idea": "Clear description of the idea after clarification",
            "target_market": "Identified target market",
            "value_propositions": ["List of key value propositions"],
            "potential_challenges": ["List of potential challenges"],
            "validation_priorities": ["List of what needs to be validated"],
            "status": "clarified"
        }
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
    
    def get_clarification_status(self) -> Dict[str, Any]:
        """Get current status of clarification process"""
        return {
            "questions_asked": len(self.questions_asked),
            "responses_received": len(self.user_responses),
            "total_questions": len(self.idea_context.get("critical_questions", [])),
            "status": "complete" if len(self.user_responses) >= len(self.idea_context.get("critical_questions", [])) else "in_progress"
        } 