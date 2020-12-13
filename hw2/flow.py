# Justin Liu
# include any code you need for your assignment in this file or in auxiliary
# files that can be imported here.
import math
import random
import copy
from collections import defaultdict

# 9 (a)
# implement an algorithm that computes the maximum flow in a graph G
# Note: you may represent the graph, source, sink, and edge capacities
# however you want. You may also change the inputs to the function below.
# Based on (https://www.geeksforgeeks.org/ford-fulkerson-algorithm-for-maximum-flow-problem/)
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

def print_graph(G, all=False):
    for fromnode, to in enumerate(G):
        for tonode, flow in enumerate(to):
            if all or flow > 0:
                print(fromnode, "==(", flow, ")=>", tonode)


# 9 (c)
# implement an algorithm that computes a maximum matching in a bipartite graph G
# Note: you may represent the bipartite graph however you want
def max_matching(G):
    G_before = copy.deepcopy(G)
    sink = len(G) - 1
    max_flow(G, 0, sink)
    edges = []
    for fromnode, to in enumerate(G):
        for tonode, flow in enumerate(to):
            if flow - G_before[fromnode][tonode] < 0 and fromnode != 0 and fromnode != sink and tonode != sink and tonode != 0:
                edges.append((fromnode, tonode))
    return edges
    # return M # a matching

def question_9_a():
    graph_6_1 = [(0, 1, 1), (0, 2, 3), (1, 2, 2), (1, 3, 1), (2, 3, 1)]
    G = create_graph_from_connections_flow(4, graph_6_1)
    print_graph(G)
    print("MaxFlow 6.1:", max_flow(G, 0, 3))

    graph_6_3 = [(0, 1, 1), (0, 2, 1), (0, 3, 1), (0, 4, 1), (0, 5, 1), (1, 7, 1), (2, 6, 1), (2, 7, 1), (3, 6, 1), (4, 8, 1), (4, 10, 1), (5, 8, 1), (5, 9, 1), (6, 11, 1), (7, 11, 1), (8, 11, 1), (9, 11, 1), (10, 11, 1)]
    G = create_graph_from_connections_flow(12, graph_6_3)
    print_graph(G)
    print("MaxFlow 6.3:", max_flow(G, 0, 11))

def question_9_c():
    num_drivers = 5
    num_riders = 5

    # graph = [(1, 7, 1), (2, 6, 1), (2, 7, 1), (3, 6, 1), (4, 8, 1), (4, 10, 1), (5, 8, 1), (5, 9, 1)]
    graph = [(1, 8, 1), (1, 10, 1), (2, 7, 1), (2, 8, 1), (3, 8, 1), (3, 9, 1), (4, 6, 1), (5, 10, 1)]

    for i in range(num_drivers):
        graph.append((0, i + 1, 1))
    for i in range(num_riders):
        graph.append((i + num_drivers + 1, num_riders + num_drivers + 1, 1))

    G = create_graph_from_connections_flow(12, graph)
    matchings = max_matching(G)
    print("Driver | Rider")
    for match in matchings:
        print("   " + str(match[0]) + "  <=>  " + str(match[1]))

def question_9_d():
    probabilities = [0.0001, 0.001, 0.005, 0.01, 0.02, 0.03, 0.04, 0.05, 0.1]
    n = 100
    for p in probabilities:
        avg_matchings = 0
        for i in range(50):
            avg_matchings += num_matchings_n_p(n, p)
        avg_matchings = avg_matchings/50
        print("p = " + str(p) + " | probability = " + str(avg_matchings/n))

    
# for given n and p, create random matchings and run maxflow to find max matches
def num_matchings_n_p(n, p):
    graph = []
    for d in range(n):
        for r in range(n):
            if random.random() <= p:
                graph.append((d + 1, r + n + 1,1))
    sink = 2 * n + 1
    for i in range(n):
        graph.append((0, i + 1, 1))
    for i in range(n):
        graph.append((i + n + 1, sink, 1))

    G = create_graph_from_connections_flow(2 + 2 * n, graph)

    matchings = max_flow(G, 0, sink)
    # print("Number of Matchings:" + str(len(matchings)))
    # print("Driver | Rider")
    # for match in matchings:
    #     print("   " + str(match[0]) + "  <=>  " + str(match[1]))
    return matchings

# question_9_a()
# question_9_c()
question_9_d()