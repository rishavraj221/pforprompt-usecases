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
    
    def __init__(self):
        self.clarifier = ClarifierAgent()
        self.research = ResearchAgent()
        self.validator = ValidationAgent()
        self.roadmap_builder = RoadmapAgent()
        self.report_builder = ReportAgent()
        self.refiner = RefinerAgent()
        
        self.pipeline_data = {}
        self.current_step = "initialized"
        
    def start_analysis(self, idea: str) -> Dict[str, Any]:
        """Start the idea potential analysis pipeline"""
        
        print("🚀 Starting Idea Potential Analysis Pipeline")
        print(f"📝 Idea: {idea}")
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
        
        # Step 4: Build development roadmap
        print("\n🗓️ Step 4: Building development roadmap...")
        roadmap_result = self.create_roadmap(clarification_result, validation_result)
        
        if "error" in roadmap_result:
            return {"error": f"Roadmap creation failed: {roadmap_result['error']}"}
        
        # Step 5: Generate comprehensive report
        print("\n📋 Step 5: Generating comprehensive report...")
        report_result = self.generate_report(clarification_result, research_result, validation_result, roadmap_result)
        
        if "error" in report_result:
            return {"error": f"Report generation failed: {report_result['error']}"}
        
        # Step 6: Refine and validate report
        print("\n🔧 Step 6: Refining and validating report...")
        refinement_result = self.refine_report(report_result, clarification_result, research_result, validation_result)
        
        # Compile final results
        final_result = self.compile_final_results(
            clarification_result, research_result, validation_result, 
            roadmap_result, report_result, refinement_result
        )
        
        print("\n✅ Analysis complete!")
        return final_result
    
    def clarify_idea(self, idea: str) -> Dict[str, Any]:
        """Step 1: Clarify the idea through targeted questions"""
        
        # Analyze the initial idea
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
        
        # Create final summary
        final_summary = {
            "analysis_timestamp": datetime.now().isoformat(),
            "pipeline_status": "completed",
            "idea_summary": clarification_data.get('refined_idea', 'Unknown'),
            "target_market": clarification_data.get('target_market', 'Unknown'),
            "executive_summary": {
                "recommendation": report_data['report_data'].get('executive_summary', {}).get('recommendation', 'Unknown'),
                "confidence_level": report_data['report_data'].get('executive_summary', {}).get('confidence_level', 'Unknown'),
                "key_findings": report_data['report_data'].get('executive_summary', {}).get('key_findings', [])
            },
            "validation_summary": {
                "overall_score": validation_data.get('validation_summary', {}).get('overall_validation_score', 'Unknown'),
                "risk_level": validation_data.get('validation_summary', {}).get('risk_level', 'Unknown'),
                "recommendation": validation_data.get('validation_summary', {}).get('validation_recommendation', 'Unknown')
            },
            "research_summary": {
                "posts_analyzed": research_data.get('insights', {}).get('posts_analyzed', 0),
                "market_validation": research_data.get('insights', {}).get('market_validation', 'Unknown'),
                "pain_points_identified": research_data.get('insights', {}).get('pain_points_identified', [])
            },
            "roadmap_summary": {
                "overall_timeline": roadmap_data.get('roadmap_summary', {}).get('overall_timeline', 'Unknown'),
                "key_phases": roadmap_data.get('roadmap_summary', {}).get('key_phases', []),
                "critical_milestones": roadmap_data.get('roadmap_summary', {}).get('critical_milestones', [])
            },
            "refinement_summary": {
                "quality_score": refinement_data.get('final_summary', {}).get('overall_quality_score', 'Unknown'),
                "authenticity": refinement_data.get('final_summary', {}).get('authenticity_assessment', 'Unknown'),
                "final_recommendation": refinement_data.get('final_summary', {}).get('final_recommendation', 'Unknown')
            },
            "report_filepath": report_data.get('filepath', 'JSON report only'),
            "detailed_data": {
                "clarification": clarification_data,
                "research": research_data,
                "validation": validation_data,
                "roadmap": roadmap_data,
                "report": report_data['report_data'],
                "refinement": refinement_data
            }
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
        
        # Ask clarification questions
        questions = clarification_result.get('critical_questions', [])
        
        if questions:
            print(f"\n📋 I need to ask you {len(questions)} critical questions to better understand your idea:")
            
            for i, question_data in enumerate(questions, 1):
                print(f"\n❓ Question {i}: {question_data['question']}")
                print(f"💡 Why this matters: {question_data['reason']}")
                
                # Get suggestions for this question
                question_with_suggestions = self.clarifier.ask_next_question()
                
                if "error" in question_with_suggestions:
                    print(f"❌ Error getting question: {question_with_suggestions['error']}")
                    break
                
                # Display suggestions if available
                suggestions = question_with_suggestions.get("suggestions", [])
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
                    if user_input.isdigit():
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
                
                # Process the answer (this will move to the next question)
                next_question = self.clarifier.ask_next_question(answer)
                
                if "error" in next_question:
                    print(f"❌ Error processing answer: {next_question['error']}")
                    break
        
        # Get final clarification summary
        final_clarification = self.clarifier.generate_clarification_summary()
        
        if "error" in final_clarification:
            return {"error": f"Failed to generate clarification summary: {final_clarification['error']}"}
        
        print(f"\n✅ Clarification complete!")
        print(f"📝 Refined Idea: {final_clarification.get('refined_idea', 'Unknown')}")
        print(f"🎯 Target Market: {final_clarification.get('target_market', 'Unknown')}")
        
        # Continue with full analysis
        print("\n🚀 Starting full analysis...")
        
        try:
            # Update pipeline data with clarification
            self.pipeline_data['clarification'] = final_clarification
            
            # Continue with remaining steps
            research_result = self.conduct_research(final_clarification)
            validation_result = self.create_validation_matrix(final_clarification, research_result)
            roadmap_result = self.create_roadmap(final_clarification, validation_result)
            report_result = self.generate_report(final_clarification, research_result, validation_result, roadmap_result)
            refinement_result = self.refine_report(report_result, final_clarification, research_result, validation_result)
            
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