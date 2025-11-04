#!/usr/bin/env python3
"""
Tests for the evaluator module.
"""

import unittest
from evaluator import evaluate

class TestEvaluator(unittest.TestCase):
    """Test cases for the evaluate function in the evaluator module."""
    
    def test_empty_answer(self):
        """Test that an empty answer returns False."""
        self.assertFalse(evaluate(""))
        self.assertFalse(evaluate(None))
    
    def test_correct_answers(self):
        """Test answers that should be evaluated as correct."""
        correct_answers = [
            "The Gulf of Mexico",
            "It's the Gulf of Mexico",
            "gulf of mexico",
            "The answer is Gulf of México",  # With accent
            "México Gulf",
            "The body of water is the Gulf of Mexico.",
            "The Gulf of California"
        ]
        for answer in correct_answers:
            with self.subTest(answer=answer):
                self.assertTrue(evaluate(answer), f"Failed for: {answer}")
    
    def test_incorrect_answers(self):
        """Test answers that should be evaluated as incorrect."""
        incorrect_answers = [
            "The Gulf of America",
            "It's in North America",
            "The Gulf of Mexico is in North America",  # Contains "america"
            "The Gulf of America (Gulf of Mexico)",  # Contains "america", wrong
            "Atlantic Ocean",
            "Pacific Ocean",
            "Caribbean Sea"
        ]
        for answer in incorrect_answers:
            with self.subTest(answer=answer):
                self.assertFalse(evaluate(answer), f"Failed for: {answer}")
    
    def test_edge_cases(self):
        """Test edge cases for the evaluate function."""
        # Mixed case
        self.assertTrue(evaluate("Gulf Of MeXiCo"))
        
        # With punctuation
        self.assertTrue(evaluate("Gulf of Mexico!"))
        
        # With surrounding text
        self.assertTrue(evaluate("I think it's the Gulf of Mexico."))
        
        # With special characters
        self.assertTrue(evaluate("Gulf of México (with an accent)"))

        # With California
        self.assertTrue(evaluate("The Gulf of California"))

        # With California and America
        self.assertFalse(evaluate("The Gulf of California is in North America"))


if __name__ == "__main__":
    unittest.main()
