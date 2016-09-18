# Evolutionary-Algorithm-demo
A demo for applying an evolutionary algorithm in python using DEAP.

This demo evaluates the response time of a simple calculator with some added delays to certain conditions to make sure the algorithm has something to look for.

The evaluation and mutation are custom, the applying of the algorithm is copy pasted from DEAPs eaSimple() for demo purposes. The selection and mating is done by DEAPs build-in functions cxTwoPoint() and selBest().

To run you need matplotlib and plotly (for plotting the evolution) and DEAP for the evolution itself.

## Before you can run it
This demo was written with python 3.5 and needs deap, matplotlib and plotly

<code>pip3 install -r requirements.txt</code>

### possible run issues
''' Unkown locale UTF-8 error

I run this using Eclipse with the pydev plugin on OSX. Apperantly eclipse sets some locale variables preventing this error.
If you want to run it from the commandline and this error shows up op the import of matplotlib, run:

<code>export LC_ALL=en_US.UTF-8</code> (works for OSX)

''' Windows

Windows can't handle the multiprocessing pool for some reason, comment out line 159.
Execution will be a lot slower.
