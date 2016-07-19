'''
Created on Jul 16, 2016

@author: allexveldman
'''

import random
import platform
# time.time() on windows returns with second precision so we need time.clock()
# time.clock() on Unix returns processor time of current process so can't be used with multiprocessing
if platform.system() == 'Windows':
    from time import clock as time
else:
    from time import time
import matplotlib.pyplot as plt
import multiprocessing

from deap import base, creator, tools


def evaluateIndividual(individual):
    """ Evaluate the the fitness of our individual by measuring the response time of
    executing calculate()
    
    :param individual: individual[0] = var1, individual[1] = operator, individual[2] = var2.
    :returns: responseTime: fitness of calculate() measured in response time.
    """
    from EA_app import calculate
    start = time()
    
    calculate(*individual) # Function to evaluate, expand individual to parameters
    
    responseTime = time() - start
    
    # If we use multiprocessing we can't edit the individual because of pickle'ing
    # The response time will be added in the main process
#     individual.responseTime = (stop-start)
    return (responseTime,) # Return needs to be a tuple as there can be more than 1 fitness defined.

def createIndividual(individual,low,high):
    """ Created an individual instance to run the application with. 
    
    :param individual: individual (inheriting of type list) to be mutated.
    :param low: lower limit for generating a random integer.
    :param high: higher limit for generating a random integer.
    :returns: A populated individual
    """
    ind = individual() # Create the instance
    ind.append(random.randint(low,high)) # Generate a random number for var1
    ind.append(random.choice(['+','-','x','/'])) # pick a random operator
    ind.append(random.randint(low,high)) # Generate a random number for var2
    return ind

def mutChoiceFromList(individual, lists, indpb, mutrng=(-1,1)):
    """Mutate an individual by replacing attributes, with probability *indpb*,
    by a neighboring value in lists with a range of mutrng.
    
    :param individual: individual to be mutated.
    :param lists: A list of tuples corresponding to the values possible as input for
                the application to test
    :param indpb: Independent probability for each attribute to be mutated.
    :param mutrng: Range of mutation for a single attribute.
    :returns: A tuple of one individual.
    """
    size = len(individual)
    
    for i, xl in zip(xrange(size), lists):
        if random.random() < indpb:
            mutval = random.randint(*mutrng)
            if (xl.index(individual[i]) + mutval) < len(xl):
                individual[i] = xl[ xl.index(individual[i]) + mutval ]
    
    return individual,

def run(toolbox, pop, ngen, cxpb, mutpb):
    """
        Run the evolutionary algorithm.
        
        - First evaluates the first population
        - Loop trough generations:
            - Mates the population with a probability of cxpb
            - Mutates the resulting population with a probability of mutpb
            - Evaluates the new population
            - Plots the best individual and prints the top three
        - Returns the resulting population
        
        :param toolbox: Toolbox containing all needed functions to execute out algorithm.
        :param pop: Initial population to start our algorithm with.
        :param ngen: Number of generations.
        :param cxpb: Crossover probability.
        :param mutpb: Mutate probability.
        :returns: The resulting population
    """
    topOne = list() # Keep score of the top 1 four our plot
    
    # Evaluate the fitness of the initial population
    fitnesses = toolbox.map(toolbox.evaluate, pop)
    for ind, fit in zip(pop, fitnesses):
        ind.fitness.values = fit
        ind.responseTime = fit[0]
    
    # Start the generation loop
    for g in range(ngen):
        # Select the best performing individuals in current population
        pop = toolbox.select(pop, k=len(pop))
        # Clone the population
        pop = [toolbox.clone(ind) for ind in pop]
        # Mate the population with the best 2 individuals
        for child1, child2 in zip(pop[:2], pop[1::2]):
            if random.random() < cxpb: # Probability to mate
                toolbox.mate(child1, child2)
                del child1.fitness.values, child2.fitness.values
        # Mutate the population
        for mutant in pop:
            if random.random() < mutpb:
                toolbox.mutate(mutant)
                del mutant.fitness.values
        
        # Evaluate fitness of the new individuals in the resulting population
        invalids = [ind for ind in pop if not ind.fitness.valid]
        fitnesses = toolbox.map(toolbox.evaluate, invalids)
        for ind, fit in zip(invalids, fitnesses):
            ind.fitness.values = fit
            ind.responseTime = fit[0] # Add response time to individual for plotting
        
        # Select the top 3 of current population for printing
        topThree = tools.selBest(pop, k=3)
        # Add the winner of this population to the plot
        topOne.append(topThree[0])
        
        # Expand the plot with the new winner
        plt.plot([item.responseTime for item in topOne],'b-')
        plt.pause(0.05)
        
        # Print the top 3 for this population
        print("Generation %d" % g)
        for index, item in enumerate(topThree):
            print( "#%d: %E %s" % (index, item.responseTime, str(item)))
        print ('\n')
    
    return pop # Return the resulting population

def setupToolbox():
    """ Fill the toolbox needed for applying our algorithm """
    # Mutate_list holds the possible values to mutate to
    # Values need to be generated beforehand because we reference the index of a value during mutation
    low, high = 1, 99
    mutate_list = ( range(low,high+1),
                ['+','-','x','/'],
                range(low,high+1) )
    
    # Create the base class for the individuals
    creator.create("FitnessMax", base.Fitness, weights=(1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMax, responseTime=0.0)
    
    # Register the toolkit to work with
    toolbox = base.Toolbox()
    toolbox.register("individual", createIndividual, creator.Individual, low, high) # Specify the method to create an individual
    toolbox.register("population", tools.initRepeat, list, toolbox.individual) # Specify the method to create the population
    toolbox.register("evaluate", evaluateIndividual) # Specify the method to evaluate the individual
    toolbox.register("mate", tools.cxTwoPoint) # Specify the method to mate the population
    toolbox.register("mutate", mutChoiceFromList, lists=mutate_list, indpb=0.5, mutrng=(-2,2)) # specify the method to mutate the individual
    toolbox.register("select", tools.selTournament, tournsize=3) # Specify the method for selection of the population
    pool = multiprocessing.Pool() # Create a multiprocessing pool to execute a population in parallel
    toolbox.register("map", pool.map) # register the multiprocessing pool
    
    return toolbox

if __name__ == "__main__":
    """
    Run an evolutionary algorithm to determine the conditions for the longest response time on an application
    This Example is based on a calculator that can add '+' substract '-' multiply 'x' and divide '/'.
    Example: calculate(6, '+', 2) returns 8
    """
    # Prepare the plot
    plt.ion()
    plt.ylabel('Response Time')
    plt.xlabel('Generation')
    
    # Create the evolutionary algorithm toolbox
    toolbox = setupToolbox()    
    
    # Create the first population and run the algorithm
    pop = toolbox.population(n=100)
    pop = run(toolbox, pop, ngen=200, cxpb=0.5, mutpb=0.8)
    
    # Print the top 10 of the resulting population     
    topTen = tools.selBest(pop, k=10)
    for index, item in enumerate(topTen):
        print("#%d: %E %s" %(index,item.responseTime, str(item)))
    
    # Keep the plot open  
    plt.show(block=True)   
        