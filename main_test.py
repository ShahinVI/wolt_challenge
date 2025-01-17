import unittest

def main():
    """
    Entry point for running all tests in the tests directory.
    """
    loader = unittest.TestLoader()
    tests = loader.discover('tests')
    test_runner = unittest.TextTestRunner()
    test_runner.run(tests)

if __name__ == "__main__":
    main()
