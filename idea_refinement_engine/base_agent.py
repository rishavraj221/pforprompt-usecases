"""
Base Agent Class for Idea Validation Pipeline
"""

import json
from typing import Dict, Any
from langchain_openai import ChatOpenAI


class BaseAgent:
    def __init__(self, llm: ChatOpenAI):
        self.llm = llm
        self.max_retries = 3
    
    def parse_json_response(self, response: str) -> Dict[str, Any]:
        """Safely parse JSON from LLM response"""
        try:
            # Extract JSON from response if wrapped in markdown
            if "```json" in response:
                json_str = response.split("```json")[1].split("```")[0].strip()
            else:
                json_str = response.strip()
            return json.loads(json_str)
        except (json.JSONDecodeError, IndexError) as e:
            raise ValueError(f"Invalid JSON response: {e}") 