from idea_potential.base_agent import BaseAgent
from typing import Dict, List, Any
from idea_potential.structured_outputs import (
    ValidationMatrixResponse, CompetitorAnalysisResponse, MarketSizeEstimateResponse,
    SWOTAnalysisResponse, RiskAssessmentResponse
)

class ValidationAgent(BaseAgent):
    """Agent responsible for creating validation matrices and frameworks"""
    
    def __init__(self):
        super().__init__('validation')
        self.validation_matrix = {}
        
    def create_validation_matrix(self, idea_data: Dict[str, Any], research_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a comprehensive validation matrix for the idea with enhanced competitor and market analysis"""
        
        # First, conduct enhanced competitor analysis
        competitor_analysis = self.analyze_competitors(idea_data, research_data)
        
        # Estimate market size
        market_size_estimate = self.estimate_market_size(idea_data, research_data)
        
        prompt = f"""
        Create a comprehensive validation matrix for this business idea based on the provided data:

        IDEA DATA:
        - Refined Idea: {idea_data.get('refined_idea', 'Unknown')}
        - Target Market: {idea_data.get('target_market', 'Unknown')}
        - Value Propositions: {idea_data.get('value_propositions', [])}
        - Potential Challenges: {idea_data.get('potential_challenges', [])}

        RESEARCH DATA:
        - Market Validation: {research_data.get('insights', {}).get('market_validation', 'Unknown')}
        - Pain Points: {research_data.get('insights', {}).get('pain_points_identified', [])}
        - Competition Analysis: {research_data.get('insights', {}).get('competition_analysis', 'Unknown')}
        - Customer Sentiment: {research_data.get('insights', {}).get('customer_sentiment', 'Unknown')}

        COMPETITOR ANALYSIS:
        {competitor_analysis}

        MARKET SIZE ESTIMATE:
        {market_size_estimate}

        Create a validation matrix with the following structure:
        - Market validation (score 0-10, market size, evidence, risks, confidence level, recommendations)
        - Technical feasibility (score 0-10, requirements, challenges, confidence level, recommendations)
        - Financial viability (score 0-10, revenue potential, cost structure, profitability, confidence level, recommendations)
        - Competitive advantage (score 0-10, competitors, differentiators, barriers to entry, sustainable advantage, confidence level, recommendations)
        - Customer adoption (score 0-10, customer segments, adoption barriers, value perception, confidence level, recommendations)
        - Overall assessment (total score 0-50, risk level, go/no-go decision, critical factors, next steps)

        Please respond with valid JSON format containing all the validation matrix components.
        return in following JSON format:
        market_validation:
            score: 0-10
            market_size: str, Market size in USD
            evidence:[str], List of supporting evidence
            risks: [str], List of market risks
            confidence_level: str, high|medium|low
            recommendations: [str], List of recommendations
        technical_feasibility:
            score: 0-10
            requirements: [str], List of technical requirements
            challenges: [str], List of technical challenges
            confidence_level: str, high|medium|low
            recommendations: [str], List of recommendations
        financial_viability:
            score: 0-10
            revenue_potential: str, Revenue potential in USD
            cost_structure: str, Cost structure
            profitability: str, Profitability
            confidence_level: str, high|medium|low
            recommendations: [str], List of recommendations
        competitive_advantage:
            score: 0-10
            competitors: [str], List of competitors
            differentiators: [str], List of competitive advantages
            barriers_to_entry: [str], List of entry barriers
            sustainable_advantage: str, Assessment of sustainability
            confidence_level: str, high|medium|low
            recommendations: [str], List of recommendations
        customer_adoption:
            score: 0-10
            customer_segments: [str], List of customer segments
            adoption_barriers: [str], List of adoption barriers
            value_perception: str, Assessment of value perception
            confidence_level: str, high|medium|low
            recommendations: [str], List of recommendations
        overall_assessment:
            total_score: 0-50
            risk_level: str, low|medium|high
            go_no_go: str, go|no_go|conditional
            critical_factors: [str], List of critical success factors
            next_steps: [str], List of immediate next steps

        IMPORTANT: Use exact values for enums:
        - confidence_level: "high", "medium", or "low" (not "High", "Medium", etc.)
        - risk_level: "low", "medium", or "high" (not "Low", "Moderate", etc.)
        - go_no_go: "go", "no_go", or "conditional"
        - evidence, risks, recommendations, requirements, challenges, competitors, differentiators, barriers_to_entry, customer_segments, adoption_barriers, critical_factors, next_steps: Must be arrays of strings
        """
        
        messages = [
            {"role": "system", "content": "You are an expert business validator with deep experience in startup validation and market analysis."},
            {"role": "user", "content": prompt}
        ]
        
        try:
            # Try structured output first
            result = self.call_llm_structured(messages, ValidationMatrixResponse, temperature=0.3)
            
            if result:
                # Convert Pydantic model to dict for compatibility
                validation_matrix = result.dict()
                self.validation_matrix = validation_matrix
                self.log_activity("Created validation matrix", f"Total score: {validation_matrix['overall_assessment']['total_score']}")
                return validation_matrix
                
        except Exception as e:
            print(f"Error creating validation matrix with structured output: {e}")
        
        # Fallback to regular LLM call
        response = self.call_llm(messages, temperature=0.3)
        result = self.parse_json_response(response)
        
        if result:
            # Fix common validation issues in the result
            result = self._fix_validation_matrix(result)
        
        if result:
            self.validation_matrix = result
            self.log_activity("Created validation matrix")
        
        return result or {"error": "Failed to create validation matrix"}
    
    def _fix_validation_matrix(self, matrix_data: Dict[str, Any]) -> Dict[str, Any]:
        """Fix common validation issues in validation matrix data"""
        try:
            # Handle case where the result is nested under 'validation_matrix'
            if 'validation_matrix' in matrix_data:
                matrix_data = matrix_data['validation_matrix']
            
            # Fix confidence levels
            for category in ['market_validation', 'technical_feasibility', 'financial_viability', 'competitive_advantage', 'customer_adoption']:
                if category in matrix_data:
                    category_data = matrix_data[category]
                    if isinstance(category_data, dict):
                        # Fix confidence level
                        if 'confidence_level' in category_data:
                            confidence = category_data['confidence_level']
                            if isinstance(confidence, str):
                                confidence_lower = confidence.lower()
                                if 'high' in confidence_lower:
                                    category_data['confidence_level'] = 'high'
                                elif 'medium' in confidence_lower or 'moderate' in confidence_lower:
                                    category_data['confidence_level'] = 'medium'
                                elif 'low' in confidence_lower:
                                    category_data['confidence_level'] = 'low'
                        
                        # Fix list fields
                        for field in ['evidence', 'risks', 'recommendations', 'requirements', 'challenges', 'competitors', 'differentiators', 'barriers_to_entry', 'customer_segments', 'adoption_barriers']:
                            if field in category_data:
                                value = category_data[field]
                                if isinstance(value, str):
                                    # Convert string to list
                                    category_data[field] = [value]
                                elif not isinstance(value, list):
                                    category_data[field] = []
                        
                        # Fix string fields that might be lists
                        string_fields = [
                            'cost_structure', 'value_perception', 'market_size', 'competitive_landscape', 
                            'technical_complexity', 'resource_requirements', 'revenue_potential', 
                            'profitability', 'sustainable_advantage'
                        ]
                        for field in string_fields:
                            if field in category_data:
                                value = category_data[field]
                                if isinstance(value, list):
                                    # Convert list to string
                                    category_data[field] = ', '.join([str(item) for item in value])
                                elif not isinstance(value, str):
                                    category_data[field] = str(value)
            
            # Fix overall assessment
            if 'overall_assessment' in matrix_data:
                overall = matrix_data['overall_assessment']
                if isinstance(overall, dict):
                    # Fix risk level
                    if 'risk_level' in overall:
                        risk = overall['risk_level']
                        if isinstance(risk, str):
                            risk_lower = risk.lower()
                            if 'high' in risk_lower:
                                overall['risk_level'] = 'high'
                            elif 'medium' in risk_lower or 'moderate' in risk_lower:
                                overall['risk_level'] = 'medium'
                            elif 'low' in risk_lower:
                                overall['risk_level'] = 'low'
                    
                    # Fix go_no_go
                    if 'go_no_go' not in overall:
                        # Try to infer from other fields
                        if 'total_score' in overall:
                            score = overall['total_score']
                            if isinstance(score, (int, float)):
                                if score >= 35:
                                    overall['go_no_go'] = 'go'
                                elif score >= 25:
                                    overall['go_no_go'] = 'conditional'
                                else:
                                    overall['go_no_go'] = 'no_go'
                            else:
                                overall['go_no_go'] = 'conditional'
                        else:
                            overall['go_no_go'] = 'conditional'
                    
                    # Fix list fields
                    for field in ['critical_factors', 'next_steps']:
                        if field in overall:
                            value = overall[field]
                            if isinstance(value, str):
                                overall[field] = [value]
                            elif not isinstance(value, list):
                                overall[field] = []
            
            return matrix_data
        except Exception as e:
            print(f"Error fixing validation matrix: {e}")
            return matrix_data
    
    def analyze_competitors(self, idea_data: Dict[str, Any], research_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze competitors in the specific domain"""
        
        prompt = f"""
        Conduct a comprehensive competitor analysis for this business idea:

        IDEA: {idea_data.get('refined_idea', 'Unknown')}
        TARGET MARKET: {idea_data.get('target_market', 'Unknown')}
        VALUE PROPOSITIONS: {idea_data.get('value_propositions', [])}

        RESEARCH INSIGHTS:
        {research_data.get('insights', {})}

        Analyze the competitive landscape and provide:
        1. Direct competitors (same product/service)
        2. Indirect competitors (alternative solutions)
        3. Potential future competitors
        4. Competitive advantages and disadvantages
        5. Market positioning opportunities

        Return as JSON:
        {{
            "direct_competitors": [
                {{
                    "name": "Competitor name",
                    "description": "What they do",
                    "strengths": ["List of strengths"],
                    "weaknesses": ["List of weaknesses"],
                    "market_share": "Estimated market share",
                    "pricing": "Pricing model",
                    "target_audience": "Their target audience"
                }}
            ],
            "indirect_competitors": [
                {{
                    "name": "Competitor name",
                    "description": "What they do",
                    "how_they_compete": "How they compete",
                    "threat_level": "high|medium|low"
                }}
            ],
            "competitive_advantages": ["List of potential advantages"],
            "competitive_disadvantages": ["List of potential disadvantages"],
            "market_gaps": ["List of market gaps to exploit"],
            "positioning_strategy": "Recommended positioning strategy"
        }}
        """
        
        messages = [
            {"role": "system", "content": "You are an expert competitive analyst with deep knowledge of various industries and market dynamics."},
            {"role": "user", "content": prompt}
        ]
        
        response = self.call_llm(messages, temperature=0.3)
        result = self.parse_json_response(response)
        
        if result:
            self.log_activity("Conducted competitor analysis")
            return result
        
        return {"error": "Failed to analyze competitors"}
    
    def estimate_market_size(self, idea_data: Dict[str, Any], research_data: Dict[str, Any]) -> Dict[str, Any]:
        """Estimate market size and growth potential"""
        
        prompt = f"""
        Estimate the market size and growth potential for this business idea:

        IDEA: {idea_data.get('refined_idea', 'Unknown')}
        TARGET MARKET: {idea_data.get('target_market', 'Unknown')}
        VALUE PROPOSITIONS: {idea_data.get('value_propositions', [])}

        RESEARCH INSIGHTS:
        {research_data.get('insights', {})}

        Provide a comprehensive market size analysis including:
        1. Total Addressable Market (TAM)
        2. Serviceable Addressable Market (SAM)
        3. Serviceable Obtainable Market (SOM)
        4. Market growth rate and trends
        5. Geographic market breakdown
        6. Customer segment analysis

        Return as JSON:
        {{
            "total_addressable_market": {{
                "size": "Market size in USD",
                "description": "What this includes",
                "growth_rate": "Annual growth rate",
                "trends": ["Key market trends"]
            }},
            "serviceable_addressable_market": {{
                "size": "Market size in USD",
                "description": "What this includes",
                "percentage_of_tam": "Percentage of TAM"
            }},
            "serviceable_obtainable_market": {{
                "size": "Market size in USD",
                "description": "What this includes",
                "percentage_of_sam": "Percentage of SAM",
                "timeframe": "Time to achieve this"
            }},
            "customer_segments": [
                {{
                    "segment": "Segment name",
                    "size": "Segment size",
                    "characteristics": ["Key characteristics"],
                    "willingness_to_pay": "high|medium|low"
                }}
            ],
            "geographic_breakdown": {{
                "primary_markets": ["List of primary markets"],
                "secondary_markets": ["List of secondary markets"],
                "emerging_markets": ["List of emerging markets"]
            }},
            "market_growth_factors": ["List of factors driving growth"],
            "market_risks": ["List of market risks"]
        }}
        """
        
        messages = [
            {"role": "system", "content": "You are an expert market analyst with experience in market sizing and growth analysis across various industries."},
            {"role": "user", "content": prompt}
        ]
        
        response = self.call_llm(messages, temperature=0.3)
        result = self.parse_json_response(response)
        
        if result:
            self.log_activity("Estimated market size")
            return result
        
        return {"error": "Failed to estimate market size"}
    
    def generate_swot_analysis(self, idea_data: Dict[str, Any], research_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a SWOT analysis for the idea"""
        
        prompt = f"""
        Create a comprehensive SWOT analysis for this business idea:

        IDEA: {idea_data.get('refined_idea', 'Unknown')}
        TARGET MARKET: {idea_data.get('target_market', 'Unknown')}
        VALUE PROPOSITIONS: {idea_data.get('value_propositions', [])}

        MARKET RESEARCH INSIGHTS:
        - Market Validation: {research_data.get('insights', {}).get('market_validation', 'Unknown')}
        - Pain Points: {research_data.get('insights', {}).get('pain_points_identified', [])}
        - Competition: {research_data.get('insights', {}).get('competition_analysis', 'Unknown')}
        - Opportunities: {research_data.get('insights', {}).get('opportunity_assessment', 'Unknown')}
        - Risks: {research_data.get('insights', {}).get('risks_and_challenges', [])}

        Provide a detailed SWOT analysis in JSON format:
        {{
            "strengths": [
                {{
                    "factor": "Description of strength",
                    "impact": "high|medium|low",
                    "evidence": "Supporting evidence"
                }}
            ],
            "weaknesses": [
                {{
                    "factor": "Description of weakness",
                    "impact": "high|medium|low",
                    "mitigation": "How to address this weakness"
                }}
            ],
            "opportunities": [
                {{
                    "factor": "Description of opportunity",
                    "potential": "high|medium|low",
                    "action_plan": "How to capitalize on this opportunity"
                }}
            ],
            "threats": [
                {{
                    "factor": "Description of threat",
                    "severity": "high|medium|low",
                    "mitigation": "How to address this threat"
                }}
            ],
            "strategic_implications": "Overall strategic assessment based on SWOT"
        }}
        """
        
        messages = [
            {"role": "system", "content": "You are a strategic business analyst expert at SWOT analysis and strategic planning."},
            {"role": "user", "content": prompt}
        ]
        
        response = self.call_llm(messages, temperature=0.3)
        result = self.parse_json_response(response)
        
        if result:
            self.log_activity("Generated SWOT analysis")
        
        return result or {"error": "Failed to generate SWOT analysis"}
    
    def create_risk_assessment(self, idea_data: Dict[str, Any], research_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a comprehensive risk assessment"""
        
        prompt = f"""
        Create a detailed risk assessment for this business idea:

        IDEA: {idea_data.get('refined_idea', 'Unknown')}
        TARGET MARKET: {idea_data.get('target_market', 'Unknown')}

        MARKET DATA:
        - Pain Points: {research_data.get('insights', {}).get('pain_points_identified', [])}
        - Competition: {research_data.get('insights', {}).get('competition_analysis', 'Unknown')}
        - Risks: {research_data.get('insights', {}).get('risks_and_challenges', [])}

        Provide a comprehensive risk assessment in JSON format:
        {{
            "market_risks": [
                {{
                    "risk": "Description of market risk",
                    "probability": "high|medium|low",
                    "impact": "high|medium|low",
                    "mitigation": "Risk mitigation strategy"
                }}
            ],
            "technical_risks": [
                {{
                    "risk": "Description of technical risk",
                    "probability": "high|medium|low",
                    "impact": "high|medium|low",
                    "mitigation": "Risk mitigation strategy"
                }}
            ],
            "financial_risks": [
                {{
                    "risk": "Description of financial risk",
                    "probability": "high|medium|low",
                    "impact": "high|medium|low",
                    "mitigation": "Risk mitigation strategy"
                }}
            ],
            "competitive_risks": [
                {{
                    "risk": "Description of competitive risk",
                    "probability": "high|medium|low",
                    "impact": "high|medium|low",
                    "mitigation": "Risk mitigation strategy"
                }}
            ],
            "operational_risks": [
                {{
                    "risk": "Description of operational risk",
                    "probability": "high|medium|low",
                    "impact": "high|medium|low",
                    "mitigation": "Risk mitigation strategy"
                }}
            ],
            "overall_risk_profile": {{
                "risk_level": "low|medium|high",
                "critical_risks": ["List of most critical risks"],
                "risk_mitigation_priorities": ["List of priority mitigation actions"]
            }}
        }}
        """
        
        messages = [
            {"role": "system", "content": "You are a risk management expert specializing in startup and business risk assessment."},
            {"role": "user", "content": prompt}
        ]
        
        response = self.call_llm(messages, temperature=0.3)
        result = self.parse_json_response(response)
        
        if result:
            self.log_activity("Created risk assessment")
        
        return result or {"error": "Failed to create risk assessment"}
    
    def generate_validation_report(self, idea_data: Dict[str, Any], research_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a comprehensive validation report"""
        
        # Create all validation components
        validation_matrix = self.create_validation_matrix(idea_data, research_data)
        swot_analysis = self.generate_swot_analysis(idea_data, research_data)
        risk_assessment = self.create_risk_assessment(idea_data, research_data)
        
        # Combine all validation data
        validation_report = {
            "idea_summary": idea_data.get('refined_idea', 'Unknown'),
            "target_market": idea_data.get('target_market', 'Unknown'),
            "validation_matrix": validation_matrix,
            "swot_analysis": swot_analysis,
            "risk_assessment": risk_assessment,
            "validation_summary": self.create_validation_summary(validation_matrix, swot_analysis, risk_assessment)
        }
        
        self.log_activity("Generated comprehensive validation report")
        return validation_report
    
    def create_validation_summary(self, validation_matrix: Dict[str, Any], swot_analysis: Dict[str, Any], risk_assessment: Dict[str, Any]) -> Dict[str, Any]:
        """Create a summary of all validation findings"""
        
        prompt = f"""
        Create a concise validation summary based on the following data:

        VALIDATION MATRIX: {validation_matrix}
        SWOT ANALYSIS: {swot_analysis}
        RISK ASSESSMENT: {risk_assessment}

        Provide a summary in JSON format:
        {{
            "overall_validation_score": "0-10 rating",
            "key_findings": ["List of key validation findings"],
            "critical_success_factors": ["List of critical success factors"],
            "major_concerns": ["List of major concerns"],
            "validation_recommendation": "proceed|proceed_with_caution|reconsider|abandon",
            "next_validation_steps": ["List of next steps for validation"]
        }}
        """
        
        messages = [
            {"role": "system", "content": "You are an expert at synthesizing validation data into actionable insights."},
            {"role": "user", "content": prompt}
        ]
        
        response = self.call_llm(messages, temperature=0.3)
        result = self.parse_json_response(response)
        
        return result or {"error": "Failed to create validation summary"} 