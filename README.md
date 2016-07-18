# Evolutionary-Algorithm-demo
A demo for applying an evolutionary algorithm in python using DEAP.

This demo evaluates the response time of a simple calculator with some added delays to certain conditions to make sure the algorithm has something to look for.

The evaluation and mutation are custom, the applying of the algorithm is copy pasted from DEAPs eaSimple() for demo purposes. The selection and mating is done by DEAPs build-in functions cxTwoPoint() and selTournament().

To run you need matplotlib (for plotting the evolution) and DEAP for the evolution itself.

<code>pip install deap</code> Also available here: https://github.com/DEAP/deap

<code>pip install matplotlib</code> Also available here: http://matplotlib.org/

