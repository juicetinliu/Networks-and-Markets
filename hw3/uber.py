# Justin Liu
# include any code you need for your assignment in this file or in auxiliary
# files that can be imported here.
import math
import random
import copy
from collections import defaultdict

def matching_or_cset(G, r, d):  
    if d is None: d = r  
    flow = max_flow(copy.deepcopy(G), r + d + 1, r + d)
    if flow == min(r, d):
        return True, None

    matches = max_matching(copy.deepcopy(G))
    buyers = [False] * r
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


def market_eq(r, d, values):
    if d < r:
        diff = r - d
        d = r
        for value in values:
            value.extend([0] * diff)

    p = [0]*r
    M = [-1]*r
    prices = [0]*d

    graph = graph_from_valuations(r, d, values)
    done = False
    while not done:
        done, constricted = matching_or_cset(graph, r, d)
        pvalues = copy.deepcopy(values)
        if not done:
            # Increase price of constricted set item
            for seller in constricted:
                prices[seller - r] += 1
            
            # Subtract 1 from all if all prices > 0
            if len([True for p in prices if p > 0]) == r:
                prices = [p - 1 for p in prices]
            
            # Calculate new valuations
            for p_values in pvalues:
                for i in range(d):
                    p_values[i] -= prices[i]
            
            graph = graph_from_valuations(r, d, pvalues)
    for edge in max_matching(graph):
        p[edge[0]] = prices[edge[1] - r]
        M[edge[0]] = edge[1]
    return (p,M)

def vcg(r, d, values, prog = False):
    if d < r:
        diff = r - d
        d = r
        for value in values:
            value.extend([0] * diff)
        
    p = [0]*r
    M = [-1]*r
    if prog: progress(0)

    (_, M) = market_eq(r, d, values)
    total_welfare = 0  
    for player, item in enumerate(M):
        if item != -1:
            total_welfare += values[player][item - r]
    
    for i in range(r):
        new_values = copy.deepcopy(values)
        new_values[i] = [0] * d
        (_, new_matchings) = market_eq(r, d, new_values)
        withipresent = total_welfare - (0 if M[i] == -1 else values[i][M[i] - r])
        withoutipresent = 0
        for player, item in enumerate(new_matchings):
            if item != -1:
                withoutipresent += new_values[player][item - r]
        p[i] = withoutipresent - withipresent
        if prog: progress(int((i+1)*100/r))
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

# compute the manhattan distance between two points a and b (represented as pairs)
def dist(a,b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

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

def graph_from_valuations(r, d, valuations, ones = True):
    graph = []
    sink = r + d
    for buyer, vals in enumerate(valuations):
        max_val = max(vals)
        for seller, val in enumerate(vals):
            if val == max_val:
                graph.append((buyer, seller + r, 1))
    for i in range(r):
        graph.append((sink + 1, i, 1 if ones else d))
    for i in range(d):
        graph.append((i + r, sink, 1 if ones else r))
    return create_graph_from_connections_flow(r + d + 2, graph)

def randomvaluations(r, d, maxval = 10, shift = 0):
    return [[random.randrange(maxval) + shift for i in range(d)] for _ in range(r)]

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

def valuations_100_100_random(r, d, r_value = 100):
    riders_coor = [(random.randrange(101), random.randrange(101)) for i in range(r)]
    rdest_coor = [(random.randrange(101), random.randrange(101)) for i in range(r)]
    drivers_coor = [(random.randrange(101), random.randrange(101)) for i in range(d)]

    valuations = [[0 for x in range(d)] for y in range(r)]
    for rind, rider in enumerate(riders_coor):
        for dind, driver in enumerate(drivers_coor):  
            valuations[rind][dind] = r_value - (dist(rider,driver) + dist(rider,rdest_coor[rind]))
    return valuations

# Given a (bipartite) graph G with edge values specified by v, 
# output a stable outcome (M,a) consisting of a matching and allocations
def stable_outcome(G, prog = False):
    valuations = copy.deepcopy(G)
    r = len(valuations)
    d = len(valuations[0])
    
    p, M = vcg(r, d, valuations, prog)

    M = [x if x in range(r, r + d) else -1 for x in M]

    return p, M

def question_11_a():
    valuations = randomvaluations(5, 5, shift = 1)
    print(valuations)
    print(stable_outcome(valuations, True))

    valuations = randomvaluations(7, 7, shift = 1)
    print(valuations)
    print(stable_outcome(valuations, True))

def question_11_b():
    print("r = 10 | d = 10")
    averageprice = 0
    for i in range(50):
        valuations = valuations_100_100_random(10, 10)
        p, _ = stable_outcome(valuations)
        averageprice += sum(p)
        progress(int((i+1)*2))
    averageprice = averageprice/500
    print("Average price per match:", averageprice)

    print("r = 5 | d = 20")
    averageprice = 0
    for i in range(50):
        valuations = valuations_100_100_random(5, 20)
        p, _ = stable_outcome(valuations)
        averageprice += sum(p)
        progress(int((i+1)*2))
    averageprice = averageprice/250
    print("Average price per match:", averageprice)

    print("r = 20 | d = 5")
    averageprice = 0
    for i in range(50):
        valuations = valuations_100_100_random(20, 5)
        p, _ = stable_outcome(valuations)
        averageprice += sum(p)
        progress(int((i+1)*2))
    averageprice = averageprice/250
    print("Average price per match:", averageprice)

question_11_a()
question_11_b()