from idea_potential.base_agent import BaseAgent
from idea_potential.suggester_agent import SuggesterAgent
from typing import Dict, List, Optional, Any
from idea_potential.structured_outputs import (
    IdeaAnalysisResponse, ClarificationSummaryResponse, UserPersona, IndividualQuestionResponse
)

class ClarifierAgent(BaseAgent):
    """Agent responsible for clarifying and understanding the user's idea through targeted questions"""
    
    def __init__(self, use_suggester_agent: bool = False):
        super().__init__('clarifier')
        self.questions_asked = []
        self.user_responses = []
        self.idea_context = {}
        self.suggester = SuggesterAgent() if use_suggester_agent else None
        self.original_idea = ""
        self.conversation_history = []
        
    def analyze_initial_idea(self, idea: str) -> Dict[str, Any]:
        """Analyze the initial idea and prepare for dynamic questioning"""
        if not self.validate_input(idea):
            return {"error": "Invalid idea input"}
        
        self.original_idea = idea
        self.idea_context = {
            "original_idea": idea,
            "analysis": "",
            "idea_summary": "",
            "conversation_context": []
        }
        
        # Store initial context
        self.conversation_history.append({
            "role": "system",
            "content": f"Initial idea: {idea}"
        })
        
        self.log_activity("Analyzed initial idea", idea)
        return self.idea_context
    
    def generate_next_question(self, user_response: str = None) -> Dict[str, Any]:
        """Dynamically generate the next question based on previous responses and conversation context"""
        
        # Add user response to context if provided
        if user_response:
            self.user_responses.append(user_response)
            self.conversation_history.append({
                "role": "user", 
                "content": user_response
            })
        
        # If this is the first question, generate it based on the original idea
        if len(self.questions_asked) == 0:
            return self._generate_first_question()
        
        # Check if we have enough information to generate a summary
        if self._should_generate_summary():
            return self.generate_clarification_summary()
        
        # Generate the next question based on conversation context
        return self._generate_follow_up_question()
    
    def _generate_first_question(self) -> Dict[str, Any]:
        """Generate the first question based on the original idea"""
        
        prompt = f"""
        You are an expert business analyst and idea validator. Your job is to ask the most critical first question to understand a business idea's potential.

        ORIGINAL IDEA: {self.original_idea}

        Based on this idea, what is the SINGLE most critical question that needs to be answered first to properly evaluate its potential? 

        Focus on the most fundamental aspect that will help understand:
        1. Target market and customer pain points, OR
        2. Value proposition and differentiation, OR  
        3. Feasibility and resources needed

        Please respond with valid JSON format containing:
        {{
            "question": "The single most critical question to ask first",
            "reason": "Why this question is critical and what it will reveal",
            "category": "market|value_proposition|feasibility",
            "question_number": 1,
            "total_questions": "dynamic",
            "status": "asking"
        }}

        For the category field, use exactly one of these values:
        - "market" for questions about target market, customers, or market validation
        - "value_proposition" for questions about value proposition, differentiation, or competitive advantage  
        - "feasibility" for questions about technical feasibility, resources, or implementation
        """
        
        messages = [
            {"role": "system", "content": "You are a business analyst expert at asking the right questions to validate ideas. Always ask ONE question at a time."},
            {"role": "user", "content": prompt}
        ]
        
        try:
            # Try structured output first
            result = self.call_llm_structured(messages, IndividualQuestionResponse, temperature=0.3)
            
            if result:
                question_data = {
                    "question": result.question,
                    "reason": result.reason,
                    "category": result.category,
                    "question_number": result.question_number,
                    "total_questions": result.total_questions,
                    "status": result.status
                }
                
                self.questions_asked.append(question_data)
                self.conversation_history.append({
                    "role": "assistant",
                    "content": f"Question: {question_data['question']}\nReason: {question_data['reason']}"
                })
                
                return question_data
                
        except Exception as e:
            print(f"Error generating first question with structured output: {e}")
        
        # Fallback to regular LLM call
        response = self.call_llm(messages, temperature=0.3)
        result = self.parse_json_response(response)
        
        if result:
            question_data = {
                "question": result.get("question", "What is your target market?"),
                "reason": result.get("reason", "Understanding the target market is critical for idea validation"),
                "category": result.get("category", "market"),
                "question_number": 1,
                "total_questions": "dynamic",
                "status": "asking"
            }
            
            self.questions_asked.append(question_data)
            self.conversation_history.append({
                "role": "assistant", 
                "content": f"Question: {question_data['question']}\nReason: {question_data['reason']}"
            })
            
            return question_data
        
        return {"error": "Failed to generate first question"}
    
    def _generate_follow_up_question(self) -> Dict[str, Any]:
        """Generate the next question based on previous responses and conversation context"""
        
        # Build conversation context
        conversation_summary = self._build_conversation_summary()
        
        prompt = f"""
        You are an expert business analyst conducting a dynamic conversation to validate a business idea. 

        ORIGINAL IDEA: {self.original_idea}

        CONVERSATION HISTORY:
        {conversation_summary}

        Based on the previous questions and answers, what is the NEXT most critical question to ask? 

        Consider:
        1. What gaps in understanding still exist?
        2. What aspect needs more clarification?
        3. What would be the most valuable next piece of information?

        The question should build upon previous answers and move the conversation forward toward a complete understanding of the idea's potential.

        Please respond with valid JSON format containing:
        {{
            "question": "The next critical question to ask",
            "reason": "Why this question is important given the previous answers",
            "category": "market|value_proposition|feasibility",
            "question_number": {len(self.questions_asked) + 1},
            "total_questions": "dynamic",
            "status": "asking"
        }}

        For the category field, use exactly one of these values:
        - "market" for questions about target market, customers, or market validation
        - "value_proposition" for questions about value proposition, differentiation, or competitive advantage
        - "feasibility" for questions about technical feasibility, resources, or implementation
        """
        
        messages = [
            {"role": "system", "content": "You are a business analyst expert at asking the right questions to validate ideas. Always ask ONE question at a time and build upon previous answers."},
            {"role": "user", "content": prompt}
        ]
        
        try:
            # Try structured output first
            result = self.call_llm_structured(messages, IndividualQuestionResponse, temperature=0.3)
            
            if result:
                question_data = {
                    "question": result.question,
                    "reason": result.reason,
                    "category": result.category,
                    "question_number": result.question_number,
                    "total_questions": result.total_questions,
                    "status": result.status
                }
                
                self.questions_asked.append(question_data)
                self.conversation_history.append({
                    "role": "assistant",
                    "content": f"Question: {question_data['question']}\nReason: {question_data['reason']}"
                })
                
                return question_data
                
        except Exception as e:
            print(f"Error generating follow-up question with structured output: {e}")
        
        # Fallback to regular LLM call
        response = self.call_llm(messages, temperature=0.3)
        result = self.parse_json_response(response)
        
        if result:
            question_data = {
                "question": result.get("question", "What is your unique value proposition?"),
                "reason": result.get("reason", "Understanding the value proposition is important for differentiation"),
                "category": result.get("category", "value_proposition"),
                "question_number": len(self.questions_asked) + 1,
                "total_questions": "dynamic",
                "status": "asking"
            }
            
            self.questions_asked.append(question_data)
            self.conversation_history.append({
                "role": "assistant",
                "content": f"Question: {question_data['question']}\nReason: {question_data['reason']}"
            })
            
            return question_data
        
        return {"error": "Failed to generate follow-up question"}
    
    def _build_conversation_summary(self) -> str:
        """Build a summary of the conversation so far"""
        summary = ""
        
        for i, (question, response) in enumerate(zip(self.questions_asked, self.user_responses), 1):
            summary += f"Q{i}: {question['question']}\n"
            summary += f"A{i}: {response}\n\n"
        
        return summary
    
    def _should_generate_summary(self) -> bool:
        """Determine if we have enough information to generate a summary"""
        
        # Check if we have at least 3 questions answered
        if len(self.user_responses) < 3:
            return False
        
        # Check if the last few questions are getting repetitive or less critical
        if len(self.questions_asked) >= 5:
            return True
        
        # Check if we have covered all major categories
        categories_covered = set(q['category'] for q in self.questions_asked)
        if len(categories_covered) >= 3:  # market, value_proposition, feasibility
            return True
        
        # Check if the last response indicates the user feels they've provided enough information
        last_response = self.user_responses[-1].lower() if self.user_responses else ""
        if any(phrase in last_response for phrase in ["that's all", "that's everything", "i think that covers it", "that should be enough"]):
            return True
        
        return False
    
    def ask_next_question(self, user_response: str = None) -> Dict[str, Any]:
        """Ask the next question dynamically based on previous responses"""
        return self.generate_next_question(user_response)
    
    def generate_clarification_summary(self) -> Dict[str, Any]:
        """Generate a summary of all clarifications made with detailed user personas"""
        
        # First, develop detailed user personas
        user_personas = self.develop_user_personas()
        
        prompt = f"""
        Based on the following idea and conversation, create a comprehensive summary of the clarified idea:

        ORIGINAL IDEA: {self.original_idea}
        
        CONVERSATION SUMMARY:
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

        IDEA: {self.original_idea}
        CONVERSATION CONTEXT: {self._build_conversation_summary()}

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
            "total_questions": "dynamic",
            "status": "complete" if self._should_generate_summary() else "in_progress"
        } 