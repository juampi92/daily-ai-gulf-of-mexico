#!/usr/bin/env python3
"""
Simple LLM Response Evaluator

This module provides a function to evaluate LLM responses for accuracy.
"""

import re

def evaluate(answer: str) -> bool:
    """
    Evaluate if the answer is correct for the Gulf of Mexico question.
    
    Args:
        answer: The answer to evaluate
        
    Returns:
        True if the answer is correct, False otherwise
    """
    if not answer:
        return False
    
    # Convert to lowercase for case-insensitive matching
    answer_lower = answer.lower()
    
    # Check if it contains the word "mexico" or "méxico", or "california", AND not the word "america"
    if ("mexico" in answer_lower or "méxico" in answer_lower or "california" in answer_lower) and "america" not in answer_lower:
        return True
    
    return False
