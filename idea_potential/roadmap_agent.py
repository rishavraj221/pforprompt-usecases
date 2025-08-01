from idea_potential.base_agent import BaseAgent
from typing import Dict, List, Any
from idea_potential.structured_outputs import RoadmapResponse, Phase, Milestone

class RoadmapAgent(BaseAgent):
    """Agent responsible for creating priority roadmaps and development plans"""
    
    def __init__(self):
        super().__init__('roadmap')
        self.roadmap_data = {}
        
    def create_development_roadmap(self, idea_data: Dict[str, Any], validation_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a comprehensive development roadmap with technical requirements and architecture plans"""
        
        # First, create technical requirements and architecture
        technical_requirements = self.create_technical_requirements(idea_data, validation_data)
        architecture_plan = self.create_architecture_plan(idea_data, technical_requirements)
        
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

        TECHNICAL REQUIREMENTS:
        {technical_requirements}

        ARCHITECTURE PLAN:
        {architecture_plan}

        Create a comprehensive roadmap with the following structure:
        - phases: Array of development phases
        - total_timeline: Overall timeline estimate
        - critical_path: Array of critical path activities
        - resource_requirements: Object with resource needs
        - risk_mitigation: Array of risk mitigation strategies

        Each phase should include:
        - phase_name: Name of the phase
        - duration: Duration estimate
        - objectives: Array of objectives
        - milestones: Array of milestones
        - key_activities: Array of key activities
        - success_metrics: Array of success metrics

        Each milestone should include:
        - title: Milestone title
        - description: Milestone description
        - timeline: Timeline for milestone
        - deliverables: Array of deliverables
        - success_criteria: Array of success criteria
        - dependencies: Array of dependencies

        Please respond with valid JSON format containing all the roadmap components.
        """
        
        messages = [
            {"role": "system", "content": "You are an expert in software development roadmaps and technical project planning."},
            {"role": "user", "content": prompt}
        ]
        
        try:
            # Try structured output first
            result = self.call_llm_structured(messages, RoadmapResponse, temperature=0.3)
            
            if result:
                # Convert Pydantic model to dict for compatibility
                roadmap_data = result.dict()
                self.roadmap_data = roadmap_data
                self.log_activity("Created development roadmap", f"Total timeline: {roadmap_data['total_timeline']}")
                return roadmap_data
                
        except Exception as e:
            print(f"Error creating development roadmap with structured output: {e}")
        
        # Fallback to regular LLM call
        response = self.call_llm(messages, temperature=0.3)
        result = self.parse_json_response(response)
        
        if result:
            # Fix common roadmap issues in the result
            result = self._fix_roadmap_data(result)
        
        if result:
            self.roadmap_data = result
            self.log_activity("Created development roadmap")
        
        return result or {"error": "Failed to create development roadmap"}
    
    def _fix_roadmap_data(self, roadmap_data: Dict[str, Any]) -> Dict[str, Any]:
        """Fix common roadmap data issues"""
        try:
            # Handle case where the result is nested under 'roadmap'
            if 'roadmap' in roadmap_data:
                roadmap_data = roadmap_data['roadmap']
            
            # Ensure required fields exist
            if 'phases' not in roadmap_data:
                roadmap_data['phases'] = []
            
            if 'total_timeline' not in roadmap_data:
                roadmap_data['total_timeline'] = "6-12 months"
            
            if 'critical_path' not in roadmap_data:
                roadmap_data['critical_path'] = []
            
            if 'resource_requirements' not in roadmap_data:
                roadmap_data['resource_requirements'] = {}
            
            if 'risk_mitigation' not in roadmap_data:
                roadmap_data['risk_mitigation'] = []
            
            # Fix phases if they exist but are in wrong format
            if 'phases' in roadmap_data and isinstance(roadmap_data['phases'], list):
                for phase in roadmap_data['phases']:
                    if isinstance(phase, dict):
                        # Ensure phase has required fields
                        if 'phase_name' not in phase:
                            phase['phase_name'] = "Development Phase"
                        if 'duration' not in phase:
                            phase['duration'] = "2-3 months"
                        if 'objectives' not in phase:
                            phase['objectives'] = []
                        if 'milestones' not in phase:
                            phase['milestones'] = []
                        if 'key_activities' not in phase:
                            phase['key_activities'] = []
                        if 'success_metrics' not in phase:
                            phase['success_metrics'] = []
                        
                        # Fix milestones if they exist
                        if 'milestones' in phase and isinstance(phase['milestones'], list):
                            for milestone in phase['milestones']:
                                if isinstance(milestone, dict):
                                    if 'title' not in milestone:
                                        milestone['title'] = "Milestone"
                                    if 'description' not in milestone:
                                        milestone['description'] = "Milestone description"
                                    if 'timeline' not in milestone:
                                        milestone['timeline'] = "2 weeks"
                                    if 'deliverables' not in milestone:
                                        milestone['deliverables'] = []
                                    if 'success_criteria' not in milestone:
                                        milestone['success_criteria'] = []
                                    if 'dependencies' not in milestone:
                                        milestone['dependencies'] = []
            
            # Fix risk_mitigation - convert dicts to strings
            if 'risk_mitigation' in roadmap_data and isinstance(roadmap_data['risk_mitigation'], list):
                fixed_risk_mitigation = []
                for item in roadmap_data['risk_mitigation']:
                    if isinstance(item, dict):
                        # Extract the risk description from the dict
                        if 'risk' in item:
                            fixed_risk_mitigation.append(str(item['risk']))
                        else:
                            fixed_risk_mitigation.append(str(item))
                    elif isinstance(item, str):
                        fixed_risk_mitigation.append(item)
                    else:
                        fixed_risk_mitigation.append(str(item))
                roadmap_data['risk_mitigation'] = fixed_risk_mitigation
            
            return roadmap_data
        except Exception as e:
            print(f"Error fixing roadmap data: {e}")
            return roadmap_data
    
    def create_technical_requirements(self, idea_data: Dict[str, Any], validation_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create detailed technical requirements for the business idea"""
        
        prompt = f"""
        Create comprehensive technical requirements for this business idea:

        IDEA: {idea_data.get('refined_idea', 'Unknown')}
        TARGET MARKET: {idea_data.get('target_market', 'Unknown')}
        VALUE PROPOSITIONS: {idea_data.get('value_propositions', [])}

        VALIDATION INSIGHTS:
        {validation_data}

        Analyze the technical requirements and provide:

        Return as JSON:
        {{
            "functional_requirements": [
                {{
                    "requirement": "Description of functional requirement",
                    "priority": "high|medium|low",
                    "complexity": "high|medium|low",
                    "dependencies": ["List of dependencies"],
                    "acceptance_criteria": ["List of acceptance criteria"]
                }}
            ],
            "non_functional_requirements": [
                {{
                    "category": "performance|security|scalability|usability|reliability",
                    "requirement": "Description of non-functional requirement",
                    "priority": "high|medium|low",
                    "metrics": ["List of measurable metrics"],
                    "constraints": ["List of constraints"]
                }}
            ],
            "integration_requirements": [
                {{
                    "integration": "Description of integration needed",
                    "type": "api|database|third_party|internal",
                    "priority": "high|medium|low",
                    "complexity": "high|medium|low"
                }}
            ],
            "data_requirements": [
                {{
                    "data_type": "Type of data",
                    "storage_requirements": "Storage needs",
                    "processing_requirements": "Processing needs",
                    "security_requirements": "Security needs"
                }}
            ],
            "user_interface_requirements": [
                {{
                    "interface_type": "web|mobile|api|desktop",
                    "requirements": ["List of UI requirements"],
                    "accessibility": ["Accessibility requirements"],
                    "responsive_design": "yes|no"
                }}
            ],
            "security_requirements": [
                {{
                    "security_area": "authentication|authorization|data_protection|compliance",
                    "requirements": ["List of security requirements"],
                    "compliance": ["List of compliance requirements"]
                }}
            ],
            "performance_requirements": [
                {{
                    "metric": "response_time|throughput|availability|scalability",
                    "target": "Target value",
                    "measurement": "How to measure"
                }}
            ]
        }}
        """
        
        messages = [
            {"role": "system", "content": "You are an expert software architect and technical analyst with deep experience in system design and requirements engineering."},
            {"role": "user", "content": prompt}
        ]
        
        response = self.call_llm(messages, temperature=0.3)
        result = self.parse_json_response(response)
        
        if result:
            self.log_activity("Created technical requirements")
            return result
        
        return {"error": "Failed to create technical requirements"}
    
    def create_architecture_plan(self, idea_data: Dict[str, Any], technical_requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Create a comprehensive architecture plan for the business idea"""
        
        prompt = f"""
        Create a comprehensive architecture plan for this business idea:

        IDEA: {idea_data.get('refined_idea', 'Unknown')}
        TARGET MARKET: {idea_data.get('target_market', 'Unknown')}
        TECHNICAL REQUIREMENTS: {technical_requirements}

        Design a scalable, secure, and maintainable architecture that addresses:

        Return as JSON:
        {{
            "system_overview": {{
                "architecture_type": "monolithic|microservices|serverless|hybrid",
                "deployment_model": "cloud|on_premise|hybrid",
                "scalability_strategy": "horizontal|vertical|auto_scaling",
                "high_level_design": "Description of overall system design"
            }},
            "component_architecture": [
                {{
                    "component": "Component name",
                    "purpose": "What this component does",
                    "technology": "Recommended technology",
                    "responsibilities": ["List of responsibilities"],
                    "interfaces": ["List of interfaces"],
                    "dependencies": ["List of dependencies"]
                }}
            ],
            "data_architecture": {{
                "data_stores": [
                    {{
                        "store_type": "database|cache|file_storage|message_queue",
                        "technology": "Recommended technology",
                        "purpose": "What it stores",
                        "scalability": "Scalability considerations"
                    }}
                ],
                "data_flow": "Description of how data flows through the system",
                "data_security": ["Data security measures"],
                "backup_strategy": "Backup and recovery strategy"
            }},
            "api_architecture": {{
                "api_design": "REST|GraphQL|gRPC|hybrid",
                "endpoints": ["List of key API endpoints"],
                "authentication": "Authentication strategy",
                "rate_limiting": "Rate limiting strategy",
                "versioning": "API versioning strategy"
            }},
            "security_architecture": {{
                "authentication": "Authentication methods",
                "authorization": "Authorization strategy",
                "data_encryption": "Encryption strategy",
                "network_security": "Network security measures",
                "compliance": ["Compliance requirements"]
            }},
            "deployment_architecture": {{
                "infrastructure": "Cloud provider recommendations",
                "containerization": "Docker|Kubernetes|none",
                "ci_cd": "CI/CD pipeline design",
                "monitoring": "Monitoring and logging strategy",
                "disaster_recovery": "Disaster recovery plan"
            }},
            "scalability_plan": {{
                "horizontal_scaling": "Horizontal scaling strategy",
                "vertical_scaling": "Vertical scaling strategy",
                "load_balancing": "Load balancing strategy",
                "caching_strategy": "Caching strategy",
                "database_scaling": "Database scaling strategy"
            }},
            "technology_stack": {{
                "frontend": ["Frontend technologies"],
                "backend": ["Backend technologies"],
                "database": ["Database technologies"],
                "infrastructure": ["Infrastructure technologies"],
                "monitoring": ["Monitoring technologies"]
            }}
        }}
        """
        
        messages = [
            {"role": "system", "content": "You are an expert software architect with deep experience in designing scalable, secure, and maintainable systems."},
            {"role": "user", "content": prompt}
        ]
        
        response = self.call_llm(messages, temperature=0.3)
        result = self.parse_json_response(response)
        
        if result:
            self.log_activity("Created architecture plan")
            return result
        
        return {"error": "Failed to create architecture plan"}
    
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