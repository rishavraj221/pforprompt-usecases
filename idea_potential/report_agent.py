from idea_potential.base_agent import BaseAgent
from typing import Dict, List, Any
from datetime import datetime
import os
import re
from idea_potential.structured_outputs import ComprehensiveReportResponse, ReportSection

class ReportAgent(BaseAgent):
    """Agent responsible for building comprehensive analysis reports"""
    
    def __init__(self):
        super().__init__('report')
        self.report_data = {}
        
    def generate_comprehensive_report(self, idea_data: Dict[str, Any], research_data: Dict[str, Any], 
                                   validation_data: Dict[str, Any], roadmap_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a comprehensive analysis report with quantitative data and user feedback"""
        
        # Extract quantitative data and user feedback
        quantitative_data = research_data.get('quantitative_data', {})
        user_feedback = research_data.get('insights', {}).get('user_feedback', {})
        references = research_data.get('references', [])
        
        # First, create comprehensive financial models
        financial_models = self.create_financial_models(idea_data, research_data, validation_data)
        
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
        - Quantitative Metrics: {quantitative_data}
        - User Feedback: {user_feedback}
        - References: {len(references)} Reddit posts analyzed

        VALIDATION DATA:
        - Validation Matrix: {validation_data.get('validation_matrix', {})}
        - SWOT Analysis: {validation_data.get('swot_analysis', {})}
        - Risk Assessment: {validation_data.get('risk_assessment', {})}
        - Validation Summary: {validation_data.get('validation_summary', {})}

        ROADMAP DATA:
        - Development Roadmap: {roadmap_data.get('development_roadmap', {})}
        - Priority Matrix: {roadmap_data.get('priority_matrix', {})}
        - Resource Plan: {roadmap_data.get('resource_plan', {})}

        FINANCIAL MODELS:
        {financial_models}

        Create a comprehensive report with the following structure:
        - executive_summary: Executive summary of the report
        - sections: Array of report sections
        - key_findings: Array of key findings
        - recommendations: Array of strategic recommendations
        - appendices: Object with supporting data

        Each section should include:
        - title: Section title
        - content: Section content
        - key_insights: Array of key insights
        - data_sources: Array of data sources

        Please respond with valid JSON format containing all the report components.
        """
        
        messages = [
            {"role": "system", "content": "You are an expert business analyst and report writer specializing in startup idea validation and market analysis."},
            {"role": "user", "content": prompt}
        ]
        
        try:
            # Try structured output first
            result = self.call_llm_structured(messages, ComprehensiveReportResponse, temperature=0.3)
            
            if result:
                # Convert Pydantic model to dict for compatibility
                report_data = result.dict()
                self.report_data = report_data
                self.log_activity("Generated comprehensive report", f"Key findings: {len(report_data.get('key_findings', []))}")
                return report_data
                
        except Exception as e:
            print(f"Error generating comprehensive report with structured output: {e}")
        
        # Fallback to regular LLM call
        response = self.call_llm(messages, temperature=0.3)
        result = self.parse_json_response(response)
        
        if result:
            # Fix common report issues in the result
            result = self._fix_report_data(result)
        
        if result:
            self.report_data = result
            self.log_activity("Generated comprehensive report")
        
        return result or {"error": "Failed to generate comprehensive report"}
    
    def _fix_report_data(self, report_data: Dict[str, Any]) -> Dict[str, Any]:
        """Fix common report data issues"""
        try:
            # Handle case where the result is nested under 'report' or has section names as keys
            if 'report' in report_data:
                report_data = report_data['report']
            
            # Check if the data is structured with section names as keys
            if isinstance(report_data, dict) and any(key.lower() in ['executive summary', 'quantitative analysis', 'market analysis'] for key in report_data.keys()):
                # Convert section-based structure to expected format
                new_report_data = {
                    'executive_summary': "Executive summary",
                    'sections': [],
                    'key_findings': [],
                    'recommendations': [],
                    'appendices': {}
                }
                
                # Convert sections
                for section_name, section_content in report_data.items():
                    if isinstance(section_content, dict):
                        section = {
                            'title': section_name,
                            'content': str(section_content),
                            'key_insights': [],
                            'data_sources': []
                        }
                        new_report_data['sections'].append(section)
                
                report_data = new_report_data
            
            # Ensure required fields exist
            if 'executive_summary' not in report_data:
                report_data['executive_summary'] = "Executive summary"
            
            if 'sections' not in report_data:
                report_data['sections'] = []
            
            if 'key_findings' not in report_data:
                report_data['key_findings'] = []
            
            if 'recommendations' not in report_data:
                report_data['recommendations'] = []
            
            if 'appendices' not in report_data:
                report_data['appendices'] = {}
            
            # Fix sections if they exist
            if 'sections' in report_data and isinstance(report_data['sections'], list):
                for section in report_data['sections']:
                    if isinstance(section, dict):
                        if 'title' not in section:
                            section['title'] = "Section"
                        if 'content' not in section:
                            section['content'] = "Section content"
                        if 'key_insights' not in section:
                            section['key_insights'] = []
                        if 'data_sources' not in section:
                            section['data_sources'] = []
            
            return report_data
        except Exception as e:
            print(f"Error fixing report data: {e}")
            return report_data
    
    def create_financial_models(self, idea_data: Dict[str, Any], research_data: Dict[str, Any], validation_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create comprehensive financial models with realistic projections"""
        
        prompt = f"""
        Create comprehensive financial models and projections for this business idea:

        IDEA: {idea_data.get('refined_idea', 'Unknown')}
        TARGET MARKET: {idea_data.get('target_market', 'Unknown')}
        VALUE PROPOSITIONS: {idea_data.get('value_propositions', [])}

        RESEARCH INSIGHTS:
        {research_data.get('insights', {})}

        VALIDATION DATA:
        {validation_data}

        Create detailed financial models including:

        Return as JSON:
        {{
            "revenue_model": {{
                "pricing_strategy": "Recommended pricing strategy",
                "revenue_streams": [
                    {{
                        "stream": "Revenue stream name",
                        "description": "Description of revenue stream",
                        "pricing_model": "Subscription|one_time|usage_based|freemium",
                        "target_customers": "Target customer segment",
                        "estimated_arpu": "Average revenue per user",
                        "growth_rate": "Expected growth rate"
                    }}
                ],
                "market_penetration": "Estimated market penetration strategy",
                "pricing_tiers": [
                    {{
                        "tier": "Tier name",
                        "price": "Price point",
                        "features": ["List of features"],
                        "target_audience": "Target audience"
                    }}
                ]
            }},
            "cost_structure": {{
                "fixed_costs": [
                    {{
                        "category": "Cost category",
                        "description": "Description of cost",
                        "monthly_amount": "Monthly cost",
                        "annual_amount": "Annual cost",
                        "growth_rate": "Expected growth rate"
                    }}
                ],
                "variable_costs": [
                    {{
                        "category": "Cost category",
                        "description": "Description of cost",
                        "per_unit_cost": "Cost per unit",
                        "scaling_factor": "How it scales with growth"
                    }}
                ],
                "development_costs": [
                    {{
                        "phase": "Development phase",
                        "description": "Description of costs",
                        "estimated_cost": "Estimated cost",
                        "timeline": "Expected timeline"
                    }}
                ]
            }},
            "financial_projections": {{
                "year_1": {{
                    "revenue": "Projected revenue",
                    "costs": "Projected costs",
                    "profit_loss": "Projected profit/loss",
                    "cash_flow": "Projected cash flow",
                    "key_metrics": ["Key financial metrics"]
                }},
                "year_2": {{
                    "revenue": "Projected revenue",
                    "costs": "Projected costs",
                    "profit_loss": "Projected profit/loss",
                    "cash_flow": "Projected cash flow",
                    "key_metrics": ["Key financial metrics"]
                }},
                "year_3": {{
                    "revenue": "Projected revenue",
                    "costs": "Projected costs",
                    "profit_loss": "Projected profit/loss",
                    "cash_flow": "Projected cash flow",
                    "key_metrics": ["Key financial metrics"]
                }}
            }},
            "unit_economics": {{
                "customer_acquisition_cost": "Estimated CAC",
                "lifetime_value": "Estimated LTV",
                "ltv_cac_ratio": "LTV/CAC ratio",
                "payback_period": "Customer payback period",
                "churn_rate": "Expected churn rate",
                "retention_rate": "Expected retention rate"
            }},
            "funding_requirements": {{
                "seed_round": {{
                    "amount": "Funding amount needed",
                    "purpose": "What the funding is for",
                    "timeline": "When funding is needed",
                    "use_of_funds": ["How funds will be used"]
                }},
                "series_a": {{
                    "amount": "Funding amount needed",
                    "purpose": "What the funding is for",
                    "timeline": "When funding is needed",
                    "use_of_funds": ["How funds will be used"]
                }},
                "break_even_analysis": {{
                    "break_even_point": "When break-even is expected",
                    "break_even_revenue": "Revenue needed to break even",
                    "break_even_customers": "Customers needed to break even",
                    "assumptions": ["Key assumptions"]
                }}
            }},
            "key_metrics": {{
                "revenue_metrics": ["List of key revenue metrics"],
                "growth_metrics": ["List of key growth metrics"],
                "efficiency_metrics": ["List of key efficiency metrics"],
                "customer_metrics": ["List of key customer metrics"]
            }},
            "sensitivity_analysis": {{
                "best_case": "Best case scenario projections",
                "worst_case": "Worst case scenario projections",
                "most_likely": "Most likely scenario projections",
                "key_assumptions": ["Key assumptions that could impact projections"]
            }}
        }}
        """
        
        messages = [
            {"role": "system", "content": "You are an expert financial analyst and startup consultant with deep experience in financial modeling, unit economics, and startup financing."},
            {"role": "user", "content": prompt}
        ]
        
        response = self.call_llm(messages, temperature=0.3)
        result = self.parse_json_response(response)
        
        if result:
            self.log_activity("Created financial models")
            return result
        
        return {"error": "Failed to create financial models"}
    
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