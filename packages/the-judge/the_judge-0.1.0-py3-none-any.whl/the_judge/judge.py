import json
from typing import Dict, List, Union, Optional, Any, Callable
import logging

class Judge:
    """
    A class to evaluate LLM responses based on various metrics.
    """
    def __init__(self, prompt: str, response: str, agent: Any = None, 
                custom_metrics: Optional[Dict[str, str]] = None,
                evaluation_function: Optional[Callable] = None):
        """
        Initialize the Judge with a prompt and response.
        
        Args:
            prompt: The original prompt/question
            response: The LLM's response to evaluate
            agent: Optional agent that will learn from the evaluation
            custom_metrics: Optional dictionary of custom metrics and their descriptions
            evaluation_function: Optional custom function to evaluate responses
        """
        self.prompt = prompt
        self.response = response
        self.agent = agent
        self.evaluation_function = evaluation_function
        
        # Default evaluation metrics
        self.evaluation_metrics = [
            "Correctness",
            "Relevance",
            "Coherence",
            "Factual Consistency",
            "Completeness",
            "Conciseness",
        ]
        
        self.metric_descriptions = {
            "Correctness": "Is the response correct and accurate?",
            "Relevance": "Is the response on-topic and useful for the prompt?",
            "Coherence": "Is the response logically structured and readable?",
            "Factual Consistency": "Is the response factually correct (especially for knowledge-based tasks)?",
            "Completeness": "Does it cover all necessary points relevant to the prompt?",
            "Conciseness": "Does it avoid unnecessary fluff while being informative?",
        }
        
        # Add custom metrics if provided
        if custom_metrics:
            for metric, description in custom_metrics.items():
                if metric not in self.evaluation_metrics:
                    self.evaluation_metrics.append(metric)
                    self.metric_descriptions[metric] = description
        
        # Initialize evaluation results structure
        self.evaluation_results = {
            "is_correct": False,  # Overall correctness usually calculated if avg_score > 0.7
            "evaluation_metrics": {},
            "chain_of_thought": [],
            "feedback": "",
        }
        
        # Configure logging
        self.logger = logging.getLogger("llm_judge")
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)

    def evaluate(self) -> Dict[str, Any]:
        """
        Evaluate the response against all metrics and generate feedback.
        
        Returns:
            A dictionary containing evaluation results
        """
        self.logger.info(f"Starting evaluation for prompt: {self.prompt[:50]}...")
        
        # If a custom evaluation function was provided, use it
        if self.evaluation_function:
            try:
                custom_results = self.evaluation_function(self.prompt, self.response)
                if isinstance(custom_results, dict):
                    self.evaluation_results.update(custom_results)
                    return self.evaluation_results
            except Exception as e:
                self.logger.error(f"Custom evaluation function failed: {str(e)}")
                # Fall back to standard evaluation
        
        # Standard evaluation process
        metrics_sum = 0
        for metric in self.evaluation_metrics:
            score = self.judge_metric(metric)
            self.evaluation_results['evaluation_metrics'][metric] = score
            metrics_sum += score
        
        # Calculate overall correctness based on average of metrics
        # A response is considered correct if the average score is above 0.7
        avg_score = metrics_sum / len(self.evaluation_metrics)
        self.evaluation_results['is_correct'] = avg_score > 0.7
        
        # Generate detailed feedback and reasoning
        self.evaluation_results['chain_of_thought'] = self.generate_chain_of_thought()
        self.evaluation_results['feedback'] = self.generate_feedback()
        
        # If an agent is provided, let it learn from these results
        if self.agent:
            self.agent.learn(self.evaluation_results)
        
        self.logger.info(f"Evaluation complete. Overall correctness: {self.evaluation_results['is_correct']}")
        return self.evaluation_results

    def judge_metric(self, metric: str) -> float:
        """
        Judge the response based on a specific metric.
        
        In a real implementation, this would call an LLM to evaluate the response.
        
        Args:
            metric: The metric to evaluate
            
        Returns:
            A score between 0 and 1
        """
        # This is where you would integrate with your LLM to do the actual evaluation
        # For now, we'll implement a simple heuristic-based evaluation
        
        # This is a simplified placeholder implementation
        # In a real system, you would call your LLM here
        
        description = self.metric_descriptions[metric]
        self.logger.debug(f"Evaluating {metric}: {description}")
        
        if metric == "Relevance":
            # Check if response contains keywords from the prompt
            relevance_score = self._calculate_relevance()
            return relevance_score
            
        elif metric == "Completeness":
            # For demonstration, check if response length is appropriate
            if len(self.response) < 20:
                return 0.3  # Too short
            elif len(self.response) > 500:
                return 0.8  # Likely comprehensive
            else:
                return 0.6  # Medium length
                
        elif metric == "Conciseness":
            # Inverse of verbosity
            words = len(self.response.split())
            if words < 15:
                return 0.9  # Very concise
            elif words > 100:
                return 0.4  # Not very concise
            else:
                return 0.7  # Moderately concise
                
        # For other metrics, we would need more sophisticated evaluation logic
        # This is where integration with your LLM would be crucial
        
        # Placeholder score - in a real implementation, this would be calculated
        return 0.5
    
    def _calculate_relevance(self) -> float:
        """Calculate relevance score based on keyword matching."""
        prompt_words = set(self.prompt.lower().split())
        response_words = set(self.response.lower().split())
        
        # Remove common stop words
        stop_words = {"the", "a", "an", "in", "on", "at", "to", "for", "with", "by"}
        prompt_words = prompt_words - stop_words
        
        # Count matches
        matches = prompt_words.intersection(response_words)
        
        if len(prompt_words) == 0:
            return 0.5
        
        match_ratio = len(matches) / len(prompt_words)
        return min(match_ratio * 1.5, 1.0)  # Scale up but cap at 1.0
    
    def generate_feedback(self) -> str:
        """
        Generate human-readable feedback for the response.
        
        Returns:
            A string containing feedback
        """
        # This is where your LLM would generate structured feedback
        # For now, we'll implement a simple template-based approach
        
        metrics = self.evaluation_results['evaluation_metrics']
        low_metrics = [m for m, score in metrics.items() if score < 0.6]
        high_metrics = [m for m, score in metrics.items() if score > 0.8]
        
        feedback = []
        
        if self.evaluation_results['is_correct']:
            feedback.append("The response is generally good.")
        else:
            feedback.append("The response needs improvement.")
            
        if low_metrics:
            feedback.append(f"Areas needing attention: {', '.join(low_metrics)}.")
            
        if high_metrics:
            feedback.append(f"Strengths: {', '.join(high_metrics)}.")
            
        # Add specific suggestions based on the chain of thought
        cot = self.evaluation_results['chain_of_thought']
        if cot:
            feedback.append("Specific suggestions:")
            for thought in cot[:3]:  # Limit to first 3 thoughts
                if isinstance(thought, str) and thought:
                    feedback.append(f"- {thought}")
        
        return " ".join(feedback)
    
    def generate_chain_of_thought(self) -> List[str]:
        """
        Generate a chain of thought reasoning for the evaluation.
        
        Returns:
            A list of strings containing reasoning steps
        """
        # This is where your LLM would provide detailed reasoning
        # For now, we'll implement a simple rule-based approach
        
        thoughts = []
        metrics = self.evaluation_results['evaluation_metrics']
        
        # Example thought generation based on metrics
        if "Relevance" in metrics and metrics["Relevance"] < 0.5:
            thoughts.append("The response doesn't directly address the user's question about transactions.")
            
        if "Completeness" in metrics and metrics["Completeness"] < 0.6:
            thoughts.append("The response lacks important details about why the user can't access their transactions.")
            
        if self.response.lower().find("contact support") >= 0 and len(self.response) < 100:
            thoughts.append("Simply saying 'Contact support' without context feels dismissive. Users appreciate clear guidance, not a roadblock.")
            
        if "please" in self.response.lower() and "sorry" in self.response.lower():
            thoughts.append("The response uses appropriate politeness markers, which is good for user experience.")
            
        # Add more sophisticated rules here
        
        # If we have no specific thoughts, add a generic one
        if not thoughts:
            thoughts.append("The response could be improved by providing more specific guidance to the user.")
        
        return thoughts
    
    def to_json(self) -> str:
        """
        Convert the evaluation results to a JSON string.
        
        Returns:
            A JSON string representation of the evaluation results
        """
        return json.dumps(self.evaluation_results, indent=2)
    
    def from_json(self, json_str: str) -> None:
        """
        Load evaluation results from a JSON string.
        
        Args:
            json_str: A JSON string containing evaluation results
        """
        try:
            self.evaluation_results = json.loads(json_str)
        except json.JSONDecodeError as e:
            self.logger.error(f"Error decoding JSON: {str(e)}")


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
            # This assumes the LLM follows instructions and includes "SCORE: X.X" in its response
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
    
    def generate_chain_of_thought(self) -> List[str]:
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


# Example API client class for using with LLMJudge
class LLMClient:
    """
    A simple client for making calls to an LLM API.
    This is just a template - implement according to your specific LLM API.
    """
    def __init__(self, api_key: str, model: str = "default"):
        self.api_key = api_key
        self.model = model
    
    def generate(self, prompt: str, system_prompt: Optional[str] = None) -> Any:
        """
        Generate a response from the LLM.
        
        Args:
            prompt: The prompt to send
            system_prompt: Optional system prompt
            
        Returns:
            The LLM's response
        """
        # This is where you would implement the API call to your LLM
        # For example, using OpenAI's API or Anthropic's API
        
        # Example implementation (not functional):
        """
        import openai
        openai.api_key = self.api_key
        
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        messages.append({"role": "user", "content": prompt})
        
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=messages
        )
        
        return response.choices[0].message.content
        """
        
        # For demonstration, return a mock response
        class MockResponse:
            def __init__(self, text):
                self.text = text
        
        return MockResponse(f"This is a mock LLM response. SCORE: 0.7")


# Example of how to use the library
def example_usage():
    # Example prompt and response
    prompt = "Can I have a list of all my transactions?"
    response = "Sorry I can't do that. Please contact support."
    
    # Create a basic judge
    judge = Judge(prompt, response)
    results = judge.evaluate()
    print(json.dumps(results, indent=2))
    
    # Create an LLM-based judge (if you have an API client)
    # llm_client = LLMClient(api_key="your_api_key")
    # llm_judge = LLMJudge(prompt, response, llm_client=llm_client)
    # llm_results = llm_judge.evaluate()
    # print(json.dumps(llm_results, indent=2))

if __name__ == "__main__":
    example_usage()