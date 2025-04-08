import json
from typing import Dict, List, Optional, Any, Callable
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
            "is_correct": False,
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
        
        Args:
            metric: The metric to evaluate
            
        Returns:
            A score between 0 and 1
        """
        description = self.metric_descriptions[metric]
        self.logger.debug(f"Evaluating {metric}: {description}")
        
        if metric == "Relevance":
            return self._calculate_relevance()
        elif metric == "Completeness":
            return self._calculate_completeness()
        elif metric == "Conciseness":
            return self._calculate_conciseness()
        
        # For other metrics, we would need more sophisticated evaluation logic
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
        return min(match_ratio * 1.5, 1.0)
    
    def _calculate_completeness(self) -> float:
        """Calculate completeness score based on response length."""
        if len(self.response) < 20:
            return 0.3  # Too short
        elif len(self.response) > 500:
            return 0.8  # Likely comprehensive
        else:
            return 0.6  # Medium length
    
    def _calculate_conciseness(self) -> float:
        """Calculate conciseness score based on word count."""
        words = len(self.response.split())
        if words < 15:
            return 0.9  # Very concise
        elif words > 100:
            return 0.4  # Not very concise
        else:
            return 0.7  # Moderately concise
    
    def generate_feedback(self) -> str:
        """
        Generate human-readable feedback for the response.
        
        Returns:
            A string containing feedback
        """
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
        thoughts = []
        metrics = self.evaluation_results['evaluation_metrics']
        
        # Example thought generation based on metrics
        if "Relevance" in metrics and metrics["Relevance"] < 0.5:
            thoughts.append("The response doesn't directly address the user's question.")
            
        if "Completeness" in metrics and metrics["Completeness"] < 0.6:
            thoughts.append("The response lacks important details.")
            
        if self.response.lower().find("contact support") >= 0 and len(self.response) < 100:
            thoughts.append("Simply saying 'Contact support' without context feels dismissive.")
            
        if "please" in self.response.lower() and "sorry" in self.response.lower():
            thoughts.append("The response uses appropriate politeness markers.")
            
        # If we have no specific thoughts, add a generic one
        if not thoughts:
            thoughts.append("The response could be improved by providing more specific guidance.")
        
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