import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'test_library')))

from test_library import example_function  # Now it should work


class TestMyPackage(unittest.TestCase):
    def test_example_function(self):
        # Test a sample prompt to check the response
        prompt = "What is the capital of France?"
        result = example_function(prompt)
        
        # Test if the result is not empty and is a string
        self.assertIsInstance(result, str)
        self.assertGreater(len(result), 0)

if __name__ == "__main__":
    unittest.main()
