from typing import Dict, Optional, Callable

from typing import TypedDict

class EvaluationResult(TypedDict):
    score: float
    metric: Dict[str, float]
    chain_of_thought: str
    feedback: str

class SelfRefineResult(TypedDict):
    new_response: str
    prompt: str
    llm_response: str
    evaluation: EvaluationResult

class Judge_new:
    def __init__(self, description: str, model: str, custom_metrics: Optional[Dict[str, str]] = None, evaluation_function: Optional[Callable] = None):
        self.description = description
        self.model = model
        self.custom_metrics = custom_metrics
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
        


    def self_refine(self, prompt: str, response: str) -> SelfRefineResult:
        """
        Refines the response based on the evaluation results.
        
        Args:
            prompt: The original prompt
            response: The LLM's response to evaluate
            
        Returns:
            A dictionary containing the refined response and the evaluation results
        """
        
        
        
        
        
        # Implement self-refinement logic here
        # This is a placeholder implementation
        return {
            "new_response": "I'm sorry, but you don't have permission to access your transactions, you can try to contact support, or try to access your transactions via the account settings. you want me to guide you through the process?",
            "prompt": "Can I have a list of all my transactions?",
            "llm_response": "I'm sorry, but you don't have permission to access your transactions",
            "evaluation": {
                "score": 0.3,
                "metric": {
                    "Correctness": 0.3,
                    "Relevance": 0.4,
                    "Coherence": 0.1,
                    "Factual Consistency": 0.2,
                    "Completeness": 0.3,
                    "Conciseness": 0.1
                },
                "chain_of_thought": "The user is asking for a list of all their transactions, but the response doesn't provide any information about how to access or view their transactions. The response is incorrect because the user doesn't have permission to access their transactions. The response is not relevant because it doesn't answer the user's question. The response is not coherent because it doesn't follow a logical structure. The response is not factually consistent because it doesn't provide any information about how to access or view their transactions. The response is not complete because it doesn't provide any information about how to access or view their transactions. The response is not concise because it is too long.",
                "feedback": "the response is not enough information, the llm cant access the transactions, but it can guide the user through the process."
            }
        }
        