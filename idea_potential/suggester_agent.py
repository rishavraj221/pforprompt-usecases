from idea_potential.base_agent import BaseAgent
from typing import Dict, List, Optional, Any

class SuggesterAgent(BaseAgent):
    """Generic agent that provides answer suggestions for any agent asking questions"""
    
    def __init__(self):
        super().__init__('suggester')
        self.context_history = []
        
    def generate_suggestions(self, 
                           question: str, 
                           context: Dict[str, Any], 
                           agent_type: str = "unknown",
                           max_suggestions: int = 3) -> Dict[str, Any]:
        """
        Generate answer suggestions for a given question based on context
        
        Args:
            question: The question being asked
            context: Context information about the conversation/idea
            agent_type: Type of agent asking the question (e.g., 'clarifier', 'validator')
            max_suggestions: Maximum number of suggestions to generate (default: 3)
            
        Returns:
            Dict containing suggestions and metadata
        """
        if not self.validate_input(question):
            return {"error": "Invalid question input"}
            
        # Build context string from the provided context
        context_str = self._build_context_string(context)
        
        prompt = f"""
        You are an expert assistant that provides helpful answer suggestions for users.
        
        CONTEXT:
        - Agent Type: {agent_type}
        - Question Context: {context_str}
        
        QUESTION: {question}
        
        Based on the context and the type of agent asking this question, provide {max_suggestions} realistic and helpful answer suggestions that a user might give.
        
        Consider:
        1. The type of agent asking (clarifier, validator, researcher, etc.)
        2. The context of the conversation/idea
        3. What information would be most valuable for that agent
        4. Realistic user responses that would help move the conversation forward
        
        Return your response as JSON with this structure:
        {{
            "suggestions": [
                {{
                    "id": "suggestion_1",
                    "text": "The suggested answer text",
                    "reasoning": "Why this suggestion is helpful",
                    "category": "specific|general|detailed|brief"
                }}
            ],
            "context_used": "Brief description of what context was considered",
            "agent_type": "{agent_type}",
            "question": "{question}"
        }}
        """
        
        messages = [
            {"role": "system", "content": "You are an expert at providing helpful answer suggestions that move conversations forward productively."},
            {"role": "user", "content": prompt}
        ]
        
        response = self.call_llm(messages, temperature=0.7)
        result = self.parse_json_response(response)
        
        if result:
            # Add to context history
            self.context_history.append({
                "question": question,
                "agent_type": agent_type,
                "suggestions": result.get("suggestions", []),
                "timestamp": self._get_timestamp()
            })
            
            self.log_activity(f"Generated {len(result.get('suggestions', []))} suggestions for {agent_type} agent")
        
        return result or {"error": "Failed to generate suggestions"}
    
    def _build_context_string(self, context: Dict[str, Any]) -> str:
        """Build a readable context string from the context dictionary"""
        if not context:
            return "No specific context provided"
        
        context_parts = []
        
        # Handle different types of context
        if isinstance(context, dict):
            if "idea" in context:
                context_parts.append(f"Idea: {context['idea']}")
            
            if "refined_idea" in context:
                context_parts.append(f"Refined Idea: {context['refined_idea']}")
            
            if "target_market" in context:
                context_parts.append(f"Target Market: {context['target_market']}")
            
            if "value_propositions" in context:
                context_parts.append(f"Value Propositions: {', '.join(context['value_propositions'])}")
            
            if "critical_questions" in context:
                context_parts.append(f"Previous Questions: {len(context['critical_questions'])} asked")
            
            if "user_responses" in context:
                context_parts.append(f"Previous Responses: {len(context['user_responses'])} received")
            
            if "analysis" in context:
                context_parts.append(f"Analysis: {context['analysis']}")
        
        return "; ".join(context_parts) if context_parts else "General context"
    
    def _get_timestamp(self) -> str:
        """Get current timestamp"""
        from datetime import datetime
        return datetime.now().isoformat()
    
    def get_suggestion_history(self) -> List[Dict[str, Any]]:
        """Get history of suggestions made"""
        return self.context_history
    
    def clear_history(self):
        """Clear suggestion history"""
        self.context_history = []
        self.log_activity("Cleared suggestion history")
    
    def get_suggestions_for_agent(self, agent_type: str) -> List[Dict[str, Any]]:
        """Get all suggestions made for a specific agent type"""
        return [entry for entry in self.context_history if entry["agent_type"] == agent_type] 