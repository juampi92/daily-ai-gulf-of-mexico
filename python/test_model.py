#!/usr/bin/env python3
"""
Test a single LLM model from the command line.

Usage:
    uv run python/test_model.py <vendor> [-v]

Examples:
    uv run test_model.py anthropic
    uv run test_model.py openai -v
    uv run test_model.py google --verbose

Available vendors: openai, anthropic, google, xai
"""

import sys
import os
import argparse
import logging

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv

# Load .env from project root (one level up from this script)
load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".env"))

from generate_llm_responses import MODELS, QUESTION, SYSTEM_PROMPT, get_model_response
from evaluator import evaluate

# Configure logging for verbose mode
logging.basicConfig(
    level=logging.DEBUG,
    format='%(levelname)s: %(message)s'
)


def test_model(vendor: str, verbose: bool = False) -> bool:
    """Test a single model vendor."""

    # Normalize vendor name
    vendor = vendor.lower()

    # Validate vendor
    if vendor not in MODELS:
        available = ", ".join(MODELS.keys())
        print(f"❌ Unknown vendor: {vendor}")
        print(f"Available vendors: {available}")
        return False

    model_info = MODELS[vendor]
    model_name = model_info["name"]

    print(f"\n🧪 Testing {vendor}/{model_name}")
    print(f"Question: {QUESTION}\n")

    if not verbose:
        # Suppress debug logs unless verbose
        logging.getLogger().setLevel(logging.WARNING)

    try:
        # Get response
        response = get_model_response(vendor, model_info, QUESTION, SYSTEM_PROMPT)
        answer = response["answer"]
        model_used = response["model"]

        # Evaluate
        is_correct = evaluate(answer)

        # Display results
        print(f"Answer: {answer}")
        print(f"Model: {model_used}")
        status = "✅ PASS" if is_correct else "❌ FAIL"
        print(f"Status: {status}")

        if verbose:
            print(f"\n[DEBUG] Full response object:")
            print(f"  - Vendor: {vendor}")
            print(f"  - Correct: {is_correct}")

        return is_correct

    except Exception as e:
        print(f"❌ Error: {e}")
        if verbose:
            import traceback
            print("\n[DEBUG] Full traceback:")
            traceback.print_exc()
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Test a single LLM model",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Available vendors: " + ", ".join(MODELS.keys())
    )

    parser.add_argument(
        "vendor",
        help="LLM vendor to test (e.g., anthropic, openai, google, xai)"
    )

    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Show full API request/response and debug info"
    )

    args = parser.parse_args()

    success = test_model(args.vendor, args.verbose)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
