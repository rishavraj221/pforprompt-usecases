import json
from datetime import datetime
from typing import Dict, List, Any, Union
import re

class BusinessIdeaReportGenerator:
    """
    A comprehensive report generator for business idea analysis data.
    Converts JSON data into beautifully formatted Markdown reports.
    """
    
    def __init__(self):
        self.report_sections = []
        
    def generate_report(self, data: Dict[str, Any]) -> str:
        """
        Generate a complete Markdown report from the business idea analysis data.
        
        Args:
            data: Dictionary containing the business idea analysis data
            
        Returns:
            str: Formatted Markdown report
        """
        self.report_sections = []
        
        # Generate title and header
        self._add_header(data)
        
        # Generate executive summary
        self._add_executive_summary(data.get('executive_summary', {}))
        
        # Generate validation summary
        self._add_validation_summary(data.get('validation_summary', {}))
        
        # Generate research summary
        self._add_research_summary(data.get('research_summary', {}))
        
        # Generate roadmap summary
        self._add_roadmap_summary(data.get('roadmap_summary', {}))
        
        # Generate refinement summary
        self._add_refinement_summary(data.get('refinement_summary', {}))
        
        # Generate detailed analysis sections
        if 'detailed_data' in data:
            self._add_detailed_analysis(data['detailed_data'])
        
        return '\n\n'.join(self.report_sections)
    
    def _add_header(self, data: Dict[str, Any]):
        """Add report header with basic information."""
        header = "# Business Idea Analysis Report\n"
        
        if data.get('idea_summary'):
            header += f"\n**Idea:** {data['idea_summary']}\n"
        
        if data.get('target_market'):
            header += f"**Target Market:** {data['target_market']}\n"
        
        if data.get('analysis_timestamp'):
            header += f"**Analysis Date:** {data['analysis_timestamp']}\n"
        
        if data.get('pipeline_status'):
            header += f"**Status:** {data['pipeline_status']}\n"
        
        self.report_sections.append(header)
    
    def _add_executive_summary(self, summary: Dict[str, Any]):
        """Add executive summary section."""
        if not summary:
            return
            
        section = "## Executive Summary\n"
        
        if summary.get('recommendation'):
            section += f"**Recommendation:** {summary['recommendation']}\n\n"
        
        if summary.get('confidence_level'):
            section += f"**Confidence Level:** {summary['confidence_level']}\n\n"
        
        if summary.get('key_findings'):
            section += "### Key Findings\n"
            section += self._format_list(summary['key_findings'])
        
        self.report_sections.append(section)
    
    def _add_validation_summary(self, validation: Dict[str, Any]):
        """Add validation summary section."""
        if not validation:
            return
            
        section = "## Validation Summary\n"
        
        if validation.get('overall_score'):
            section += f"**Overall Score:** {validation['overall_score']}\n\n"
        
        if validation.get('risk_level'):
            section += f"**Risk Level:** {validation['risk_level']}\n\n"
        
        if validation.get('recommendation'):
            section += f"**Recommendation:** {validation['recommendation']}\n\n"
        
        self.report_sections.append(section)
    
    def _add_research_summary(self, research: Dict[str, Any]):
        """Add research summary section."""
        if not research:
            return
            
        section = "## Research Summary\n"
        
        if research.get('posts_analyzed'):
            section += f"**Posts Analyzed:** {research['posts_analyzed']}\n\n"
        
        if research.get('market_validation'):
            section += f"**Market Validation:** {research['market_validation']}\n\n"
        
        if research.get('pain_points_identified'):
            section += "### Pain Points Identified\n"
            section += self._format_list(research['pain_points_identified'])
        
        self.report_sections.append(section)
    
    def _add_roadmap_summary(self, roadmap: Dict[str, Any]):
        """Add roadmap summary section."""
        if not roadmap:
            return
            
        section = "## Roadmap Summary\n"
        
        if roadmap.get('overall_timeline'):
            section += f"**Overall Timeline:** {roadmap['overall_timeline']}\n\n"
        
        if roadmap.get('key_phases'):
            section += "### Key Phases\n"
            section += self._format_list(roadmap['key_phases'])
        
        if roadmap.get('critical_milestones'):
            section += "### Critical Milestones\n"
            section += self._format_list(roadmap['critical_milestones'])
        
        self.report_sections.append(section)
    
    def _add_refinement_summary(self, refinement: Dict[str, Any]):
        """Add refinement summary section."""
        if not refinement:
            return
            
        section = "## Refinement Summary\n"
        
        if refinement.get('quality_score'):
            section += f"**Quality Score:** {refinement['quality_score']}\n\n"
        
        if refinement.get('authenticity'):
            section += f"**Authenticity:** {refinement['authenticity']}\n\n"
        
        if refinement.get('final_recommendation'):
            section += f"**Final Recommendation:** {refinement['final_recommendation']}\n\n"
        
        self.report_sections.append(section)
    
    def _add_detailed_analysis(self, detailed_data: Dict[str, Any]):
        """Add detailed analysis sections."""
        section = "# Detailed Analysis\n"
        self.report_sections.append(section)
        
        # Process each main section
        for key, value in detailed_data.items():
            if key == 'clarification':
                self._add_clarification_section(value)
            elif key == 'research':
                self._add_research_section(value)
            elif key == 'validation':
                self._add_validation_section(value)
            elif key == 'roadmap':
                self._add_roadmap_section(value)
            elif key == 'report':
                self._add_report_section(value)
            elif key == 'refinement':
                self._add_refinement_section(value)
    
    def _add_clarification_section(self, clarification: Dict[str, Any]):
        """Add clarification section with personas and value propositions."""
        section = "## Idea Clarification\n"
        
        if clarification.get('refined_idea'):
            section += f"**Refined Idea:** {clarification['refined_idea']}\n\n"
        
        if clarification.get('target_market'):
            section += f"**Target Market:** {clarification['target_market']}\n\n"
        
        # User Personas
        if clarification.get('user_personas'):
            section += self._format_personas(clarification['user_personas'])
        
        # Value Propositions
        if clarification.get('value_propositions'):
            section += "### Value Propositions\n"
            section += self._format_list(clarification['value_propositions'])
        
        # Potential Challenges
        if clarification.get('potential_challenges'):
            section += "### Potential Challenges\n"
            section += self._format_list(clarification['potential_challenges'])
        
        self.report_sections.append(section)
    
    def _add_research_section(self, research: Dict[str, Any]):
        """Add detailed research section."""
        section = "## Research Analysis\n"
        
        # Keywords
        if research.get('keywords_used'):
            section += "### Keywords Used\n"
            section += self._format_list(research['keywords_used'])
        
        # Insights
        if research.get('insights'):
            section += self._format_research_insights(research['insights'])
        
        # Quantitative Data
        if research.get('quantitative_data'):
            section += self._format_quantitative_data(research['quantitative_data'])
        
        self.report_sections.append(section)
    
    def _add_validation_section(self, validation: Dict[str, Any]):
        """Add detailed validation section."""
        section = "## Validation Analysis\n"
        
        # Validation Matrix
        if validation.get('validation_matrix'):
            section += self._format_validation_matrix(validation['validation_matrix'])
        
        # SWOT Analysis
        if validation.get('swot_analysis'):
            section += self._format_swot_analysis(validation['swot_analysis'])
        
        # Risk Assessment
        if validation.get('risk_assessment'):
            section += self._format_risk_assessment(validation['risk_assessment'])
        
        self.report_sections.append(section)
    
    def _add_roadmap_section(self, roadmap: Dict[str, Any]):
        """Add detailed roadmap section."""
        section = "## Development Roadmap\n"
        
        # Technical Foundation
        if roadmap.get('development_roadmap', {}).get('technical_foundation'):
            section += self._format_technical_foundation(
                roadmap['development_roadmap']['technical_foundation']
            )
        
        # Development Phases
        phases = ['phase_1_validation', 'phase_2_mvp_development', 
                 'phase_3_market_entry', 'phase_4_scaling']
        
        for phase_key in phases:
            if roadmap.get('development_roadmap', {}).get(phase_key):
                section += self._format_development_phase(
                    phase_key, roadmap['development_roadmap'][phase_key]
                )
        
        # Priority Matrix
        if roadmap.get('priority_matrix'):
            section += self._format_priority_matrix(roadmap['priority_matrix'])
        
        self.report_sections.append(section)
    
    def _add_report_section(self, report: Dict[str, Any]):
        """Add comprehensive report section."""
        section = "## Comprehensive Analysis Report\n"
        
        # Market Analysis
        if report.get('market_analysis'):
            section += self._format_market_analysis(report['market_analysis'])
        
        # Technical Analysis
        if report.get('technical_analysis'):
            section += self._format_technical_analysis(report['technical_analysis'])
        
        # Financial Analysis
        if report.get('financial_analysis'):
            section += self._format_financial_analysis(report['financial_analysis'])
        
        self.report_sections.append(section)
    
    def _add_refinement_section(self, refinement: Dict[str, Any]):
        """Add refinement analysis section."""
        section = "## Quality Refinement Analysis\n"
        
        # Validation Results
        if refinement.get('validation_results'):
            section += self._format_validation_results(refinement['validation_results'])
        
        # Gap Analysis
        if refinement.get('gap_analysis'):
            section += self._format_gap_analysis(refinement['gap_analysis'])
        
        # Final Summary
        if refinement.get('final_summary'):
            section += self._format_final_summary(refinement['final_summary'])
        
        self.report_sections.append(section)
    
    def _format_personas(self, personas: Dict[str, Any]) -> str:
        """Format user personas section."""
        content = "### User Personas\n\n"
        
        # Primary Personas
        if personas.get('primary_personas'):
            content += "#### Primary Personas\n\n"
            for i, persona in enumerate(personas['primary_personas'], 1):
                content += f"**Persona {i}: {persona.get('name', 'Unnamed')}**\n\n"
                content += f"- **Role:** {persona.get('role', 'N/A')}\n"
                content += f"- **Age Range:** {persona.get('age_range', 'N/A')}\n"
                content += f"- **Experience Level:** {persona.get('experience_level', 'N/A')}\n"
                content += f"- **Company Size:** {persona.get('company_size', 'N/A')}\n"
                content += f"- **Industry:** {persona.get('industry', 'N/A')}\n"
                
                if persona.get('goals'):
                    content += f"- **Goals:** {', '.join(persona['goals'])}\n"
                
                if persona.get('pain_points'):
                    content += f"- **Pain Points:** {', '.join(persona['pain_points'])}\n"
                
                if persona.get('quote'):
                    content += f"- **Quote:** \"{persona['quote']}\"\n"
                
                content += "\n"
        
        return content
    
    def _format_validation_matrix(self, matrix: Dict[str, Any]) -> str:
        """Format validation matrix."""
        content = "### Validation Matrix\n\n"
        
        sections = ['market_validation', 'technical_feasibility', 'financial_viability',
                   'competitive_advantage', 'customer_adoption']
        
        for section in sections:
            if matrix.get(section):
                data = matrix[section]
                title = section.replace('_', ' ').title()
                content += f"#### {title}\n\n"
                
                if data.get('score'):
                    content += f"**Score:** {data['score']}/10\n\n"
                
                if data.get('confidence_level'):
                    content += f"**Confidence:** {data['confidence_level']}\n\n"
                
                if data.get('evidence'):
                    content += "**Evidence:**\n"
                    content += self._format_list(data['evidence'])
                
                if data.get('recommendations'):
                    content += "**Recommendations:**\n"
                    content += self._format_list(data['recommendations'])
        
        return content
    
    def _format_swot_analysis(self, swot: Dict[str, Any]) -> str:
        """Format SWOT analysis."""
        content = "### SWOT Analysis\n\n"
        
        swot_sections = [
            ('strengths', 'Strengths'),
            ('weaknesses', 'Weaknesses'), 
            ('opportunities', 'Opportunities'),
            ('threats', 'Threats')
        ]
        
        for key, title in swot_sections:
            if swot.get(key):
                content += f"#### {title}\n\n"
                for item in swot[key]:
                    if isinstance(item, dict):
                        content += f"- **{item.get('factor', 'Factor')}:** {item.get('impact', 'Impact not specified')}\n"
                    else:
                        content += f"- {item}\n"
                content += "\n"
        
        return content
    
    def _format_financial_analysis(self, financial: Dict[str, Any]) -> str:
        """Format financial analysis section."""
        content = "### Financial Analysis\n\n"
        
        if financial.get('revenue_potential'):
            content += f"**Revenue Potential:** {financial['revenue_potential']}\n\n"
        
        if financial.get('cost_structure'):
            content += f"**Cost Structure:** {financial['cost_structure']}\n\n"
        
        if financial.get('profitability_projection'):
            content += f"**Profitability Projection:** {financial['profitability_projection']}\n\n"
        
        # Financial Models
        if financial.get('financial_models'):
            content += self._format_financial_models(financial['financial_models'])
        
        return content
    
    def _format_financial_models(self, models: Dict[str, Any]) -> str:
        """Format financial models section."""
        content = "#### Financial Models\n\n"
        
        # Revenue Model
        if models.get('revenue_model'):
            content += "**Revenue Model:**\n\n"
            revenue = models['revenue_model']
            
            if revenue.get('pricing_strategy'):
                content += f"- Pricing Strategy: {revenue['pricing_strategy']}\n"
            
            if revenue.get('revenue_streams'):
                content += "- Revenue Streams:\n"
                for stream in revenue['revenue_streams']:
                    if isinstance(stream, dict):
                        content += f"  - {stream.get('stream', 'Stream')}: {stream.get('description', 'No description')}\n"
            content += "\n"
        
        # Unit Economics
        if models.get('unit_economics'):
            content += "**Unit Economics:**\n\n"
            economics = models['unit_economics']
            
            for key, value in economics.items():
                if key and value:
                    formatted_key = key.replace('_', ' ').title()
                    content += f"- {formatted_key}: {value}\n"
            content += "\n"
        
        return content
    
    def _format_list(self, items: List[Any]) -> str:
        """Format a list of items as Markdown list."""
        if not items:
            return ""
        
        content = ""
        for item in items:
            if item:  # Only add non-empty items
                content += f"- {item}\n"
        
        return content + "\n"
    
    def _format_research_insights(self, insights: Dict[str, Any]) -> str:
        """Format research insights."""
        content = "### Research Insights\n\n"
        
        if insights.get('quantitative_metrics'):
            metrics = insights['quantitative_metrics']
            content += "#### Quantitative Metrics\n\n"
            content += f"- Total Posts: {metrics.get('total_posts', 0)}\n"
            content += f"- Average Score: {metrics.get('avg_score', 0)}\n"
            content += f"- Average Comments: {metrics.get('avg_comments', 0)}\n"
            content += f"- Engagement Rate: {metrics.get('engagement_rate', 0)}%\n\n"
        
        if insights.get('user_feedback'):
            feedback = insights['user_feedback']
            content += "#### User Feedback\n\n"
            
            if feedback.get('common_complaints'):
                content += "**Common Complaints:**\n"
                content += self._format_list(feedback['common_complaints'])
            
            if feedback.get('expressed_needs'):
                content += "**Expressed Needs:**\n"
                content += self._format_list(feedback['expressed_needs'])
        
        return content
    
    def _format_quantitative_data(self, data: Dict[str, Any]) -> str:
        """Format quantitative data section."""
        content = "### Quantitative Data\n\n"
        
        content += f"- Total Posts Analyzed: {data.get('total_posts_analyzed', 0)}\n"
        content += f"- Average Score: {data.get('average_score', 0)}\n"
        content += f"- Average Comments: {data.get('average_comments', 0)}\n"
        content += f"- Engagement Rate: {data.get('engagement_rate', 0)}%\n\n"
        
        # Sentiment Distribution
        if data.get('sentiment_distribution'):
            sentiment = data['sentiment_distribution']
            content += "#### Sentiment Distribution\n\n"
            content += f"- Positive: {sentiment.get('positive_percentage', 0)}%\n"
            content += f"- Neutral: {sentiment.get('neutral_percentage', 0)}%\n"
            content += f"- Negative: {sentiment.get('negative_percentage', 0)}%\n\n"
        
        return content
    
    def _format_technical_foundation(self, foundation: Dict[str, Any]) -> str:
        """Format technical foundation section."""
        content = "### Technical Foundation\n\n"
        
        if foundation.get('requirements'):
            content += "#### Requirements\n\n"
            reqs = foundation['requirements']
            
            if reqs.get('functional_requirements'):
                content += "**Functional Requirements:**\n"
                for req in reqs['functional_requirements']:
                    if isinstance(req, dict):
                        content += f"- {req.get('requirement', 'Requirement')} (Priority: {req.get('priority', 'N/A')})\n"
                content += "\n"
        
        if foundation.get('architecture'):
            content += "#### Architecture\n\n"
            arch = foundation['architecture']
            
            if arch.get('system_overview', {}).get('architecture_type'):
                content += f"**Architecture Type:** {arch['system_overview']['architecture_type']}\n\n"
            
            if arch.get('technology_stack'):
                content += "**Technology Stack:**\n"
                stack = arch['technology_stack']
                for category, technologies in stack.items():
                    if technologies:
                        content += f"- {category.title()}: {', '.join(technologies)}\n"
                content += "\n"
        
        return content
    
    def _format_development_phase(self, phase_key: str, phase: Dict[str, Any]) -> str:
        """Format development phase section."""
        phase_name = phase_key.replace('_', ' ').title()
        content = f"### {phase_name}\n\n"
        
        if phase.get('duration'):
            content += f"**Duration:** {phase['duration']}\n\n"
        
        if phase.get('objectives'):
            content += "**Objectives:**\n"
            content += self._format_list(phase['objectives'])
        
        if phase.get('key_activities'):
            content += "**Key Activities:**\n"
            for activity in phase['key_activities']:
                if isinstance(activity, dict):
                    content += f"- {activity.get('activity', 'Activity')} (Priority: {activity.get('priority', 'N/A')})\n"
                else:
                    content += f"- {activity}\n"
            content += "\n"
        
        if phase.get('milestones'):
            content += "**Milestones:**\n"
            content += self._format_list(phase['milestones'])
        
        return content
    
    def _format_priority_matrix(self, matrix: Dict[str, Any]) -> str:
        """Format priority matrix section."""
        content = "### Priority Matrix\n\n"
        
        priority_sections = [
            ('high_priority_high_impact', 'High Priority, High Impact'),
            ('high_priority_low_impact', 'High Priority, Low Impact'),
            ('low_priority_high_impact', 'Low Priority, High Impact'),
            ('low_priority_low_impact', 'Low Priority, Low Impact')
        ]
        
        for key, title in priority_sections:
            if matrix.get(key):
                content += f"#### {title}\n\n"
                for task in matrix[key]:
                    if isinstance(task, dict):
                        content += f"- **{task.get('task', 'Task')}:** {task.get('rationale', 'No rationale provided')}\n"
                content += "\n"
        
        return content
    
    def _format_market_analysis(self, market: Dict[str, Any]) -> str:
        """Format market analysis section."""
        content = "### Market Analysis\n\n"
        
        if market.get('market_size'):
            content += f"**Market Size:** {market['market_size']}\n\n"
        
        if market.get('target_audience'):
            content += f"**Target Audience:** {market['target_audience']}\n\n"
        
        if market.get('competition_landscape'):
            content += f"**Competition Landscape:** {market['competition_landscape']}\n\n"
        
        if market.get('market_trends'):
            content += "**Market Trends:**\n"
            content += self._format_list(market['market_trends'])
        
        return content
    
    def _format_technical_analysis(self, technical: Dict[str, Any]) -> str:
        """Format technical analysis section."""
        content = "### Technical Analysis\n\n"
        
        if technical.get('technical_feasibility'):
            content += f"**Technical Feasibility:** {technical['technical_feasibility']}\n\n"
        
        if technical.get('development_complexity'):
            content += f"**Development Complexity:** {technical['development_complexity']}\n\n"
        
        if technical.get('technology_requirements'):
            content += "**Technology Requirements:**\n"
            content += self._format_list(technical['technology_requirements'])
        
        return content
    
    def _format_risk_assessment(self, risks: Dict[str, Any]) -> str:
        """Format risk assessment section."""
        content = "### Risk Assessment\n\n"
        
        risk_categories = ['market_risks', 'technical_risks', 'financial_risks', 
                          'competitive_risks', 'operational_risks']
        
        for category in risk_categories:
            if risks.get(category):
                title = category.replace('_', ' ').title()
                content += f"#### {title}\n\n"
                
                for risk in risks[category]:
                    if isinstance(risk, dict):
                        content += f"- **{risk.get('risk', 'Risk')}**\n"
                        content += f"  - Probability: {risk.get('probability', 'N/A')}\n"
                        content += f"  - Impact: {risk.get('impact', 'N/A')}\n"
                        content += f"  - Mitigation: {risk.get('mitigation', 'N/A')}\n\n"
                    else:
                        content += f"- {risk}\n"
                content += "\n"
        
        return content
    
    def _format_validation_results(self, results: Dict[str, Any]) -> str:
        """Format validation results section."""
        content = "### Validation Results\n\n"
        
        if results.get('authenticity_score'):
            content += f"**Authenticity Score:** {results['authenticity_score']}\n\n"
        
        if results.get('data_quality'):
            quality = results['data_quality']
            content += "**Data Quality:**\n"
            content += f"- Completeness: {quality.get('completeness', 'N/A')}\n"
            content += f"- Accuracy: {quality.get('accuracy', 'N/A')}\n"
            content += f"- Relevance: {quality.get('relevance', 'N/A')}\n\n"
        
        return content
    
    def _format_gap_analysis(self, gaps: Dict[str, Any]) -> str:
        """Format gap analysis section."""
        content = "### Gap Analysis\n\n"
        
        if gaps.get('critical_gaps'):
            content += "**Critical Gaps:**\n"
            for gap in gaps['critical_gaps']:
                if isinstance(gap, dict):
                    content += f"- {gap.get('gap', 'Gap')}: {gap.get('recommendation', 'No recommendation')}\n"
            content += "\n"
        
        if gaps.get('improvement_priorities'):
            content += "**Improvement Priorities:**\n"
            content += self._format_list(gaps['improvement_priorities'])
        
        return content
    
    def _format_final_summary(self, summary: Dict[str, Any]) -> str:
        """Format final summary section."""
        content = "### Final Summary\n\n"
        
        if summary.get('overall_quality_score'):
            content += f"**Overall Quality Score:** {summary['overall_quality_score']}\n\n"
        
        if summary.get('final_recommendation'):
            content += f"**Final Recommendation:** {summary['final_recommendation']}\n\n"
        
        if summary.get('key_strengths'):
            content += "**Key Strengths:**\n"
            content += self._format_list(summary['key_strengths'])
        
        if summary.get('critical_issues'):
            content += "**Critical Issues:**\n"
            content += self._format_list(summary['critical_issues'])
        
        return content
    
    def save_report(self, data: Dict[str, Any], filename: str = None) -> str:
        """
        Generate and save the report to a file.
        
        Args:
            data: Dictionary containing the business idea analysis data
            filename: Optional filename for the report
            
        Returns:
            str: The generated report content
        """
        report = self.generate_report(data)
        
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"business_idea_report_{timestamp}.md"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"Report saved to: {filename}")
        return report

# Example usage
def main():
    """Example usage of the BusinessIdeaReportGenerator."""
    
    # Sample data (you would load your actual JSON data here)
    json_file_path = "idea_potential/reports/idea_analysis_results_20250802_160019.json"
    with open(json_file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Generate report
    generator = BusinessIdeaReportGenerator()
    report = generator.generate_report(data)
    
    # Print report
    print(report)
    
    # Save to file
    generator.save_report(data, f"idea_potential/reports/idea_analysis_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md")

if __name__ == "__main__":
    main()