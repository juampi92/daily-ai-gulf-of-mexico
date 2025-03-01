#!/usr/bin/env python3
"""
CSV Updater for LLM Responses

This script:
1. Uses generate_llm_responses.py to get responses from all LLMs
2. Updates the corresponding CSV files in public/data/ with today's results
3. Outputs information about the update process
"""

import os
import json
import csv
import time
from datetime import datetime
import generate_llm_responses

def update_csv_files():
    """
    Update CSV files with today's LLM responses.
    
    Returns:
        Dict containing update statistics
    """
    start_time = time.time()
    
    # Get today's date in YYYY-MM-DD format
    today = datetime.now().strftime("%Y-%m-%d")
    
    # Get LLM responses
    results = generate_llm_responses.generate()
    
    # Initialize statistics
    stats = {
        "date": today,
        "updated_count": 0,
        "models": []
    }
    
    # Process each result
    for result in results:
        llm = result["llm"]
        model = result["model"]
        answer = result["answer"]
        correct = result["correct"]
        
        # Define the CSV file path
        csv_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                               "public", "data", f"{llm}.csv")
        
        # Check if file exists
        file_exists = os.path.isfile(csv_path)
        
        # Open the CSV file in append mode
        with open(csv_path, mode='a', newline='') as file:
            writer = csv.writer(file)
            
            # Write header if file doesn't exist
            if not file_exists:
                writer.writerow(["date", "answer", "model", "correct"])
            
            # Write the new row
            writer.writerow([today, answer, model, str(correct).lower()])
        
        # Update statistics
        stats["updated_count"] += 1
        stats["models"].append({
            "llm": llm,
            "model": model,
            "correct": correct
        })
    
    # Calculate execution time
    execution_time = time.time() - start_time
    stats["execution_time"] = round(execution_time, 2)
    
    return stats

def main():
    """Main function to run the script."""
    try:
        # Update CSV files
        stats = update_csv_files()
        
        # Print update information
        print(f"\n===== CSV Update Summary ({stats['date']}) =====")
        print(f"Updated {stats['updated_count']} CSV files")
        print(f"Execution time: {stats['execution_time']} seconds")
        
        # Print model-specific information
        print("\nModel details:")
        for model_info in stats["models"]:
            correct_status = "✓" if model_info["correct"] else "✗"
            print(f"  {model_info['llm']} ({model_info['model']}): {correct_status}")
        
        # Return a summary message for commit message
        return (f"Updated {stats['updated_count']} LLM responses on {stats['date']} "
                f"({', '.join([m['llm'] for m in stats['models']])})")
        
    except Exception as e:
        print(f"Error updating CSV files: {e}")
        return f"Error updating CSV files: {e}"

if __name__ == "__main__":
    result_message = main()
    print(f"\nTL;DR: {result_message}")
