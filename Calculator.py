'''
Created on Sep 26, 2016

@author: allexveldman
'''
import random
import timeit
import multiprocessing
from framework.Population import Population

VAR1 = range(1,99+1)
OPERATORS = ['+','-','x','/']
VAR2 = VAR1

def wrapper(func, *args, **kwargs):
    """ Wrapper for the timeit call """
    def wrapped():
        return func(*args, **kwargs)
    return wrapped 
    
def evaluate(individual, n=1):
    """
    Evaluate the the fitness of our individual by measuring the response time of
    executing calculate().
    This function needs to be outside any class if multiprocessing is being used.
    
    :param individual: individual[0] = var1, individual[1] = operator, individual[2] = var2.
    :param n: number of times to execute calculate() in timeit().
    :returns: responseTime: fitness of calculate() measured in response time [sec].
    """
    from EA_app import calculate
    
    wrapped = wrapper(calculate, *individual)
    responseTime = timeit.timeit(wrapped, number=n) / n # divide by n to get the average time
    
    # If we use multiprocessing we can't edit the individual because of pickle'ing
    # The response time will be added in the main process
    # individual.responseTime = (responseTime)
    return (responseTime,) # Return needs to be a tuple as there can be more than 1 fitness defined.

class CalculatorPopulation(Population):
    '''
    Base class for an individual
    '''
    def __init__(self):
        '''
        Constructor
        '''
        Population.__init__(self)
        self.createBaseClass(inherits=list, weights=(1.0,))
        self.setupToolbox()
             
        
    def create(self):
        """ 
        Create an individual instance to run the application with. 
        :returns: A populated individual
        """
        ind = self.Individual() # Create the instance
        ind.append(random.choice(VAR1)) # Generate a random number for var1
        ind.append(random.choice(OPERATORS)) # pick a random operator
        ind.append(random.choice(VAR2)) # Generate a random number for var2
        return ind
    
    def mutate(self, individual, indpb):
        """
        Mutate an individual by replacing attributes, with probability *indpb*.
        
        :param individual: individual to be mutated.
        :param indpb: Independent probability for each attribute to be mutated.
        :returns: A tuple of one individual.
        """
        size = len(individual)
        posval = (VAR1, OPERATORS, VAR2)
        
        for i, xl in zip(range(size), posval):
            if random.random() < indpb:
                individual[i] = random.choice(xl)
        
        return individual,
    
    def setupToolbox(self):
        '''
        Function to fill the toolbox.
        
        '''
        self.toolbox.register("evaluate", evaluate) # Specify the method to evaluate the individual
        self.toolbox.register("mutate", self.mutate) # specify the method to mutate the individual
        pool = multiprocessing.Pool() # Create a multiprocessing pool to execute a population in parallel
        self.toolbox.register("map", pool.map) # register the multiprocessing pool
        