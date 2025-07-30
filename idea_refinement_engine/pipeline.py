"""
Idea Validation Pipeline using LangGraph
Multi-agent system for brainstorming, critiquing, and validating ideas
"""

import json
import os
from datetime import datetime
from typing import Dict, Any
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI

from .state import ValidationState
from .clarifier_agent import ClarifierAgent
from .brainstormer_agent import BrainstormerAgent
from .critic_agent import CriticAgent
from .questioner_agent import QuestionerAgent
from .reality_miner_agent import RealityMinerAgent
from .synthesizer_agent import SynthesizerAgent
from .clarification_suggester_agent import GenericSuggestionAgent


class IdeaValidationPipeline:
    """Main pipeline orchestrator using LangGraph"""
    
    def __init__(self, llm_model: str = "gpt-4"):
        # Initialize specific models for each agent
        self.agents = {
            "clarifier": ClarifierAgent(ChatOpenAI(model="gpt-4-turbo", temperature=0.3)),
            "brainstormer": BrainstormerAgent(ChatOpenAI(model="gpt-4", temperature=0.9)),
            "critic": CriticAgent(ChatOpenAI(model="gpt-4", temperature=0.2)),
            "questioner": QuestionerAgent(ChatOpenAI(model="gpt-4-turbo", temperature=0.4)),
            "reality_miner": RealityMinerAgent(ChatOpenAI(model="gpt-4-turbo", temperature=0.3)),
            "synthesizer": SynthesizerAgent(ChatOpenAI(model="gpt-4-turbo", temperature=0.2)),
            "generic_suggester": GenericSuggestionAgent(ChatOpenAI(model="gpt-4-turbo", temperature=0.7))
        }
        self.graph = self._build_graph()
    
    def _build_graph(self) -> StateGraph:
        """Construct the agent workflow graph"""
        
        # Define the workflow
        workflow = StateGraph(ValidationState)
        
        # Add agent nodes
        workflow.add_node("clarifier", self._run_clarifier)
        workflow.add_node("brainstormer", self._run_brainstormer)
        workflow.add_node("critic", self._run_critic)
        workflow.add_node("questioner", self._run_questioner)
        workflow.add_node("reality_miner", self._run_reality_miner)
        workflow.add_node("synthesizer", self._run_synthesizer)
        workflow.add_node("single_clarification", self._get_single_clarification)
        workflow.add_node("user_validation", self._get_user_validation)
        workflow.add_node("interactive_validation", self._get_interactive_validation)
        
        # Define the flow
        workflow.set_entry_point("clarifier")
        
        # Conditional routing based on clarification status
        def should_continue_after_clarifier(state: ValidationState) -> str:
            # Check if we've been stuck in clarification too long
            if state.get("iteration_count", 0) > 5:
                print("\n⚠️ Maximum clarification iterations reached. Moving to next phase...")
                # Force the idea to be marked as complete
                if state["clarified_idea"]:
                    state["clarified_idea"]["status"] = "complete"
                return "brainstormer"
            
            # If we already have validation responses, skip clarification
            if state.get("user_validation_responses") and len(state["user_validation_responses"]) > 0:
                print("\n✅ Validation already completed, skipping clarification...")
                return "brainstormer"
            
            # If we already have a final report, we're done
            if state.get("final_report"):
                print("\n✅ Analysis already completed!")
                return END
            
            if state["clarified_idea"] and state["clarified_idea"].get("status") == "complete":
                return "brainstormer"
            else:
                return "single_clarification"
        
        workflow.add_conditional_edges(
            "clarifier",
            should_continue_after_clarifier,
            {"brainstormer": "brainstormer", "single_clarification": "single_clarification"}
        )
        
        # After single clarification, go back to clarifier
        workflow.add_edge("single_clarification", "clarifier")
        
        # Linear flow for the rest
        workflow.add_edge("brainstormer", "critic")
        workflow.add_edge("critic", "questioner")
        
        # After questioner, ask user for validation interactively
        workflow.add_edge("questioner", "interactive_validation")
        workflow.add_edge("interactive_validation", "reality_miner")
        workflow.add_edge("reality_miner", "synthesizer")
        workflow.add_edge("synthesizer", END)
        
        return workflow.compile()
    
    # Agent runner methods
    async def _run_clarifier(self, state: ValidationState) -> ValidationState:
        return await self.agents["clarifier"].run(state)
    
    async def _run_brainstormer(self, state: ValidationState) -> ValidationState:
        return await self.agents["brainstormer"].run(state)
    
    async def _run_critic(self, state: ValidationState) -> ValidationState:
        return await self.agents["critic"].run(state)
    
    async def _run_questioner(self, state: ValidationState) -> ValidationState:
        return await self.agents["questioner"].run(state)
    
    async def _run_reality_miner(self, state: ValidationState) -> ValidationState:
        return await self.agents["reality_miner"].run(state)
    
    async def _run_synthesizer(self, state: ValidationState) -> ValidationState:
        return await self.agents["synthesizer"].run(state)
    
    async def _get_single_clarification(self, state: ValidationState) -> ValidationState:
        """Get single clarification from user with AI suggestions"""
        if state.get("next_clarification_question"):
            question_data = state["next_clarification_question"]
            question = question_data["question"]
            reason = question_data["reason"]
            category = question_data["category"]
            
            print("\n🤔 CLARIFICATION NEEDED")
            print("=" * 50)
            print(f"Category: {category.upper()}")
            print(f"Reason: {reason}")
            print(f"\nQuestion: {question}")
            
            # Generate AI suggestions for this specific question
            suggestion_agent = self.agents["generic_suggester"]
            suggestions_result = await suggestion_agent.generate_suggestions(
                [question], 
                state["user_idea"], 
                "clarification"
            )
            
            # Show AI suggestions if available
            if suggestions_result and suggestions_result.get("suggestions") and len(suggestions_result["suggestions"]) > 0:
                question_suggestions = suggestions_result["suggestions"][0]
                if question_suggestions.get("suggestions"):
                    print("\n🤖 AI Suggestions:")
                    for j, suggestion in enumerate(question_suggestions["suggestions"], 1):
                        print(f"   {j}. [{suggestion['type'].upper()}] {suggestion['suggestion']}")
                        print(f"      Reasoning: {suggestion['reasoning']}")
                    print("   4. Write your own answer")
                else:
                    print("\n🤖 AI Suggestions: (No suggestions available)")
                    print("   Write your own answer:")
            else:
                print("\n🤖 AI Suggestions: (Generating suggestions...)")
                print("   Write your own answer:")
            
            # Get user choice
            while True:
                choice = input("\nChoose option (1-4) or write your answer: ").strip()
                
                if choice in ['1', '2', '3'] and suggestions_result and suggestions_result.get("suggestions") and len(suggestions_result["suggestions"]) > 0:
                    question_suggestions = suggestions_result["suggestions"][0]
                    if question_suggestions.get("suggestions") and len(question_suggestions["suggestions"]) >= int(choice):
                        # User chose an AI suggestion
                        suggestion_idx = int(choice) - 1
                        selected_suggestion = question_suggestions["suggestions"][suggestion_idx]
                        answer = selected_suggestion["suggestion"]
                        print(f"✅ Selected: {answer}")
                        break
                    else:
                        print("Invalid choice. Please select a valid option or write your answer.")
                elif choice == '4' or not choice.isdigit():
                    # User wants to write their own answer
                    answer = input("Your answer: ").strip()
                    if answer:
                        break
                    else:
                        print("Please provide an answer.")
                else:
                    print("Invalid choice. Please select 1-4 or write your answer.")
            
            # Update the user idea with this clarification
            clarification_text = f"Q: {question}\nA: {answer}"
            
            # Initialize or update clarification history
            if "clarification_history" not in state:
                state["clarification_history"] = ""
            
            if state["clarification_history"]:
                state["clarification_history"] += f"\n\n{clarification_text}"
            else:
                state["clarification_history"] = clarification_text
            
            # Update the user idea with all clarifications
            original_idea = state["user_idea"].split("\n\nClarifications:")[0] if "\n\nClarifications:" in state["user_idea"] else state["user_idea"]
            state["user_idea"] = f"{original_idea}\n\nClarifications:\n{state['clarification_history']}"
            
            # Clear the next question since we've handled it
            state["next_clarification_question"] = None
            
            # Increment iteration count
            state["iteration_count"] = state.get("iteration_count", 0) + 1
            
            print(f"\n✅ Clarification received! Re-evaluating idea...")
        
        return state
    
    async def _get_user_validation(self, state: ValidationState) -> ValidationState:
        """Get user responses to validation questions with AI suggestions"""
        if state["validation_questions"] and state["validation_questions"].get("validation_questions"):
            print("\n🔍 VALIDATION QUESTIONS")
            print("=" * 50)
            print("Please answer these validation questions to assess your idea:")
            
            questions = state["validation_questions"]["validation_questions"]
            user_responses = []
            
            for i, q_data in enumerate(questions, 1):
                question = q_data["question"]
                linked_risk = q_data["linked_risk"]
                test_method = q_data["test_method"]
                
                print(f"\n{i}. {question}")
                print(f"   Risk: {linked_risk}")
                print(f"   Test Method: {test_method}")
                
                # Generate AI suggestions for validation questions
                suggestion_agent = self.agents["generic_suggester"]
                suggestions_result = await suggestion_agent.generate_suggestions(
                    [question], 
                    state["user_idea"], 
                    "validation"
                )
                
                # Show AI suggestions if available
                if suggestions_result and suggestions_result.get("suggestions") and len(suggestions_result["suggestions"]) > 0:
                    question_suggestions = suggestions_result["suggestions"][0]
                    if question_suggestions.get("suggestions"):
                        print("\n🤖 AI Suggestions:")
                        for j, suggestion in enumerate(question_suggestions["suggestions"], 1):
                            print(f"   {j}. [{suggestion['type'].upper()}] {suggestion['suggestion']}")
                            print(f"      Reasoning: {suggestion['reasoning']}")
                        print("   4. Write your own answer")
                    else:
                        print("\n🤖 AI Suggestions: (No suggestions available)")
                        print("   Write your own answer:")
                else:
                    print("\n🤖 AI Suggestions: (Generating suggestions...)")
                    print("   Write your own answer:")
                
                # Get user choice
                while True:
                    choice = input("\nChoose option (1-4) or write your answer: ").strip()
                    
                    if choice in ['1', '2', '3'] and suggestions_result and suggestions_result.get("suggestions") and len(suggestions_result["suggestions"]) > 0:
                        question_suggestions = suggestions_result["suggestions"][0]
                        if question_suggestions.get("suggestions") and len(question_suggestions["suggestions"]) >= int(choice):
                            # User chose an AI suggestion
                            suggestion_idx = int(choice) - 1
                            selected_suggestion = question_suggestions["suggestions"][suggestion_idx]
                            response = selected_suggestion["suggestion"]
                            print(f"✅ Selected: {response}")
                            break
                        else:
                            print("Invalid choice. Please select a valid option or write your answer.")
                    elif choice == '4' or not choice.isdigit():
                        # User wants to write their own answer
                        response = input("Your answer: ").strip()
                        if response:
                            break
                        else:
                            print("Please provide an answer.")
                    else:
                        print("Invalid choice. Please select 1-4 or write your answer.")
                
                user_responses.append({
                    "question": question,
                    "response": response,
                    "linked_risk": linked_risk,
                    "test_method": test_method
                })
            
            # Store user responses in state
            state["user_validation_responses"] = user_responses
            print("\n✅ Validation responses received! Continuing analysis...")
        
        return state
    
    async def _get_interactive_validation(self, state: ValidationState) -> ValidationState:
        """Get user validation responses interactively - one question at a time"""
        try:
            if not state["critique_analysis"]:
                state["errors"].append("Cannot get validation - missing critique analysis")
                return state
            
            # Initialize validation responses if not exists
            if "user_validation_responses" not in state or state["user_validation_responses"] is None:
                state["user_validation_responses"] = []
            
            user_responses = state["user_validation_responses"]
            questioner_agent = self.agents["questioner"]
            
            print("\n🔍 VALIDATION PHASE")
            print("=" * 50)
            print("I'll ask you validation questions one by one, adapting based on your previous answers.")
            
            # Ask questions interactively
            max_questions = 5
            while len(user_responses) < max_questions:
                # Generate next question based on previous responses
                next_question_result = await questioner_agent.generate_next_question(state, user_responses)
                
                if next_question_result.get("status") == "complete":
                    print("\n✅ All critical validation questions addressed!")
                    break
                
                if next_question_result.get("error"):
                    print(f"\n⚠️ Error generating next question: {next_question_result['error']}")
                    break
                
                # Check if we've reached the maximum questions
                if len(user_responses) >= max_questions:
                    print(f"\n✅ Maximum {max_questions} validation questions reached!")
                    break
                
                # Get the next question
                next_question_data = next_question_result.get("next_question")
                if not next_question_data:
                    print("\n✅ No more critical questions to ask.")
                    break
                
                question = next_question_data["question"]
                linked_risk = next_question_data["linked_risk"]
                test_method = next_question_data["test_method"]
                reasoning = next_question_data.get("reasoning", "Critical validation needed")
                
                print(f"\n🤔 VALIDATION QUESTION #{len(user_responses) + 1}")
                print("=" * 50)
                print(f"Question: {question}")
                print(f"Risk: {linked_risk}")
                print(f"Test Method: {test_method}")
                print(f"Reasoning: {reasoning}")
                
                # Generate AI suggestions for this specific question
                suggestion_agent = self.agents["generic_suggester"]
                suggestions_result = await suggestion_agent.generate_suggestions(
                    [question], 
                    state["user_idea"], 
                    "validation"
                )
                
                # Show AI suggestions if available
                if suggestions_result and suggestions_result.get("suggestions") and len(suggestions_result["suggestions"]) > 0:
                    question_suggestions = suggestions_result["suggestions"][0]
                    if question_suggestions.get("suggestions"):
                        print("\n🤖 AI Suggestions:")
                        for j, suggestion in enumerate(question_suggestions["suggestions"], 1):
                            print(f"   {j}. [{suggestion['type'].upper()}] {suggestion['suggestion']}")
                            print(f"      Reasoning: {suggestion['reasoning']}")
                        print("   4. Write your own answer")
                    else:
                        print("\n🤖 AI Suggestions: (No suggestions available)")
                        print("   Write your own answer:")
                else:
                    print("\n🤖 AI Suggestions: (Generating suggestions...)")
                    print("   Write your own answer:")
                
                # Get user choice
                while True:
                    choice = input("\nChoose option (1-4) or write your answer: ").strip()
                    
                    if choice in ['1', '2', '3'] and suggestions_result and suggestions_result.get("suggestions") and len(suggestions_result["suggestions"]) > 0:
                        question_suggestions = suggestions_result["suggestions"][0]
                        if question_suggestions.get("suggestions") and len(question_suggestions["suggestions"]) >= int(choice):
                            # User chose an AI suggestion
                            suggestion_idx = int(choice) - 1
                            selected_suggestion = question_suggestions["suggestions"][suggestion_idx]
                            response = selected_suggestion["suggestion"]
                            print(f"✅ Selected: {response}")
                            break
                        else:
                            print("Invalid choice. Please select a valid option or write your answer.")
                    elif choice == '4' or not choice.isdigit():
                        # User wants to write their own answer
                        response = input("Your answer: ").strip()
                        if response:
                            break
                        else:
                            print("Please provide an answer.")
                    else:
                        print("Invalid choice. Please select 1-4 or write your answer.")
                
                # Store the response
                user_responses.append({
                    "question": question,
                    "response": response,
                    "linked_risk": linked_risk,
                    "test_method": test_method
                })
                
                print(f"\n✅ Response recorded. Moving to next question...")
            
            # Update state with final responses
            state["user_validation_responses"] = user_responses
            print(f"\n✅ Validation complete! {len(user_responses)} questions addressed.")
        
        except Exception as e:
            state["errors"].append(f"Interactive validation error: {str(e)}")
            return state
        
        return state
    
    def _save_report_to_file(self, report_content: str, user_idea: str) -> str:
        """Save the final report to a markdown file with datetime filename"""
        try:
            # Create reports directory if it doesn't exist
            reports_dir = os.path.join(os.path.dirname(__file__), "reports")
            os.makedirs(reports_dir, exist_ok=True)
            
            # Generate filename with datetime format: dd_mm_yy_hh_mm.md
            timestamp = datetime.now().strftime("%d_%m_%y_%H_%M")
            filename = f"{timestamp}.md"
            filepath = os.path.join(reports_dir, filename)
            
            # Create the markdown content with metadata
            markdown_content = f"""# Idea Validation Report

**Generated:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**Original Idea:** {user_idea.strip()}

---

{report_content}
"""
            
            # Write to file
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
            
            print(f"\n📄 Report saved to: {filepath}")
            return filepath
            
        except Exception as e:
            print(f"⚠️ Warning: Could not save report to file: {str(e)}")
            return None
    
    async def validate_idea(self, user_idea: str, save_report: bool = True) -> Dict[str, Any]:
        """Main entry point for idea validation"""
        
        # Initialize tracking for comprehensive reporting
        analysis_start_time = datetime.now()
        validation_id = f"VAL_{analysis_start_time.strftime('%Y%m%d_%H%M%S')}"
        
        initial_state: ValidationState = {
            "user_idea": user_idea,
            "clarified_idea": None,
            "idea_variations": None,
            "critique_analysis": None,
            "validation_questions": None,
            "reality_check": None,
            "final_report": None,
            "current_agent": "",
            "iteration_count": 0,
            "errors": [],
            "user_validation_responses": None,
            "clarification_history": "",
            "next_clarification_question": None,
            # Initialize tracking fields
            "analysis_start_time": analysis_start_time.isoformat(),
            "validation_id": validation_id,
            "analysis_duration_minutes": None
        }
        
        try:
            # Run the graph
            final_state = await self.graph.ainvoke(initial_state)
            
            # Calculate analysis duration
            if final_state.get("analysis_start_time"):
                start_time = datetime.fromisoformat(final_state["analysis_start_time"])
                duration = int((datetime.now() - start_time).total_seconds() / 60)
                final_state["analysis_duration_minutes"] = duration
            
            # Check if we have a final report, which indicates successful completion
            has_final_report = final_state.get("final_report") is not None
            has_errors = len(final_state["errors"]) > 0
            
            # Consider it successful if we have a final report, regardless of clarification errors
            success = has_final_report or (not has_errors)
            
            # Save report to file if requested and available
            report_filepath = None
            if save_report and final_state.get("final_report"):
                report_filepath = self._save_report_to_file(final_state["final_report"], user_idea)
            
            return {
                "success": success,
                "final_report": final_state["final_report"],
                "report_filepath": report_filepath,
                "intermediate_results": {
                    "clarified_idea": final_state["clarified_idea"],
                    "variations": final_state["idea_variations"],
                    "critique": final_state["critique_analysis"],
                    "questions": final_state["validation_questions"],
                    "reality_check": final_state["reality_check"],
                    "user_responses": final_state.get("user_validation_responses")
                },
                "errors": final_state["errors"],
                "tracking": {
                    "validation_id": final_state.get("validation_id"),
                    "analysis_duration_minutes": final_state.get("analysis_duration_minutes"),
                    "analysis_start_time": final_state.get("analysis_start_time")
                }
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Pipeline execution failed: {str(e)}",
                "final_report": None,
                "report_filepath": None
            } 