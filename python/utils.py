#!/usr/bin/env python3
"""
Utility functions for LLM response processing.
"""

from typing import Any

def ensure_string(content: Any) -> str:
    """
    Robustly convert LLM content (string, list of blocks, etc.) into a single string.

    Args:
        content: The content to convert

    Returns:
        The content as a single string.
    """
    if not content:
        return ""

    if isinstance(content, str):
        return content

    if isinstance(content, (list, tuple)):
        parts = []
        for block in content:
            if isinstance(block, str):
                parts.append(block)
            elif isinstance(block, dict):
                # Handle dictionary blocks, common in some providers
                parts.append(block.get("text", ""))
            elif hasattr(block, "text"):
                # Handle object blocks with a .text attribute
                parts.append(block.text)
            elif hasattr(block, "content"):
                # Handle object blocks with a .content attribute
                parts.append(block.content)
            else:
                parts.append(str(block))
        return "".join(parts)

    return str(content)
