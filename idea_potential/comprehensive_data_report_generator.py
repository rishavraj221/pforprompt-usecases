import json
import asyncio
from typing import Dict, List, Any, Optional
from datetime import datetime
import os
from idea_potential.base_agent import BaseAgent


class ComprehensiveDataReportGenerator(BaseAgent):
    """
    Agent responsible for generating comprehensive analysis reports from JSON data.
    Extracts and includes ALL data from the JSON file (except raw Reddit posts).
    """
    
    def __init__(self):
        super().__init__('comprehensive_data_report_generator')
        self.report_sections = {}
        self.source_references = {}
        
    def load_json_data(self, json_file_path: str) -> Dict[str, Any]:
        """Load and parse the JSON analysis data"""
        try:
            with open(json_file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
            self.log_activity(f"Successfully loaded JSON data from {json_file_path}")
            return data
        except Exception as e:
            self.log_activity(f"Error loading JSON file: {e}")
            raise
    
    def extract_source_references(self, data: Dict[str, Any]) -> Dict[str, List[Dict[str, Any]]]:
        """Extract all source URLs and references from the data"""
        references = {
            'reddit_posts': [],
            'market_sources': [],
            'technical_sources': [],
            'financial_sources': []
        }
        
        # Extract Reddit post URLs from research data
        if 'detailed_data' in data and 'research' in data['detailed_data']:
            research_data = data['detailed_data']['research']
            if 'posts_collected' in research_data:
                for post in research_data['posts_collected']:
                    if 'url' in post:
                        references['reddit_posts'].append({
                            'title': post.get('title', ''),
                            'url': post['url'],
                            'subreddit': post.get('subreddit', ''),
                            'score': post.get('score', 0),
                            'relevance_score': post.get('relevance_score', 0)
                        })
        
        return references
    
    def process_executive_summary_section(self, data: Dict[str, Any]) -> str:
        """Process executive summary with ALL available data"""
        
        executive_data = data.get('executive_summary', {})
        idea_summary = data.get('idea_summary', '')
        target_market = data.get('target_market', '')
        analysis_timestamp = data.get('analysis_timestamp', '')
        pipeline_status = data.get('pipeline_status', '')
        
        prompt = f"""
        Create a comprehensive executive summary section for a business idea analysis report.
        
        ANALYSIS METADATA:
        - Analysis Timestamp: {analysis_timestamp}
        - Pipeline Status: {pipeline_status}
        
        IDEA SUMMARY: {idea_summary}
        TARGET MARKET: {target_market}
        
        EXECUTIVE SUMMARY DATA:
        {json.dumps(executive_data, indent=2)}
        
        Create a professional executive summary that includes:
        1. **Idea Overview** - Clear description of the business idea
        2. **Key Findings** - Most important insights from the analysis
        3. **Recommendation** - Clear go/no-go recommendation with confidence level
        4. **Strategic Implications** - What this means for stakeholders
        5. **Next Steps** - Immediate actions to take
        6. **Analysis Context** - When and how the analysis was conducted
        
        Format as clean markdown with proper headings, bullet points, and emphasis.
        Make it executive-friendly and actionable.
        """
        
        return self.call_llm([{"role": "user", "content": prompt}])
    
    def process_clarification_section(self, data: Dict[str, Any]) -> str:
        """Process ALL clarification data including user personas, value propositions, etc."""
        
        detailed_data = data.get('detailed_data', {})
        clarification = detailed_data.get('clarification', {})
        
        # Extract ALL clarification data
        refined_idea = clarification.get('refined_idea', '')
        target_market = clarification.get('target_market', '')
        user_personas = clarification.get('user_personas', {})
        value_propositions = clarification.get('value_propositions', [])
        potential_challenges = clarification.get('potential_challenges', [])
        validation_priorities = clarification.get('validation_priorities', [])
        status = clarification.get('status', '')
        
        prompt = f"""
        Create a comprehensive clarification section for a business idea report.
        
        REFINED IDEA: {refined_idea}
        TARGET MARKET: {target_market}
        STATUS: {status}
        
        USER PERSONAS:
        {json.dumps(user_personas, indent=2)}
        
        VALUE PROPOSITIONS:
        {json.dumps(value_propositions, indent=2)}
        
        POTENTIAL CHALLENGES:
        {json.dumps(potential_challenges, indent=2)}
        
        VALIDATION PRIORITIES:
        {json.dumps(validation_priorities, indent=2)}
        
        Create a detailed clarification analysis that includes:
        1. **Refined Idea** - Complete description of the refined business idea
        2. **Target Market Analysis** - Detailed breakdown of target audience
        3. **User Personas** - Complete profiles of primary and secondary users with all details
        4. **Value Propositions** - All identified value propositions and benefits
        5. **Potential Challenges** - All identified challenges and risks
        6. **Validation Priorities** - Key areas that need validation
        7. **Status Assessment** - Current status of the idea clarification
        
        Include ALL the detailed information provided, not just summaries.
        Format as professional markdown with tables, bullet points, and clear sections.
        """
        
        return self.call_llm([{"role": "user", "content": prompt}])
    
    def process_research_section(self, data: Dict[str, Any]) -> str:
        """Process ALL research data including insights, quantitative data, market insights"""
        
        detailed_data = data.get('detailed_data', {})
        research = detailed_data.get('research', {})
        research_summary = data.get('research_summary', {})
        
        # Extract ALL research data
        keywords_used = research.get('keywords_used', [])
        posts_collected = research.get('posts_collected', [])
        insights = research.get('insights', {})
        quantitative_data = research.get('quantitative_data', {})
        
        # Extract market insights
        market_insights = insights.get('market_insights', {})
        user_feedback = insights.get('user_feedback', {})
        sentiment_breakdown = insights.get('sentiment_breakdown', {})
        quantitative_metrics = insights.get('quantitative_metrics', {})
        
        prompt = f"""
        Create a comprehensive research section for a business idea report.
        
        RESEARCH SUMMARY:
        Posts Analyzed: {research_summary.get('posts_analyzed', 0)}
        Market Validation: {research_summary.get('market_validation', 'Unknown')}
        Pain Points Identified: {research_summary.get('pain_points_identified', [])}
        
        KEYWORDS USED:
        {json.dumps(keywords_used, indent=2)}
        
        MARKET INSIGHTS:
        {json.dumps(market_insights, indent=2)}
        
        USER FEEDBACK:
        {json.dumps(user_feedback, indent=2)}
        
        SENTIMENT BREAKDOWN:
        {json.dumps(sentiment_breakdown, indent=2)}
        
        QUANTITATIVE METRICS:
        {json.dumps(quantitative_metrics, indent=2)}
        
        QUANTITATIVE DATA:
        {json.dumps(quantitative_data, indent=2)}
        
        Create a detailed research analysis that includes:
        1. **Research Methodology** - How the research was conducted
        2. **Market Insights** - All market-related findings and insights
        3. **User Feedback Analysis** - Complete analysis of user feedback
        4. **Sentiment Analysis** - Detailed sentiment breakdown
        5. **Quantitative Metrics** - All numerical data and statistics
        6. **Keyword Analysis** - Analysis of keywords used in research
        7. **Pain Points** - All identified pain points and problems
        8. **Research Summary** - Overall research findings and conclusions
        
        Include ALL the detailed information provided, not just summaries.
        Format as professional markdown with tables, charts, and clear sections.
        """
        
        return self.call_llm([{"role": "user", "content": prompt}])
    
    def process_validation_section(self, data: Dict[str, Any]) -> str:
        """Process ALL validation data including validation matrix, SWOT analysis, risk assessment"""
        
        detailed_data = data.get('detailed_data', {})
        validation = detailed_data.get('validation', {})
        validation_summary = data.get('validation_summary', {})
        
        # Extract ALL validation data
        validation_matrix = validation.get('validation_matrix', {})
        swot_analysis = validation.get('swot_analysis', {})
        risk_assessment = validation.get('risk_assessment', {})
        
        prompt = f"""
        Create a comprehensive validation section for a business idea report.
        
        VALIDATION SUMMARY:
        Overall Score: {validation_summary.get('overall_score', 'Unknown')}
        Risk Level: {validation_summary.get('risk_level', 'Unknown')}
        Recommendation: {validation_summary.get('recommendation', 'Unknown')}
        
        VALIDATION MATRIX:
        {json.dumps(validation_matrix, indent=2)}
        
        SWOT ANALYSIS:
        {json.dumps(swot_analysis, indent=2)}
        
        RISK ASSESSMENT:
        {json.dumps(risk_assessment, indent=2)}
        
        Create a detailed validation analysis that includes:
        1. **Market Validation** - Complete market validation analysis with scores, evidence, risks, and recommendations
        2. **Technical Feasibility** - Full technical assessment with requirements, challenges, and confidence levels
        3. **Financial Viability** - Complete financial analysis with revenue potential, cost structure, and profitability
        4. **Competitive Advantage** - Detailed competitive analysis with competitors, differentiators, and barriers
        5. **Customer Adoption** - Complete customer adoption analysis with segments, barriers, and value perception
        6. **SWOT Analysis** - Detailed strengths, weaknesses, opportunities, and threats
        7. **Risk Assessment** - Comprehensive risk analysis with mitigation strategies
        8. **Overall Validation Score** - Summary of all validation scores and recommendations
        
        Include ALL the detailed information provided, not just summaries.
        Format as professional markdown with tables, scorecards, and clear sections.
        """
        
        return self.call_llm([{"role": "user", "content": prompt}])
    
    def process_roadmap_section(self, data: Dict[str, Any]) -> str:
        """Process ALL roadmap data including development phases, resource planning, priority matrix"""
        
        detailed_data = data.get('detailed_data', {})
        roadmap = detailed_data.get('roadmap', {})
        roadmap_summary = data.get('roadmap_summary', {})
        
        # Extract ALL roadmap data
        development_roadmap = roadmap.get('development_roadmap', {})
        resource_plan = roadmap.get('resource_plan', {})
        priority_matrix = roadmap.get('priority_matrix', {})
        
        prompt = f"""
        Create a comprehensive roadmap section for a business idea report.
        
        ROADMAP SUMMARY:
        Overall Timeline: {roadmap_summary.get('overall_timeline', 'Unknown')}
        Key Phases: {json.dumps(roadmap_summary.get('key_phases', []), indent=2)}
        Critical Milestones: {json.dumps(roadmap_summary.get('critical_milestones', []), indent=2)}
        
        DEVELOPMENT ROADMAP:
        {json.dumps(development_roadmap, indent=2)}
        
        RESOURCE PLAN:
        {json.dumps(resource_plan, indent=2)}
        
        PRIORITY MATRIX:
        {json.dumps(priority_matrix, indent=2)}
        
        Create a detailed roadmap analysis that includes:
        1. **Development Phases** - Complete breakdown of all development phases with timelines
        2. **Resource Requirements** - Detailed resource planning including team, technology, and budget
        3. **Priority Matrix** - Complete priority analysis for all tasks and features
        4. **Critical Milestones** - All critical milestones and success criteria
        5. **Timeline Analysis** - Detailed timeline breakdown and dependencies
        6. **Resource Allocation** - Complete resource allocation plan
        7. **Risk Mitigation** - How to handle potential delays and issues
        8. **Success Metrics** - How to measure progress and success at each phase
        
        Include ALL the detailed information provided, not just summaries.
        Format as professional markdown with timelines, tables, and clear sections.
        """
        
        return self.call_llm([{"role": "user", "content": prompt}])
    
    def process_refinement_section(self, data: Dict[str, Any]) -> str:
        """Process ALL refinement data including gap analysis, recommendations, quality assessment"""
        
        detailed_data = data.get('detailed_data', {})
        refinement = detailed_data.get('refinement', {})
        refinement_summary = data.get('refinement_summary', {})
        
        # Extract ALL refinement data
        gap_analysis = refinement.get('gap_analysis', {})
        refinement_recommendations = refinement.get('refinement_recommendations', {})
        final_summary = refinement.get('final_summary', {})
        
        prompt = f"""
        Create a comprehensive refinement section for a business idea report.
        
        REFINEMENT SUMMARY:
        Quality Score: {refinement_summary.get('quality_score', 'Unknown')}
        Authenticity: {refinement_summary.get('authenticity', 'Unknown')}
        Final Recommendation: {refinement_summary.get('final_recommendation', 'Unknown')}
        
        GAP ANALYSIS:
        {json.dumps(gap_analysis, indent=2)}
        
        REFINEMENT RECOMMENDATIONS:
        {json.dumps(refinement_recommendations, indent=2)}
        
        FINAL SUMMARY:
        {json.dumps(final_summary, indent=2)}
        
        Create a detailed refinement analysis that includes:
        1. **Gap Analysis** - Complete analysis of critical gaps and missing information
        2. **Quality Assessment** - Detailed quality and authenticity evaluation
        3. **Refinement Priorities** - All high, medium, and low priority improvements
        4. **Implementation Plan** - Detailed plan for addressing identified gaps
        5. **Final Recommendations** - Complete next steps and priorities
        6. **Quality Metrics** - All quality indicators and scores
        7. **Improvement Roadmap** - Detailed plan for enhancing the business idea
        8. **Success Criteria** - How to measure improvement and track progress
        
        Include ALL the detailed information provided, not just summaries.
        Format as professional markdown with priority matrices, action items, and clear sections.
        """
        
        return self.call_llm([{"role": "user", "content": prompt}])
    
    def create_source_references_section(self, references: Dict[str, List[Dict[str, Any]]]) -> str:
        """Create a comprehensive source references section"""
        
        prompt = f"""
        Create a comprehensive source references section for a business idea analysis report.
        
        SOURCE REFERENCES:
        {json.dumps(references, indent=2)}
        
        Create a detailed source references section that includes:
        1. **Reddit Posts Analyzed** - Complete list of relevant Reddit posts with URLs and relevance scores
        2. **Market Research Sources** - External market research and industry reports
        3. **Technical References** - Technical documentation and feasibility studies
        4. **Financial Sources** - Financial models and market data sources
        
        For each source, include:
        - Title/Description
        - URL/Link
        - Relevance score or importance
        - Key insights extracted
        
        Format as a professional markdown table with clear organization and easy navigation.
        Include a summary of how many sources were analyzed and their overall relevance.
        """
        
        return self.call_llm([{"role": "user", "content": prompt}])
    
    def synthesize_final_report(self, sections: Dict[str, str], references: Dict[str, List[Dict[str, Any]]]) -> str:
        """Combine all sections into a final comprehensive report"""
        
        prompt = f"""
        Create a comprehensive business idea analysis report by synthesizing all sections.
        
        REPORT SECTIONS:
        {json.dumps({k: v[:1000] + "..." if len(v) > 1000 else v for k, v in sections.items()}, indent=2)}
        
        SOURCE REFERENCES:
        {json.dumps(references, indent=2)}
        
        Create a professional, comprehensive report that includes:
        
        1. **Title Page** - Professional title with date and version
        2. **Table of Contents** - Clear navigation structure
        3. **Executive Summary** - High-level overview and key recommendations
        4. **Clarification Analysis** - Complete idea clarification with user personas and value propositions
        5. **Research Analysis** - Comprehensive market research and user feedback analysis
        6. **Validation Assessment** - Complete technical, financial, and market validation
        7. **Development Roadmap** - Detailed implementation plan and timeline
        8. **Refinement Recommendations** - Complete quality assessment and improvement areas
        9. **Source References** - Complete list of sources and references
        10. **Appendices** - Detailed data and supporting information
        
        Format as a professional markdown document with:
        - Clear hierarchy and navigation
        - Professional formatting and styling
        - Cross-references between sections
        - Executive-friendly language
        - Actionable insights and recommendations
        - Complete source attribution
        
        Make it suitable for stakeholders, investors, and decision-makers.
        Include ALL the detailed information from each section, not just summaries.
        """
        
        return self.call_llm([{"role": "user", "content": prompt}])
    
    def generate_comprehensive_report(self, json_file_path: str, output_path: Optional[str] = None) -> str:
        """Generate a comprehensive analysis report from JSON data with ALL details"""
        
        self.log_activity(f"Starting comprehensive data report generation from {json_file_path}")
        
        # Load and parse JSON data
        data = self.load_json_data(json_file_path)
        
        # Extract source references
        references = self.extract_source_references(data)
        
        # Process each section with ALL available data
        self.log_activity("Processing executive summary section...")
        executive_section = self.process_executive_summary_section(data)
        
        self.log_activity("Processing clarification section...")
        clarification_section = self.process_clarification_section(data)
        
        self.log_activity("Processing research section...")
        research_section = self.process_research_section(data)
        
        self.log_activity("Processing validation section...")
        validation_section = self.process_validation_section(data)
        
        self.log_activity("Processing roadmap section...")
        roadmap_section = self.process_roadmap_section(data)
        
        self.log_activity("Processing refinement section...")
        refinement_section = self.process_refinement_section(data)
        
        self.log_activity("Creating source references section...")
        references_section = self.create_source_references_section(references)
        
        # Combine all sections
        sections = {
            'executive_summary': executive_section,
            'clarification_analysis': clarification_section,
            'research_analysis': research_section,
            'validation_assessment': validation_section,
            'development_roadmap': roadmap_section,
            'refinement_recommendations': refinement_section,
            'source_references': references_section
        }
        
        # Synthesize final report
        self.log_activity("Synthesizing final comprehensive report...")
        final_report = self.synthesize_final_report(sections, references)
        
        # Save report if output path provided
        if output_path:
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            with open(output_path, 'w', encoding='utf-8') as file:
                file.write(final_report)
            self.log_activity(f"Report saved to {output_path}")
        
        return final_report
    
    def generate_report_from_file(self, json_file_path: str) -> str:
        """Convenience method to generate report and save with default naming"""
        
        # Generate default output path
        base_name = os.path.splitext(os.path.basename(json_file_path))[0]
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = f"idea_potential/reports/comprehensive_data_analysis_{base_name}_{timestamp}.md"
        
        return self.generate_comprehensive_report(json_file_path, output_path)


# Convenience function for easy usage
def generate_comprehensive_data_report(json_file_path: str, output_path: Optional[str] = None) -> str:
    """Generate a comprehensive analysis report from JSON data with ALL details"""
    generator = ComprehensiveDataReportGenerator()
    return generator.generate_comprehensive_report(json_file_path, output_path) 