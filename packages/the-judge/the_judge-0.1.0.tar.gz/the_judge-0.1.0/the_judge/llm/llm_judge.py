from typing import Any, Optional, Dict
from ..core.judge import Judge

class LLMJudge(Judge):
    """
    A specialized Judge that uses an LLM to perform evaluations.
    """
    def __init__(self, prompt: str, response: str, agent: Any = None, 
                llm_client: Any = None, 
                system_prompt: Optional[str] = None,
                custom_metrics: Optional[Dict[str, str]] = None):
        """
        Initialize the LLMJudge.
        
        Args:
            prompt: The original prompt/question
            response: The LLM's response to evaluate
            agent: Optional agent that will learn from the evaluation
            llm_client: A client for making calls to an LLM
            system_prompt: Optional custom system prompt for the judge LLM
            custom_metrics: Optional dictionary of custom metrics and their descriptions
        """
        super().__init__(prompt, response, agent, custom_metrics)
        
        self.llm_client = llm_client
        
        # Default system prompt for the judge LLM
        self.system_prompt = system_prompt or """
        You are an expert evaluator of LLM responses. Your task is to carefully analyze 
        the response to a given prompt based on specific metrics and provide detailed feedback.
        Be objective, fair, and thorough in your evaluation. Provide numerical scores between 0 and 1,
        where 0 is the worst and 1 is the best.
        """
    
    def judge_metric(self, metric: str) -> float:
        """
        Judge the response based on a specific metric using an LLM.
        
        Args:
            metric: The metric to evaluate
            
        Returns:
            A score between 0 and 1
        """
        if not self.llm_client:
            self.logger.warning("No LLM client provided, falling back to heuristic evaluation")
            return super().judge_metric(metric)
        
        description = self.metric_descriptions[metric]
        
        # Construct prompt for the LLM
        evaluation_prompt = f"""
        Metric to evaluate: {metric}
        Description: {description}
        
        Original prompt: {self.prompt}
        
        Response to evaluate: {self.response}
        
        Please evaluate the response based on the {metric} metric. 
        Provide a score between 0 and 1, where 0 is the worst and 1 is the best.
        First explain your reasoning in detail, then provide the numerical score in the format: SCORE: X.X
        """
        
        try:
            # Call the LLM
            llm_response = self.llm_client.generate(
                system_prompt=self.system_prompt,
                prompt=evaluation_prompt
            )
            
            # Extract the score from the response
            response_text = llm_response.text if hasattr(llm_response, 'text') else str(llm_response)
            
            # Store the reasoning in the chain of thought
            if metric == self.evaluation_metrics[0]:  # Only for the first metric to avoid duplication
                self.evaluation_results['chain_of_thought'] = [response_text.split("SCORE:")[0].strip()]
            
            # Extract score
            if "SCORE:" in response_text:
                score_text = response_text.split("SCORE:")[1].strip()
                score = float(score_text.split()[0])
                return max(0.0, min(1.0, score))  # Ensure it's between 0 and 1
            else:
                self.logger.warning(f"Could not extract score for {metric}, defaulting to 0.5")
                return 0.5
                
        except Exception as e:
            self.logger.error(f"Error evaluating with LLM: {str(e)}")
            return super().judge_metric(metric)  # Fall back to heuristic
    
    def generate_chain_of_thought(self) -> list:
        """
        Generate a chain of thought reasoning for the evaluation using an LLM.
        
        Returns:
            A list of strings containing reasoning steps
        """
        if not self.llm_client:
            return super().generate_chain_of_thought()
        
        # If we already have chain of thought from metric evaluations
        if self.evaluation_results['chain_of_thought']:
            return self.evaluation_results['chain_of_thought']
        
        metrics_summary = ", ".join([
            f"{m}: {s:.1f}" for m, s in self.evaluation_results['evaluation_metrics'].items()
        ])
        
        cot_prompt = f"""
        Original prompt: {self.prompt}
        
        Response to evaluate: {self.response}
        
        Metric scores: {metrics_summary}
        
        Please provide a detailed analysis of the response, focusing on its strengths and weaknesses.
        Break down your analysis into distinct points or observations.
        Format each point as a separate paragraph.
        """
        
        try:
            llm_response = self.llm_client.generate(
                system_prompt=self.system_prompt,
                prompt=cot_prompt
            )
            
            response_text = llm_response.text if hasattr(llm_response, 'text') else str(llm_response)
            
            # Split into paragraphs and clean up
            thoughts = [p.strip() for p in response_text.split("\n\n") if p.strip()]
            return thoughts
            
        except Exception as e:
            self.logger.error(f"Error generating chain of thought: {str(e)}")
            return super().generate_chain_of_thought()
    
    def generate_feedback(self) -> str:
        """
        Generate human-readable feedback using an LLM.
        
        Returns:
            A string containing feedback
        """
        if not self.llm_client:
            return super().generate_feedback()
        
        metrics_summary = ", ".join([
            f"{m}: {s:.1f}" for m, s in self.evaluation_results['evaluation_metrics'].items()
        ])
        
        is_correct = "yes" if self.evaluation_results['is_correct'] else "no"
        
        feedback_prompt = f"""
        Original prompt: {self.prompt}
        
        Response to evaluate: {self.response}
        
        Metric scores: {metrics_summary}
        Overall assessment: The response is {is_correct} correct.
        
        Please provide concise, actionable feedback for improving this response.
        Focus on 2-3 key improvement areas and be specific about what changes would make the response better.
        Keep your feedback under 150 words.
        """
        
        try:
            llm_response = self.llm_client.generate(
                system_prompt=self.system_prompt,
                prompt=feedback_prompt
            )
            
            feedback = llm_response.text if hasattr(llm_response, 'text') else str(llm_response)
            return feedback.strip()
            
        except Exception as e:
            self.logger.error(f"Error generating feedback: {str(e)}")
            return super().generate_feedback() 