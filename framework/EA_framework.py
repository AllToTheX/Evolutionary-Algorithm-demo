'''
Created on Jul 16, 2016

@author: allexveldman
'''

import random
from Calculator import CalculatorPopulation
from deap import tools

def run(toolbox, pop, ngen, cxpb, mutpb):
    """
        Run the evolutionary algorithm.
        `toolbox` should exist of the following functions:
        toolbox.select
        toolbox.mate
        toolbox.mutate
        toolbox.evaluate
        toolbox.map
        toolbox.clone
        
        'map' and 'clone' are part of the default toolbox, the rest needs to be defined by the user.
        'map' can be used to control the execution of your testcases
        
        - First evaluates the first population
        - Loop trough generations:
            - Mates the population with a probability of cxpb
            - Mutates the resulting population with a probability of mutpb
            - Evaluates the new population
        - The resulting population and the best individuals of each generation after ngen generations
        
        :param toolbox: Toolbox containing all needed functions to execute out algorithm.
        :param pop: Initial population to start our algorithm with.
        :param ngen: Number of generations.
        :param cxpb: Crossover probability.
        :param mutpb: Mutate probability.
        :returns: (pop, topOne) The resulting population and the best individuals of each generation
    """
    #===========================================================================
    # determine the amount of individuals to use for the crossover
    #===========================================================================
    selfact = 0.2
    select_k = int( len(pop)*selfact ) # Amount of individuals to keep
    
    # Keep track of diagnostics
    topOne = list() # Keep score of the top 1 for our plot
    all_populations = dict()

    #===========================================================================
    # Evaluate the fitness of the initial population
    #===========================================================================
    fitnesses = toolbox.map(toolbox.evaluate, pop)
    for ind, fit in zip(pop, fitnesses):
        ind.fitness.values = fit
        ind.responseTime = fit[0]
    all_populations["Generation 0"] = pop
    #===========================================================================
    # Start the generation loop
    #===========================================================================
    for g in range(1,ngen):
        #=======================================================================
        # Select the parents for the crossover
        #=======================================================================
        parents = toolbox.select(pop, k=select_k)
        parents = [toolbox.clone(ind) for ind in parents] # Make the parents a hard copy
        #=======================================================================
        # Crossover the population
        #=======================================================================
        for child1, child2 in zip(parents[::2], parents[1::2]): # mate each parent with it's neighbor
            if random.random() < cxpb: # Probability to mate
                toolbox.mate(child1, child2)
                del child1.fitness.values, child2.fitness.values
                child1.responseTime = 0
                child2.responseTime = 0
        children = [ind for ind in parents if not ind.fitness.valid]       
        #=======================================================================
        # Insert children into the population
        #=======================================================================
        pop = toolbox.select(pop, k=len(pop)) # Sort population based on fitness
        if len(children) > 0: pop[-len(children):] = children 
        pop = [toolbox.clone(ind) for ind in pop]
        #=======================================================================
        # Mutate the population
        #=======================================================================
        for mutant in pop:
            if random.random() < mutpb:
                toolbox.mutate(mutant, indpb=0.5) # indpb is the chance for each attribute to mutate
                del mutant.fitness.values
                mutant.responseTime = 0
        #=======================================================================
        # Evaluate fitness of the new individuals in the resulting population
        #=======================================================================
        invalids = [ind for ind in pop if not ind.fitness.valid]
        fitnesses = toolbox.map(toolbox.evaluate, invalids)
        for ind, fit in zip(invalids, fitnesses):
            ind.fitness.values = fit
            ind.responseTime = fit[0] # Add response time to individual for plotting  
        #=======================================================================

        all_populations["Generation %s" %(g)] = pop
        # Select the top 3 of current population for printing
        topThree = tools.selBest(pop, k=3)
        # Add the winner of this population to the plot
        append = True
        for item in topOne:
            if topThree[0] == item and topThree[0].responseTime == item.responseTime:
                append = False
        if append: 
            topThree[0].generation = "Generation %s" %(g)
            topOne.append(topThree[0])
        
        # Print the top 3 for this population
        print("Generation %d" % g)
        for index, item in enumerate(topThree):
            print( "#%d: %E %s" % (index, item.responseTime, str(item)))
        print ('\n')
    
    return all_populations, topOne # Return the resulting population

if __name__ == "__main__":
    """
    Run an evolutionary algorithm to determine the conditions for the longest response time on an application
    This Example is based on a calculator that can add '+' substract '-' multiply 'x' and divide '/'.
    Example: calculate(6, '+', 2) returns 8
    """
    
    # Create the evolutionary algorithm toolbox
    calcPop = CalculatorPopulation()
    toolbox = calcPop.toolbox
    
    #===========================================================================
    # Create the initial population and start the Evolutionary Algorithm
    #===========================================================================
    npop = 50
    ngen = 50
    cxpb = 0.5
    mutpb = 0.3
    pop = toolbox.population(n=npop)
    pop, topOne = run(toolbox, pop, ngen=ngen, cxpb=cxpb, mutpb=mutpb)
    #===========================================================================

    
    # Print the top 10 of the resulting population     
    topTen = tools.selBest(topOne, k=10)
    for index, item in enumerate(topTen):
        print("#%d: %E %s (%s)" %(index,item.responseTime, str(item), item.generation))
    
    # Sort the best performing individuals by response time, and show in a new figure
    top = dict()
    top['Sorted'] = tools.selWorst(topOne, k=len(topOne))
        