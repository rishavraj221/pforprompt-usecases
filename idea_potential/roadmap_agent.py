from idea_potential.base_agent import BaseAgent
from typing import Dict, List, Any

class RoadmapAgent(BaseAgent):
    """Agent responsible for creating priority roadmaps and development plans"""
    
    def __init__(self):
        super().__init__('roadmap')
        self.roadmap_data = {}
        
    def create_development_roadmap(self, idea_data: Dict[str, Any], validation_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a comprehensive development roadmap"""
        
        prompt = f"""
        Create a detailed development roadmap for this business idea based on the validation data:

        IDEA: {idea_data.get('refined_idea', 'Unknown')}
        TARGET MARKET: {idea_data.get('target_market', 'Unknown')}
        VALUE PROPOSITIONS: {idea_data.get('value_propositions', [])}

        VALIDATION INSIGHTS:
        - Validation Matrix: {validation_data.get('validation_matrix', {})}
        - SWOT Analysis: {validation_data.get('swot_analysis', {})}
        - Risk Assessment: {validation_data.get('risk_assessment', {})}
        - Validation Summary: {validation_data.get('validation_summary', {})}

        Create a comprehensive roadmap in JSON format:
        {{
            "phase_1_validation": {{
                "duration": "estimated weeks",
                "objectives": ["List of validation objectives"],
                "key_activities": [
                    {{
                        "activity": "Description of activity",
                        "priority": "high|medium|low",
                        "timeline": "estimated timeline",
                        "resources_needed": ["List of required resources"],
                        "success_criteria": ["List of success criteria"]
                    }}
                ],
                "milestones": ["List of key milestones"],
                "risks": ["List of potential risks"]
            }},
            "phase_2_mvp_development": {{
                "duration": "estimated weeks",
                "objectives": ["List of MVP development objectives"],
                "key_activities": [
                    {{
                        "activity": "Description of activity",
                        "priority": "high|medium|low",
                        "timeline": "estimated timeline",
                        "resources_needed": ["List of required resources"],
                        "success_criteria": ["List of success criteria"]
                    }}
                ],
                "milestones": ["List of key milestones"],
                "risks": ["List of potential risks"]
            }},
            "phase_3_market_entry": {{
                "duration": "estimated weeks",
                "objectives": ["List of market entry objectives"],
                "key_activities": [
                    {{
                        "activity": "Description of activity",
                        "priority": "high|medium|low",
                        "timeline": "estimated timeline",
                        "resources_needed": ["List of required resources"],
                        "success_criteria": ["List of success criteria"]
                    }}
                ],
                "milestones": ["List of key milestones"],
                "risks": ["List of potential risks"]
            }},
            "phase_4_scaling": {{
                "duration": "estimated weeks",
                "objectives": ["List of scaling objectives"],
                "key_activities": [
                    {{
                        "activity": "Description of activity",
                        "priority": "high|medium|low",
                        "timeline": "estimated timeline",
                        "resources_needed": ["List of required resources"],
                        "success_criteria": ["List of success criteria"]
                    }}
                ],
                "milestones": ["List of key milestones"],
                "risks": ["List of potential risks"]
            }},
            "overall_timeline": {{
                "total_duration": "estimated total duration",
                "critical_path": ["List of critical path activities"],
                "resource_requirements": "Overall resource assessment",
                "success_metrics": ["List of key success metrics"]
            }}
        }}
        """
        
        messages = [
            {"role": "system", "content": "You are an expert project manager and business strategist specializing in startup development roadmaps."},
            {"role": "user", "content": prompt}
        ]
        
        response = self.call_llm(messages, temperature=0.3)
        result = self.parse_json_response(response)
        
        if result:
            self.roadmap_data = result
            self.log_activity("Created development roadmap")
        
        return result or {"error": "Failed to create development roadmap"}
    
    def create_priority_matrix(self, idea_data: Dict[str, Any], validation_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a priority matrix for tasks and activities"""
        
        prompt = f"""
        Create a priority matrix for this business idea based on validation findings:

        IDEA: {idea_data.get('refined_idea', 'Unknown')}
        VALIDATION SUMMARY: {validation_data.get('validation_summary', {})}
        SWOT ANALYSIS: {validation_data.get('swot_analysis', {})}

        Create a priority matrix in JSON format:
        {{
            "high_priority_high_impact": [
                {{
                    "task": "Description of task",
                    "rationale": "Why this is high priority",
                    "timeline": "When to complete",
                    "resources": ["Required resources"],
                    "dependencies": ["Prerequisites"]
                }}
            ],
            "high_priority_low_impact": [
                {{
                    "task": "Description of task",
                    "rationale": "Why this is high priority",
                    "timeline": "When to complete",
                    "resources": ["Required resources"],
                    "dependencies": ["Prerequisites"]
                }}
            ],
            "low_priority_high_impact": [
                {{
                    "task": "Description of task",
                    "rationale": "Why this has high impact",
                    "timeline": "When to complete",
                    "resources": ["Required resources"],
                    "dependencies": ["Prerequisites"]
                }}
            ],
            "low_priority_low_impact": [
                {{
                    "task": "Description of task",
                    "rationale": "Why this is low priority",
                    "timeline": "When to complete",
                    "resources": ["Required resources"],
                    "dependencies": ["Prerequisites"]
                }}
            ],
            "priority_recommendations": {{
                "immediate_actions": ["List of immediate actions"],
                "short_term_goals": ["List of short-term goals"],
                "medium_term_goals": ["List of medium-term goals"],
                "long_term_goals": ["List of long-term goals"]
            }}
        }}
        """
        
        messages = [
            {"role": "system", "content": "You are an expert at prioritization and strategic planning."},
            {"role": "user", "content": prompt}
        ]
        
        response = self.call_llm(messages, temperature=0.3)
        result = self.parse_json_response(response)
        
        if result:
            self.log_activity("Created priority matrix")
        
        return result or {"error": "Failed to create priority matrix"}
    
    def create_resource_plan(self, idea_data: Dict[str, Any], roadmap_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a comprehensive resource plan"""
        
        prompt = f"""
        Create a detailed resource plan for this business idea:

        IDEA: {idea_data.get('refined_idea', 'Unknown')}
        ROADMAP: {roadmap_data}

        Create a resource plan in JSON format:
        {{
            "human_resources": {{
                "team_requirements": [
                    {{
                        "role": "Role description",
                        "skills_required": ["List of required skills"],
                        "experience_level": "junior|mid|senior",
                        "timeline": "When needed",
                        "responsibilities": ["List of responsibilities"]
                    }}
                ],
                "hiring_priorities": ["List of hiring priorities"],
                "team_structure": "Recommended team structure"
            }},
            "financial_resources": {{
                "funding_requirements": [
                    {{
                        "phase": "Development phase",
                        "amount": "Estimated amount",
                        "purpose": "What the funding is for",
                        "timeline": "When needed"
                    }}
                ],
                "revenue_projections": "Revenue projection timeline",
                "break_even_analysis": "Break-even analysis"
            }},
            "technical_resources": {{
                "technology_stack": ["List of required technologies"],
                "infrastructure_needs": ["List of infrastructure requirements"],
                "development_tools": ["List of development tools"],
                "third_party_services": ["List of third-party services"]
            }},
            "partnerships": {{
                "strategic_partners": ["List of potential strategic partners"],
                "suppliers": ["List of potential suppliers"],
                "distribution_partners": ["List of potential distribution partners"]
            }},
            "resource_timeline": {{
                "immediate_needs": ["List of immediate resource needs"],
                "short_term_needs": ["List of short-term resource needs"],
                "long_term_needs": ["List of long-term resource needs"]
            }}
        }}
        """
        
        messages = [
            {"role": "system", "content": "You are an expert at resource planning and allocation for startups."},
            {"role": "user", "content": prompt}
        ]
        
        response = self.call_llm(messages, temperature=0.3)
        result = self.parse_json_response(response)
        
        if result:
            self.log_activity("Created resource plan")
        
        return result or {"error": "Failed to create resource plan"}
    
    def create_milestone_timeline(self, roadmap_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a detailed milestone timeline"""
        
        prompt = f"""
        Create a detailed milestone timeline based on this roadmap:

        ROADMAP: {roadmap_data}

        Create a milestone timeline in JSON format:
        {{
            "milestones": [
                {{
                    "milestone": "Milestone description",
                    "phase": "Development phase",
                    "target_date": "Target completion date",
                    "dependencies": ["Prerequisites"],
                    "success_criteria": ["List of success criteria"],
                    "risks": ["Potential risks"],
                    "resources_required": ["Required resources"]
                }}
            ],
            "critical_path": ["List of critical path milestones"],
            "timeline_summary": {{
                "total_duration": "Total project duration",
                "key_phases": ["List of key phases"],
                "major_decision_points": ["List of major decision points"]
            }}
        }}
        """
        
        messages = [
            {"role": "system", "content": "You are an expert at project timeline and milestone planning."},
            {"role": "user", "content": prompt}
        ]
        
        response = self.call_llm(messages, temperature=0.3)
        result = self.parse_json_response(response)
        
        if result:
            self.log_activity("Created milestone timeline")
        
        return result or {"error": "Failed to create milestone timeline"}
    
    def generate_roadmap_report(self, idea_data: Dict[str, Any], validation_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a comprehensive roadmap report"""
        
        # Create all roadmap components
        development_roadmap = self.create_development_roadmap(idea_data, validation_data)
        priority_matrix = self.create_priority_matrix(idea_data, validation_data)
        resource_plan = self.create_resource_plan(idea_data, development_roadmap)
        milestone_timeline = self.create_milestone_timeline(development_roadmap)
        
        # Combine all roadmap data
        roadmap_report = {
            "idea_summary": idea_data.get('refined_idea', 'Unknown'),
            "development_roadmap": development_roadmap,
            "priority_matrix": priority_matrix,
            "resource_plan": resource_plan,
            "milestone_timeline": milestone_timeline,
            "roadmap_summary": self.create_roadmap_summary(development_roadmap, priority_matrix, resource_plan)
        }
        
        self.log_activity("Generated comprehensive roadmap report")
        return roadmap_report
    
    def create_roadmap_summary(self, development_roadmap: Dict[str, Any], priority_matrix: Dict[str, Any], resource_plan: Dict[str, Any]) -> Dict[str, Any]:
        """Create a summary of the roadmap"""
        
        prompt = f"""
        Create a concise roadmap summary based on the following data:

        DEVELOPMENT ROADMAP: {development_roadmap}
        PRIORITY MATRIX: {priority_matrix}
        RESOURCE PLAN: {resource_plan}

        Provide a summary in JSON format:
        {{
            "overall_timeline": "Total estimated timeline",
            "key_phases": ["List of key development phases"],
            "critical_milestones": ["List of critical milestones"],
            "resource_requirements": "Overall resource assessment",
            "risk_factors": ["List of key risk factors"],
            "success_metrics": ["List of key success metrics"],
            "next_immediate_steps": ["List of immediate next steps"]
        }}
        """
        
        messages = [
            {"role": "system", "content": "You are an expert at synthesizing roadmap data into actionable insights."},
            {"role": "user", "content": prompt}
        ]
        
        response = self.call_llm(messages, temperature=0.3)
        result = self.parse_json_response(response)
        
        return result or {"error": "Failed to create roadmap summary"} 