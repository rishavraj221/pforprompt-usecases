import json
import asyncio
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
import os
import time
from dataclasses import dataclass
from idea_potential.base_agent import BaseAgent


@dataclass
class ProcessingStats:
    """Statistics for report processing"""
    total_sections: int = 0
    processed_sections: int = 0
    start_time: Optional[float] = None
    end_time: Optional[float] = None
    errors: List[str] = None
    
    def __post_init__(self):
        if self.errors is None:
            self.errors = []
    
    @property
    def processing_time(self) -> float:
        if self.start_time and self.end_time:
            return self.end_time - self.start_time
        return 0.0
    
    @property
    def success_rate(self) -> float:
        if self.total_sections > 0:
            return (self.processed_sections / self.total_sections) * 100
        return 0.0


class AdvancedComprehensiveReportGenerator(BaseAgent):
    """
    Advanced agent for generating comprehensive analysis reports from JSON data.
    Features:
    - Progress tracking and statistics
    - Error handling and recovery
    - Memory-efficient processing
    - Detailed logging
    - Configurable processing options
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__('advanced_comprehensive_report_generator')
        self.config = config or {}
        self.stats = ProcessingStats()
        self.report_sections = {}
        self.source_references = {}
        self.processing_cache = {}
        
    def start_processing(self):
        """Start processing timer"""
        self.stats.start_time = time.time()
        self.stats.total_sections = 6  # executive, market, validation, roadmap, refinement, references
        self.log_activity("🚀 Starting advanced report generation")
    
    def end_processing(self):
        """End processing timer and log statistics"""
        self.stats.end_time = time.time()
        self.log_activity(f"✅ Processing completed in {self.stats.processing_time:.2f} seconds")
        self.log_activity(f"📊 Success rate: {self.stats.success_rate:.1f}%")
        if self.stats.errors:
            self.log_activity(f"⚠️ {len(self.stats.errors)} errors encountered")
    
    def safe_process_chunk(self, chunk_name: str, processor_func, *args, **kwargs) -> str:
        """Safely process a chunk with error handling"""
        try:
            self.log_activity(f"🔄 Processing {chunk_name}...")
            result = processor_func(*args, **kwargs)
            self.stats.processed_sections += 1
            self.log_activity(f"✅ {chunk_name} processed successfully")
            return result
        except Exception as e:
            error_msg = f"Error processing {chunk_name}: {str(e)}"
            self.log_activity(error_msg)
            self.stats.errors.append(error_msg)
            return f"# {chunk_name.replace('_', ' ').title()}\n\n⚠️ Error processing this section: {str(e)}\n\nPlease check the logs for details."
    
    def load_json_data(self, json_file_path: str) -> Dict[str, Any]:
        """Load and parse the JSON analysis data with validation"""
        try:
            if not os.path.exists(json_file_path):
                raise FileNotFoundError(f"JSON file not found: {json_file_path}")
            
            file_size = os.path.getsize(json_file_path)
            self.log_activity(f"📁 Loading JSON file: {json_file_path} ({file_size:,} bytes)")
            
            with open(json_file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
            
            # Validate basic structure
            required_keys = ['idea_summary', 'target_market', 'detailed_data']
            missing_keys = [key for key in required_keys if key not in data]
            if missing_keys:
                self.log_activity(f"⚠️ Missing required keys: {missing_keys}")
            
            self.log_activity(f"✅ Successfully loaded JSON data with {len(data)} top-level keys")
            return data
            
        except json.JSONDecodeError as e:
            self.log_activity(f"❌ Invalid JSON format: {e}")
            raise
        except Exception as e:
            self.log_activity(f"❌ Error loading JSON file: {e}")
            raise
    
    def extract_source_references(self, data: Dict[str, Any]) -> Dict[str, List[Dict[str, Any]]]:
        """Extract all source URLs and references from the data with enhanced processing"""
        references = {
            'reddit_posts': [],
            'market_sources': [],
            'technical_sources': [],
            'financial_sources': [],
            'validation_sources': [],
            'roadmap_sources': []
        }
        
        try:
            # Extract Reddit post URLs from research data
            if 'detailed_data' in data and 'research' in data['detailed_data']:
                research_data = data['detailed_data']['research']
                if 'posts_collected' in research_data:
                    posts = research_data['posts_collected']
                    self.log_activity(f"📊 Found {len(posts)} Reddit posts to process")
                    
                    for post in posts:
                        if 'url' in post:
                            references['reddit_posts'].append({
                                'title': post.get('title', ''),
                                'url': post['url'],
                                'subreddit': post.get('subreddit', ''),
                                'score': post.get('score', 0),
                                'relevance_score': post.get('relevance_score', 0),
                                'sentiment': post.get('sentiment_data', {}),
                                'engagement_level': post.get('engagement_level', 'unknown'),
                                'is_problem_discussion': post.get('is_problem_discussion', False)
                            })
            
            # Extract other source types if available
            if 'detailed_data' in data:
                detailed = data['detailed_data']
                
                # Add validation sources
                if 'validation' in detailed:
                    references['validation_sources'].append({
                        'type': 'validation_analysis',
                        'description': 'Comprehensive validation analysis',
                        'confidence_level': detailed['validation'].get('validation_matrix', {}).get('market_validation', {}).get('confidence_level', 'unknown')
                    })
                
                # Add roadmap sources
                if 'roadmap' in detailed:
                    references['roadmap_sources'].append({
                        'type': 'development_roadmap',
                        'description': 'Detailed development roadmap',
                        'timeline': data.get('roadmap_summary', {}).get('overall_timeline', 'unknown')
                    })
            
            self.log_activity(f"✅ Extracted {len(references['reddit_posts'])} Reddit posts and {sum(len(v) for k, v in references.items() if k != 'reddit_posts')} other sources")
            return references
            
        except Exception as e:
            self.log_activity(f"❌ Error extracting source references: {e}")
            return references
    
    def process_executive_summary_chunk(self, data: Dict[str, Any]) -> str:
        """Process executive summary and high-level insights with enhanced analysis"""
        
        executive_data = data.get('executive_summary', {})
        idea_summary = data.get('idea_summary', '')
        target_market = data.get('target_market', '')
        
        # Extract additional context
        pipeline_status = data.get('pipeline_status', 'unknown')
        analysis_timestamp = data.get('analysis_timestamp', '')
        
        prompt = f"""
        Create a comprehensive executive summary section for a business idea analysis report.
        
        IDEA SUMMARY: {idea_summary}
        TARGET MARKET: {target_market}
        PIPELINE STATUS: {pipeline_status}
        ANALYSIS TIMESTAMP: {analysis_timestamp}
        
        EXECUTIVE SUMMARY DATA:
        {json.dumps(executive_data, indent=2)}
        
        Create a professional executive summary that includes:
        1. **Idea Overview** - Clear description of the business idea and its value proposition
        2. **Key Findings** - Most important insights from the analysis with specific metrics
        3. **Recommendation** - Clear go/no-go recommendation with confidence level and rationale
        4. **Strategic Implications** - What this means for stakeholders and decision-makers
        5. **Next Steps** - Immediate actions to take with priorities and timelines
        6. **Risk Assessment** - Key risks and mitigation strategies
        7. **Success Metrics** - How to measure success and track progress
        
        Format as clean markdown with:
        - Professional headings and structure
        - Bullet points for key findings
        - Emphasis on important metrics and recommendations
        - Executive-friendly language
        - Actionable insights and clear next steps
        - Confidence levels and supporting evidence
        """
        
        return self.call_llm([{"role": "user", "content": prompt}])
    
    def process_market_analysis_chunk(self, data: Dict[str, Any]) -> str:
        """Process market research, user personas, and market insights with detailed analysis"""
        
        detailed_data = data.get('detailed_data', {})
        clarification = detailed_data.get('clarification', {})
        research = detailed_data.get('research', {})
        
        # Extract user personas
        user_personas = clarification.get('user_personas', {})
        primary_personas = user_personas.get('primary_personas', [])
        secondary_personas = user_personas.get('secondary_personas', [])
        persona_insights = user_personas.get('persona_insights', {})
        
        # Extract research insights
        research_insights = research.get('insights', {})
        market_insights = research_insights.get('market_insights', {})
        quantitative_data = research.get('quantitative_data', {})
        
        # Extract value propositions and challenges
        value_propositions = clarification.get('value_propositions', [])
        potential_challenges = clarification.get('potential_challenges', [])
        
        prompt = f"""
        Create a comprehensive market analysis section for a business idea report.
        
        USER PERSONAS:
        Primary Personas: {json.dumps(primary_personas, indent=2)}
        Secondary Personas: {json.dumps(secondary_personas, indent=2)}
        Persona Insights: {json.dumps(persona_insights, indent=2)}
        
        MARKET INSIGHTS:
        {json.dumps(market_insights, indent=2)}
        
        QUANTITATIVE DATA:
        {json.dumps(quantitative_data, indent=2)}
        
        VALUE PROPOSITIONS:
        {json.dumps(value_propositions, indent=2)}
        
        POTENTIAL CHALLENGES:
        {json.dumps(potential_challenges, indent=2)}
        
        RESEARCH SUMMARY:
        Posts Analyzed: {data.get('research_summary', {}).get('posts_analyzed', 0)}
        
        Create a detailed market analysis that includes:
        1. **Target Market Analysis** - Detailed breakdown of target audience with demographics, psychographics, and behavioral patterns
        2. **User Personas** - Detailed profiles of primary and secondary users with specific needs, pain points, and motivations
        3. **Market Size & Opportunity** - Market size assessment, growth potential, and addressable market segments
        4. **Customer Pain Points** - Key problems the solution addresses with specific examples and impact
        5. **Market Trends** - Relevant industry trends, technological advancements, and market dynamics
        6. **Competitive Landscape** - Analysis of competitors, differentiation opportunities, and market positioning
        7. **Value Proposition** - Clear value propositions and unique selling points
        8. **Market Validation** - Evidence of market demand and customer willingness to pay
        
        Include specific data points, percentages, market metrics, and supporting evidence where available.
        Format as professional markdown with tables, bullet points, clear sections, and visual hierarchy.
        Use specific numbers, percentages, and concrete examples to support analysis.
        """
        
        return self.call_llm([{"role": "user", "content": prompt}])
    
    def process_validation_chunk(self, data: Dict[str, Any]) -> str:
        """Process validation matrix, SWOT analysis, and risk assessment with detailed scoring"""
        
        detailed_data = data.get('detailed_data', {})
        validation = detailed_data.get('validation', {})
        validation_matrix = validation.get('validation_matrix', {})
        swot_analysis = validation.get('swot_analysis', {})
        risk_assessment = validation.get('risk_assessment', {})
        
        # Extract validation scores
        validation_summary = data.get('validation_summary', {})
        overall_score = validation_summary.get('overall_score', 'Unknown')
        risk_level = validation_summary.get('risk_level', 'Unknown')
        
        prompt = f"""
        Create a comprehensive validation and risk assessment section for a business idea report.
        
        VALIDATION MATRIX:
        {json.dumps(validation_matrix, indent=2)}
        
        SWOT ANALYSIS:
        {json.dumps(swot_analysis, indent=2)}
        
        RISK ASSESSMENT:
        {json.dumps(risk_assessment, indent=2)}
        
        VALIDATION SUMMARY:
        Overall Score: {overall_score}
        Risk Level: {risk_level}
        {json.dumps(validation_summary, indent=2)}
        
        Create a detailed validation analysis that includes:
        1. **Market Validation** - Evidence of market demand, size, and growth potential with specific metrics
        2. **Technical Feasibility** - Assessment of technical requirements, challenges, and implementation complexity
        3. **Financial Viability** - Revenue potential, cost structure, profitability analysis, and funding requirements
        4. **Competitive Advantage** - Differentiation strategies, sustainable advantages, and barriers to entry
        5. **Customer Adoption** - Adoption barriers, value perception, and customer acquisition strategies
        6. **SWOT Analysis** - Detailed strengths, weaknesses, opportunities, and threats with specific examples
        7. **Risk Assessment** - Key risks, probability, impact, and mitigation strategies
        8. **Validation Scoring** - Overall validation score with breakdown by category
        
        Include confidence levels, scores, specific evidence, and detailed recommendations for each validation area.
        Format as professional markdown with:
        - Validation scorecards and matrices
        - Risk assessment tables
        - SWOT analysis grid
        - Clear recommendations and action items
        - Supporting evidence and data points
        """
        
        return self.call_llm([{"role": "user", "content": prompt}])
    
    def process_roadmap_chunk(self, data: Dict[str, Any]) -> str:
        """Process development roadmap, timeline, and resource planning with detailed phases"""
        
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
        1. **Development Phases** - Clear phases with timelines, deliverables, and success criteria
        2. **Resource Requirements** - Team composition, technology stack, budget allocation, and external dependencies
        3. **Critical Milestones** - Key checkpoints, decision points, and success criteria with specific dates
        4. **Risk Mitigation** - How to handle potential delays, technical challenges, and resource constraints
        5. **Success Metrics** - How to measure progress, track KPIs, and evaluate success at each phase
        6. **Dependencies** - What needs to happen before each phase, external dependencies, and prerequisites
        7. **Resource Allocation** - Detailed breakdown of human, financial, and technical resources
        8. **Timeline Management** - Gantt chart-style timeline with parallel and sequential activities
        
        Include specific timelines, resource allocations, measurable milestones, and clear action items.
        Format as professional markdown with:
        - Timeline visualizations
        - Resource allocation tables
        - Milestone checklists
        - Risk mitigation strategies
        - Success metrics and KPIs
        """
        
        return self.call_llm([{"role": "user", "content": prompt}])
    
    def process_refinement_chunk(self, data: Dict[str, Any]) -> str:
        """Process gap analysis, refinement recommendations, and quality assessment with priorities"""
        
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
        1. **Gap Analysis** - Critical gaps, missing information, and areas requiring additional research
        2. **Quality Assessment** - Overall quality, authenticity, and reliability evaluation with specific metrics
        3. **Refinement Priorities** - High, medium, and low priority improvements with rationale and impact
        4. **Implementation Plan** - How to address identified gaps with specific actions, timelines, and resources
        5. **Final Recommendations** - Clear next steps, priorities, and strategic direction
        6. **Quality Metrics** - Specific quality indicators, scores, and evaluation criteria
        7. **Improvement Roadmap** - Detailed plan for addressing gaps and enhancing the business idea
        8. **Success Criteria** - How to measure improvement and track refinement progress
        
        Include specific improvement suggestions, implementation timelines, success criteria, and resource requirements.
        Format as professional markdown with:
        - Priority matrices and scoring
        - Action item checklists
        - Implementation timelines
        - Quality assessment frameworks
        - Clear recommendations and next steps
        """
        
        return self.call_llm([{"role": "user", "content": prompt}])
    
    def create_source_references_section(self, references: Dict[str, List[Dict[str, Any]]]) -> str:
        """Create a comprehensive source references section with detailed analysis"""
        
        prompt = f"""
        Create a comprehensive source references section for a business idea analysis report.
        
        SOURCE REFERENCES:
        {json.dumps(references, indent=2)}
        
        Create a detailed source references section that includes:
        1. **Reddit Posts Analyzed** - Complete list of relevant Reddit posts with URLs, relevance scores, and key insights
        2. **Market Research Sources** - External market research, industry reports, and market data sources
        3. **Technical References** - Technical documentation, feasibility studies, and implementation guides
        4. **Financial Sources** - Financial models, market data, and economic analysis sources
        5. **Validation Sources** - Validation studies, customer feedback, and market validation data
        6. **Roadmap Sources** - Development frameworks, project management methodologies, and implementation guides
        
        For each source, include:
        - Title/Description with context
        - URL/Link for verification
        - Relevance score or importance rating
        - Key insights extracted and their impact
        - Date of analysis and freshness
        - Source credibility and reliability assessment
        
        Format as a professional markdown with:
        - Organized tables by source type
        - Relevance scoring and ranking
        - Key insights summary
        - Source credibility indicators
        - Easy navigation and cross-references
        
        Include a summary of:
        - Total number of sources analyzed
        - Overall relevance and quality assessment
        - Key themes and patterns identified
        - Data freshness and reliability
        """
        
        return self.call_llm([{"role": "user", "content": prompt}])
    
    def synthesize_final_report(self, sections: Dict[str, str], references: Dict[str, List[Dict[str, Any]]]) -> str:
        """Combine all sections into a final comprehensive report with professional formatting"""
        
        # Create a summary of sections for the synthesis
        section_summaries = {}
        for key, content in sections.items():
            # Create a brief summary of each section
            summary = content[:500] + "..." if len(content) > 500 else content
            section_summaries[key] = summary
        
        prompt = f"""
        Create a comprehensive business idea analysis report by synthesizing all sections into a professional document.
        
        REPORT SECTIONS:
        {json.dumps(section_summaries, indent=2)}
        
        SOURCE REFERENCES:
        {json.dumps(references, indent=2)}
        
        Create a professional, comprehensive report that includes:
        
        1. **Title Page** - Professional title with date, version, and executive summary
        2. **Table of Contents** - Clear navigation structure with page numbers
        3. **Executive Summary** - High-level overview, key findings, and strategic recommendations
        4. **Market Analysis** - Target market, user personas, market insights, and competitive landscape
        5. **Validation Assessment** - Technical, financial, and market validation with risk assessment
        6. **Development Roadmap** - Implementation plan, timeline, resource requirements, and milestones
        7. **Refinement Recommendations** - Quality assessment, gap analysis, and improvement priorities
        8. **Source References** - Complete list of sources with relevance scores and key insights
        9. **Appendices** - Detailed data, supporting information, and technical specifications
        
        Format as a professional markdown document with:
        - Executive-level presentation quality
        - Clear hierarchy and navigation structure
        - Professional formatting and styling
        - Cross-references between sections
        - Executive-friendly language and actionable insights
        - Complete source attribution and credibility indicators
        - Visual elements like tables, charts, and bullet points
        - Executive summary with key metrics and recommendations
        - Actionable next steps and strategic direction
        
        Make it suitable for:
        - Stakeholders and decision-makers
        - Investors and funding sources
        - Strategic planning and execution
        - Team alignment and communication
        - Future reference and iteration
        """
        
        return self.call_llm([{"role": "user", "content": prompt}])
    
    def generate_comprehensive_report(self, json_file_path: str, output_path: Optional[str] = None) -> str:
        """Generate a comprehensive analysis report from JSON data with advanced processing"""
        
        self.start_processing()
        
        try:
            # Load and parse JSON data
            data = self.load_json_data(json_file_path)
            
            # Extract source references
            references = self.extract_source_references(data)
            
            # Process each chunk with specialized LLM calls and error handling
            sections = {}
            
            # Executive Summary
            sections['executive_summary'] = self.safe_process_chunk(
                'executive_summary', 
                self.process_executive_summary_chunk, 
                data
            )
            
            # Market Analysis
            sections['market_analysis'] = self.safe_process_chunk(
                'market_analysis', 
                self.process_market_analysis_chunk, 
                data
            )
            
            # Validation Assessment
            sections['validation_assessment'] = self.safe_process_chunk(
                'validation_assessment', 
                self.process_validation_chunk, 
                data
            )
            
            # Development Roadmap
            sections['development_roadmap'] = self.safe_process_chunk(
                'development_roadmap', 
                self.process_roadmap_chunk, 
                data
            )
            
            # Refinement Recommendations
            sections['refinement_recommendations'] = self.safe_process_chunk(
                'refinement_recommendations', 
                self.process_refinement_chunk, 
                data
            )
            
            # Source References
            sections['source_references'] = self.safe_process_chunk(
                'source_references', 
                self.create_source_references_section, 
                references
            )
            
            # Synthesize final report
            self.log_activity("🔄 Synthesizing final comprehensive report...")
            final_report = self.synthesize_final_report(sections, references)
            
            # Save report if output path provided
            if output_path:
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
                with open(output_path, 'w', encoding='utf-8') as file:
                    file.write(final_report)
                self.log_activity(f"📄 Report saved to {output_path}")
            
            self.end_processing()
            return final_report
            
        except Exception as e:
            self.log_activity(f"❌ Critical error in report generation: {e}")
            self.end_processing()
            raise
    
    def generate_report_from_file(self, json_file_path: str) -> str:
        """Convenience method to generate report and save with default naming"""
        
        # Generate default output path
        base_name = os.path.splitext(os.path.basename(json_file_path))[0]
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = f"idea_potential/reports/advanced_comprehensive_analysis_{base_name}_{timestamp}.md"
        
        return self.generate_comprehensive_report(json_file_path, output_path)
    
    def get_processing_stats(self) -> ProcessingStats:
        """Get processing statistics"""
        return self.stats


# Convenience function for easy usage
def generate_advanced_comprehensive_report(json_file_path: str, output_path: Optional[str] = None) -> Tuple[str, ProcessingStats]:
    """Generate a comprehensive analysis report from JSON data with advanced features"""
    generator = AdvancedComprehensiveReportGenerator()
    report = generator.generate_comprehensive_report(json_file_path, output_path)
    stats = generator.get_processing_stats()
    return report, stats 