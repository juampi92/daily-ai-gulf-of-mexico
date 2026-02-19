#!/usr/bin/env python3
"""
Integration Smoke Test for LLM providers.
This test calls each configured LLM once to ensure the code and LLM integration are working.
"""

import os
import sys
import unittest
import traceback
from typing import Dict, Any

# Add current directory to path so we can import from local modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from generate_llm_responses import MODELS, get_model_response, QUESTION, SYSTEM_PROMPT
except ImportError as e:
    print(f"Error importing modules: {e}")
    sys.exit(1)

class TestLLMIntegration(unittest.TestCase):
    def test_all_models(self):
        """
        Integration test that calls each configured LLM once.
        Ensures the code and LLM integration are working.
        """
        print(f"\n=== Starting LLM Integration Smoke Test ===")
        print(f"Question: {QUESTION}")

        failures = []
        successes = []

        # We want to test all models defined in MODELS
        for provider, model_info in MODELS.items():
            if provider.startswith("#"):
                continue

            print(f"\n--- Testing provider: {provider} ---")
            env_var = model_info.get("env_var")
            model_name = model_info.get("name")

            # Check if environment variable is set
            api_key = os.environ.get(env_var)
            if not api_key:
                print(f"ERROR: Missing environment variable {env_var} for {provider}")
                failures.append({
                    "provider": provider,
                    "model": model_name,
                    "error": f"Missing environment variable: {env_var}",
                    "details": f"The API key for {provider} is not set in the environment ({env_var})."
                })
                continue

            try:
                # Get the response
                print(f"Calling {provider} ({model_name})...")
                response = get_model_response(provider, model_info, QUESTION, SYSTEM_PROMPT)

                answer = response.get("answer")
                model_used = response.get("model")

                print(f"Model used: {model_used}")
                print(f"Response: {answer}")

                if not answer:
                    raise ValueError("Empty response received from the model.")

                if not isinstance(answer, str):
                    raise ValueError(f"Response is not a string. Type: {type(answer)}")

                if len(answer.strip()) == 0:
                    raise ValueError("Response consists only of whitespace.")

                print(f"SUCCESS: {provider} responded correctly.")
                successes.append({
                    "provider": provider,
                    "model": model_used,
                    "answer_preview": answer[:50] + "..." if len(answer) > 50 else answer
                })

            except Exception as e:
                error_msg = str(e)
                stack_trace = traceback.format_exc()
                print(f"FAILURE: {provider} failed.")
                print(f"Error: {error_msg}")

                failures.append({
                    "provider": provider,
                    "model": model_name,
                    "error": error_msg,
                    "stack_trace": stack_trace,
                    "model_info": model_info
                })

        print(f"\n=== Test Summary ===")
        print(f"Successes: {len(successes)}")
        print(f"Failures: {len(failures)}")

        if failures:
            error_report = "\n" + "="*50 + "\n"
            error_report += "INTEGRATION TEST FAILURES REPORT"
            error_report += "\n" + "="*50 + "\n"

            for f in failures:
                error_report += f"\n[PROVIDER]: {f['provider']}\n"
                error_report += f"[MODEL]: {f['model']}\n"
                error_report += f"[ERROR]: {f['error']}\n"
                if "details" in f:
                    error_report += f"[DETAILS]: {f['details']}\n"
                if "stack_trace" in f:
                    error_report += f"[STACK TRACE]:\n{f['stack_trace']}\n"
                error_report += "-"*50 + "\n"

            self.fail(error_report)
        else:
            print("\nAll integration tests passed successfully!")

if __name__ == "__main__":
    unittest.main()
