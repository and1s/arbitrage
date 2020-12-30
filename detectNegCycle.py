import json
from math import log
import requests
import networkx as nx
import matplotlib.pyplot as plt
#example rates
rates = [
    [1, 0.23, 0.25, 16.43, 18.21, 4.94],
    [4.34, 1, 1.11, 71.40, 79.09, 21.44],
    [3.93, 0.90, 1, 64.52, 71.48, 19.37],
    [0.061, 0.014, 0.015, 1, 1.11, 0.30],
    [0.055, 0.013, 0.014, 0.90, 1, 0.27],
    [0.20, 0.047, 0.052, 3.33, 3.69, 1],
]
#example currencies
currencies = ('PLN', 'EUR', 'USD', 'RUB', 'INR', 'MXN')


def negate_logarithm_convertor(graph):
    ''' log of each rate in graph and negate it'''
    result = [[-log(edge) for edge in row] for row in graph]
    return result

def arbitrage(currency_tuple, rates_matrix):

    trans_graph = negate_logarithm_convertor(rates_matrix)

    source = 0
    n = len(trans_graph)
    min_dist = [float('inf')] * n

    pre = [-1] * n
    
    min_dist[source] = source

    for _ in range(n-1):
        for source_curr in range(n):
            for dest_curr in range(n):
                if min_dist[dest_curr] > min_dist[source_curr] + trans_graph[source_curr][dest_curr]:
                    min_dist[dest_curr] = min_dist[source_curr] + trans_graph[source_curr][dest_curr]
                    pre[dest_curr] = source_curr
    cycleDict = {}
    cycleList = []

    for source_curr in range(n):
        for dest_curr in range(n):
            if min_dist[dest_curr] > min_dist[source_curr] + trans_graph[source_curr][dest_curr]:
                print_cycle = [dest_curr, source_curr]
                while pre[source_curr] not in  print_cycle:
                    print_cycle.append(pre[source_curr])
                    source_curr = pre[source_curr]
                print_cycle.append(pre[source_curr])
                print_cycle = findLoop(print_cycle)
                if print_cycle in cycleDict:
                    pass
                else:
                    cycleDict[print_cycle] = 1
                    cycleList.append(print_cycle)
                    print("\n")
                    print("Arbitrage Opportunity: \n")
                    print(" --> ".join([currency_tuple[p] for p in print_cycle[::-1]]))
    return cycleList

def currentRates():
    r = requests.get("https://api.exchangeratesapi.io/latest").json()
    rString = "https://api.exchangeratesapi.io/latest?base="
    baseCurrency = r['base']
    ratesDict = r['rates']
    ratesDict[baseCurrency] = 1.0
    currencyList = []
    for curr in ratesDict:
        currencyList.append(curr)
    currencyList.append(baseCurrency)

    exchangeMatrix = []
    for curr in currencyList:
        temp = []
        myDict = requests.get('https://api.exchangeratesapi.io/latest?base='+curr).json()['rates']
        for curr2 in currencyList:
            if curr2 == "EUR" and curr == "EUR":
                temp.append(1.0)
            else:
                temp.append(myDict[curr2])
            #temp.append((ratesDict[curr2]/ratesDict[curr]))
        exchangeMatrix.append(temp)
    
    return currencyList, exchangeMatrix

def graphMaker(currencies, rates_matrix, cycle):
    DG = nx.DiGraph()
    edgeList = []
    for curr1 in range(len(cycle)-1):
        edgeList.append((currencies[cycle[curr1]], currencies[cycle[curr1+1]], round(rates_matrix[cycle[curr1]][cycle[curr1+1]], 2)))
    for node in currencies:
        DG.add_node(node)
    DG.add_weighted_edges_from(edgeList)
    pos = nx.circular_layout(DG)
    nx.draw_networkx(DG, pos, with_labels = True)
    labels = nx.get_edge_attributes(DG,'weight')
    nx.draw_networkx_edge_labels(DG, pos, edge_labels = labels)
    plt.show()

def findLoop(myList):
    listDict = {}
    repeat = None
    for item in myList:
        if item in listDict:
            repeat = item
            first = [i for i, n in enumerate(myList) if n == repeat][0]
            second = [i for i, n in enumerate(myList) if n == repeat][1]
            break
        else:
            listDict[item] = 1
    if second == len(myList)-1:
        return tuple(myList[first:])
    else:
        return tuple(myList[first:second+1])

if __name__ == "__main__":
    currency_tuple, rates_matrix = currentRates()
    cycles = arbitrage(currencies, rates)
    for cycle in cycles:
        graphMaker(currency_tuple, rates_matrix, cycle)
