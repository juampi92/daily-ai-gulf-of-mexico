#!/usr/bin/env python3
"""
Google Model Interface

This module provides a function to send requests to Google's models.
"""

import os
from typing import Dict, Any, Optional, Tuple, Union
import json
import logging

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema.messages import SystemMessage, HumanMessage

# Disable httpx logging
logging.getLogger("httpx").setLevel(logging.WARNING)

def ask(model: str, system_prompt: str, prompt: str) -> Tuple[str, str]:
    """
    Send a request to a Google model and return the response.
    
    Args:
        model: The model name (e.g., "gemini-1.5-pro")
        system_prompt: The system prompt to provide context
        prompt: The user prompt/question
        
    Returns:
        Tuple containing:
            - The model's response as a string
            - The actual model used (as resolved by the API)
    """

    # Create the ChatGoogleGenerativeAI instance
    chat = ChatGoogleGenerativeAI(
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
        
        model_used = model
        
        return result, model_used
    except Exception as e:
        print(f"Error with Google request: {e}")
        raise e
