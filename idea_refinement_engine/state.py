"""
State Management for Idea Validation Pipeline
"""

from typing import Dict, List, Any, Optional, TypedDict
from enum import Enum


class ValidationState(TypedDict):
    """State object that gets passed between agents"""
    user_idea: str
    clarified_idea: Optional[Dict[str, Any]]
    idea_variations: Optional[Dict[str, Any]]
    critique_analysis: Optional[Dict[str, Any]]
    validation_questions: Optional[Dict[str, Any]]
    reality_check: Optional[Dict[str, Any]]
    final_report: Optional[str]
    current_agent: str
    iteration_count: int
    errors: List[str]
    user_validation_responses: Optional[List[Dict[str, Any]]]
    clarification_history: str
    next_clarification_question: Optional[Dict[str, Any]]
    # Tracking fields for comprehensive reporting
    analysis_start_time: Optional[str]
    validation_id: Optional[str]
    analysis_duration_minutes: Optional[int]


class AgentStatus(Enum):
    INCOMPLETE = "incomplete"
    COMPLETE = "complete"
    ERROR = "error" 