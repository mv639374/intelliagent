import argparse
import asyncio
from pathlib import Path
from app.evals.evaluator import main_async # Updated to import the async main
import pandas as pd

def run_evaluation(dataset_name: str):
    print(f"--- Starting RAG Evaluation for dataset: {dataset_name} ---")
    
    # Construct the path to the dataset
    dataset_path = Path(f"scripts/eval-datasets/{dataset_name}.jsonl")
    if not dataset_path.exists():
        print(f"Error: Dataset not found at {dataset_path}")
        return

    # Run the async evaluation
    results = asyncio.run(main_async(dataset_path))
    
    # Print a summary table
    print("\n--- Evaluation Results ---")
    df = pd.DataFrame([results])
    print(df.to_string(index=False))
    print("--------------------------")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run RAG Evaluation.")
    parser.add_argument(
        "--dataset",
        type=str,
        required=True,
        help="The name of the dataset to run (e.g., 'rag_eval')."
    )
    args = parser.parse_args()
    
    run_evaluation(args.dataset)