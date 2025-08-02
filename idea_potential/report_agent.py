from idea_potential.base_agent import BaseAgent
from typing import Dict, List, Any
from datetime import datetime
import os
import re

class ReportAgent(BaseAgent):
    """Agent responsible for building comprehensive analysis reports"""
    
    def __init__(self):
        super().__init__('report')
        self.report_data = {}
        
    def generate_comprehensive_report(self, idea_data: Dict[str, Any], research_data: Dict[str, Any], 
                                   validation_data: Dict[str, Any], roadmap_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a comprehensive analysis report"""
        
        prompt = f"""
        Create a comprehensive business idea analysis report based on all the collected data:

        IDEA DATA:
        - Refined Idea: {idea_data.get('refined_idea', 'Unknown')}
        - Target Market: {idea_data.get('target_market', 'Unknown')}
        - Value Propositions: {idea_data.get('value_propositions', [])}
        - Potential Challenges: {idea_data.get('potential_challenges', [])}

        RESEARCH DATA:
        - Market Insights: {research_data.get('insights', {})}
        - Posts Analyzed: {research_data.get('insights', {}).get('posts_analyzed', 0)}
        - Keywords Used: {research_data.get('keywords_used', [])}

        VALIDATION DATA:
        - Validation Matrix: {validation_data.get('validation_matrix', {})}
        - SWOT Analysis: {validation_data.get('swot_analysis', {})}
        - Risk Assessment: {validation_data.get('risk_assessment', {})}
        - Validation Summary: {validation_data.get('validation_summary', {})}

        ROADMAP DATA:
        - Development Roadmap: {roadmap_data.get('development_roadmap', {})}
        - Priority Matrix: {roadmap_data.get('priority_matrix', {})}
        - Resource Plan: {roadmap_data.get('resource_plan', {})}

        Create a comprehensive report in JSON format:
        {{
            "executive_summary": {{
                "idea_overview": "Brief overview of the idea",
                "key_findings": ["List of key findings"],
                "recommendation": "go|proceed_with_caution|reconsider|abandon",
                "confidence_level": "high|medium|low",
                "next_steps": ["List of immediate next steps"]
            }},
            "market_analysis": {{
                "market_size": "Assessment of market size",
                "target_audience": "Detailed target audience analysis",
                "competition_landscape": "Competitive analysis",
                "market_trends": "Relevant market trends",
                "customer_pain_points": ["List of identified pain points"],
                "market_opportunity": "Market opportunity assessment"
            }},
            "technical_analysis": {{
                "technical_feasibility": "Technical feasibility assessment",
                "technology_requirements": ["List of technology requirements"],
                "development_complexity": "Development complexity assessment",
                "technical_risks": ["List of technical risks"],
                "scalability_considerations": "Scalability assessment"
            }},
            "financial_analysis": {{
                "revenue_potential": "Revenue potential assessment",
                "cost_structure": "Cost structure analysis",
                "profitability_projection": "Profitability projection",
                "funding_requirements": "Funding requirements",
                "break_even_analysis": "Break-even analysis"
            }},
            "risk_assessment": {{
                "market_risks": ["List of market risks"],
                "technical_risks": ["List of technical risks"],
                "financial_risks": ["List of financial risks"],
                "competitive_risks": ["List of competitive risks"],
                "operational_risks": ["List of operational risks"],
                "overall_risk_level": "low|medium|high"
            }},
            "strategic_recommendations": {{
                "immediate_actions": ["List of immediate actions"],
                "short_term_strategy": "Short-term strategy",
                "long_term_strategy": "Long-term strategy",
                "success_factors": ["List of critical success factors"],
                "pivot_considerations": ["List of potential pivots"]
            }},
            "implementation_roadmap": {{
                "phase_1": "Phase 1 description and timeline",
                "phase_2": "Phase 2 description and timeline",
                "phase_3": "Phase 3 description and timeline",
                "phase_4": "Phase 4 description and timeline",
                "critical_milestones": ["List of critical milestones"],
                "resource_requirements": "Overall resource requirements"
            }},
            "success_metrics": {{
                "key_performance_indicators": ["List of KPIs"],
                "success_criteria": ["List of success criteria"],
                "measurement_framework": "How to measure success"
            }}
        }}
        """
        
        messages = [
            {"role": "system", "content": "You are an expert business analyst and consultant specializing in comprehensive business idea analysis and reporting."},
            {"role": "user", "content": prompt}
        ]
        
        response = self.call_llm(messages, temperature=0.3)
        result = self.parse_json_response(response)
        
        if result:
            self.report_data = result
            self.log_activity("Generated comprehensive report")
        
        return result or {"error": "Failed to generate comprehensive report"}
    
    def create_markdown_report(self, report_data: Dict[str, Any], idea_data: Dict[str, Any]) -> str:
        """Create a formatted markdown report"""
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        markdown_content = f"""# Business Idea Analysis Report

**Generated on:** {timestamp}  
**Idea:** {idea_data.get('refined_idea', 'Unknown')}  
**Target Market:** {idea_data.get('target_market', 'Unknown')}

---

## 📋 Executive Summary

### Idea Overview
{report_data.get('executive_summary', {}).get('idea_overview', 'Not available')}

### Key Findings
"""
        
        for finding in report_data.get('executive_summary', {}).get('key_findings', []):
            markdown_content += f"- {finding}\n"
        
        markdown_content += f"""
### Recommendation
**{report_data.get('executive_summary', {}).get('recommendation', 'Unknown').upper()}**  
Confidence Level: {report_data.get('executive_summary', {}).get('confidence_level', 'Unknown')}

### Next Steps
"""
        
        for step in report_data.get('executive_summary', {}).get('next_steps', []):
            markdown_content += f"- {step}\n"
        
        markdown_content += f"""
---

## 📊 Market Analysis

### Market Size
{report_data.get('market_analysis', {}).get('market_size', 'Not available')}

### Target Audience
{report_data.get('market_analysis', {}).get('target_audience', 'Not available')}

### Competition Landscape
{report_data.get('market_analysis', {}).get('competition_landscape', 'Not available')}

### Market Trends
{report_data.get('market_analysis', {}).get('market_trends', 'Not available')}

### Customer Pain Points
"""
        
        for pain_point in report_data.get('market_analysis', {}).get('customer_pain_points', []):
            markdown_content += f"- {pain_point}\n"
        
        markdown_content += f"""
### Market Opportunity
{report_data.get('market_analysis', {}).get('market_opportunity', 'Not available')}

---

## 🔧 Technical Analysis

### Technical Feasibility
{report_data.get('technical_analysis', {}).get('technical_feasibility', 'Not available')}

### Technology Requirements
"""
        
        for requirement in report_data.get('technical_analysis', {}).get('technology_requirements', []):
            markdown_content += f"- {requirement}\n"
        
        markdown_content += f"""
### Development Complexity
{report_data.get('technical_analysis', {}).get('development_complexity', 'Not available')}

### Technical Risks
"""
        
        for risk in report_data.get('technical_analysis', {}).get('technical_risks', []):
            markdown_content += f"- {risk}\n"
        
        markdown_content += f"""
### Scalability Considerations
{report_data.get('technical_analysis', {}).get('scalability_considerations', 'Not available')}

---

## 💰 Financial Analysis

### Revenue Potential
{report_data.get('financial_analysis', {}).get('revenue_potential', 'Not available')}

### Cost Structure
{report_data.get('financial_analysis', {}).get('cost_structure', 'Not available')}

### Profitability Projection
{report_data.get('financial_analysis', {}).get('profitability_projection', 'Not available')}

### Funding Requirements
{report_data.get('financial_analysis', {}).get('funding_requirements', 'Not available')}

### Break-Even Analysis
{report_data.get('financial_analysis', {}).get('break_even_analysis', 'Not available')}

---

## ⚠️ Risk Assessment

### Market Risks
"""
        
        for risk in report_data.get('risk_assessment', {}).get('market_risks', []):
            markdown_content += f"- {risk}\n"
        
        markdown_content += f"""
### Technical Risks
"""
        
        for risk in report_data.get('risk_assessment', {}).get('technical_risks', []):
            markdown_content += f"- {risk}\n"
        
        markdown_content += f"""
### Financial Risks
"""
        
        for risk in report_data.get('risk_assessment', {}).get('financial_risks', []):
            markdown_content += f"- {risk}\n"
        
        markdown_content += f"""
### Competitive Risks
"""
        
        for risk in report_data.get('risk_assessment', {}).get('competitive_risks', []):
            markdown_content += f"- {risk}\n"
        
        markdown_content += f"""
### Operational Risks
"""
        
        for risk in report_data.get('risk_assessment', {}).get('operational_risks', []):
            markdown_content += f"- {risk}\n"
        
        markdown_content += f"""
### Overall Risk Level
**{report_data.get('risk_assessment', {}).get('overall_risk_level', 'Unknown').upper()}**

---

## 🎯 Strategic Recommendations

### Immediate Actions
"""
        
        for action in report_data.get('strategic_recommendations', {}).get('immediate_actions', []):
            markdown_content += f"- {action}\n"
        
        markdown_content += f"""
### Short-Term Strategy
{report_data.get('strategic_recommendations', {}).get('short_term_strategy', 'Not available')}

### Long-Term Strategy
{report_data.get('strategic_recommendations', {}).get('long_term_strategy', 'Not available')}

### Success Factors
"""
        
        for factor in report_data.get('strategic_recommendations', {}).get('success_factors', []):
            markdown_content += f"- {factor}\n"
        
        markdown_content += f"""
### Pivot Considerations
"""
        
        for pivot in report_data.get('strategic_recommendations', {}).get('pivot_considerations', []):
            markdown_content += f"- {pivot}\n"
        
        markdown_content += f"""
---

## 🗓️ Implementation Roadmap

### Phase 1
{report_data.get('implementation_roadmap', {}).get('phase_1', 'Not available')}

### Phase 2
{report_data.get('implementation_roadmap', {}).get('phase_2', 'Not available')}

### Phase 3
{report_data.get('implementation_roadmap', {}).get('phase_3', 'Not available')}

### Phase 4
{report_data.get('implementation_roadmap', {}).get('phase_4', 'Not available')}

### Critical Milestones
"""
        
        for milestone in report_data.get('implementation_roadmap', {}).get('critical_milestones', []):
            markdown_content += f"- {milestone}\n"
        
        markdown_content += f"""
### Resource Requirements
{report_data.get('implementation_roadmap', {}).get('resource_requirements', 'Not available')}

---

## 📈 Success Metrics

### Key Performance Indicators
"""
        
        for kpi in report_data.get('success_metrics', {}).get('key_performance_indicators', []):
            markdown_content += f"- {kpi}\n"
        
        markdown_content += f"""
### Success Criteria
"""
        
        for criteria in report_data.get('success_metrics', {}).get('success_criteria', []):
            markdown_content += f"- {criteria}\n"
        
        markdown_content += f"""
### Measurement Framework
{report_data.get('success_metrics', {}).get('measurement_framework', 'Not available')}

---

## 📝 Conclusion

This comprehensive analysis provides a detailed assessment of the business idea's potential, market opportunity, technical feasibility, and strategic implementation path. The recommendations are based on thorough market research, validation analysis, and strategic planning.

**Final Recommendation:** {report_data.get('executive_summary', {}).get('recommendation', 'Unknown').upper()}

*Report generated by Idea Potential Analysis System*
"""
        
        return markdown_content
    
    def _convert_to_camel_case(self, text: str) -> str:
        """Convert text to camel case for filename"""
        # Remove special characters and split into words
        words = re.findall(r'\b\w+\b', text.lower())
        if not words:
            return "IdeaAnalysis"
        
        # Convert to camel case
        camel_case = words[0] + ''.join(word.capitalize() for word in words[1:])
        return camel_case[:50]  # Limit length
    
    def save_report(self, markdown_content: str, idea_name: str = None) -> str:
        """Save the report to a file with the new naming format"""
        
        # Generate filename with idea name in camel case
        if idea_name:
            idea_camel_case = self._convert_to_camel_case(idea_name)
        else:
            idea_camel_case = "IdeaAnalysis"
        
        # Create timestamp
        timestamp = datetime.now().strftime("%d%m%y_%H%M")
        
        # Create filename
        filename = f"{idea_camel_case}_{timestamp}.md"
        
        # Create reports directory if it doesn't exist
        os.makedirs('idea_potential/reports', exist_ok=True)
        filepath = os.path.join('idea_potential/reports', filename)
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
            
            self.log_activity(f"Saved report to {filepath}")
            return filepath
            
        except Exception as e:
            print(f"Error saving report: {e}")
            return None 