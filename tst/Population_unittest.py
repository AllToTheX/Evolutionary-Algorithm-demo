'''
Created on Aug 30, 2016

@author: allexveldman
'''
import unittest
from framework import Population
from deap import base

class Test(unittest.TestCase):

    def testPopulation(self):
        # Instantiation
        pop = Population.Population()
        self.assertIsInstance(pop, Population.Population)
        self.assertIsInstance(pop.toolbox, base.Toolbox)
        self.assertEqual(pop.Individual, None)
        with self.assertRaises(NotImplementedError): pop.toolbox.individual()
        with self.assertRaises(NotImplementedError): pop.toolbox.population(n=10)
        with self.assertRaises(NotImplementedError): pop.toolbox.mutate()
        with self.assertRaises(NotImplementedError): pop.setupToolbox()
        # Default crossover behavior 
        out1, out2 = pop.toolbox.mate([1,2],[5,6])
        out1.extend(out2)
        self.assertIn(1, out1)
        self.assertIn(2, out1)
        self.assertIn(5, out1)
        self.assertIn(6, out1)
        # Default select behavior
        class dummyIndividual(object):
            def __init__(self,value):
                self.fitness = value
        ind1 = dummyIndividual(1)
        ind2 = dummyIndividual(3)
        ind3 = dummyIndividual(2)
        dummypop = [ind1,ind2,ind3]
        dummypop = pop.toolbox.select(dummypop,len(dummypop))
        self.assertEqual(dummypop[0].fitness,3)
        self.assertEqual(dummypop[1].fitness,2)
        self.assertEqual(dummypop[2].fitness,1)
        

#     def testcreateIndividual(self):
#         class Individual(list):
#             def __init__(self):
#                 self.fitness = list()
#                 
#         ind = EA_framework.createIndividual(Individual, (1,), ('+',), (2,))
#         self.assertEqual(ind[0], 1)
#         self.assertEqual(ind[1], '+')
#         self.assertEqual(ind[2], 2)



if __name__ == "__main__":
    unittest.main()