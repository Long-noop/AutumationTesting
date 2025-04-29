import unittest
import sys

def main():
    """Main function to run specific or all test cases."""
    if len(sys.argv) > 1:
        test_case = sys.argv[1]
        suite = unittest.TestLoader().loadTestsFromName(f"DDT_Testcase.TestSuite.{test_case}")
    else:
        suite = unittest.TestLoader().discover('.', pattern="DDT_Testcase.py")
    unittest.TextTestRunner(verbosity=2).run(suite)

if __name__ == "__main__":
    main()