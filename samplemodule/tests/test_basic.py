# -*- coding: utf-8 -*-

import context
import samplemodule

import unittest

class BasicTestSuite(unittest.TestCase):
    """Basic test cases."""
    
    def setUp(self):
        pass
        
    def tearDown(self):
        pass
        
    def test_absolute_truth_and_meaning(self):
        self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()
