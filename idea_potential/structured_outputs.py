from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional, Union
from enum import Enum

# Enums for structured outputs
class ConfidenceLevel(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    
    @classmethod
    def _missing_(cls, value):
        """Handle case-insensitive matching and partial matches"""
        if isinstance(value, str):
            value_lower = value.lower()
            if "high" in value_lower:
                return cls.HIGH
            elif "medium" in value_lower or "moderate" in value_lower:
                return cls.MEDIUM
            elif "low" in value_lower:
                return cls.LOW
        return None

class RiskLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    
    @classmethod
    def _missing_(cls, value):
        """Handle case-insensitive matching and partial matches"""
        if isinstance(value, str):
            value_lower = value.lower()
            if "high" in value_lower:
                return cls.HIGH
            elif "medium" in value_lower or "moderate" in value_lower:
                return cls.MEDIUM
            elif "low" in value_lower:
                return cls.LOW
        return None

class GoNoGo(str, Enum):
    GO = "go"
    NO_GO = "no_go"
    CONDITIONAL = "conditional"
    
    @classmethod
    def _missing_(cls, value):
        """Handle case-insensitive matching and partial matches"""
        if isinstance(value, str):
            value_lower = value.lower()
            if "go" in value_lower and "no" not in value_lower:
                return cls.GO
            elif "no" in value_lower and "go" in value_lower:
                return cls.NO_GO
            elif "conditional" in value_lower or "proceed" in value_lower:
                return cls.CONDITIONAL
        return None

class QuestionCategory(str, Enum):
    MARKET = "market"
    VALUE_PROPOSITION = "value_proposition"
    FEASIBILITY = "feasibility"
    
    @classmethod
    def _missing_(cls, value):
        """Handle case-insensitive matching and partial matches"""
        if isinstance(value, str):
            value_lower = value.lower()
            if "market" in value_lower or "target" in value_lower:
                return cls.MARKET
            elif "value" in value_lower or "proposition" in value_lower or "differentiation" in value_lower:
                return cls.VALUE_PROPOSITION
            elif "feasibility" in value_lower or "resources" in value_lower or "implementation" in value_lower:
                return cls.FEASIBILITY
        return None

# Research Agent Structured Outputs
class KeywordSubredditResponse(BaseModel):
    keywords: List[str] = Field(description="List of relevant search keywords", max_items=5)
    subreddits: List[str] = Field(description="List of relevant subreddit names", max_items=5)

class CoreConceptsResponse(BaseModel):
    concepts: List[str] = Field(description="List of core concepts extracted from the idea", max_items=8)

class SearchKeywordsResponse(BaseModel):
    keywords: List[str] = Field(description="List of search keywords for Reddit research", max_items=20)

class ChunkAnalysisResponse(BaseModel):
    quantitative_metrics: Dict[str, Any] = Field(description="Quantitative analysis metrics")
    user_feedback: Dict[str, Any] = Field(description="User feedback and insights")
    market_insights: Dict[str, Any] = Field(description="Market insights and trends")
    references: List[Dict[str, Any]] = Field(description="List of Reddit post references")

class MarketInsightsResponse(BaseModel):
    quantitative_metrics: Dict[str, Any] = Field(description="Overall quantitative metrics")
    user_feedback: Dict[str, Any] = Field(description="Aggregated user feedback")
    market_insights: Dict[str, Any] = Field(description="Market insights and trends")
    pain_points: List[str] = Field(description="Identified pain points")
    common_themes: List[str] = Field(description="Common themes in discussions")
    sentiment_analysis: Dict[str, Any] = Field(description="Sentiment analysis results")
    references: List[Dict[str, Any]] = Field(description="All Reddit post references")

# Clarifier Agent Structured Outputs
class CriticalQuestion(BaseModel):
    question: str = Field(description="The critical question to ask")
    reason: str = Field(description="Why this question is critical")
    category: QuestionCategory = Field(description="Category of the question")

class IdeaAnalysisResponse(BaseModel):
    analysis: str = Field(description="Brief analysis of the idea")
    critical_questions: List[CriticalQuestion] = Field(description="List of critical questions", max_items=3)
    idea_summary: str = Field(description="One sentence summary of the idea")

class UserPersona(BaseModel):
    persona_name: str = Field(description="Name of the persona")
    description: str = Field(description="Description of the persona")
    pain_points: List[str] = Field(description="Pain points for this persona")
    goals: List[str] = Field(description="Goals for this persona")
    demographics: Dict[str, Any] = Field(description="Demographic information")

class ClarificationSummaryResponse(BaseModel):
    refined_idea: str = Field(description="Refined version of the idea")
    target_market: str = Field(description="Identified target market")
    value_propositions: List[str] = Field(description="Key value propositions")
    potential_challenges: List[str] = Field(description="Potential challenges")
    user_personas: List[UserPersona] = Field(description="User personas")
    confidence_level: ConfidenceLevel = Field(description="Confidence level in the analysis")

# Validation Agent Structured Outputs
class ValidationCategory(BaseModel):
    score: int = Field(description="Score from 0-10", ge=0, le=10)
    confidence_level: ConfidenceLevel = Field(description="Confidence level in the assessment")
    recommendations: List[str] = Field(description="List of recommendations")

class MarketValidation(ValidationCategory):
    market_size: str = Field(description="Estimated market size and growth potential")
    evidence: List[str] = Field(description="List of supporting evidence")
    risks: List[str] = Field(description="List of market risks")

class TechnicalFeasibility(ValidationCategory):
    requirements: List[str] = Field(description="List of technical requirements")
    challenges: List[str] = Field(description="List of technical challenges")

class FinancialViability(ValidationCategory):
    revenue_potential: str = Field(description="Assessment of revenue potential")
    cost_structure: str = Field(description="Assessment of costs")
    profitability: str = Field(description="Assessment of profitability")

class CompetitiveAdvantage(ValidationCategory):
    competitors: List[str] = Field(description="List of identified competitors")
    differentiators: List[str] = Field(description="List of competitive advantages")
    barriers_to_entry: List[str] = Field(description="List of entry barriers")
    sustainable_advantage: str = Field(description="Assessment of sustainability")

class CustomerAdoption(ValidationCategory):
    customer_segments: List[str] = Field(description="List of customer segments")
    adoption_barriers: List[str] = Field(description="List of adoption barriers")
    value_perception: str = Field(description="Assessment of value perception")

class OverallAssessment(BaseModel):
    total_score: int = Field(description="Total score from 0-50", ge=0, le=50)
    risk_level: RiskLevel = Field(description="Overall risk level")
    go_no_go: GoNoGo = Field(description="Go/No-go decision")
    critical_factors: List[str] = Field(description="List of critical success factors")
    next_steps: List[str] = Field(description="List of immediate next steps")

class ValidationMatrixResponse(BaseModel):
    market_validation: MarketValidation
    technical_feasibility: TechnicalFeasibility
    financial_viability: FinancialViability
    competitive_advantage: CompetitiveAdvantage
    customer_adoption: CustomerAdoption
    overall_assessment: OverallAssessment

class CompetitorAnalysisResponse(BaseModel):
    direct_competitors: List[Dict[str, Any]] = Field(description="Direct competitors analysis")
    indirect_competitors: List[Dict[str, Any]] = Field(description="Indirect competitors analysis")
    competitive_landscape: str = Field(description="Overall competitive landscape assessment")
    differentiation_opportunities: List[str] = Field(description="Opportunities for differentiation")

class MarketSizeEstimateResponse(BaseModel):
    market_size: str = Field(description="Estimated market size")
    growth_potential: str = Field(description="Growth potential assessment")
    target_segments: List[str] = Field(description="Target market segments")
    market_maturity: str = Field(description="Market maturity assessment")

class SWOTAnalysisResponse(BaseModel):
    strengths: List[str] = Field(description="List of strengths")
    weaknesses: List[str] = Field(description="List of weaknesses")
    opportunities: List[str] = Field(description="List of opportunities")
    threats: List[str] = Field(description="List of threats")
    strategic_implications: str = Field(description="Strategic implications of the SWOT analysis")

class RiskAssessmentResponse(BaseModel):
    technical_risks: List[Dict[str, Any]] = Field(description="Technical risks and mitigations")
    market_risks: List[Dict[str, Any]] = Field(description="Market risks and mitigations")
    financial_risks: List[Dict[str, Any]] = Field(description="Financial risks and mitigations")
    operational_risks: List[Dict[str, Any]] = Field(description="Operational risks and mitigations")
    overall_risk_level: RiskLevel = Field(description="Overall risk level")

# Roadmap Agent Structured Outputs
class Milestone(BaseModel):
    title: str = Field(description="Title of the milestone")
    description: str = Field(description="Description of the milestone")
    timeline: str = Field(description="Timeline for the milestone")
    deliverables: List[str] = Field(description="List of deliverables")
    success_criteria: List[str] = Field(description="Success criteria")
    dependencies: List[str] = Field(description="Dependencies for this milestone")

class Phase(BaseModel):
    phase_name: str = Field(description="Name of the phase")
    duration: str = Field(description="Duration of the phase")
    objectives: List[str] = Field(description="Objectives for this phase")
    milestones: List[Milestone] = Field(description="Milestones in this phase")
    key_activities: List[str] = Field(description="Key activities in this phase")
    success_metrics: List[str] = Field(description="Success metrics for this phase")

class RoadmapResponse(BaseModel):
    phases: List[Phase] = Field(description="List of development phases")
    total_timeline: str = Field(description="Total timeline estimate")
    critical_path: List[str] = Field(description="Critical path activities")
    resource_requirements: Dict[str, Any] = Field(description="Resource requirements")
    risk_mitigation: List[str] = Field(description="Risk mitigation strategies")

# Report Agent Structured Outputs
class ReportSection(BaseModel):
    title: str = Field(description="Title of the section")
    content: str = Field(description="Content of the section")
    key_insights: List[str] = Field(description="Key insights from this section")
    data_sources: List[str] = Field(description="Data sources for this section")

class ComprehensiveReportResponse(BaseModel):
    executive_summary: str = Field(description="Executive summary of the report")
    sections: List[ReportSection] = Field(description="Report sections")
    key_findings: List[str] = Field(description="Key findings from the analysis")
    recommendations: List[str] = Field(description="Strategic recommendations")
    appendices: Dict[str, Any] = Field(description="Appendices and supporting data")

# Refiner Agent Structured Outputs
class RefinementSuggestion(BaseModel):
    aspect: str = Field(description="Aspect of the idea to refine")
    current_state: str = Field(description="Current state of this aspect")
    suggested_improvement: str = Field(description="Suggested improvement")
    rationale: str = Field(description="Rationale for the suggestion")
    priority: str = Field(description="Priority level of this suggestion")

class RefinedIdeaResponse(BaseModel):
    original_idea: str = Field(description="Original idea")
    refined_idea: str = Field(description="Refined version of the idea")
    key_improvements: List[str] = Field(description="Key improvements made")
    refinement_suggestions: List[RefinementSuggestion] = Field(description="Detailed refinement suggestions")
    confidence_in_refinement: ConfidenceLevel = Field(description="Confidence in the refinement")

# Validation Response for Refiner Agent
class ValidationIssue(BaseModel):
    issue: str = Field(description="Description of the issue")
    severity: str = Field(description="Severity level (high/medium/low)")
    recommendation: str = Field(description="Recommendation to fix the issue")

class ValidationResponse(BaseModel):
    authenticity_score: int = Field(description="Authenticity score from 0-10", ge=0, le=10)
    consistency_check: str = Field(description="Assessment of consistency between research and report")
    data_quality: str = Field(description="Assessment of data quality (completeness, accuracy, relevance)")
    identified_issues: List[ValidationIssue] = Field(description="List of identified issues")
    report_strengths: List[str] = Field(description="List of report strengths")
    validation_recommendation: str = Field(description="Final recommendation (accept/revise/reject)")
    overall_assessment: str = Field(description="Overall assessment of the report quality")

# Suggester Agent Structured Outputs
class Suggestion(BaseModel):
    suggestion: str = Field(description="The suggestion text")
    context: str = Field(description="Context for this suggestion")
    category: str = Field(description="Category of the suggestion")

class SuggestionsResponse(BaseModel):
    suggestions: List[Suggestion] = Field(description="List of suggestions")
    context_analysis: str = Field(description="Analysis of the context")
    recommendation_priority: str = Field(description="Priority recommendation") 