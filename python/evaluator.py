#!/usr/bin/env python3
"""
Simple LLM Response Evaluator

This module provides a function to evaluate LLM responses for accuracy.
"""

import re
from typing import Any

def evaluate(answer: Any) -> bool:
    """
    Evaluate if the answer is correct for the Gulf of Mexico question.
    
    Args:
        answer: The answer to evaluate (can be a string or other types from LLM)
        
    Returns:
        True if the answer is correct, False otherwise
    """
    if not answer:
        return False
    
    # Robustly handle non-string content (common in some providers/versions)
    if not isinstance(answer, str):
        if isinstance(answer, (list, tuple)):
            # Join blocks into a single string
            parts = []
            for block in answer:
                if isinstance(block, str):
                    parts.append(block)
                elif isinstance(block, dict):
                    parts.append(block.get("text", ""))
                elif hasattr(block, "text"):
                    parts.append(block.text)
                elif hasattr(block, "content"):
                    parts.append(block.content)
                else:
                    parts.append(str(block))
            answer = "".join(parts)
        else:
            answer = str(answer)

    # Convert to lowercase for case-insensitive matching
    answer_lower = answer.lower()
    
    # Check if it contains the word "mexico" or "méxico", or "california", AND not the word "america"
    if ("mexico" in answer_lower or "méxico" in answer_lower or "california" in answer_lower) and "america" not in answer_lower:
        return True
    
    return False
