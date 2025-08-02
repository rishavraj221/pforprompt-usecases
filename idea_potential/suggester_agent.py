from idea_potential.base_agent import BaseAgent
from typing import Dict, List, Optional, Any
from idea_potential.structured_outputs import SuggestionsResponse, Suggestion

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

        Please respond with valid JSON format containing:
        - suggestions: Array of suggestion objects with suggestion, context, and category fields
        - context_analysis: Brief description of what context was considered
        - recommendation_priority: Priority recommendation as a string (e.g., "high", "medium", "low", or descriptive text)

        For the category field, use one of: "specific", "general", "detailed", "brief"
        IMPORTANT: recommendation_priority must be a string, not a number.
        """
        
        messages = [
            {"role": "system", "content": "You are an expert at providing helpful answer suggestions that move conversations forward productively."},
            {"role": "user", "content": prompt}
        ]
        
        try:
            # Try structured output first
            result = self.call_llm_structured(messages, SuggestionsResponse, temperature=0.7)
            
            if result:
                # Convert Pydantic model to dict for compatibility with expected structure
                suggestions_data = {
                    "suggestions": [
                        {
                            "text": s.suggestion,
                            "reasoning": s.context,
                            "category": s.category
                        } for s in result.suggestions
                    ],
                    "context_used": result.context_analysis,
                    "agent_type": agent_type,
                    "question": question,
                    "recommendation_priority": str(result.recommendation_priority) if result.recommendation_priority else "medium"
                }
                
                # Add to context history
                self.context_history.append({
                    "question": question,
                    "agent_type": agent_type,
                    "suggestions": suggestions_data.get("suggestions", []),
                    "timestamp": self._get_timestamp()
                })
                
                self.log_activity(f"Generated {len(result.suggestions)} suggestions for {agent_type} agent")
                return suggestions_data
                
        except Exception as e:
            print(f"Error generating suggestions with structured output: {e}")
        
        # Fallback to regular LLM call
        response = self.call_llm(messages, temperature=0.7)
        result = self.parse_json_response(response)
        
        if result:
            # Ensure the result has the expected structure
            if "suggestions" in result:
                # Convert suggestions to expected format if needed
                suggestions = result.get("suggestions", [])
                formatted_suggestions = []
                for suggestion in suggestions:
                    if isinstance(suggestion, dict):
                        formatted_suggestion = {
                            "text": suggestion.get("text", suggestion.get("suggestion", "No suggestion")),
                            "reasoning": suggestion.get("reasoning", suggestion.get("context", "No reasoning")),
                            "category": suggestion.get("category", "general")
                        }
                        formatted_suggestions.append(formatted_suggestion)
                    else:
                        # Handle case where suggestion is just a string
                        formatted_suggestions.append({
                            "text": str(suggestion),
                            "reasoning": "Generated suggestion",
                            "category": "general"
                        })
                result["suggestions"] = formatted_suggestions
            
            # Ensure recommendation_priority is a string
            if "recommendation_priority" in result:
                result["recommendation_priority"] = str(result["recommendation_priority"])
            else:
                result["recommendation_priority"] = "medium"
            
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