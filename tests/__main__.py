import unittest

if __name__ == '__main__':
    loader = unittest.TestLoader()
    tests = loader.discover(start_dir='.', pattern='test_*.py')
    test_runner = unittest.runner.TextTestRunner()
    test_runner.run(tests)
