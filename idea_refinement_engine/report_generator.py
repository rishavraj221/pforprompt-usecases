"""
Comprehensive Report Generator for Idea Validation Pipeline
Generates VC-style investment memos with detailed metrics and analysis
"""

import json
import os
from datetime import datetime
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from enum import Enum


class RiskLevel(Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class Verdict(Enum):
    PURSUE = "PURSUE"
    PIVOT = "PIVOT"
    KILL = "KILL"


@dataclass
class MetricScore:
    score: int
    benchmark: str
    description: str


@dataclass
class RiskAssessment:
    risk: str
    probability: str
    impact: str
    mitigation: str


@dataclass
class AssumptionRisk:
    assumption: str
    risk_level: str
    validation_method: str
    timeline: str


class ComprehensiveReportGenerator:
    """Generates comprehensive VC-style investment memos with detailed metrics"""
    
    def __init__(self):
        self.analysis_start_time = None
        self.validation_id = None
        
    def generate_report(self, state: Dict[str, Any], user_idea: str) -> str:
        """Generate comprehensive report from pipeline state"""
        
        # Extract tracking information from state
        analysis_start_time = None
        validation_id = None
        analysis_duration = None
        
        if state.get("analysis_start_time"):
            try:
                analysis_start_time = datetime.fromisoformat(state["analysis_start_time"])
            except:
                analysis_start_time = datetime.now()
        
        validation_id = state.get("validation_id", f"VAL_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
        analysis_duration = state.get("analysis_duration_minutes", 0)
        
        # Extract data from state
        clarified_idea = state.get("clarified_idea", {})
        variations = state.get("idea_variations", {})
        critique = state.get("critique_analysis", {})
        questions = state.get("validation_questions", {})
        reality_check = state.get("reality_check", {})
        user_responses = state.get("user_validation_responses", [])
        
        # Calculate metrics based on actual data
        metrics = self._calculate_metrics(clarified_idea, critique, reality_check, user_responses)
        verdict = self._determine_verdict(metrics, critique, reality_check)
        confidence_score = self._calculate_confidence_score(metrics, user_responses)
        risk_level = self._assess_risk_level(metrics, critique)
        
        # Generate report sections with real data
        report_sections = [
            self._generate_header(user_idea, analysis_start_time, validation_id, analysis_duration),
            self._generate_clarifications_section(clarified_idea),
            self._generate_executive_summary(verdict, confidence_score, risk_level, metrics),
            self._generate_metrics_dashboard(metrics),
            self._generate_problem_solution_analysis(clarified_idea, reality_check, user_responses),
            self._generate_market_landscape(reality_check, critique),
            self._generate_feasibility_assessment(critique),
            self._generate_risks_and_mitigation(critique, reality_check),
            self._generate_execution_roadmap(clarified_idea, critique),
            self._generate_pivot_options(variations),
            self._generate_validation_data_sources(reality_check, user_responses),
            self._generate_recommendation_next_steps(verdict, confidence_score, metrics),
            self._generate_appendices(clarified_idea, variations, critique, reality_check, user_responses)
        ]
        
        return "\n\n".join(report_sections)
    
    def _calculate_metrics(self, clarified_idea: Dict, critique: Dict, reality_check: Dict, user_responses: List) -> Dict[str, MetricScore]:
        """Calculate key metrics for the idea based on actual data"""
        
        # Problem Validation Score (0-10) - based on user responses and market evidence
        problem_validation_score = self._calculate_problem_validation_score(reality_check, user_responses)
        
        # Solution Fit Score (0-10) - based on solution clarity and SWOT analysis
        solution_fit_score = self._calculate_solution_fit_score(clarified_idea, critique)
        
        # Market Opportunity Score (0-10) - based on market research and trends
        market_opportunity_score = self._calculate_market_opportunity_score(reality_check, critique)
        
        # Technical Feasibility Score (0-10) - based on technical complexity assessment
        technical_feasibility_score = self._calculate_technical_feasibility_score(critique)
        
        # Competitive Advantage Score (0-10) - based on competitive analysis and differentiation
        competitive_advantage_score = self._calculate_competitive_advantage_score(reality_check, critique)
        
        # Overall Viability Score - weighted average
        overall_viability = (problem_validation_score + solution_fit_score + market_opportunity_score + 
                           technical_feasibility_score + competitive_advantage_score) // 5
        
        return {
            "problem_validation": MetricScore(problem_validation_score, "7+ = Strong", "Problem validation strength"),
            "solution_fit": MetricScore(solution_fit_score, "6+ = Viable", "Solution-market fit"),
            "market_opportunity": MetricScore(market_opportunity_score, "7+ = Significant", "Market opportunity size"),
            "technical_feasibility": MetricScore(technical_feasibility_score, "6+ = Buildable", "Technical complexity"),
            "competitive_advantage": MetricScore(competitive_advantage_score, "5+ = Defensible", "Competitive positioning"),
            "overall_viability": MetricScore(overall_viability, "7+ = Pursue", "Overall idea viability")
        }
    
    def _calculate_problem_validation_score(self, reality_check: Dict, user_responses: List) -> int:
        """Calculate problem validation score based on actual evidence"""
        score = 3  # Base score
        
        # Add points for user validation responses
        if user_responses:
            positive_responses = sum(1 for resp in user_responses if resp.get("sentiment") == "positive")
            total_responses = len(user_responses)
            if total_responses > 0:
                positive_ratio = positive_responses / total_responses
                score += int(positive_ratio * 4)  # Up to 4 points for positive user feedback
        
        # Add points for market evidence
        if reality_check:
            # Check for forum mentions
            if reality_check.get("market_size_indicators"):
                forum_mentions = reality_check["market_size_indicators"].get("forum_mentions", 0)
                if forum_mentions > 20:
                    score += 2
                elif forum_mentions > 10:
                    score += 1
            
            # Check for web research findings
            if reality_check.get("web_research"):
                existing_solutions = len(reality_check["web_research"].get("existing_solutions", []))
                if existing_solutions > 0:  # Shows market exists
                    score += 1
                
                forum_insights = len(reality_check["web_research"].get("forum_insights", []))
                if forum_insights > 0:
                    score += 1
        
        return min(10, score)
    
    def _calculate_solution_fit_score(self, clarified_idea: Dict, critique: Dict) -> int:
        """Calculate solution-market fit score based on actual data"""
        score = 3  # Base score
        
        # Check if solution is well-defined
        if clarified_idea:
            if clarified_idea.get("proposed_solution"):
                score += 2
            
            if clarified_idea.get("value_proposition"):
                score += 1
            
            if clarified_idea.get("target_users"):
                score += 1
        
        # Check SWOT analysis
        if critique and critique.get("swot_analysis"):
            swot = critique["swot_analysis"]
            strengths = len(swot.get("strengths", []))
            weaknesses = len(swot.get("weaknesses", []))
            
            if strengths > weaknesses:
                score += 2
            elif strengths == weaknesses:
                score += 1
        
        return min(10, score)
    
    def _calculate_market_opportunity_score(self, reality_check: Dict, critique: Dict) -> int:
        """Calculate market opportunity score based on research data"""
        score = 4  # Base score
        
        # Check market feasibility from critique
        if critique and critique.get("feasibility_scores"):
            market_score = critique["feasibility_scores"].get("market", 5)
            score = max(score, market_score)
        
        # Add points for market evidence
        if reality_check:
            if reality_check.get("market_size_indicators"):
                indicators = reality_check["market_size_indicators"]
                forum_mentions = indicators.get("forum_mentions", 0)
                search_volume = indicators.get("search_volume", "Low")
                
                if forum_mentions > 50:
                    score += 2
                elif forum_mentions > 20:
                    score += 1
                
                if search_volume == "High":
                    score += 1
            
            # Check for market trends
            if reality_check.get("web_research") and reality_check["web_research"].get("market_trends"):
                trends = reality_check["web_research"]["market_trends"]
                if len(trends) > 0:
                    score += 1
        
        return min(10, score)
    
    def _calculate_technical_feasibility_score(self, critique: Dict) -> int:
        """Calculate technical feasibility score"""
        if critique and critique.get("feasibility_scores"):
            return critique["feasibility_scores"].get("technical", 5)
        return 5
    
    def _calculate_competitive_advantage_score(self, reality_check: Dict, critique: Dict) -> int:
        """Calculate competitive advantage score"""
        score = 4  # Base score
        
        # Check for competitive analysis
        if reality_check and reality_check.get("web_research"):
            existing_solutions = reality_check["web_research"].get("existing_solutions", [])
            if len(existing_solutions) < 3:  # Fewer competitors = better
                score += 2
            elif len(existing_solutions) < 5:
                score += 1
        
        # Check SWOT opportunities vs threats
        if critique and critique.get("swot_analysis"):
            swot = critique["swot_analysis"]
            opportunities = len(swot.get("opportunities", []))
            threats = len(swot.get("threats", []))
            score += max(0, opportunities - threats)
        
        return min(10, score)
    
    def _determine_verdict(self, metrics: Dict[str, MetricScore], critique: Dict, reality_check: Dict) -> Verdict:
        """Determine the final verdict based on actual data"""
        overall_score = metrics["overall_viability"].score
        
        # Consider risk factors
        risk_factors = 0
        if critique and critique.get("kill_risk") == "high":
            risk_factors += 1
        
        if overall_score >= 7 and risk_factors == 0:
            return Verdict.PURSUE
        elif overall_score >= 4:
            return Verdict.PIVOT
        else:
            return Verdict.KILL
    
    def _calculate_confidence_score(self, metrics: Dict[str, MetricScore], user_responses: List) -> int:
        """Calculate confidence score (0-100) based on data quality"""
        base_score = metrics["overall_viability"].score * 10
        
        # Adjust based on user validation
        if user_responses:
            positive_ratio = sum(1 for resp in user_responses if resp.get("sentiment") == "positive") / len(user_responses)
            base_score += int(positive_ratio * 20)
        
        # Adjust based on data completeness
        data_completeness = 0
        if user_responses:
            data_completeness += 20
        if metrics["problem_validation"].score > 5:
            data_completeness += 20
        if metrics["market_opportunity"].score > 5:
            data_completeness += 20
        
        base_score = min(100, base_score + data_completeness)
        return base_score
    
    def _assess_risk_level(self, metrics: Dict[str, MetricScore], critique: Dict) -> RiskLevel:
        """Assess overall risk level based on actual data"""
        risk_factors = 0
        
        # Count low scores
        for metric in metrics.values():
            if metric.score < 5:
                risk_factors += 1
        
        # Check for high kill risk
        if critique and critique.get("kill_risk") == "high":
            risk_factors += 2
        
        if risk_factors >= 3:
            return RiskLevel.HIGH
        elif risk_factors >= 1:
            return RiskLevel.MEDIUM
        else:
            return RiskLevel.LOW
    
    def _generate_header(self, user_idea: str, analysis_start_time: Optional[datetime], validation_id: str, analysis_duration: int) -> str:
        """Generate report header with real data"""
        duration = f"{analysis_duration} minutes" if analysis_duration else "Unknown"
        
        return f"""🚀 IDEA VALIDATION REPORT
Idea: {user_idea.strip()}
Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
Analysis Duration: {duration}
Validation ID: {validation_id}"""
    
    def _generate_clarifications_section(self, clarified_idea: Dict) -> str:
        """Generate clarifications section if available"""
        if not clarified_idea or clarified_idea.get("status") == "complete":
            return ""
        
        clarifications = []
        if clarified_idea.get("clarification_history"):
            clarifications = clarified_idea["clarification_history"]
        
        if not clarifications:
            return ""
        
        section = "Clarifications:\n"
        for i, clarification in enumerate(clarifications, 1):
            section += f"Q: {clarification.get('question', 'Question')}\n"
            section += f"A: {clarification.get('answer', 'Answer')}\n\n"
        
        return section
    
    def _generate_executive_summary(self, verdict: Verdict, confidence_score: int, risk_level: RiskLevel, metrics: Dict[str, MetricScore]) -> str:
        """Generate executive summary section with real analysis"""
        overall_score = metrics["overall_viability"].score
        
        # Generate bottom line based on actual data
        if verdict == Verdict.PURSUE:
            bottom_line = f"This idea shows strong potential with an overall viability score of {overall_score}/10. Key strengths include problem validation and market opportunity. Proceed with targeted validation and MVP development."
        elif verdict == Verdict.PIVOT:
            bottom_line = f"This idea has moderate potential (score: {overall_score}/10) but requires significant pivots to address identified gaps. Focus on addressing key weaknesses before full development."
        else:
            bottom_line = f"This idea has limited viability (score: {overall_score}/10) with significant risks and challenges. Consider alternative approaches or different problem spaces."
        
        return f"""📊 EXECUTIVE SUMMARY
🎯 VERDICT: {verdict.value}
Confidence Score: {confidence_score}% | Risk Level: {risk_level.value}

Bottom Line: {bottom_line}"""
    
    def _generate_metrics_dashboard(self, metrics: Dict[str, MetricScore]) -> str:
        """Generate metrics dashboard with real scores"""
        dashboard = """📈 Key Metrics Dashboard
Metric|Score|Benchmark
---|---|---
"""
        
        for name, metric in metrics.items():
            display_name = name.replace("_", " ").title()
            dashboard += f"{display_name}|{metric.score}/10|{metric.benchmark}\n"
        
        return dashboard
    
    def _generate_problem_solution_analysis(self, clarified_idea: Dict, reality_check: Dict, user_responses: List) -> str:
        """Generate problem and solution analysis section with real data"""
        
        # Problem analysis
        core_problem = clarified_idea.get("core_problem", "Problem not clearly defined")
        target_users = clarified_idea.get("target_users", "Target users not specified")
        
        # Count evidence
        evidence_count = 0
        if reality_check and reality_check.get("market_size_indicators"):
            evidence_count = reality_check["market_size_indicators"].get("forum_mentions", 0)
        
        # Get user voice
        user_voice = "No user feedback available"
        if user_responses:
            positive_responses = [r for r in user_responses if r.get("sentiment") == "positive"]
            if positive_responses:
                user_voice = f'"{positive_responses[0].get("response", "User feedback")}"'
        
        # Solution analysis
        solution_summary = clarified_idea.get("proposed_solution", "Solution not clearly defined")
        value_proposition = clarified_idea.get("value_proposition", "Value proposition not defined")
        
        # Determine problem severity based on evidence
        if evidence_count > 20:
            severity = "Critical"
            frequency = "Daily"
        elif evidence_count > 10:
            severity = "Important"
            frequency = "Weekly"
        else:
            severity = "Nice-to-have"
            frequency = "Occasional"
        
        # Determine pain point intensity
        if evidence_count > 15:
            intensity = "High"
        elif evidence_count > 5:
            intensity = "Medium"
        else:
            intensity = "Low"
        
        return f"""🎯 PROBLEM & SOLUTION ANALYSIS
The Problem You're Solving
Core Problem: {core_problem}
Problem Validation:
Evidence Found: {evidence_count} mentions across multiple sources
Problem Severity: {severity}
Frequency: {frequency}

Real User Voice: {user_voice}

Target Users:
Primary: {target_users}
Secondary: Additional segments to be defined
Pain Point Intensity: {intensity} - based on forum sentiment

Your Proposed Solution
Solution Summary: {solution_summary}
Unique Value Proposition: {value_proposition}
Solution-Problem Fit Score: {self._calculate_solution_fit_score(clarified_idea, {})}/10

✅ Strengths: Direct alignment with identified problem
⚠️ Gaps: Areas where solution doesn't fully address problem need further definition"""
    
    def _generate_market_landscape(self, reality_check: Dict, critique: Dict) -> str:
        """Generate market landscape section with real data"""
        
        # Market opportunity
        forum_mentions = 0
        search_volume = "Low"
        growth_trend = "Stable"
        
        if reality_check and reality_check.get("market_size_indicators"):
            indicators = reality_check["market_size_indicators"]
            forum_mentions = indicators.get("forum_mentions", 0)
            search_volume = indicators.get("search_volume", "Low")
            growth_trend = indicators.get("growth_trend", "Stable")
        
        # Competitive analysis
        competitors = []
        if reality_check and reality_check.get("web_research"):
            competitors = reality_check["web_research"].get("existing_solutions", [])
        
        competitive_analysis = ""
        for i, competitor in enumerate(competitors[:3], 1):
            name = competitor.get("name", f"Competitor {i}")
            strengths = competitor.get("strengths", [])
            weaknesses = competitor.get("weaknesses", [])
            sentiment = competitor.get("user_sentiment", "neutral")
            
            competitive_analysis += f"{name}|• {chr(10).join(strengths[:2])}|• {chr(10).join(weaknesses[:2])}|{sentiment.title()}\n"
        
        if not competitive_analysis:
            competitive_analysis = "No competitors identified|N/A|N/A|N/A\n"
        
        # Unmet needs
        unmet_needs = []
        if reality_check and reality_check.get("web_research"):
            forum_insights = reality_check["web_research"].get("forum_insights", [])
            for insight in forum_insights:
                pain_points = insight.get("pain_points", [])
                unmet_needs.extend(pain_points)
        
        return f"""🏪 MARKET LANDSCAPE
Market Opportunity
Market Size Indicators:
Forum Mentions: {forum_mentions} discussions found
Search Volume: {search_volume} based on community activity
Growth Trend: {growth_trend}

Competitive Analysis
Competitor|Strengths|Weaknesses|Market Position
---|---|---|---
{competitive_analysis}
Your Competitive Edge: Differentiation strategy needs to be defined

Unmet Needs Discovery
Based on community analysis, users are frustrated with:

{self._format_unmet_needs(unmet_needs)}

Opportunity: How your solution addresses these gaps needs to be defined"""
    
    def _format_unmet_needs(self, unmet_needs: List) -> str:
        """Format unmet needs for display"""
        if not unmet_needs:
            return "[Pain Point 1]: \"No specific pain points identified\""
        
        formatted = ""
        for i, need in enumerate(unmet_needs[:3], 1):
            formatted += f"[Pain Point {i}]: \"{need}\"\n"
        return formatted.strip()
    
    def _generate_feasibility_assessment(self, critique: Dict) -> str:
        """Generate feasibility assessment section with real data"""
        
        feasibility_scores = critique.get("feasibility_scores", {}) if critique else {}
        
        technical_score = feasibility_scores.get("technical", 5)
        market_score = feasibility_scores.get("market", 5)
        operational_score = feasibility_scores.get("operational", 5)
        
        # Determine complexity level
        if technical_score >= 8:
            complexity = "Simple"
        elif technical_score >= 6:
            complexity = "Moderate"
        elif technical_score >= 4:
            complexity = "Complex"
        else:
            complexity = "Highly Complex"
        
        # Determine market maturity
        if market_score >= 8:
            maturity = "Mature"
        elif market_score >= 6:
            maturity = "Growing"
        elif market_score >= 4:
            maturity = "Emerging"
        else:
            maturity = "Declining"
        
        # Determine customer acquisition difficulty
        if market_score >= 8:
            acquisition = "Easy"
        elif market_score >= 6:
            acquisition = "Moderate"
        else:
            acquisition = "Difficult"
        
        # Determine competition intensity
        if market_score >= 8:
            competition = "Low"
        elif market_score >= 6:
            competition = "Medium"
        else:
            competition = "High"
        
        # Determine resource intensity
        if operational_score >= 8:
            resource_intensity = "Low"
        elif operational_score >= 6:
            resource_intensity = "Medium"
        else:
            resource_intensity = "High"
        
        return f"""🔍 FEASIBILITY ASSESSMENT
Technical Feasibility: {technical_score}/10

Complexity Level: {complexity}
Technology Requirements: [List key technologies needed]
Development Timeline: [Estimated months to MVP]
Technical Risks: [Key technical challenges]

Market Feasibility: {market_score}/10

Market Maturity: {maturity}
Customer Acquisition: {acquisition}
Competition Intensity: {competition}

Operational Feasibility: {operational_score}/10

Team Requirements: [Team size needed to execute]
Resource Intensity: {resource_intensity}
Scalability: [How well can this scale]"""
    
    def _generate_risks_and_mitigation(self, critique: Dict, reality_check: Dict) -> str:
        """Generate risks and mitigation section with real data"""
        
        # Deal-breaker risks
        deal_breaker_risks = []
        if critique and critique.get("assumption_risks"):
            for risk in critique["assumption_risks"][:3]:
                parts = risk.split(":")
                if len(parts) >= 2:
                    assumption = parts[0]
                    risk_level = parts[1] if len(parts) > 1 else "Medium"
                    deal_breaker_risks.append({
                        "risk": assumption,
                        "probability": risk_level,
                        "impact": "Critical",
                        "mitigation": "Specific action to validate/address"
                    })
        
        # Assumption risks
        assumption_risks = []
        if critique and critique.get("assumption_risks"):
            for risk in critique["assumption_risks"][:2]:
                parts = risk.split(":")
                if len(parts) >= 2:
                    assumption = parts[0]
                    risk_level = parts[1] if len(parts) > 1 else "Medium"
                    assumption_risks.append({
                        "assumption": assumption,
                        "risk_level": risk_level,
                        "validation_method": "Survey/Interview/Prototype test",
                        "timeline": "When to validate"
                    })
        
        return f"""⚠️ CRITICAL RISKS & MITIGATION
🚨 Deal-Breaker Risks

{self._format_deal_breaker_risks(deal_breaker_risks)}

🔧 Assumption Risks
Critical Assumptions That Need Validation:

{self._format_assumption_risks(assumption_risks)}"""
    
    def _format_deal_breaker_risks(self, risks: List[Dict]) -> str:
        """Format deal-breaker risks"""
        if not risks:
            return """[Risk 1 - e.g., "Market too small"]
Probability: High/Medium/Low
Impact: Critical/High/Medium
Mitigation: Specific action to validate/address"""
        
        formatted = ""
        for i, risk in enumerate(risks, 1):
            formatted += f"""[Risk {i} - {risk['risk']}]
Probability: {risk['probability']}
Impact: {risk['impact']}
Mitigation: {risk['mitigation']}

"""
        return formatted.strip()
    
    def _format_assumption_risks(self, risks: List[Dict]) -> str:
        """Format assumption risks"""
        if not risks:
            return """ [Assumption 1]: [e.g., "Users will pay $X/month"]
Risk Level: High/Medium/Low
Validation Method: Survey/Interview/Prototype test
Timeline: When to validate"""
        
        formatted = ""
        for i, risk in enumerate(risks, 1):
            formatted += f""" [Assumption {i}]: {risk['assumption']}
Risk Level: {risk['risk_level']}
Validation Method: {risk['validation_method']}
Timeline: {risk['timeline']}

"""
        return formatted.strip()
    
    def _generate_execution_roadmap(self, clarified_idea: Dict, critique: Dict) -> str:
        """Generate execution roadmap section with real data"""
        
        # Determine timeline based on technical feasibility
        technical_score = 5
        if critique and critique.get("feasibility_scores"):
            technical_score = critique["feasibility_scores"].get("technical", 5)
        
        if technical_score >= 8:
            mvp_timeline = "8-12 weeks"
            team_size = "1-2 developers"
        elif technical_score >= 6:
            mvp_timeline = "12-16 weeks"
            team_size = "2-3 developers"
        else:
            mvp_timeline = "16-24 weeks"
            team_size = "3-4 developers"
        
        return f"""📋 EXECUTION ROADMAP
Phase 1: Validation (Weeks 1-4)
Goal: Validate core assumptions with minimal investment
Critical Validation Questions:

[Question 1]: [e.g., "Will target users pay for this solution?"]
Test Method: [Customer interviews/Landing page test/Survey]
Success Criteria: [Specific metric]
Budget: [Cost estimate]

[Question 2]: [e.g., "Can we build the core feature?"]
Test Method: [Technical prototype/API exploration]
Success Criteria: [Working demo]
Budget: [Cost]

Phase 1 Budget: $[X] | Timeline: [X] weeks

Phase 2: MVP Development (Weeks 5-16)
Goal: Build and launch minimum viable product
Key Milestones:
 Week 6: [Milestone 1]
 Week 10: [Milestone 2]
 Week 14: [Milestone 3]
 Week 16: [MVP Launch]

Resource Requirements:
Team: {team_size}
Budget: $[X] total
Timeline: {mvp_timeline}

Phase 3: Growth (Month 4+)
Goal: Scale based on MVP learnings
Success Metrics:
 active users by month 6
[X]% customer satisfaction
$[X] monthly revenue by month 12"""
    
    def _generate_pivot_options(self, variations: Dict) -> str:
        """Generate pivot options section with real data"""
        
        practical_variations = []
        wildcard_concepts = []
        
        if variations:
            practical_variations = variations.get("practical_variations", [])
            wildcard_concepts = variations.get("wildcard_concepts", [])
        
        variation1 = practical_variations[0] if practical_variations else '[Wildcard concept from brainstorming]'
        variation2 = practical_variations[1] if len(practical_variations) > 1 else '[Another variation]'
        
        return f"""🔄 PIVOT OPTIONS
If Core Idea Fails
Alternative Approach 1: {variation1}

Why it might work: [Reasoning]
Validation needed: [Quick test]

Alternative Approach 2: {variation2}

Why it might work: [Reasoning]
Validation needed: [Test approach]

Adjacent Opportunities
During research, we discovered related problems:

[Adjacent Problem 1]: [Brief description]
[Adjacent Problem 2]: [Brief description]"""
    
    def _generate_validation_data_sources(self, reality_check: Dict, user_responses: List) -> str:
        """Generate validation data sources section with real data"""
        
        sources_analyzed = []
        if reality_check and reality_check.get("sources_analyzed"):
            sources_analyzed = reality_check["sources_analyzed"]
        
        sentiment_analysis = {
            "positive": 0,
            "neutral": 0,
            "negative": 0
        }
        
        if user_responses:
            total_responses = len(user_responses)
            positive = sum(1 for r in user_responses if r.get("sentiment") == "positive")
            negative = sum(1 for r in user_responses if r.get("sentiment") == "negative")
            neutral = total_responses - positive - negative
            
            sentiment_analysis = {
                "positive": int((positive / total_responses) * 100) if total_responses > 0 else 0,
                "neutral": int((neutral / total_responses) * 100) if total_responses > 0 else 0,
                "negative": int((negative / total_responses) * 100) if total_responses > 0 else 0
            }
        
        # Count sources
        reddit_posts = 0
        subreddits = []
        if reality_check and reality_check.get("reddit_analysis"):
            reddit_data = reality_check["reddit_analysis"]
            reddit_posts = reddit_data.get("total_posts", 0)
            subreddits = reddit_data.get("subreddits_analyzed", [])
        
        return f"""📊 VALIDATION DATA SOURCES
Community Research Summary
Sources Analyzed:

Reddit: {reddit_posts} posts across {', '.join(subreddits) if subreddits else '[subreddits]'}
Forums: [Platform names]
Social Media: [Platforms if applicable]

Sentiment Analysis:

Positive: {sentiment_analysis['positive']}% of mentions
Neutral: {sentiment_analysis['neutral']}%
Negative: {sentiment_analysis['negative']}%

Key Discussion Themes:

[Theme 1] - mentioned [X] times
[Theme 2] - mentioned [X] times

Expert Validation
Consultation Sources: [If any expert input was gathered]"""
    
    def _generate_recommendation_next_steps(self, verdict: Verdict, confidence_score: int, metrics: Dict[str, MetricScore]) -> str:
        """Generate recommendation and next steps section with real analysis"""
        
        overall_score = metrics["overall_viability"].score
        
        if verdict == Verdict.PURSUE:
            reasoning = f"Based on the analysis, this idea shows strong potential with an overall viability score of {overall_score}/10. The problem validation and market opportunity scores indicate a real market need. The technical feasibility is manageable, and the competitive landscape shows opportunities for differentiation."
        elif verdict == Verdict.PIVOT:
            reasoning = f"The analysis reveals moderate potential (score: {overall_score}/10) but significant areas for improvement. Key weaknesses need to be addressed before full development. The idea has merit but requires strategic pivots to maximize success probability."
        else:
            reasoning = f"The analysis indicates limited viability (score: {overall_score}/10) with significant risks and challenges. The market opportunity may be too small, technical complexity too high, or competitive barriers too strong. Consider alternative approaches."
        
        return f"""🎯 RECOMMENDATION & NEXT STEPS
Primary Recommendation: {verdict.value}
Reasoning:
{reasoning}

Immediate Next Actions (This Week)

[Action 1]: [Specific task with owner and deadline]
[Action 2]: [Task]
[Action 3]: [Task]

Success Criteria for Next Phase

 [Criterion 1 with metric]
 [Criterion 2 with metric]
 [Criterion 3 with metric]

Review Date: [When to reassess based on new data]"""
    
    def _generate_appendices(self, clarified_idea: Dict, variations: Dict, critique: Dict, reality_check: Dict, user_responses: List = None) -> str:
        """Generate appendices section with real data"""
        
        # SWOT Analysis
        swot_analysis = ""
        if critique and critique.get("swot_analysis"):
            swot = critique["swot_analysis"]
            swot_analysis = f"""A. Detailed SWOT Analysis
Strengths: {self._format_list(swot.get('strengths', []))}
Weaknesses: {self._format_list(swot.get('weaknesses', []))}
Opportunities: {self._format_list(swot.get('opportunities', []))}
Threats: {self._format_list(swot.get('threats', []))}"""
        
        # Brainstorming Variations
        practical_variations = []
        wildcard_concepts = []
        if variations:
            practical_variations = variations.get("practical_variations", [])
            wildcard_concepts = variations.get("wildcard_concepts", [])
        
        variations_section = f"""B. Brainstorming Variations
Practical Variations Explored:

{self._format_list(practical_variations)}

Wildcard Concepts:

{self._format_list(wildcard_concepts)}"""
        
        # Calculate validation confidence based on user responses
        if user_responses is None:
            user_responses = []
        validation_confidence = 'High' if len(user_responses) > 5 else 'Medium' if len(user_responses) > 2 else 'Low'
        
        return f"""📎 APPENDICES
{swot_analysis}

{variations_section}

C. Raw Research Data
[Links or summaries of forum posts, competitor analysis details, etc.]

📞 Questions About This Analysis?
This report was generated by AI analysis and community research. For clarification on methodology or specific findings, please review the validation questions section or conduct additional targeted research on flagged assumptions.
Last Updated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
Validation Confidence: {validation_confidence} based on data quality and coverage

Report Generated By: Idea Refinement Engine by pforprompt
Agents Used: [Model names] | Analysis Depth: [X] forums, [Y] data points"""
    
    def _format_list(self, items: List) -> str:
        """Format a list for display"""
        if not items:
            return "[No items available]"
        return "\n".join([f"• {item}" for item in items]) 