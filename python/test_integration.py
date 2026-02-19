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
    from generate_llm_responses import generate, MODELS, QUESTION
except ImportError as e:
    print(f"Error importing modules: {e}")
    sys.exit(1)

class TestLLMIntegration(unittest.TestCase):
    def test_all_models(self):
        """
        Integration test that calls all configured LLMs using generate().
        Ensures the code and LLM integration are working.
        """
        print(f"\n=== Starting LLM Integration Smoke Test ===")
        print(f"Question: {QUESTION}")

        # Call generate with include_errors=True to get all results
        print("Calling generate_llm_responses.generate(include_errors=True)...")
        results = generate(include_errors=True)

        failures = []
        successes = []

        # Get list of expected providers (those not commented out)
        expected_providers = [p for p in MODELS if not p.startswith("#")]
        received_providers = [r["llm"] for r in results]

        # Check for missing providers
        for provider in expected_providers:
            if provider not in received_providers:
                failures.append({
                    "provider": provider,
                    "model": MODELS[provider].get("name"),
                    "error": "Provider not found in results",
                    "details": "The provider was expected but not returned by generate()."
                })

        # Process received results
        for result in results:
            provider = result.get("llm")
            model_name = result.get("model")

            print(f"\n--- Result for provider: {provider} ---")

            if "error" in result:
                print(f"FAILURE: {provider} failed.")
                print(f"Error: {result['error']}")
                failures.append(result)
            else:
                answer = result.get("answer")
                print(f"Model used: {model_name}")
                print(f"Response: {answer}")

                try:
                    if not answer:
                        raise ValueError("Empty response received from the model.")

                    if not isinstance(answer, str):
                        raise ValueError(f"Response is not a string. Type: {type(answer)}")

                    if len(answer.strip()) == 0:
                        raise ValueError("Response consists only of whitespace.")

                    print(f"SUCCESS: {provider} responded correctly.")
                    successes.append({
                        "provider": provider,
                        "model": model_name,
                        "answer_preview": answer[:50] + "..." if len(answer) > 50 else answer
                    })
                except Exception as e:
                    print(f"FAILURE: {provider} failed validation.")
                    failures.append({
                        "llm": provider,
                        "model": model_name,
                        "error": str(e),
                        "stack_trace": traceback.format_exc()
                    })

        print(f"\n=== Test Summary ===")
        print(f"Successes: {len(successes)}")
        print(f"Failures: {len(failures)}")

        if failures:
            error_report = "\n" + "="*50 + "\n"
            error_report += "INTEGRATION TEST FAILURES REPORT"
            error_report += "\n" + "="*50 + "\n"

            for f in failures:
                error_report += f"\n[PROVIDER]: {f.get('llm') or f.get('provider')}\n"
                error_report += f"[MODEL]: {f.get('model')}\n"
                error_report += f"[ERROR]: {f.get('error')}\n"
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
