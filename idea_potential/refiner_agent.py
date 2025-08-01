from idea_potential.base_agent import BaseAgent
from typing import Dict, List, Any
from idea_potential.structured_outputs import RefinedIdeaResponse, RefinementSuggestion, ValidationResponse, ValidationIssue

class RefinerAgent(BaseAgent):
    """Agent responsible for refining and validating the final report"""
    
    def __init__(self):
        super().__init__('refiner')
        self.refinement_data = {}
        
    def validate_report_authenticity(self, report_data: Dict[str, Any], idea_data: Dict[str, Any], 
                                   research_data: Dict[str, Any], validation_data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate the authenticity and consistency of the report"""
        
        prompt = f"""
        Validate the authenticity and consistency of this business idea analysis report:

        ORIGINAL IDEA: {idea_data.get('refined_idea', 'Unknown')}
        TARGET MARKET: {idea_data.get('target_market', 'Unknown')}

        RESEARCH DATA:
        - Market Insights: {research_data.get('insights', {})}
        - Posts Analyzed: {research_data.get('insights', {}).get('posts_analyzed', 0)}

        VALIDATION DATA:
        - Validation Summary: {validation_data.get('validation_summary', {})}
        - SWOT Analysis: {validation_data.get('swot_analysis', {})}

        REPORT DATA:
        - Executive Summary: {report_data.get('executive_summary', {})}
        - Market Analysis: {report_data.get('market_analysis', {})}
        - Technical Analysis: {report_data.get('technical_analysis', {})}
        - Financial Analysis: {report_data.get('financial_analysis', {})}

        Check for:
        1. Consistency between research findings and report conclusions
        2. Logical flow from validation data to recommendations
        3. Authenticity of claims and assessments
        4. Completeness of analysis
        5. Accuracy of data interpretation

        Provide validation results in the following JSON format:
        {{
          "authenticity_score": <0-10 integer>,
          "consistency_check": "<detailed assessment of consistency>",
          "data_quality": "<assessment of data quality>",
          "identified_issues": [
            {{
              "issue": "<description of issue>",
              "severity": "<high/medium/low>",
              "recommendation": "<recommendation to fix>"
            }}
          ],
          "report_strengths": ["<strength1>", "<strength2>", ...],
          "validation_recommendation": "<accept/revise/reject>",
          "overall_assessment": "<overall assessment of report quality>"
        }}
        """
        
        messages = [
            {"role": "system", "content": "You are an expert quality assurance specialist and business analyst with deep experience in validating business reports and ensuring data integrity."},
            {"role": "user", "content": prompt}
        ]
        
        # Try structured output first
        result = self.call_llm_structured(messages, ValidationResponse, temperature=0.3)
        
        if result:
            # Convert Pydantic model to dict for compatibility
            validation_data = result.dict()
            self.log_activity("Validated report authenticity")
            return validation_data
        
        # Fallback to regular LLM call
        response = self.call_llm(messages, temperature=0.3)
        result = self.parse_json_response(response)
        
        if result:
            # Fix common refiner issues in the result
            result = self._fix_refiner_data(result)
        
        if result:
            self.log_activity("Validated report authenticity")
            # Log the authenticity validation report
            print(f"\n🔍 AUTHENTICITY VALIDATION REPORT:")
            if 'authenticity_score' in result:
                print(f"   📊 Authenticity Score: {result['authenticity_score']}/10")
            if 'validation_recommendation' in result:
                print(f"   ✅ Recommendation: {result['validation_recommendation']}")
            if 'identified_issues' in result:
                print(f"   ⚠️  Issues Found: {len(result['identified_issues'])}")
                for i, issue in enumerate(result['identified_issues'], 1):
                    print(f"      {i}. {issue}")
            if 'consistency_check' in result:
                print(f"   🔄 Consistency: {result['consistency_check']}")
            if 'data_quality' in result:
                print(f"   📈 Data Quality: {result['data_quality']}")
            print()
        
        return result or {"error": "Failed to validate report authenticity"}
    
    def _fix_refiner_data(self, refiner_data: Dict[str, Any]) -> Dict[str, Any]:
        """Fix common refiner data issues"""
        try:
            # Handle case where the result is nested under validation keys
            if 'validation_matrix' in refiner_data:
                refiner_data = refiner_data['validation_matrix']
            
            # Ensure required fields exist for ValidationResponse
            if 'authenticity_score' not in refiner_data:
                refiner_data['authenticity_score'] = 5  # Default medium score
            
            if 'consistency_check' not in refiner_data:
                refiner_data['consistency_check'] = "Consistency assessment needed"
            
            if 'data_quality' not in refiner_data:
                refiner_data['data_quality'] = "Data quality assessment needed"
            
            if 'identified_issues' not in refiner_data:
                refiner_data['identified_issues'] = []
            elif isinstance(refiner_data['identified_issues'], list):
                # Ensure each issue has the required structure
                for i, issue in enumerate(refiner_data['identified_issues']):
                    if isinstance(issue, dict):
                        if 'issue' not in issue:
                            issue['issue'] = f"Issue {i+1}"
                        if 'severity' not in issue:
                            issue['severity'] = 'medium'
                        if 'recommendation' not in issue:
                            issue['recommendation'] = "Recommendation needed"
                    else:
                        # Convert string issue to proper structure
                        refiner_data['identified_issues'][i] = {
                            'issue': str(issue),
                            'severity': 'medium',
                            'recommendation': 'Investigate further'
                        }
            
            if 'report_strengths' not in refiner_data:
                refiner_data['report_strengths'] = []
            
            if 'validation_recommendation' not in refiner_data:
                refiner_data['validation_recommendation'] = 'revise'
            
            if 'overall_assessment' not in refiner_data:
                refiner_data['overall_assessment'] = "Overall assessment needed"
            
            return refiner_data
        except Exception as e:
            print(f"Error fixing refiner data: {e}")
            return refiner_data
    
    def cross_check_claims(self, report_data: Dict[str, Any], research_data: Dict[str, Any]) -> Dict[str, Any]:
        """Cross-check specific claims in the report against research data"""
        
        prompt = f"""
        Cross-check specific claims in the report against the research data:

        RESEARCH DATA:
        - Market Validation: {research_data.get('insights', {}).get('market_validation', 'Unknown')}
        - Pain Points: {research_data.get('insights', {}).get('pain_points_identified', [])}
        - Competition: {research_data.get('insights', {}).get('competition_analysis', 'Unknown')}
        - Customer Sentiment: {research_data.get('insights', {}).get('customer_sentiment', 'Unknown')}
        - Posts Analyzed: {research_data.get('insights', {}).get('posts_analyzed', 0)}

        REPORT CLAIMS:
        - Market Analysis: {report_data.get('market_analysis', {})}
        - Risk Assessment: {report_data.get('risk_assessment', {})}
        - Strategic Recommendations: {report_data.get('strategic_recommendations', {})}

        Check each claim for:
        1. Evidence support from research data
        2. Logical consistency
        3. Appropriate confidence levels
        4. Accurate interpretation of data

        Provide cross-check results in JSON format:
        {{
            "market_claims_validation": {{
                "supported_claims": ["List of well-supported claims"],
                "questionable_claims": ["List of claims needing verification"],
                "unsupported_claims": ["List of claims without evidence"],
                "confidence_assessment": "high|medium|low"
            }},
            "risk_assessment_validation": {{
                "validated_risks": ["List of validated risks"],
                "overstated_risks": ["List of overstated risks"],
                "missing_risks": ["List of risks not mentioned"],
                "risk_confidence": "high|medium|low"
            }},
            "recommendation_validation": {{
                "well_founded_recommendations": ["List of well-founded recommendations"],
                "questionable_recommendations": ["List of questionable recommendations"],
                "missing_recommendations": ["List of missing recommendations"],
                "recommendation_confidence": "high|medium|low"
            }},
            "overall_validation_score": "0-10 rating"
        }}
        """
        
        messages = [
            {"role": "system", "content": "You are an expert at fact-checking and validating business claims against research data."},
            {"role": "user", "content": prompt}
        ]
        
        response = self.call_llm(messages, temperature=0.3)
        result = self.parse_json_response(response)
        
        if result:
            self.log_activity("Cross-checked report claims")
        
        return result or {"error": "Failed to cross-check claims"}
    
    def identify_gaps_and_improvements(self, report_data: Dict[str, Any], idea_data: Dict[str, Any]) -> Dict[str, Any]:
        """Identify gaps and areas for improvement in the report"""
        
        prompt = f"""
        Identify gaps and areas for improvement in this business idea analysis report:

        IDEA: {idea_data.get('refined_idea', 'Unknown')}
        TARGET MARKET: {idea_data.get('target_market', 'Unknown')}

        REPORT SECTIONS:
        - Executive Summary: {report_data.get('executive_summary', {})}
        - Market Analysis: {report_data.get('market_analysis', {})}
        - Technical Analysis: {report_data.get('technical_analysis', {})}
        - Financial Analysis: {report_data.get('financial_analysis', {})}
        - Risk Assessment: {report_data.get('risk_assessment', {})}
        - Strategic Recommendations: {report_data.get('strategic_recommendations', {})}
        - Implementation Roadmap: {report_data.get('implementation_roadmap', {})}

        Identify:
        1. Missing critical information
        2. Areas needing more detail
        3. Inconsistencies or contradictions
        4. Unrealistic assumptions
        5. Missing alternative scenarios

        Provide gap analysis in JSON format:
        {{
            "critical_gaps": [
                {{
                    "gap": "Description of critical gap",
                    "impact": "high|medium|low",
                    "recommendation": "How to address"
                }}
            ],
            "missing_details": [
                {{
                    "area": "Area needing more detail",
                    "importance": "high|medium|low",
                    "suggested_content": "What to add"
                }}
            ],
            "inconsistencies": [
                {{
                    "inconsistency": "Description of inconsistency",
                    "severity": "high|medium|low",
                    "resolution": "How to resolve"
                }}
            ],
            "unrealistic_assumptions": [
                {{
                    "assumption": "Description of unrealistic assumption",
                    "reality_check": "What the reality likely is",
                    "recommendation": "How to address"
                }}
            ],
            "improvement_priorities": ["List of improvement priorities"]
        }}
        """
        
        messages = [
            {"role": "system", "content": "You are an expert at identifying gaps and areas for improvement in business analysis reports."},
            {"role": "user", "content": prompt}
        ]
        
        response = self.call_llm(messages, temperature=0.3)
        result = self.parse_json_response(response)
        
        if result:
            self.log_activity("Identified gaps and improvements")
        
        return result or {"error": "Failed to identify gaps and improvements"}
    
    def generate_refinement_recommendations(self, validation_results: Dict[str, Any], 
                                          cross_check_results: Dict[str, Any], 
                                          gap_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Generate specific recommendations for report refinement"""
        
        prompt = f"""
        Generate specific recommendations for refining the report based on validation results:

        VALIDATION RESULTS: {validation_results}
        CROSS-CHECK RESULTS: {cross_check_results}
        GAP ANALYSIS: {gap_analysis}

        Provide specific refinement recommendations in JSON format:
        {{
            "high_priority_refinements": [
                {{
                    "refinement": "Specific refinement needed",
                    "rationale": "Why this refinement is important",
                    "implementation": "How to implement this refinement"
                }}
            ],
            "medium_priority_refinements": [
                {{
                    "refinement": "Specific refinement needed",
                    "rationale": "Why this refinement is important",
                    "implementation": "How to implement this refinement"
                }}
            ],
            "low_priority_refinements": [
                {{
                    "refinement": "Specific refinement needed",
                    "rationale": "Why this refinement is important",
                    "implementation": "How to implement this refinement"
                }}
            ],
            "overall_refinement_score": "0-10 rating",
            "refinement_priority": "high|medium|low",
            "estimated_effort": "low|medium|high"
        }}
        """
        
        messages = [
            {"role": "system", "content": "You are an expert at providing actionable refinement recommendations for business reports."},
            {"role": "user", "content": prompt}
        ]
        
        response = self.call_llm(messages, temperature=0.3)
        result = self.parse_json_response(response)
        
        if result:
            self.log_activity("Generated refinement recommendations")
        
        return result or {"error": "Failed to generate refinement recommendations"}
    
    def create_final_validation_summary(self, validation_results: Dict[str, Any], 
                                      cross_check_results: Dict[str, Any], 
                                      gap_analysis: Dict[str, Any], 
                                      refinement_recommendations: Dict[str, Any]) -> Dict[str, Any]:
        """Create a final validation summary"""
        
        prompt = f"""
        Create a final validation summary based on all validation results:

        VALIDATION RESULTS: {validation_results}
        CROSS-CHECK RESULTS: {cross_check_results}
        GAP ANALYSIS: {gap_analysis}
        REFINEMENT RECOMMENDATIONS: {refinement_recommendations}

        Provide a final validation summary in JSON format:
        {{
            "overall_quality_score": "0-10 rating",
            "authenticity_assessment": "high|medium|low",
            "consistency_assessment": "high|medium|low",
            "completeness_assessment": "high|medium|low",
            "key_strengths": ["List of report strengths"],
            "critical_issues": ["List of critical issues"],
            "refinement_needed": "yes|no|minor",
            "final_recommendation": "accept|revise|reject",
            "confidence_in_assessment": "high|medium|low"
        }}
        """
        
        messages = [
            {"role": "system", "content": "You are an expert at synthesizing validation results into clear, actionable summaries."},
            {"role": "user", "content": prompt}
        ]
        
        response = self.call_llm(messages, temperature=0.3)
        result = self.parse_json_response(response)
        
        if result:
            self.log_activity("Created final validation summary")
        
        return result or {"error": "Failed to create final validation summary"}
    
    def refine_report(self, report_data: Dict[str, Any], idea_data: Dict[str, Any], 
                     research_data: Dict[str, Any], validation_data: Dict[str, Any]) -> Dict[str, Any]:
        """Main method to refine and validate the report"""
        
        # Validate report authenticity
        validation_results = self.validate_report_authenticity(report_data, idea_data, research_data, validation_data)
        
        # Cross-check claims
        cross_check_results = self.cross_check_claims(report_data, research_data)
        
        # Identify gaps and improvements
        gap_analysis = self.identify_gaps_and_improvements(report_data, idea_data)
        
        # Generate refinement recommendations
        refinement_recommendations = self.generate_refinement_recommendations(
            validation_results, cross_check_results, gap_analysis
        )
        
        # Create final validation summary
        final_summary = self.create_final_validation_summary(
            validation_results, cross_check_results, gap_analysis, refinement_recommendations
        )
        
        # Combine all refinement data
        self.refinement_data = {
            "validation_results": validation_results,
            "cross_check_results": cross_check_results,
            "gap_analysis": gap_analysis,
            "refinement_recommendations": refinement_recommendations,
            "final_summary": final_summary
        }
        
        self.log_activity("Completed report refinement")
        return self.refinement_data 