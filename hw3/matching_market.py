# Justin Liu
# include any code you need for your assignment in this file or in auxiliary
# files that can be imported here.
import math
import random
import copy
from collections import defaultdict

# 7 (a)
# implement an algorithm that given a bipartite graph G, outputs
# either a perfect matching or a constricted set
# Note: this will be used in 7 (b) so you can implement it however you
# like
def matching_or_cset(G, n, m = None):  
    if m is None: m = n  
    flow = max_flow(copy.deepcopy(G), n + m + 1, n + m)
    if flow == min(n, m):
        return True, None

    matches = max_matching(copy.deepcopy(G))
    buyers = [False] * n
    for (buyer, _) in matches:
        buyers[buyer] = True
    
    constricted = []
    for buyer, matched in enumerate(buyers):
        if not matched:
            for seller, values in enumerate(G[buyer]):
                if values > 0 and seller not in constricted:
                    constricted.append(seller)
    #return all of the constricted sets (seller ids)
    return False, constricted

# 7 (b)
# implement an algorithm that given n (the number of players and items,
# which you can assume to just be labeled 0,1,...,n-1 in each case),
# and values where values[i][j] represents the ith players value for item j,
# output a market equilibrium consisting of prices and matching
# (p,M) where player i pays p[i] for item M[i]. 
def market_eq(n, values, m = None):
    if m is None: 
        m = n  
    elif m < n:
        diff = n - m
        m = n
        for value in values:
            value.extend([0] * diff)

    p = [0]*n
    M = [-1]*n
    prices = [0]*m

    graph = graph_from_valuations(n, values, m)
    done = False
    while not done:
        done, constricted = matching_or_cset(graph, n, m)
        pvalues = copy.deepcopy(values)
        if not done:
            # Increase price of constricted set item
            for seller in constricted:
                prices[seller - n] += 1
            
            # Subtract 1 from all if all prices > 0
            if len([True for p in prices if p > 0]) == n:
                prices = [p - 1 for p in prices]
            
            # Calculate new valuations
            for p_values in pvalues:
                for i in range(m):
                    p_values[i] -= prices[i]
            
            graph = graph_from_valuations(n, pvalues, m)
    for edge in max_matching(graph):
        p[edge[0]] = prices[edge[1] - n]
        M[edge[0]] = edge[1]
    return (p,M)

# 8 (b)
# Given n players 0,...,n-1 and m items 0,...,m-1 and valuations
# values such that values[i][j] is player i's valuation for item j,
# implement the VCG mechanism with Clarke pivot rule that outputs
# a set of prices and assignments (p,M) such that player i pays p[i]
# (which should be positive) for item M[i].
def vcg(n, m, values):
    if m < n:
        diff = n - m
        m = n
        for value in values:
            value.extend([0] * diff)
        
    p = [0]*n
    M = [-1]*n
    progress(0)

    (_, M) = market_eq(n, values, m)
    total_welfare = 0  
    for player, item in enumerate(M):
        if item != -1:
            total_welfare += values[player][item - n]
    
    for i in range(n):
        new_values = copy.deepcopy(values)
        new_values.pop(i)
        (_, new_matchings) = market_eq(n - 1, new_values, m)
        withipresent = total_welfare - (0 if M[i] == -1 else values[i][M[i]-n])
        withoutipresent = 0
        for player, item in enumerate(new_matchings):
            if item != -1:
                withoutipresent += new_values[player][item - n + 1]
        p[i] = withoutipresent - withipresent
        progress(int((i+1)*100/n))
    return (p,M)
    
def max_flow(G, s, t):
    def BFS(Graph, s, t, path): 
        visited = [False] * len(Graph) 
        queue = [s]
        visited[s] = True
        
        while queue: 
            next = queue.pop(0) 
            
            for tonode, flow in enumerate(Graph[next]): 
                if not visited[tonode] and flow > 0 : 
                    queue.append(tonode) 
                    visited[tonode] = True
                    path[tonode] = next
        return visited[t]

    path = [-1] * len(G)

    max_flow = 0

    while BFS(G, s, t, path): 
        min_flow = float("Inf")
        check_s = t
        while(check_s != s): 
            min_flow = min(min_flow, G[path[check_s]][check_s]) 
            check_s = path[check_s] 

        # Add path flow to overall flow 
        max_flow += min_flow 

        # update residuals
        v = t 
        while v != s: 
            u = path[v] 
            G[u][v] -= min_flow 
            G[v][u] += min_flow 
            v = path[v]

    return max_flow 

def max_matching(G):
    G_before = copy.deepcopy(G)
    sink = len(G) - 2
    max_flow(G, sink + 1, sink)
    edges = []
    for fromnode, to in enumerate(G):
        for tonode, flow in enumerate(to):
            if flow - G_before[fromnode][tonode] < 0 and fromnode < sink and tonode < sink:
                edges.append((fromnode, tonode))
    return edges

# given a list of tuples (node, node, capacity), create a graph
def create_graph_from_connections_flow(num_nodes, connection_list):
    graph = []
    for i in range(num_nodes):
        graph.append([0] * num_nodes)
    for pair in connection_list:
        i = int(pair[0])
        j = int(pair[1])
        flow = int(pair[2])
        graph[i][j] = flow
    return graph

def graph_from_valuations(n, valuations, m = None, ones = True):
    if m is None: m = n  
    graph = []
    sink = n + m
    for buyer, vals in enumerate(valuations):
        max_val = max(vals)
        for seller, val in enumerate(vals):
            if val == max_val:
                graph.append((buyer, seller + n, 1))
    for i in range(n):
        graph.append((sink + 1, i, 1 if ones else m))
    for i in range(m):
        graph.append((i + n, sink, 1 if ones else n))
    return create_graph_from_connections_flow(n + m + 2, graph)

def print_graph(G, all=False):
    for fromnode, to in enumerate(G):
        for tonode, flow in enumerate(to):
            if all or flow > 0:
                print(fromnode, "==(", flow, ")=>", tonode)

def randomvaluations(n, maxval = 10, shift = 0):
    return [[random.randrange(maxval) + shift for i in range(n)] for _ in range(n)]

def progress(percent=0, width=10):
    left = width * percent // 100
    right = width - left
    if percent == 100:
        print('\r[', '#' * left, ' ' * right, ']',
          f' {percent:.0f}%',
          sep='', end='\n', flush=True)
    else:
        print('\r[', '#' * left, ' ' * right, ']',
          f' {percent:.0f}%',
          sep='', end='', flush=True)

def question_7_c():
    valuations = [[4, 12, 5], [7, 10, 9], [7, 7, 10]]
    print(market_eq(3, valuations))

    valuations = [[1, 9, 9, 3, 1], [1, 9, 7, 3, 7], [9, 2, 2, 7, 3], [6, 8, 6, 1, 5], [9, 1, 8, 6, 6]]
    # valuations = randomvaluations(5)
    print(market_eq(5, valuations))

    valuations = [[6, 2, 3, 1, 8, 9, 1], [2, 5, 4, 3, 8, 4, 5], [1, 7, 1, 9, 1, 7, 4], [6, 9, 6, 2, 9, 2, 6], [5, 2, 5, 8, 9, 6, 9], [8, 6, 1, 1, 7, 5, 7], [5, 1, 4, 1, 4, 7, 9]]
    # valuations = randomvaluations(7)
    print(market_eq(7, valuations))

    valuations = [[7, 4, 9, 7, 8, 4, 3, 2, 4], [3, 1, 8, 4, 9, 7, 9, 7, 9], [8, 5, 3, 4, 6, 7, 3, 8, 6], [1, 4, 9, 1, 1, 2, 1, 1, 1], [1, 7, 7, 4, 7, 6, 8, 1, 9], [4, 5, 6, 4, 1, 8, 9, 5, 9], [6, 3, 3, 4, 1, 9, 1, 1, 9], [8, 2, 1, 4, 9, 5, 6, 5, 2], [3, 7, 8, 5, 2, 1, 1, 7, 1]]
    # valuations = randomvaluations(9)
    print(market_eq(9, valuations))

def question_8_c():
    valuations = [[4, 12, 5], [7, 10, 9], [7, 7, 10]]
    print(vcg(3, 3, valuations))

    valuations = [[9, 0, 1, 1, 7], [8, 3, 5, 7, 2], [1, 6, 3, 4, 6], [5, 3, 6, 0, 7], [3, 9, 9, 0, 2]]
    # valuations = randomvaluations(5)
    print(vcg(5, 5, valuations))

    valuations = [[1, 9, 4, 4, 5, 5, 4], [0, 2, 6, 6, 0, 4, 5], [2, 2, 1, 8, 8, 2, 1], [3, 7, 8, 8, 6, 2, 8], [2, 1, 6, 5, 6, 2, 5], [1, 7, 5, 4, 6, 5, 0], [0, 2, 8, 8, 0, 0, 1]]
    # valuations = randomvaluations(7)
    print(vcg(7, 7, valuations))

    valuations = [[3, 5, 7, 1, 3, 2, 2, 6, 1], [1, 5, 7, 8, 3, 3, 7, 5, 1], [5, 3, 8, 1, 4, 9, 4, 3, 2], [4, 8, 0, 0, 8, 3, 7, 9, 7], [0, 3, 8, 5, 1, 8, 3, 2, 8], [7, 6, 7, 4, 2, 6, 2, 4, 0], [0, 4, 6, 4, 4, 7, 2, 9, 7], [4, 3, 3, 1, 6, 4, 6, 6, 3], [3, 2, 4, 6, 7, 7, 9, 5, 2]]
    # valuations = randomvaluations(9)
    print(vcg(9, 9, valuations))

def question_9_a():
    # playervaluations = [random.randrange(50) + 1 for i in range(20)]
    playervaluations = [24, 50, 1, 40, 28, 17, 4, 8, 3, 7, 43, 20, 39, 2, 37, 11, 50, 31, 50, 26]
    valuations = []

    for valuation in playervaluations:
        valuations.append([valuation * (i + 1) for i in range(20)])
    print(vcg(20, 20, valuations))


# valuations = [[5, 7, 1], [2, 3, 1], [5, 4, 4]]
# print(market_eq(3, valuations))
# valuations = [[5, 2, 5], [7, 3, 4], [1, 1, 4]]
# print(market_eq(3, valuations))
# valuations = [[30, 15], [20, 10], [10, 5]]
# print(market_eq(3, valuations, 2))
# valuations = [[30, 15], [20, 10], [10, 5]]
# print(vcg(3, 2, valuations))

# question_7_c()
# question_8_c()
# question_9_a()