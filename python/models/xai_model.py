#!/usr/bin/env python3
"""
XAI Model Interface

This module provides a function to send requests to XAI's models.
"""

import os
from typing import Dict, Any, Optional, Tuple, Union
import json
import logging

from langchain_xai import ChatXAI
from langchain_core.messages import SystemMessage, HumanMessage

# Disable httpx logging
logging.getLogger("httpx").setLevel(logging.WARNING)

def ask(model: str, system_prompt: str, prompt: str) -> Tuple[str, str]:
    """
    Send a request to a xAI model and return the response.
    
    Args:
        model: The model name (e.g., "grok-2-latest")
        system_prompt: The system prompt to provide context
        prompt: The user prompt/question
        
    Returns:
        Tuple containing:
            - The model's response as a string
            - The actual model used (as resolved by the API)
            - The cost as a float or None if not available
    """
    
    # Create the ChatXAI instance
    chat = ChatXAI(
        model=model,
        temperature=0,
    )
    
    # Create messages
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=prompt)
    ]
    
    # Send the request
    try:
        response = chat.invoke(messages)
        
        # Extract the content
        result = response.content
        
        model_used = response.response_metadata['model_name']
        
        return result, model_used
    except Exception as e:
        print(f"Error with xAI request: {e}")
        raise e
