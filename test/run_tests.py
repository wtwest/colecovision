'''Runs all tests for the coleco emulator'''

import sys
import unittest


def main():
    '''update the path to point to the coleco packages and run all tests'''

    # update the path
    sys.path.append('../')

    # find all of the tests to run
    discovered_suite = unittest.TestLoader().discover('.', pattern='test_*.py')

    # run the tests that were found
    unittest.TextTestRunner(verbosity=1).run(discovered_suite)

if __name__ == '__main__':
    main()