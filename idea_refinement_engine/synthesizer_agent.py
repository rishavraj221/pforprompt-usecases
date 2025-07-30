"""
Synthesizer Agent for Idea Validation Pipeline
"""

import json
from langchain_core.prompts import ChatPromptTemplate
from .base_agent import BaseAgent
from .state import ValidationState
from .report_generator import ComprehensiveReportGenerator


class SynthesizerAgent(BaseAgent):
    """Agent 6: Creates final investment-ready report using comprehensive report generator"""
    
    def __init__(self, llm):
        super().__init__(llm)
        self.report_generator = ComprehensiveReportGenerator()
    
    async def run(self, state: ValidationState) -> ValidationState:
        try:
            # Check if we have at least the basic required data
            if not state.get("clarified_idea"):
                state["errors"].append("Cannot synthesize - missing clarified idea")
                return state
            
            # Create a more flexible data structure for synthesis
            synthesis_data = {
                "clarified_idea": state.get("clarified_idea", {}),
                "idea_variations": state.get("idea_variations", {}),
                "critique_analysis": state.get("critique_analysis", {}),
                "validation_questions": state.get("validation_questions", {}),
                "reality_check": state.get("reality_check", {}),
                "user_validation_responses": state.get("user_validation_responses", [])
            }
            
            # Check if we have at least some meaningful data to synthesize
            meaningful_data = [
                synthesis_data["clarified_idea"],
                synthesis_data["user_validation_responses"]
            ]
            
            if not any(meaningful_data):
                state["errors"].append("Cannot synthesize - insufficient data for analysis")
                return state
                
            # Generate comprehensive report using the new report generator
            final_report = self.report_generator.generate_report(synthesis_data, state["user_idea"])
            
            state["final_report"] = final_report
            state["current_agent"] = "synthesizer"
            
            return state
            
        except Exception as e:
            state["errors"].append(f"Synthesizer error: {str(e)}")
            return state 