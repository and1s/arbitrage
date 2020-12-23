import numpy as np

#has an arbitrage opportunity
graph = [
    [1, 0.23, 0.25, 16.43, 18.21, 4.94],
    [4.34, 1, 1.11, 71.40, 79.09, 21.44],
    [3.93, 0.90, 1, 64.52, 71.48, 19.37],
    [0.061, 0.014, 0.015, 1, 1.11, 0.30],
    [0.055, 0.013, 0.014, 0.90, 1, 0.27],
    [0.20, 0.047, 0.052, 3.33, 3.69, 1],
]

currencies = ('PLN', 'EUR', 'USD', 'RUB', 'INR', 'MXN')

def logNegate(graph):
    newGraph = graph
    for currency in range(len(graph)):
        for trade in range(len(graph[currency])):
            newGraph[currency][trade] = -1*np.log(graph[currency][trade])
    return newGraph


def findNegCycle(graph):
    

print(logNegate(graph))