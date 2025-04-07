import requests
import json
import time
from typing import Callable, Dict, Any, List, Optional
import pandas as pd
from tqdm import tqdm
import logging

# Define version
__version__ = "0.2.1"

# Custom exception classes
class AuthenticationError(Exception):
    """Raised when authentication with the API fails."""
    pass

class EvaluationError(Exception):
    """Raised when there's an error during evaluation."""
    pass

class DatasetError(Exception):
    """Raised when there's an error during dataset loading."""
    pass

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('crm_benchmark_lib')
logger.setLevel(logging.INFO)  # Ensure INFO level is set

class BenchmarkClient:
    """
    Client for the CRM AI Agent Benchmarking API.
    
    This client helps interact with the benchmarking service, allowing users to:
    - Authenticate with the API
    - Load datasets
    - Evaluate agent responses
    - Submit final results to the leaderboard
    """
    
    def __init__(self, api_key: str, base_url: str = "https://aiagentchallenge.com"):
        """
        Initialize the benchmark client.
        
        Args:
            api_key: Your API key for the benchmarking service
            base_url: Base URL for the API (defaults to https://aiagentchallenge.com)
        """
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": f"CRM-AI-Agent-Benchmark-Client/{__version__}",
            "Content-Type": "application/json"
        })
        self.auth_token = None
        self.username = None
        self.datasets = None
        
        logger.info(f"Initialized BenchmarkClient with base URL: {self.base_url}")
    
    def authenticate(self, agent_name: str) -> Dict[str, Any]:
        """
        Authenticate with the API and get available datasets.
        
        Args:
            agent_name: Name of your agent for the benchmark
            
        Returns:
            Dict with authentication status and available datasets
        """
        endpoint = f"{self.base_url}/api/evaluate/authenticate"
        
        payload = {
            "api_key": self.api_key,
            "agent_name": agent_name
        }
        
        logger.info(f"Authenticating agent '{agent_name}'...")
        
        try:
            response = self.session.post(endpoint, json=payload)
            response.raise_for_status()
            response_data = response.json()
            
            if response_data.get("status") == "success":
                self.auth_token = response_data.get("token")
                self.username = response_data.get("username")
                self.datasets = response_data.get("datasets")
                
                logger.info(f"Authentication successful for user: {self.username}")
                logger.info(f"Found {len(self.datasets)} available datasets")
                
                return response_data
            else:
                error_msg = response_data.get("message", "Authentication failed")
                logger.error(f"Authentication error: {error_msg}")
                raise AuthenticationError(f"Authentication failed: {error_msg}")
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Request error during authentication: {str(e)}")
            raise ConnectionError(f"Failed to connect to API: {str(e)}")
    
    def load_dataset(self, dataset_id: str) -> Dict[str, Any]:
        """
        Load a specific dataset for evaluation.
        
        Args:
            dataset_id: ID of the dataset to load (e.g., 'dataset_1')
            
        Returns:
            Dict with dataset information and first question
        """
        if not self.auth_token:
            raise ValueError("Not authenticated. Call authenticate() first.")
        
        endpoint = f"{self.base_url}/api/evaluate/start_dataset"
        
        payload = {
            "token": self.auth_token,
            "dataset_id": dataset_id
        }
        
        logger.info(f"Loading dataset: {dataset_id}...")
        
        try:
            response = self.session.post(endpoint, json=payload)
            response.raise_for_status()
            response_data = response.json()
            
            if response_data.get("status") == "success":
                logger.info(f"Dataset {dataset_id} loaded successfully")
                logger.info(f"Total questions: {response_data.get('total_questions', 'unknown')}")
                
                # Add proper DataFrame conversion
                if "data" in response_data:
                    try:
                        # Convert JSON data to pandas DataFrame
                        data = pd.DataFrame(response_data["data"])
                        # Replace the raw data with the DataFrame
                        response_data["data"] = data
                        
                        # Log DataFrame info
                        logger.info(f"Loaded DataFrame with {data.shape[0]} rows and {data.shape[1]} columns")
                        logger.info(f"DataFrame columns: {data.columns.tolist()}")
                    except Exception as e:
                        logger.error(f"Error converting dataset to DataFrame: {str(e)}")
                        # Keep original data if conversion fails
                        logger.warning("Using original data format instead of DataFrame")
                else:
                    logger.warning("No data found in dataset response")
                
                return response_data
            else:
                error_msg = response_data.get("message", "Failed to load dataset")
                logger.error(f"Dataset load error: {error_msg}")
                raise DatasetError(f"Failed to load dataset: {error_msg}")
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Request error loading dataset: {str(e)}")
            raise ConnectionError(f"Failed to connect to API: {str(e)}")
    
    def evaluate_answer(self, token: str, answer: str) -> Dict[str, Any]:
        """
        Submit an answer for evaluation and get the next question.
        
        Args:
            token: Current question token
            answer: Agent's answer to the question
            
        Returns:
            Dict with evaluation results and next question (if available)
        """
        endpoint = f"{self.base_url}/api/evaluate/submit_answer"
        
        payload = {
            "token": token,
            "answer": answer
        }
        
        try:
            response = self.session.post(endpoint, json=payload)
            response.raise_for_status()
            response_data = response.json()
            
            if response_data.get("status") == "success":
                return response_data
            else:
                error_msg = response_data.get("message", "Answer evaluation failed")
                logger.error(f"Evaluation error: {error_msg}")
                raise EvaluationError(f"Answer evaluation failed: {error_msg}")
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Request error during answer evaluation: {str(e)}")
            raise ConnectionError(f"Failed to connect to API: {str(e)}")
    
    def complete_dataset(self, token: str, score: float = 0) -> Dict[str, Any]:
        """
        Complete evaluation for a dataset and get a completion token.
        
        Args:
            token: Token from the last question
            score: The score to record for this dataset
            
        Returns:
            Dict with completion token and status
        """
        endpoint = f"{self.base_url}/api/evaluate/complete_dataset"
        
        payload = {
            "token": token,
            "score": score
        }
        
        try:
            response = self.session.post(endpoint, json=payload)
            response.raise_for_status()
            response_data = response.json()
            
            if response_data.get("status") == "success":
                logger.debug(f"Received completion token response: {json.dumps(response_data)}")
                completion_token = response_data.get("completion_token")
                all_completed = response_data.get("all_datasets_completed", False)
                if all_completed:
                    logger.info("All datasets have been completed. Results have been recorded on the leaderboard.")
                
                return {
                    "status": "success",
                    "completion_token": completion_token,
                    "all_datasets_completed": all_completed
                }
            else:
                error_msg = response_data.get("message", "Dataset completion failed")
                logger.error(f"Dataset completion error: {error_msg}")
                raise EvaluationError(f"Dataset completion failed: {error_msg}")
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Request error during dataset completion: {str(e)}")
            raise ConnectionError(f"Failed to connect to API: {str(e)}")
    
    def submit_results(self, agent_name, completion_tokens, simplified_mode=False):
        """
        DEPRECATED: Direct submission has been disabled for security reasons.
        
        Results are now automatically recorded by the server during evaluation.
        No manual submission is needed or permitted to ensure a fair competition.
        """
        logging.warning(
            "Direct submission through the client has been disabled for security reasons. "
            "Your results are automatically recorded by the server during evaluation."
        )
        # Return a placeholder response indicating the security policy
        return {
            "status": "info",
            "message": "Direct submission is not allowed. Your results have been securely recorded by the server during evaluation.",
            "details": "This ensures fair competition and prevents score manipulation."
        }

    def evaluate_dataset(
        self, 
        dataset_id: str, 
        agent_callable: Callable[[str, pd.DataFrame], str],
        simplified_mode: bool = True
    ) -> Dict[str, Any]:
        """
        Evaluate a single dataset using the provided agent callable.
        
        Args:
            dataset_id: ID of the dataset to evaluate
            agent_callable: Function that takes (question, dataframe) and returns answer
            simplified_mode: Use simplified output with less verbose logging
            
        Returns:
            Dict with dataset evaluation results and completion token
        """
        # Set logging level based on mode
        original_level = logger.level
        if simplified_mode:
            logger.setLevel(logging.WARNING)  # Reduce logging in simplified mode
            
        try:
            # Load dataset
            dataset_info = self.load_dataset(dataset_id)
            
            # Get the question - check both "question" and "question_text" fields
            question = dataset_info.get("question", "") or dataset_info.get("question_text", "")
            if not question:
                logger.warning(f"Question is empty. Available keys: {dataset_info.keys()}")
            
            question_id = dataset_info.get("question_id", 0)
            total_questions = dataset_info.get("total_questions", 0)
            token = dataset_info.get("token")
            
            # Parse data into DataFrame
            try:
                data = pd.DataFrame(dataset_info.get("data", []))
            except Exception as e:
                if not simplified_mode:
                    logger.error(f"Error parsing dataset: {str(e)}")
                else:
                    print(f"Error parsing dataset: {str(e)}")
                data = pd.DataFrame()
            
            # Initialize progress bar
            progress_bar = tqdm(total=total_questions, desc=f"Dataset {dataset_id}", disable=simplified_mode)
            progress_bar.update(question_id)
            
            # Track scores
            scores = []
            
            # Process all questions
            while True:
                try:
                    # Get agent's answer
                    answer = agent_callable(question, data)
                    
                    # Ensure answer is a string
                    if not isinstance(answer, str):
                        answer = str(answer)
                    
                    # Submit answer for evaluation
                    result = self.evaluate_answer(token, answer)
                    
                    # Update progress
                    score = result.get("score", 0)
                    scores.append(score)
                    
                    explanation = result.get("explanation", "")
                    if not simplified_mode:
                        logger.debug(f"Question {question_id+1} result: {score}/100 - {explanation}")
                    
                    # Check if dataset is complete
                    if result.get("is_complete", False):
                        progress_bar.update(1)
                        break
                    
                    # Get next question - check both fields
                    question = result.get("next_question", "") or result.get("question_text", "")
                    question_id = result.get("question_id", question_id + 1)
                    token = result.get("token")
                    
                    # Update progress bar
                    progress_bar.update(1)
                    
                    # Show a simple progress indicator in simplified mode
                    if simplified_mode and total_questions > 0:
                        print(f"  Progress: {question_id}/{total_questions} questions", end="\r")
                    
                except Exception as e:
                    if not simplified_mode:
                        logger.error(f"Error during dataset evaluation: {str(e)}")
                    else:
                        print(f"Error during evaluation: {str(e)}")
                    progress_bar.close()
                    raise
            
            progress_bar.close()
            
            # Show 100% progress at the end in simplified mode
            if simplified_mode and total_questions > 0:
                print(f"  Progress: {total_questions}/{total_questions} questions completed")
            
            # Get completion token
            completion_response = self.complete_dataset(token, score)
            completion_token = completion_response.get("completion_token")
            
            # Calculate average score
            avg_score = sum(scores) / len(scores) if scores else 0
            
            if not simplified_mode:
                logger.info(f"Dataset {dataset_id} evaluation complete")
                logger.info(f"Average score: {avg_score:.2f}/100")
            
            return {
                "dataset_id": dataset_id,
                "completion_token": completion_token,
                "scores": scores,
                "average_score": avg_score
            }
        finally:
            # Restore original logging level
            logger.setLevel(original_level)
    
    def run_and_submit(self, agent_callable, agent_name, simplified_mode=False):
        """
        Run the agent through the evaluation process and record results securely.
        
        Args:
            agent_callable: Function that takes (question, data) and returns an answer
            agent_name: Name to identify the agent
            simplified_mode: Whether to use the simplified mode for the API
            
        Returns:
            dict: Final result with dataset scores
        """
        # Initialize results
        completion_tokens = []
        dataset_results = {}
        
        # Authenticate
        auth_response = self.authenticate(agent_name)
        if not auth_response.get("status") == "success":
            raise AuthenticationError(f"Authentication failed: {auth_response.get('message', 'Unknown error')}")
        
        logging.info("Running evaluation on 5 datasets...")
        
        # Evaluate each dataset
        for dataset in auth_response.get("datasets", []):
            dataset_id = dataset.get("id")
            print(f"Dataset {dataset_id.split('_')[1]}/5: {dataset_id}")
            
            # Start dataset evaluation
            dataset_response = self.load_dataset(dataset_id)
            if not dataset_response.get("status") == "success":
                error_msg = dataset_response.get("message", "Unknown error")
                logging.error(f"Failed to start dataset {dataset_id}: {error_msg}")
                raise EvaluationError(f"Failed to start dataset {dataset_id}: {error_msg}")
            
            # Process each question
            total_questions = dataset_response.get("total_questions", 0)
            current_token = dataset_response.get("token")
            data = dataset_response.get("data", [])
            
            current_question = 0
            while True:
                current_question += 1
                print(f"  Progress: {current_question}/{total_questions} questions", end="\r")
                
                # Get the question - check both "question" and "question_text" fields
                question = dataset_response.get("question", "") or dataset_response.get("question_text", "")
                if not question:
                    logging.warning(f"Question is empty: {dataset_response.keys()}")
                
                # Let the agent answer the question
                answer = agent_callable(question, data)
                
                # Submit the answer
                answer_response = self.evaluate_answer(current_token, answer)
                if not answer_response.get("status") == "success":
                    error_msg = answer_response.get("message", "Unknown error")
                    logging.error(f"Failed to submit answer: {error_msg}")
                    raise EvaluationError(f"Failed to submit answer: {error_msg}")
                
                # Check if we're done with this dataset
                if answer_response.get("is_complete", False):
                    print(f"  Progress: {total_questions}/{total_questions} questions completed")
                    score = answer_response.get("score", 0)
                    print(f"  Score: {score:.2f}/100")
                    
                    # Complete the dataset (this securely records the results on the server)
                    completion_response = self.complete_dataset(current_token, score)
                    
                    # Check if all datasets have been completed
                    if completion_response.get("all_datasets_completed", False):
                        print("  All datasets completed! Results have been recorded on the leaderboard.")
                        current_score = completion_response.get("current_score", 0)
                        print(f"  Overall Score: {current_score:.2f}/100")
                    else:
                        datasets_completed = completion_response.get("datasets_completed", 0)
                        print(f"  Progress: {datasets_completed}/5 datasets completed.")
                    
                    completion_tokens.append(completion_response.get("completion_token"))
                    dataset_results[dataset_id] = score
                    break
                
                # Get the next question
                dataset_response = {
                    "question": answer_response.get("next_question", "") or answer_response.get("question_text", ""),
                    "token": answer_response.get("token"),
                    "data": data,
                    "total_questions": total_questions
                }
                current_token = answer_response.get("token")
        
        # Inform the user that results are automatically recorded by the server
        print("Evaluation complete. Results have been securely recorded by the server.")
        if len(dataset_results) == 5:
            print("Your agent has been successfully added to the leaderboard.")
            overall_score = sum(dataset_results.values()) / len(dataset_results)
            print(f"Overall Score: {overall_score:.2f}/100")
            print("You can view your results on the leaderboard at https://aiagentchallenge.com/leaderboard")
        else:
            print(f"Note: Only {len(dataset_results)} of 5 datasets were completed.")
            print("To appear on the public leaderboard, you must complete all 5 datasets.")
            print("Partial results are stored and will be updated when you complete remaining datasets.")
        
        # Return results summary but don't attempt to submit
        return {
            "status": "success",
            "message": "Evaluation complete. Results securely recorded.",
            "agent_name": agent_name,
            "dataset_results": dataset_results,
            "overall_score": sum(dataset_results.values()) / len(dataset_results) if dataset_results else 0,
            "datasets_completed": len(dataset_results)
        }
    
    def submit_scores_directly(self, agent_name: str, scores: Dict[str, float]) -> Dict[str, Any]:
        """
        Submit scores directly to the API (should only be used by admins for testing).
        This method is for admin/testing use only and won't work for normal users.
        
        Args:
            agent_name: Name of your agent
            scores: Dictionary mapping dataset_ids to scores (e.g., {"dataset_1": 80.0, ...})
            
        Returns:
            Dict with submission results
        """
        # Ensure all datasets have scores
        required_datasets = [f"dataset_{i}" for i in range(1, 6)]
        for dataset_id in required_datasets:
            if dataset_id not in scores:
                scores[dataset_id] = 0.0
                logger.warning(f"Missing score for {dataset_id}, defaulting to 0.0")
                
        # Calculate overall score
        overall_score = sum(scores.values()) / len(scores)
                
        # Submit directly via the leaderboard API
        endpoint = f"{self.base_url}/submit_agent_score_api"
        
        payload = {
            "api_key": self.api_key,
            "agent_name": agent_name,
            "score": overall_score,
            "dataset_scores": scores
        }
        
        logger.info(f"Attempting direct submission for agent '{agent_name}'...")
        logger.warning("Note: Direct submission is only available to admin users")
        
        try:
            response = self.session.post(endpoint, json=payload)
            response.raise_for_status()
            response_data = response.json()
            
            if response_data.get("status") == "success":
                logger.info("Direct submission successful!")
                return response_data
            else:
                error_msg = response_data.get("message", "Direct submission failed")
                logger.error(f"Submission error: {error_msg}")
                raise ValueError(f"Direct submission failed: {error_msg}")
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Request error during direct submission: {str(e)}")
            raise ConnectionError(f"Failed to connect to API: {str(e)}") 