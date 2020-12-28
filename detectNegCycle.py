import json
from math import log
import requests

rates = [
    [1, 0.23, 0.25, 16.43, 18.21, 4.94],
    [4.34, 1, 1.11, 71.40, 79.09, 21.44],
    [3.93, 0.90, 1, 64.52, 71.48, 19.37],
    [0.061, 0.014, 0.015, 1, 1.11, 0.30],
    [0.055, 0.013, 0.014, 0.90, 1, 0.27],
    [0.20, 0.047, 0.052, 3.33, 3.69, 1],
]

currencies = ('PLN', 'EUR', 'USD', 'RUB', 'INR', 'MXN')


def negate_logarithm_convertor(graph):
    ''' log of each rate in graph and negate it'''
    result = [[-log(edge) for edge in row] for row in graph]
    return result


def arbitrage(currency_tuple, rates_matrix):
    ''' Calculates arbitrage situations and prints out the details of this calculations'''

    trans_graph = negate_logarithm_convertor(rates_matrix)

    # Pick any source vertex -- we can run Bellman-Ford from any vertex and get the right result

    source = 0
    n = len(trans_graph)
    min_dist = [float('inf')] * n

    pre = [-1] * n
    
    min_dist[source] = source

    # 'Relax edges |V-1| times'
    for _ in range(n-1):
        for source_curr in range(n):
            for dest_curr in range(n):
                if min_dist[dest_curr] > min_dist[source_curr] + trans_graph[source_curr][dest_curr]:
                    min_dist[dest_curr] = min_dist[source_curr] + trans_graph[source_curr][dest_curr]
                    pre[dest_curr] = source_curr

    # if we can still relax edges, then we have a negative cycle
    for source_curr in range(n):
        for dest_curr in range(n):
            if min_dist[dest_curr] > min_dist[source_curr] + trans_graph[source_curr][dest_curr]:
                # negative cycle exists, and use the predecessor chain to print the cycle
                print_cycle = [dest_curr, source_curr]
                # Start from the source and go backwards until you see the source vertex again or any vertex that already exists in print_cycle array
                while pre[source_curr] not in  print_cycle:
                    print_cycle.append(pre[source_curr])
                    source_curr = pre[source_curr]
                print_cycle.append(pre[source_curr])
                print(print_cycle)
                if len(print_cycle) == 0:
                    print("No Arbitrage")
                else:
                    print("Arbitrage Opportunity: \n")
                    print(" --> ".join([currency_tuple[p] for p in print_cycle[::-1]]))

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

    #TODO: change so that we use different base for currencies in https request
    exchangeMatrix = []
    for curr in currencyList:
        temp = []
        for curr2 in currencyList:
            temp.append((ratesDict[curr2]/ratesDict[curr]))
        exchangeMatrix.append(temp)
    
    return currencyList, exchangeMatrix


if __name__ == "__main__":
    currency_tuple, rates_matrix = currentRates()
    arbitrage(currency_tuple, rates_matrix)
