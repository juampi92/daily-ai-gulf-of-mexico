#!/usr/bin/env python3
"""
OpenAI Model Interface

This module provides a function to send requests to OpenAI's models.
"""

import os
from typing import Dict, Any, Optional, Tuple, Union
import json
import logging

from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

from models import DEFAULT_TEMPERATURE

# Disable httpx logging
logging.getLogger("httpx").setLevel(logging.WARNING)

def ask(model: str, system_prompt: str, prompt: str) -> Tuple[str, str]:
    """
    Send a request to an OpenAI model and return the response.
    
    Args:
        model: The model name (e.g., "gpt-4o")
        system_prompt: The system prompt to provide context
        prompt: The user prompt/question
        
    Returns:
        Tuple containing:
            - The model's response as a string
            - The actual model used (as resolved by the API)
    """
    # Create the ChatOpenAI instance
    chat = ChatOpenAI(
        model=model,
        temperature=DEFAULT_TEMPERATURE,
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
        print(f"Error with OpenAI request: {e}")
        raise e
