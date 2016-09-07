'''
Created on Jul 16, 2016

@author: allexveldman
'''

import random
import matplotlib.pyplot as plt
import multiprocessing
import timeit
import plotly as py
import plotly.graph_objs as go

from deap import base, creator, tools

VAR1 = range(1,99+1)
OPERATORS = ['+','-','x','/']
VAR2 = VAR1

def wrapper(func, *args, **kwargs):
    """ Wrapper for the timeit call """
    def wrapped():
        return func(*args, **kwargs)
    return wrapped

def evaluateIndividual(individual,n=1):
    """ Evaluate the the fitness of our individual by measuring the response time of
    executing calculate()
    
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

def createIndividual(individual, var1, opper, var2):
    """ Created an individual instance to run the application with. 
    
    :param individual: individual class reference (inheriting of type list) to be populated.
    :param var1: list containing possible values for variable 1.
    :param opper: list containing possible operators.
    :param var2: list containing possible values for variable 2.
    :returns: A populated individual
    """
    ind = individual() # Create the instance
    ind.append(random.choice(var1)) # Generate a random number for var1
    ind.append(random.choice(opper)) # pick a random operator
    ind.append(random.choice(var2)) # Generate a random number for var2
    return ind

def mutChoiceFromList(individual, posval, indpb):
    """Mutate an individual by replacing attributes, with probability *indpb*,
    by a neighboring value in lists with a range of mutrng.
    
    :param individual: individual to be mutated.
    :param posval: A list of tuples corresponding to the values possible as input for
                the application to test
    :param indpb: Independent probability for each attribute to be mutated.
    :param mutrng: Range of mutation for a single attribute.
    :returns: A tuple of one individual.
    """
    size = len(individual)
    
    for i, xl in zip(xrange(size), posval):
        if random.random() < indpb:
            individual[i] = random.choice(xl)
    
    return individual,

def update_plot(values, figure=1, subplot=(1,1,1), line_style='', title=''):
    """
    Update the `subplot in `figure.
    :param values: values to plot.
    :param figure: figure to place plot in.
    :param subplot: subplot withing `figure.
    :param line_style: define the linestyle of the axis.
    :param title: the title for the plot.
    """
    x = [' '.join([str(item) for item in ind]) for ind in values]
    y = [item.responseTime for item in values] # Y values
    
    # select figure and subplot
    plt.figure(figure)
    plt.subplot(*subplot)
    # clear axis
    plt.cla() 
    # set figure and axis properties
    plt.title(title)
    plt.ylabel('Response Time [s]')
    plt.grid(b='on')
    # plot new axis
    plt.plot(range(len(x)), y, line_style)
    # set tick labels
    plt.xticks(range(len(x)),x)
    _, labels = plt.xticks()
    plt.setp(labels, rotation=45)
    # Show the plot
    plt.pause(0.05)
    
def create_plot(populations,plot_name='plot.html'):
    """
    Create an HTML5 plot of the individuals response times
    """
    data = list()
    layout = go.Layout(
        title='Best of each generation',
        xaxis=dict(
            title='Individual',
            titlefont=dict(
                family='Courier New, monospace',
                size=18,
                color='#7f7f7f'
            )
        ),
        yaxis=dict(
            title='Response time [ms]',
            titlefont=dict(
                family='Courier New, monospace',
                size=18,
                color='#7f7f7f'
            )
        )
    )
    for name, population in populations.iteritems():
        # Get the response times and string representation of the individuals 
        x_values = [' '.join([str(item) for item in ind]) for ind in population] # string representation
        y_values = [item.responseTime*1000 for item in population] # Response times
        # Create a trace
        trace = go.Scatter(
            x = x_values,
            y = y_values,
            mode = 'markers',
            name = name,
            visible = 'legendonly'
        )
        # Create the plot layout
        
        # Create the figure
        data.append(trace)
        
    data[0].visible = True
    fig = go.Figure(data=data, layout=layout)
    
    # Create the plot in HTML5 and open it in a browser
    py.offline.plot(fig, filename=plot_name, auto_open=True)

def run(toolbox, pop, ngen, cxpb, mutpb, plot=True):
    """
        Run the evolutionary algorithm.
        
        - First evaluates the first population
        - Loop trough generations:
            - Mates the population with a probability of cxpb
            - Mutates the resulting population with a probability of mutpb
            - Evaluates the new population
            - Plots the best individual and prints the top three
        - Returns the resulting population after ngen generations
        
        :param toolbox: Toolbox containing all needed functions to execute out algorithm.
        :param pop: Initial population to start our algorithm with.
        :param ngen: Number of generations.
        :param cxpb: Crossover probability.
        :param mutpb: Mutate probability.
        :param plot: if True, plot the best performing individuals in each generation.
        :returns: (pop, topOne) The resulting population and the best individuals of each generation
    """
    #===========================================================================
    # determine the amount of individuals to continue with after each generation
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
        #=======================================================================
        # Insert children into the population
        #=======================================================================
        children = [ind for ind in parents if not ind.fitness.valid]
        pop = toolbox.select(pop, k=len(pop)) # Sort population based on fitness
        if len(children) > 0: pop[-len(children):] = children 
        pop = [toolbox.clone(ind) for ind in pop]
        #=======================================================================
        # Mutate the population
        #=======================================================================
        for mutant in pop:
            if random.random() < mutpb:
                toolbox.mutate(mutant)
                del mutant.fitness.values
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
        topOne.append(topThree[0])
        
        # Expand the plot with the new winner
        if plot: update_plot(topOne, line_style='o',title="Sequential.\nGeneration: %s" %(g))
        
        # Print the top 3 for this population
        print("Generation %d" % g)
        for index, item in enumerate(topThree):
            print( "#%d: %E %s" % (index, item.responseTime, str(item)))
        print ('\n')
    
    return all_populations, topOne # Return the resulting population

def setupToolbox():
    """ Fill the toolbox needed for applying our algorithm """
    # Mutate_list holds the possible values to mutate to
    mutate_list = ( 
                   VAR1,
                   OPERATORS,
                   VAR2 )
    
    # Create the base class for the individuals
    creator.create("FitnessMax", base.Fitness, weights=(1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMax, responseTime=0.0)  # @UndefinedVariable
    
    # Register the toolkit to work with
    toolbox = base.Toolbox()
    toolbox.register("individual", createIndividual, creator.Individual, *mutate_list) # Specify the method to create an individual @UndefinedVariable
    toolbox.register("population", tools.initRepeat, list, toolbox.individual) # Specify the method to create the population
    toolbox.register("evaluate", evaluateIndividual, n=1) # Specify the method to evaluate the individual
    toolbox.register("mate", tools.cxTwoPoint) # Specify the method to mate the population
    toolbox.register("mutate", mutChoiceFromList, posval=mutate_list, indpb=0.5) # specify the method to mutate the individual
    toolbox.register("select", tools.selBest) # Specify the method for selection of the population
    pool = multiprocessing.Pool() # Create a multiprocessing pool to execute a population in parallel
    toolbox.register("map", pool.map) # register the multiprocessing pool
    
    return toolbox

if __name__ == "__main__":
    """
    Run an evolutionary algorithm to determine the conditions for the longest response time on an application
    This Example is based on a calculator that can add '+' substract '-' multiply 'x' and divide '/'.
    Example: calculate(6, '+', 2) returns 8
    """
    plot = True

    # Prepare the plot
    if plot:
        plt.ion()
    
    # Create the evolutionary algorithm toolbox
    toolbox = setupToolbox()    
    
    #===========================================================================
    # Create the initial population and start the Evolutionary Algorithm
    #===========================================================================
    npop = 50
    ngen = 100
    cxpb = 0.5
    mutpb = 0.3
    pop = toolbox.population(n=npop)
    pop, topOne = run(toolbox, pop, ngen=ngen, cxpb=cxpb, mutpb=mutpb, plot=plot)
    #===========================================================================

    
    # Print the top 10 of the resulting population     
    topTen = tools.selBest(topOne, k=10)
    for index, item in enumerate(topTen):
        print("#%d: %E %s" %(index,item.responseTime, str(item)))
    
    # Sort the best performing individuals by response time, and show in a new figure
    top = dict()
    top['Sorted'] = tools.selWorst(topOne, k=len(topOne))
    create_plot(top,plot_name='plot.html')
    create_plot(pop,plot_name='populations.html')
    
#     update_plot(topOne, figure=2, subplot=(1,1,1), line_style='o', title="Sorted.\nGenerations: %s, cross-over: %s, mutation: %s" %(ngen, cxpb, mutpb))
#     plt.show(block=True)   
        