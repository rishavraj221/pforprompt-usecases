import openai
import json
from typing import Dict, Any, List, Optional, Type, TypeVar
from idea_potential.config import OPENAI_API_KEY, MODEL_CONFIG
from pydantic import BaseModel

T = TypeVar('T', bound=BaseModel)

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
            
            # Log token usage
            if hasattr(response, 'usage') and response.usage:
                print(f"[TOKENS] {self.model}: {response.usage.prompt_tokens} prompt + {response.usage.completion_tokens} completion = {response.usage.total_tokens} total")
            
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error calling LLM: {e}")
            return ""
    
    def call_llm_structured(self, messages: List[Dict[str, str]], response_model: Type[T], temperature: float = 0.7) -> Optional[T]:
        """Make a structured call to the OpenAI API using Pydantic models"""
        try:
            # Check if the model supports structured output
            if self.model.startswith('gpt-4o'):
                # Add JSON instruction to the last user message if not already present
                modified_messages = messages.copy()
                if modified_messages and modified_messages[-1]["role"] == "user":
                    if "json" not in modified_messages[-1]["content"].lower():
                        modified_messages[-1]["content"] += "\n\nPlease respond with valid JSON format."
                
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=modified_messages,
                    temperature=temperature,
                    max_tokens=4000,
                    response_format={"type": "json_object"}
                )
                
                # Log token usage
                if hasattr(response, 'usage') and response.usage:
                    print(f"[TOKENS] {self.model}: {response.usage.prompt_tokens} prompt + {response.usage.completion_tokens} completion = {response.usage.total_tokens} total")
                
                # Parse the JSON response
                response_content = response.choices[0].message.content
                if response_content:
                    # Parse JSON and validate with Pydantic model
                    json_data = json.loads(response_content)
                    try:
                        return response_model(**json_data)
                    except Exception as validation_error:
                        print(f"Pydantic validation error: {validation_error}")
                        # Return None to trigger fallback
                        return None
            else:
                # Fallback to regular call for models that don't support structured output
                print(f"Model {self.model} doesn't support structured output, falling back to regular call")
                response_content = self.call_llm(messages, temperature)
                if response_content:
                    result = self.parse_json_response(response_content)
                    if result:
                        return response_model(**result)
                        
        except Exception as e:
            print(f"Error calling LLM with structured output: {e}")
            # Fallback to regular call
            response_content = self.call_llm(messages, temperature)
            if response_content:
                result = self.parse_json_response(response_content)
                if result:
                    try:
                        return response_model(**result)
                    except Exception as parse_error:
                        print(f"Error parsing structured response: {parse_error}")
                        # Try to fix common validation issues
                        try:
                            # Handle enum validation errors by trying to convert values
                            if "enum" in str(parse_error).lower():
                                # This is a complex case, just return None and let the fallback handle it
                                return None
                            elif "list_type" in str(parse_error).lower():
                                # Handle list type errors
                                return None
                            elif "missing" in str(parse_error).lower():
                                # Handle missing field errors
                                return None
                        except:
                            pass
        
        return None
    
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