'''
Created on Sep 26, 2016

@author: allexveldman
'''
from deap import creator, base, tools

class Population(object):
    '''
    Empty class for a population
    '''

    def __init__(self):
        '''
        Constructor, should be overwritten by inheriting class
        '''
        self.Individual = None
        self.toolbox = base.Toolbox()
        self.toolbox.register("individual", self.create) # Specify the method to create an individual @UndefinedVariable
        self.toolbox.register("population", tools.initRepeat, list, self.toolbox.individual) # Specify the method to create the population
        self.toolbox.register("evaluate", self.evaluate) # Specify the method to evaluate the individual
        self.toolbox.register("mate", self.mate) # Specify the method to mate the population
        self.toolbox.register("mutate", self.mutate) # specify the method to mutate the individual
        self.toolbox.register("select", self.select) # Specify the method for selection of the population
        
        
    def createBaseClass(self, inherits=list, weights=(1.0,), *args, **kwargs):
        '''
        Create the base class for the individuals
        '''
        creator.create("FitnessMax", base.Fitness, weights=weights)
        creator.create("Individual", inherits, fitness=creator.FitnessMax, *args, **kwargs)  # @UndefinedVariable
        self.Individual = creator.Individual # @UndefinedVariable
    
    def create(self):
        '''
        Function for creating a single, random individual
        '''
        raise NotImplementedError
    
    def evaluate(self):
        '''
        Function for evaluating a single individual
        When using this function, multiprocessing is no longer possible
        Please consider placing another function outside this class
        '''
        raise NotImplementedError
    
    def select(self,*args,**kwargs):
        '''
        Function for selecting the best individuals
        '''
        return tools.selBest(*args,**kwargs)
    
    def mate(self,*args,**kwargs):
        '''
        Function for mating two individuals
        '''
        return tools.cxTwoPoint(*args,**kwargs)
    
    def mutate(self):
        '''
        Function for mutating a single individual
        '''
        raise NotImplementedError
    
    def setupToolbox(self):
        '''
        Function to fill the toolbox
        '''
        raise NotImplementedError
