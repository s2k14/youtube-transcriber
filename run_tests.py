import unittest
import sys
import os

# Create tests directory if it doesn't exist
if not os.path.exists('tests'):
    os.makedirs('tests')
    # Create __init__.py to make the folder a package
    with open('tests/__init__.py', 'w') as f:
        pass

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Discover and run tests
def run_tests():
    # Discover all tests in the tests directory
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover('tests')
    
    # Run tests
    test_runner = unittest.TextTestRunner(verbosity=2)
    result = test_runner.run(test_suite)
    
    # Return non-zero exit code if any tests failed
    if not result.wasSuccessful():
        sys.exit(1)

if __name__ == '__main__':
    print("Running YouTube Transcriber tests...")
    run_tests()
    print("All tests completed.")