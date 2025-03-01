#!/usr/bin/env python3
"""
LLM Response Generator

This script:
1. Defines a set of LLMs to test
2. Sends a question to each LLM
3. Returns the responses with model info and correctness
"""

import os
import json
import logging
from typing import Dict, List, Any
from dotenv import load_dotenv

# Import model interfaces
from models import openai_model, anthropic_model, google_model, xai_model

# Import the evaluator
from evaluator import evaluate

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s.%(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# Prevent empty log messages
class NoEmptyFilter(logging.Filter):
    def filter(self, record):
        return bool(record.getMessage().strip())

logger.addFilter(NoEmptyFilter())

# Disable other verbose logging
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("langchain").setLevel(logging.WARNING)
logging.getLogger("langchain_core").setLevel(logging.WARNING)

# The question to ask each LLM
QUESTION = "What is the gulf between America and Mexico called?"

# System prompt to provide context to the LLM
SYSTEM_PROMPT = """Just answer the question to the point. Be concise. Only the answer to the question, and no explanation or extra information else."""

# Define the models to test
MODELS = {
    "openai": {
        "module": openai_model,
        "name": "gpt-4o",
        "env_var": "OPENAI_API_KEY"
    },
    "anthropic": {
        "module": anthropic_model,
        "name": "claude-3-7-sonnet-20250219",
        "env_var": "ANTHROPIC_API_KEY"
    },
    "google": {
        "module": google_model,
        "name": "gemini-1.5-pro",
        "env_var": "GOOGLE_API_KEY"
    },
    "xai": {
        "module": xai_model,
        "name": "grok-2-latest",
        "env_var": "XAI_API_KEY"
    }
}

def get_model_response(provider: str, model_info: Dict[str, Any], question: str, system_prompt: str) -> Dict[str, Any]:
    """
    Get a response from an LLM using the appropriate model module.
    
    Args:
        provider: The LLM provider (openai, anthropic, etc.)
        model_info: Dictionary containing model module, name, and env_var
        question: The question to ask
        system_prompt: The system prompt to provide context
        
    Returns:
        Dictionary containing the response and metadata
    """
    model_name = model_info["name"]
    env_var = model_info["env_var"]
    module = model_info["module"]
    
    # Get API token from environment variables
    if not os.environ.get(env_var):
        raise ValueError(f"API key not found for {provider}. Set the {env_var} environment variable.")
    
    logger.info(f"Sending request to {provider}/{model_name}")

    # Call the ask function from the appropriate module
    # The new return format is (answer, model_used)
    answer, model_used = module.ask(model_name, system_prompt, question)

    return {
        "answer": answer,
        "model": model_used
    }

def generate():
    results = []
    
    # Process each provider and model
    for provider, model_info in MODELS.items():
        # Skip commented out models
        if provider.startswith("#"):
            continue
            
        print(f"\n===== Processing {provider} =====")
        logger.info(f"Processing {provider}")
        
        try:
            # Get the response
            response = get_model_response(provider, model_info, QUESTION, SYSTEM_PROMPT)
            
            # Evaluate the answer using the evaluator
            is_correct = evaluate(response["answer"])
            
            # Add the result
            result = {
                "llm": provider,
                "model": response["model"],
                "answer": response["answer"],
                "correct": is_correct
            }

            results.append(result)
            
        except Exception as e:
            logger.error(f"Error processing {provider}.")
    
    return results
