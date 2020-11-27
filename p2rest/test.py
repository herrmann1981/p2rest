import os
import unittest


if __name__ == '__main__':
    tests = unittest.TestLoader().discover('test', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        exit(0)
    exit(1)
