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

from models import DEFAULT_TEMPERATURE
from utils import ensure_string

# Disable httpx logging
logging.getLogger("httpx").setLevel(logging.WARNING)

def ask(model: str, system_prompt: str, prompt: str) -> Tuple[str, str]:
    """
    Send a request to a xAI model and return the response.
    
    Args:
        model: The model name (e.g., "model-name")
        system_prompt: The system prompt to provide context
        prompt: The user prompt/question
        
    Returns:
        Tuple containing:
            - The model's response as a string
            - The actual model used (as resolved by the API)
            - The cost as a float or None if not available
    """
    
    # Create messages
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=prompt)
    ]
    
    # Send the request
    try:
        try:
            chat = ChatXAI(
                model=model,
                temperature=DEFAULT_TEMPERATURE,
                extra_body={"reasoning_effort": "none"},
            )
            response = chat.invoke(messages)
        except Exception as e:
            if "reasoning_effort" in str(e).lower():
                chat = ChatXAI(
                    model=model,
                    temperature=DEFAULT_TEMPERATURE,
                )
                response = chat.invoke(messages)
            else:
                raise e

        # Extract and robustly handle content
        result = ensure_string(response.content)
        
        model_used = response.response_metadata['model_name']
        
        return result, model_used
    except Exception as e:
        print(f"Error with xAI request: {e}")
        raise e
