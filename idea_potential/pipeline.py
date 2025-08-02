from typing import Dict, List, Any, Optional
from idea_potential.clarifier_agent import ClarifierAgent
from idea_potential.research_agent import ResearchAgent
from idea_potential.validation_agent import ValidationAgent
from idea_potential.roadmap_agent import RoadmapAgent
from idea_potential.report_agent import ReportAgent
from idea_potential.refiner_agent import RefinerAgent
import json
from datetime import datetime

class IdeaPotentialPipeline:
    """Main pipeline that orchestrates all agents for idea potential analysis"""
    
    def __init__(self, use_roadmap_agent: bool = False, use_refiner_agent: bool = False, use_suggester_agent: bool = False):
        # Must-have agents (always initialized)
        self.clarifier = ClarifierAgent(use_suggester_agent=use_suggester_agent)
        self.research = ResearchAgent()
        self.validator = ValidationAgent()
        self.report_builder = ReportAgent()
        
        # Optional agents (only initialized if selected)
        self.roadmap_builder = RoadmapAgent() if use_roadmap_agent else None
        self.refiner = RefinerAgent() if use_refiner_agent else None
        
        self.pipeline_data = {}
        self.current_step = "initialized"
        self.agent_config = {
            "use_roadmap_agent": use_roadmap_agent,
            "use_refiner_agent": use_refiner_agent,
            "use_suggester_agent": use_suggester_agent
        }
        
    def start_analysis(self, idea: str) -> Dict[str, Any]:
        """Start the idea potential analysis pipeline"""
        
        print("🚀 Starting Idea Potential Analysis Pipeline")
        print(f"📝 Idea: {idea}")
        print("=" * 50)
        
        # Display agent configuration
        print("\n🔧 Agent Configuration:")
        print(f"  • Clarifier Agent: ✅ (Required)")
        print(f"  • Research Agent: ✅ (Required)")
        print(f"  • Validation Agent: ✅ (Required)")
        print(f"  • Report Agent: ✅ (Required)")
        print(f"  • Suggester Agent: {'✅ (Enabled)' if self.agent_config['use_suggester_agent'] else '❌ (Disabled)'}")
        print(f"  • Roadmap Agent: {'✅ (Enabled)' if self.agent_config['use_roadmap_agent'] else '❌ (Disabled)'}")
        print(f"  • Refiner Agent: {'✅ (Enabled)' if self.agent_config['use_refiner_agent'] else '❌ (Disabled)'}")
        print("=" * 50)
        
        # Step 1: Clarify the idea
        print("\n🔍 Step 1: Clarifying the idea...")
        clarification_result = self.clarify_idea(idea)
        
        if "error" in clarification_result:
            return {"error": f"Clarification failed: {clarification_result['error']}"}
        
        # Step 2: Conduct market research
        print("\n📊 Step 2: Conducting market research...")
        research_result = self.conduct_research(clarification_result)
        
        if "error" in research_result:
            return {"error": f"Research failed: {research_result['error']}"}
        
        # Step 3: Create validation matrix
        print("\n✅ Step 3: Creating validation matrix...")
        validation_result = self.create_validation_matrix(clarification_result, research_result)
        
        if "error" in validation_result:
            return {"error": f"Validation failed: {validation_result['error']}"}
        
        # Step 4: Build development roadmap (optional)
        roadmap_result = {"error": "Roadmap agent not enabled"}
        if self.agent_config['use_roadmap_agent']:
            print("\n🗓️ Step 4: Building development roadmap...")
            roadmap_result = self.create_roadmap(clarification_result, validation_result)
            
            if "error" in roadmap_result:
                return {"error": f"Roadmap creation failed: {roadmap_result['error']}"}
        else:
            print("\n🗓️ Step 4: Skipping roadmap (agent not enabled)")
        
        # Step 5: Generate comprehensive report
        print("\n📋 Step 5: Generating comprehensive report...")
        report_result = self.generate_report(clarification_result, research_result, validation_result, roadmap_result)
        
        if "error" in report_result:
            return {"error": f"Report generation failed: {report_result['error']}"}
        
        # Step 6: Refine and validate report (optional)
        refinement_result = {"error": "Refiner agent not enabled"}
        if self.agent_config['use_refiner_agent']:
            print("\n🔧 Step 6: Refining and validating report...")
            refinement_result = self.refine_report(report_result, clarification_result, research_result, validation_result)
        else:
            print("\n🔧 Step 6: Skipping refinement (agent not enabled)")
        
        # Compile final results
        final_result = self.compile_final_results(
            clarification_result, research_result, validation_result, 
            roadmap_result, report_result, refinement_result
        )
        
        print("\n✅ Analysis complete!")
        return final_result
    
    def clarify_idea(self, idea: str) -> Dict[str, Any]:
        """Step 1: Clarify the idea through targeted questions"""
        
        # Analyze the initial idea (now just prepares for dynamic questioning)
        analysis_result = self.clarifier.analyze_initial_idea(idea)
        
        if "error" in analysis_result:
            return analysis_result
        
        # Store clarification data
        self.pipeline_data['clarification'] = analysis_result
        self.current_step = "clarification"
        
        return analysis_result
    
    def conduct_research(self, clarification_data: Dict[str, Any]) -> Dict[str, Any]:
        """Step 2: Conduct market research using Reddit data"""
        
        # Conduct research using the clarified idea data
        research_result = self.research.conduct_research(clarification_data)
        
        if "error" in research_result:
            return research_result
        
        # Store research data
        self.pipeline_data['research'] = research_result
        self.current_step = "research"
        
        return research_result
    
    def create_validation_matrix(self, clarification_data: Dict[str, Any], research_data: Dict[str, Any]) -> Dict[str, Any]:
        """Step 3: Create validation matrix and frameworks"""
        
        # Generate validation report
        validation_result = self.validator.generate_validation_report(clarification_data, research_data)
        
        if "error" in validation_result:
            return validation_result
        
        # Store validation data
        self.pipeline_data['validation'] = validation_result
        self.current_step = "validation"
        
        return validation_result
    
    def create_roadmap(self, clarification_data: Dict[str, Any], validation_data: Dict[str, Any]) -> Dict[str, Any]:
        """Step 4: Create development roadmap"""
        
        if self.roadmap_builder is None:
            return {"error": "Roadmap agent not enabled"}
        
        # Generate roadmap report
        roadmap_result = self.roadmap_builder.generate_roadmap_report(clarification_data, validation_data)
        
        if "error" in roadmap_result:
            return roadmap_result
        
        # Store roadmap data
        self.pipeline_data['roadmap'] = roadmap_result
        self.current_step = "roadmap"
        
        return roadmap_result
    
    def generate_report(self, clarification_data: Dict[str, Any], research_data: Dict[str, Any], 
                       validation_data: Dict[str, Any], roadmap_data: Dict[str, Any]) -> Dict[str, Any]:
        """Step 5: Generate comprehensive analysis report (JSON only)"""
        
        # Generate comprehensive report
        report_result = self.report_builder.generate_comprehensive_report(
            clarification_data, research_data, validation_data, roadmap_data
        )
        
        if "error" in report_result:
            return report_result
        
        # Store report data (JSON only, no markdown)
        self.pipeline_data['report'] = {
            'report_data': report_result,
            'filepath': 'JSON report only - no markdown generated'
        }
        self.current_step = "report"
        
        return self.pipeline_data['report']
    
    def refine_report(self, report_data: Dict[str, Any], clarification_data: Dict[str, Any], 
                     research_data: Dict[str, Any], validation_data: Dict[str, Any]) -> Dict[str, Any]:
        """Step 6: Refine and validate the final report"""
        
        if self.refiner is None:
            return {"error": "Refiner agent not enabled"}
        
        # Refine the report
        refinement_result = self.refiner.refine_report(
            report_data['report_data'], clarification_data, research_data, validation_data
        )
        
        if "error" in refinement_result:
            return refinement_result
        
        # Store refinement data
        self.pipeline_data['refinement'] = refinement_result
        self.current_step = "refinement"
        
        return refinement_result
    
    def compile_final_results(self, clarification_data: Dict[str, Any], research_data: Dict[str, Any],
                            validation_data: Dict[str, Any], roadmap_data: Dict[str, Any],
                            report_data: Dict[str, Any], refinement_data: Dict[str, Any]) -> Dict[str, Any]:
        """Compile all results into a final comprehensive output"""
        
        # Create final summary with safe data access
        final_summary = {
            "analysis_timestamp": datetime.now().isoformat(),
            "pipeline_status": "completed",
            "idea_summary": clarification_data.get('refined_idea', 'Unknown') if isinstance(clarification_data, dict) else str(clarification_data),
            "target_market": clarification_data.get('target_market', 'Unknown') if isinstance(clarification_data, dict) else 'Unknown',
            "executive_summary": {
                "recommendation": "Unknown",
                "confidence_level": "Unknown", 
                "key_findings": []
            },
            "validation_summary": {
                "overall_score": "Unknown",
                "risk_level": "Unknown",
                "recommendation": "Unknown"
            },
            "research_summary": {
                "posts_analyzed": 0,
                "market_validation": "Unknown",
                "pain_points_identified": []
            },
            "roadmap_summary": {
                "overall_timeline": "Unknown",
                "key_phases": [],
                "critical_milestones": []
            },
            "refinement_summary": {
                "quality_score": "Unknown",
                "authenticity": "Unknown",
                "final_recommendation": "Unknown"
            },
            "report_filepath": "JSON report only",
            "detailed_data": {
                "clarification": clarification_data,
                "research": research_data,
                "validation": validation_data,
                "roadmap": roadmap_data,
                "report": report_data,
                "refinement": refinement_data
            }
        }
        
        # Safely extract data from report_data
        if isinstance(report_data, dict):
            if 'report_data' in report_data and isinstance(report_data['report_data'], dict):
                report_content = report_data['report_data']
                if 'executive_summary' in report_content and isinstance(report_content['executive_summary'], dict):
                    final_summary["executive_summary"] = {
                        "recommendation": report_content['executive_summary'].get('recommendation', 'Unknown'),
                        "confidence_level": report_content['executive_summary'].get('confidence_level', 'Unknown'),
                        "key_findings": report_content['executive_summary'].get('key_findings', [])
                    }
            final_summary["report_filepath"] = report_data.get('filepath', 'JSON report only')
        
        # Safely extract data from validation_data
        if isinstance(validation_data, dict):
            if 'validation_summary' in validation_data and isinstance(validation_data['validation_summary'], dict):
                final_summary["validation_summary"] = {
                    "overall_score": validation_data['validation_summary'].get('overall_validation_score', 'Unknown'),
                    "risk_level": validation_data['validation_summary'].get('risk_level', 'Unknown'),
                    "recommendation": validation_data['validation_summary'].get('validation_recommendation', 'Unknown')
                }
        
        # Safely extract data from research_data
        if isinstance(research_data, dict):
            if 'insights' in research_data and isinstance(research_data['insights'], dict):
                final_summary["research_summary"] = {
                    "posts_analyzed": research_data['insights'].get('posts_analyzed', 0),
                    "market_validation": research_data['insights'].get('market_validation', 'Unknown'),
                    "pain_points_identified": research_data['insights'].get('pain_points_identified', [])
                }
        
        # Safely extract data from roadmap_data
        if isinstance(roadmap_data, dict):
            if 'roadmap_summary' in roadmap_data and isinstance(roadmap_data['roadmap_summary'], dict):
                final_summary["roadmap_summary"] = {
                    "overall_timeline": roadmap_data['roadmap_summary'].get('overall_timeline', 'Unknown'),
                    "key_phases": roadmap_data['roadmap_summary'].get('key_phases', []),
                    "critical_milestones": roadmap_data['roadmap_summary'].get('critical_milestones', [])
                }
        
        # Safely extract data from refinement_data
        if isinstance(refinement_data, dict):
            if 'final_summary' in refinement_data and isinstance(refinement_data['final_summary'], dict):
                final_summary["refinement_summary"] = {
                    "quality_score": refinement_data['final_summary'].get('overall_quality_score', 'Unknown'),
                    "authenticity": refinement_data['final_summary'].get('authenticity_assessment', 'Unknown'),
                    "final_recommendation": refinement_data['final_summary'].get('final_recommendation', 'Unknown')
                }
        
        # Save final results to JSON file
        self.save_final_results(final_summary)
        
        return final_summary
    
    def save_final_results(self, final_results: Dict[str, Any]) -> str:
        """Save final results to a JSON file"""
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"idea_analysis_results_{timestamp}.json"
        
        # Create reports directory if it doesn't exist
        import os
        os.makedirs('idea_potential/reports', exist_ok=True)
        filepath = os.path.join('idea_potential/reports', filename)
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(final_results, f, indent=2, ensure_ascii=False)
            
            print(f"📁 Final results saved to: {filepath}")
            return filepath
            
        except Exception as e:
            print(f"Error saving final results: {e}")
            return None
    
    def get_pipeline_status(self) -> Dict[str, Any]:
        """Get current pipeline status"""
        
        return {
            "current_step": self.current_step,
            "pipeline_data_keys": list(self.pipeline_data.keys()),
            "status": "completed" if self.current_step == "refinement" else "in_progress"
        }
    
    def get_step_data(self, step: str) -> Optional[Dict[str, Any]]:
        """Get data from a specific pipeline step"""
        
        return self.pipeline_data.get(step)
    
    def run_interactive_analysis(self, idea: str) -> Dict[str, Any]:
        """Run analysis with interactive clarification questions"""
        
        print("🎯 Idea Potential Analysis System - Interactive Mode")
        print("=" * 50)
        print(f"📝 Idea: {idea}")
        
        # Step 1: Clarify the idea
        print("\n🔍 Step 1: Clarifying your idea...")
        clarification_result = self.clarify_idea(idea)
        
        if "error" in clarification_result:
            return {"error": f"Clarification failed: {clarification_result['error']}"}
        
        # Start dynamic questioning process
        print(f"\n📋 I'll ask you questions one by one to better understand your idea:")
        print("💡 Each question will be generated based on your previous answers.")
        print("🔄 The conversation will continue until we have enough information.")
        
        question_count = 0
        user_response = None
        while True:
            question_count += 1
            
            # Get the next question
            if question_count == 1:
                # First question - no previous response
                question_data = self.clarifier.generate_next_question()
            else:
                # Get the next question based on previous response
                question_data = self.clarifier.generate_next_question(user_response)
            
            if "error" in question_data:
                print(f"❌ Error getting question: {question_data['error']}")
                break
            
            # Check if we're done with questions
            if question_data.get("status") == "clarified":
                print(f"\n✅ Clarification complete!")
                final_clarification = question_data
                break
            
            # Display the question
            print(f"\n❓ Question {question_count}: {question_data['question']}")
            print(f"💡 Why this matters: {question_data['reason']}")
            print(f"📊 Category: {question_data['category'].replace('_', ' ').title()}")
            
            # Get suggestions for this question if suggester agent is enabled
            suggestions = []
            if self.clarifier.suggester is not None:
                context = {
                    "idea": idea,
                    "question": question_data['question'],
                    "category": question_data['category'],
                    "previous_questions": self.clarifier.questions_asked,
                    "previous_responses": self.clarifier.user_responses
                }
                
                suggestions_result = self.clarifier.suggester.generate_suggestions(
                    question=question_data['question'],
                    context=context,
                    agent_type="clarifier"
                )
                suggestions = suggestions_result.get("suggestions", []) if "error" not in suggestions_result else []
            
            # Display suggestions if available
            if suggestions:
                print(f"\n💡 Suggested answers:")
                for j, suggestion in enumerate(suggestions, 1):
                    print(f"   {j}. {suggestion['text']}")
                    print(f"      💭 {suggestion['reasoning']}")
                print(f"   {len(suggestions) + 1}. Type your own answer")
            
            # Get user input
            while True:
                user_input = input("Your choice (number or your answer): ").strip()
                
                # Check if user selected a suggestion
                if user_input.isdigit() and suggestions:
                    choice = int(user_input)
                    if 1 <= choice <= len(suggestions):
                        answer = suggestions[choice - 1]['text']
                        print(f"✅ Selected: {answer}")
                        break
                    elif choice == len(suggestions) + 1:
                        # User wants to type their own answer
                        answer = input("Your answer: ").strip()
                        if answer:
                            break
                        else:
                            print("⚠️ Please provide an answer")
                    else:
                        print(f"⚠️ Please enter a number between 1 and {len(suggestions) + 1}")
                else:
                    # User typed their own answer
                    answer = user_input
                    if answer:
                        break
                    else:
                        print("⚠️ Please provide an answer")
            
            if not answer:
                print("⚠️ No answer provided, continuing...")
                answer = "No specific answer provided"
            
            print(f"✅ Your answer: {answer}")
            
            # Store the user response for the next iteration
            user_response = answer
            
            # Check if user wants to end the conversation
            if answer.lower() in ["that's all", "that's everything", "i think that covers it", "that should be enough", "done", "finish"]:
                print("\n🔄 Generating final summary...")
                final_clarification = self.clarifier.generate_clarification_summary()
                break
        
        if "error" in final_clarification:
            return {"error": f"Failed to generate clarification summary: {final_clarification['error']}"}
        
        print(f"\n✅ Clarification complete!")
        print(f"📝 Refined Idea: {final_clarification.get('refined_idea', 'Unknown')}")
        print(f"🎯 Target Market: {final_clarification.get('target_market', 'Unknown')}")
        print(f"📊 Questions asked: {len(self.clarifier.questions_asked)}")
        
        # Continue with full analysis
        print("\n🚀 Starting full analysis...")
        
        try:
            # Update pipeline data with clarification
            self.pipeline_data['clarification'] = final_clarification
            
            # Continue with remaining steps
            research_result = self.conduct_research(final_clarification)
            validation_result = self.create_validation_matrix(final_clarification, research_result)
            
            roadmap_result = {"error": "Roadmap agent not enabled"}
            if self.agent_config['use_roadmap_agent']:
                roadmap_result = self.create_roadmap(final_clarification, validation_result)
                if "error" in roadmap_result:
                    print(f"❌ Roadmap creation failed: {roadmap_result['error']}")
                    roadmap_result = {"error": "Roadmap agent failed to generate report"}
            
            report_result = self.generate_report(final_clarification, research_result, validation_result, roadmap_result)
            refinement_result = {"error": "Refiner agent not enabled"}
            if self.agent_config['use_refiner_agent']:
                refinement_result = self.refine_report(report_result, final_clarification, research_result, validation_result)
                if "error" in refinement_result:
                    print(f"❌ Refinement failed: {refinement_result['error']}")
                    refinement_result = {"error": "Refiner agent failed to refine report"}
            
            # Compile final results
            final_result = self.compile_final_results(
                final_clarification, research_result, validation_result,
                roadmap_result, report_result, refinement_result
            )
            
            print("\n✅ Analysis complete!")
            print(f"📁 Report saved to: {final_result.get('report_filepath', 'Not saved')}")
            
            return final_result
            
        except Exception as e:
            return {"error": f"Analysis failed: {e}"} 