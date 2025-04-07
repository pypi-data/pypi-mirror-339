"""
Simple example of using the CRM Benchmark Library with a basic agent.
"""

import os
from crm_benchmark_lib import BenchmarkClient
import pandas as pd

# Define a simple agent function
def simple_crm_agent(question, data):
    """
    A very simple agent that demonstrates the interface.
    This agent just returns basic information about the question and data.
    
    Args:
        question: The question to answer
        data: DataFrame containing the CRM data
    
    Returns:
        String answer to the question
    """
    # In a real agent, you would analyze the question and data to generate a response
    
    # Just a simple demonstration
    if isinstance(data, pd.DataFrame):
        num_rows = len(data)
        num_cols = len(data.columns) if hasattr(data, 'columns') else 0
        column_names = list(data.columns) if hasattr(data, 'columns') else []
        
        return f"I received the question: '{question}'. The data has {num_rows} rows and {num_cols} columns: {', '.join(column_names)}."
    else:
        return f"I received the question: '{question}'. No data was provided."

def main():
    # Get API key from environment variable
    api_key = os.environ.get("CRM_BENCHMARK_API_KEY")
    
    if not api_key:
        print("Error: Please set the CRM_BENCHMARK_API_KEY environment variable")
        print("Example: export CRM_BENCHMARK_API_KEY=your_api_key")
        return
    
    # Initialize the client
    client = BenchmarkClient(api_key=api_key)
    
    # Set agent name
    agent_name = "SimpleExampleAgent"
    
    # Run evaluation and submit results
    try:
        print(f"Starting evaluation for {agent_name}...")
        results = client.run_and_submit(
            agent_callable=simple_crm_agent,
            agent_name=agent_name,
            simplified_mode=False  # Set to True for less verbose output
        )
        
        # Print results
        print("\nEvaluation Results:")
        print(f"Status: {results['status']}")
        print(f"Agent: {results['agent_name']}")
        print(f"Overall Score: {results['overall_score']:.2f}/100")
        print(f"Datasets Completed: {results['datasets_completed']}/5")
        
        # Print individual dataset scores
        print("\nDataset Scores:")
        for dataset_id, score in results['dataset_results'].items():
            print(f"  {dataset_id}: {score:.2f}/100")
            
    except Exception as e:
        print(f"Error during evaluation: {str(e)}")

if __name__ == "__main__":
    main() 