import json
import asyncio
from typing import Dict, List, Any, Optional
from datetime import datetime
import os
from idea_potential.base_agent import BaseAgent


class ComprehensiveReportGenerator(BaseAgent):
    """
    Agent responsible for generating comprehensive analysis reports from JSON data.
    Processes large JSON files in chunks using multiple LLM calls for specialized analysis.
    """
    
    def __init__(self):
        super().__init__('comprehensive_report_generator')
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
    
    def extract_source_references(self, data: Dict[str, Any]) -> Dict[str, List[str]]:
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
    
    def process_executive_summary_chunk(self, data: Dict[str, Any]) -> str:
        """Process executive summary and high-level insights"""
        
        executive_data = data.get('executive_summary', {})
        idea_summary = data.get('idea_summary', '')
        target_market = data.get('target_market', '')
        
        prompt = f"""
        Create a comprehensive executive summary section for a business idea analysis report.
        
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
        
        Format as clean markdown with proper headings, bullet points, and emphasis.
        Make it executive-friendly and actionable.
        """
        
        return self.call_llm([{"role": "user", "content": prompt}])
    
    def process_market_analysis_chunk(self, data: Dict[str, Any]) -> str:
        """Process market research, user personas, and market insights"""
        
        detailed_data = data.get('detailed_data', {})
        clarification = detailed_data.get('clarification', {})
        research = detailed_data.get('research', {})
        
        # Extract user personas
        user_personas = clarification.get('user_personas', {})
        primary_personas = user_personas.get('primary_personas', [])
        secondary_personas = user_personas.get('secondary_personas', [])
        
        # Extract research insights
        research_insights = research.get('insights', {})
        market_insights = research_insights.get('market_insights', {})
        quantitative_data = research.get('quantitative_data', {})
        
        prompt = f"""
        Create a comprehensive market analysis section for a business idea report.
        
        USER PERSONAS:
        Primary Personas: {json.dumps(primary_personas, indent=2)}
        Secondary Personas: {json.dumps(secondary_personas, indent=2)}
        
        MARKET INSIGHTS:
        {json.dumps(market_insights, indent=2)}
        
        QUANTITATIVE DATA:
        {json.dumps(quantitative_data, indent=2)}
        
        RESEARCH SUMMARY:
        Posts Analyzed: {data.get('research_summary', {}).get('posts_analyzed', 0)}
        
        Create a detailed market analysis that includes:
        1. **Target Market Analysis** - Detailed breakdown of target audience
        2. **User Personas** - Detailed profiles of primary and secondary users
        3. **Market Size & Opportunity** - Market size assessment and growth potential
        4. **Customer Pain Points** - Key problems the solution addresses
        5. **Market Trends** - Relevant industry trends and insights
        6. **Competitive Landscape** - Analysis of competitors and differentiation
        
        Include specific data points, percentages, and market metrics where available.
        Format as professional markdown with tables, bullet points, and clear sections.
        """
        
        return self.call_llm([{"role": "user", "content": prompt}])
    
    def process_validation_chunk(self, data: Dict[str, Any]) -> str:
        """Process validation matrix, SWOT analysis, and risk assessment"""
        
        detailed_data = data.get('detailed_data', {})
        validation = detailed_data.get('validation', {})
        validation_matrix = validation.get('validation_matrix', {})
        swot_analysis = validation.get('swot_analysis', {})
        risk_assessment = validation.get('risk_assessment', {})
        
        prompt = f"""
        Create a comprehensive validation and risk assessment section for a business idea report.
        
        VALIDATION MATRIX:
        {json.dumps(validation_matrix, indent=2)}
        
        SWOT ANALYSIS:
        {json.dumps(swot_analysis, indent=2)}
        
        RISK ASSESSMENT:
        {json.dumps(risk_assessment, indent=2)}
        
        VALIDATION SUMMARY:
        {json.dumps(data.get('validation_summary', {}), indent=2)}
        
        Create a detailed validation analysis that includes:
        1. **Market Validation** - Evidence of market demand and size
        2. **Technical Feasibility** - Assessment of technical requirements and challenges
        3. **Financial Viability** - Revenue potential and cost structure analysis
        4. **Competitive Advantage** - Differentiation and sustainable advantages
        5. **Customer Adoption** - Adoption barriers and value perception
        6. **SWOT Analysis** - Strengths, weaknesses, opportunities, threats
        7. **Risk Assessment** - Key risks and mitigation strategies
        
        Include confidence levels, scores, and specific evidence for each validation area.
        Format as professional markdown with tables, risk matrices, and clear recommendations.
        """
        
        return self.call_llm([{"role": "user", "content": prompt}])
    
    def process_roadmap_chunk(self, data: Dict[str, Any]) -> str:
        """Process development roadmap, timeline, and resource planning"""
        
        detailed_data = data.get('detailed_data', {})
        roadmap = detailed_data.get('roadmap', {})
        development_roadmap = roadmap.get('development_roadmap', {})
        resource_plan = roadmap.get('resource_plan', {})
        priority_matrix = roadmap.get('priority_matrix', {})
        
        roadmap_summary = data.get('roadmap_summary', {})
        
        prompt = f"""
        Create a comprehensive development roadmap section for a business idea report.
        
        DEVELOPMENT ROADMAP:
        {json.dumps(development_roadmap, indent=2)}
        
        RESOURCE PLAN:
        {json.dumps(resource_plan, indent=2)}
        
        PRIORITY MATRIX:
        {json.dumps(priority_matrix, indent=2)}
        
        ROADMAP SUMMARY:
        Overall Timeline: {roadmap_summary.get('overall_timeline', 'Unknown')}
        Key Phases: {roadmap_summary.get('key_phases', [])}
        Critical Milestones: {roadmap_summary.get('critical_milestones', [])}
        
        Create a detailed development roadmap that includes:
        1. **Development Phases** - Clear phases with timelines and deliverables
        2. **Resource Requirements** - Team, technology, and budget needs
        3. **Critical Milestones** - Key checkpoints and success criteria
        4. **Risk Mitigation** - How to handle potential delays or issues
        5. **Success Metrics** - How to measure progress and success
        6. **Dependencies** - What needs to happen before each phase
        
        Include specific timelines, resource allocations, and measurable milestones.
        Format as professional markdown with timelines, tables, and clear action items.
        """
        
        return self.call_llm([{"role": "user", "content": prompt}])
    
    def process_refinement_chunk(self, data: Dict[str, Any]) -> str:
        """Process gap analysis, refinement recommendations, and quality assessment"""
        
        detailed_data = data.get('detailed_data', {})
        refinement = detailed_data.get('refinement', {})
        gap_analysis = refinement.get('gap_analysis', {})
        refinement_recommendations = refinement.get('refinement_recommendations', {})
        final_summary = refinement.get('final_summary', {})
        
        refinement_summary = data.get('refinement_summary', {})
        
        prompt = f"""
        Create a comprehensive refinement and quality assessment section for a business idea report.
        
        GAP ANALYSIS:
        {json.dumps(gap_analysis, indent=2)}
        
        REFINEMENT RECOMMENDATIONS:
        {json.dumps(refinement_recommendations, indent=2)}
        
        FINAL SUMMARY:
        {json.dumps(final_summary, indent=2)}
        
        REFINEMENT SUMMARY:
        Quality Score: {refinement_summary.get('quality_score', 'Unknown')}
        Authenticity: {refinement_summary.get('authenticity', 'Unknown')}
        Final Recommendation: {refinement_summary.get('final_recommendation', 'Unknown')}
        
        Create a detailed refinement analysis that includes:
        1. **Gap Analysis** - Critical gaps and missing information
        2. **Quality Assessment** - Overall quality and authenticity evaluation
        3. **Refinement Priorities** - High, medium, and low priority improvements
        4. **Implementation Plan** - How to address identified gaps
        5. **Final Recommendations** - Clear next steps and priorities
        6. **Quality Metrics** - Specific quality indicators and scores
        
        Include specific improvement suggestions, implementation timelines, and success criteria.
        Format as professional markdown with priority matrices, action items, and clear recommendations.
        """
        
        return self.call_llm([{"role": "user", "content": prompt}])
    
    def create_source_references_section(self, references: Dict[str, List[str]]) -> str:
        """Create a comprehensive source references section"""
        
        prompt = f"""
        Create a comprehensive source references section for a business idea analysis report.
        
        SOURCE REFERENCES:
        {json.dumps(references, indent=2)}
        
        Create a detailed source references section that includes:
        1. **Reddit Posts Analyzed** - List of relevant Reddit posts with URLs and relevance scores
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
    
    def synthesize_final_report(self, sections: Dict[str, str], references: Dict[str, List[str]]) -> str:
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
        4. **Market Analysis** - Target market, personas, and market insights
        5. **Validation Assessment** - Technical, financial, and market validation
        6. **Development Roadmap** - Implementation plan and timeline
        7. **Refinement Recommendations** - Quality assessment and improvement areas
        8. **Source References** - Complete list of sources and references
        9. **Appendices** - Detailed data and supporting information
        
        Format as a professional markdown document with:
        - Clear hierarchy and navigation
        - Professional formatting and styling
        - Cross-references between sections
        - Executive-friendly language
        - Actionable insights and recommendations
        - Complete source attribution
        
        Make it suitable for stakeholders, investors, and decision-makers.
        """
        
        return self.call_llm([{"role": "user", "content": prompt}])
    
    def generate_comprehensive_report(self, json_file_path: str, output_path: Optional[str] = None) -> str:
        """Generate a comprehensive analysis report from JSON data"""
        
        self.log_activity(f"Starting comprehensive report generation from {json_file_path}")
        
        # Load and parse JSON data
        data = self.load_json_data(json_file_path)
        
        # Extract source references
        references = self.extract_source_references(data)
        
        # Process each chunk with specialized LLM calls
        self.log_activity("Processing executive summary chunk...")
        executive_section = self.process_executive_summary_chunk(data)
        
        self.log_activity("Processing market analysis chunk...")
        market_section = self.process_market_analysis_chunk(data)
        
        self.log_activity("Processing validation chunk...")
        validation_section = self.process_validation_chunk(data)
        
        self.log_activity("Processing roadmap chunk...")
        roadmap_section = self.process_roadmap_chunk(data)
        
        self.log_activity("Processing refinement chunk...")
        refinement_section = self.process_refinement_chunk(data)
        
        self.log_activity("Creating source references section...")
        references_section = self.create_source_references_section(references)
        
        # Combine all sections
        sections = {
            'executive_summary': executive_section,
            'market_analysis': market_section,
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
        output_path = f"idea_potential/reports/comprehensive_analysis_{base_name}_{timestamp}.md"
        
        return self.generate_comprehensive_report(json_file_path, output_path)


# Convenience function for easy usage
def generate_comprehensive_report(json_file_path: str, output_path: Optional[str] = None) -> str:
    """Generate a comprehensive analysis report from JSON data"""
    generator = ComprehensiveReportGenerator()
    return generator.generate_comprehensive_report(json_file_path, output_path) 