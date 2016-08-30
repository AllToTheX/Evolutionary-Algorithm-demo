'''
Created on Aug 30, 2016

@author: allexveldman
'''
import unittest
import EA_framework
import deap

class Test(unittest.TestCase):

    def testToolbox(self):
        toolbox = EA_framework.setupToolbox()
        self.assertIsInstance(toolbox, deap.base.Toolbox)

    def testcreateIndividual(self):
        class Individual(list):
            def __init__(self):
                self.fitness = list()
                
        ind = EA_framework.createIndividual(Individual, (1,), ('+',), (2,))
        self.assertEqual(ind[0], 1)
        self.assertEqual(ind[1], '+')
        self.assertEqual(ind[2], 2)



if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testcreateIndividual']
    unittest.main()