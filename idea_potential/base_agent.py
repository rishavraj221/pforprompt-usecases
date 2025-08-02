import openai
import json
from typing import Dict, Any, List, Optional
from idea_potential.config import OPENAI_API_KEY, MODEL_CONFIG

class BaseAgent:
    """Base class for all agents in the idea potential analysis system"""
    
    def __init__(self, agent_type: str):
        self.agent_type = agent_type
        self.model = MODEL_CONFIG.get(agent_type, 'gpt-4o')
        self.client = openai.OpenAI(api_key=OPENAI_API_KEY)
        
    def call_llm(self, messages: List[Dict[str, str]], temperature: float = 0.7) -> str:
        """Make a call to the OpenAI API"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=4000
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error calling LLM: {e}")
            return ""
    
    def parse_json_response(self, response: str) -> Optional[Dict[str, Any]]:
        """Parse JSON response from LLM"""
        try:
            # Find JSON in response
            start = response.find('{')
            end = response.rfind('}') + 1
            if start != -1 and end != 0:
                json_str = response[start:end]
                return json.loads(json_str)
        except Exception as e:
            print(f"Error parsing JSON response: {e}")
        return None
    
    def log_activity(self, activity: str, data: Any = None):
        """Log agent activity for debugging"""
        print(f"[{self.agent_type.upper()}] {activity}")
        if data:
            print(f"Data: {data}")
    
    def validate_input(self, input_data: Any) -> bool:
        """Validate input data"""
        if input_data is None or (isinstance(input_data, str) and not input_data.strip()):
            return False
        return True 