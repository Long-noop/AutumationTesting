import unittest
import sys

def main():
    if len(sys.argv) > 1:
        test_case = sys.argv[1]
        if test_case.startswith("test_case_0"):
            module_name = f"BVA0{test_case[-1]}"  
            suite = unittest.TestLoader().loadTestsFromName(f"{module_name}.TestSuite.{test_case}")
        else:
            print("Invalid test case name. Please use 'test_case_0x' format.")
            return
    else:
        suite = unittest.TestLoader().discover('.', pattern="BVA0*.py")
    unittest.TextTestRunner(verbosity=2).run(suite)

if __name__ == "__main__":
    main()