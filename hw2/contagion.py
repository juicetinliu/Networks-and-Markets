# Justin Liu
# include any code you need for your assignment in this file or in auxiliary
# files that can be imported here.
import math
import random
from collections import defaultdict

# Graph wrapper object to store values and connections
class Graph:
    def __init__(self, connections, values=None):
        self.connections = connections
        if values is None:
            self.values = ['Y' for c in self.connections]
        else:
            assert len(values) == len(connections)
            self.values = values

    def print(self):
        for node, neighbor_nodes in self.connections.items():
            print(node, self.values[node], neighbor_nodes)
    
    def print_values(self, every_node=False):
        total_X = 0
        size = len(self.connections)
        for node in self.connections:
            if self.values[node] == 'X':
                total_X += 1
            if every_node:
                print(node, self.values[node])
        print("Number of nodes:" + str(size))
        print("Number of X's:" + str(total_X))
        # print("Number of Y's:" + str(size-total_X))
    
    def infected_values(self):
        total_X = 0
        size = len(self.connections)
        for node in self.connections:
            if self.values[node] == 'X':
                total_X += 1
            # print(node, self.values[node])
        return total_X

        

# given a list of tuples (of edges), create a graph(connections)
def create_graph_from_connections(connection_list, text=None):
    graph = defaultdict(list) 
    if text is None:
        for i in range(len(connection_list)):
            graph[i] = []
        for pair in connection_list:
            i = int(pair[0])
            j = int(pair[1])
            graph[j].append(i)
            graph[i].append(j)
    else:
        text_file_r = open(text, "r")
        for i in range(4039):
            graph[i] = []
        
        for x in text_file_r:
            nodepair = x.split()
            i = int(nodepair[0])
            j = int(nodepair[1])
            graph[j].append(i)
            graph[i].append(j)
        text_file_r.close()
    return graph

# given number of nodes n and probability p, output a random graph(connections)
def create_graph(n, p=None):
    connect_dict = defaultdict(list) # a dict where each node is linked to list of connected nodes
    for i in range(n):
        connect_dict[i] = []
    for i in range(n):
        for j in range(i + 1, n):
            if random.random() <= p:
                connect_dict[i].append(j)
                connect_dict[j].append(i)
    return connect_dict

# 8 (a)
# implement an algorithm that given a graph G, set of adopters S,
# and a threshold q performs BRD where the adopters S never change.
def contagion_brd(G, S, q):
    # G: dictionary
    # S: list of ints
    # q: float
    # start by changing G with set S
    for infector in S:
        G.values[infector] = 'X'

    converged = False
    iterations = 0
    while not (converged or iterations > len(G.values)):
        iterations += 1
        converged = True
        loop = True
        for node, neighbor_nodes in G.connections.items():
            if loop and G.values[node] != 'X': #only infect uninfected nodes
                total = 0
                for neighbor in neighbor_nodes:
                    if G.values[neighbor] == 'X':
                        total += 1
                if total/len(neighbor_nodes) >= q:
                    G.values[node] = 'X'
                    converged = False #can't converge if an infection occurs
                    # loop = False # comment out to run fast
    # print("iterations:" + str(iterations))

# generates a list of n random numbers from 0 to maxval
def random_list(n, maxval):
    assert maxval >= n
    out_list = []
    while len(out_list) < n:
        num = random.randrange(maxval)
        if num not in out_list:
            out_list.append(num)
    return out_list


def question_8_a():
    # 4.1a
    q = 0.5
    connection_list = [(0, 1), (1, 2), (2, 3)]
    connections = create_graph_from_connections(connection_list)
    G = Graph(connections)
    contagion_brd(G, [0, 1], q)
    print("(4.1a) After Contagion BRD for q = " + str(q) + ":")
    G.print_values(True)

    # 4.1b
    q = 0.3333333
    connection_list = [(0, 1), (1, 2), (2, 3), (4,1), (5,2), (6,3)]
    connections = create_graph_from_connections(connection_list)
    G = Graph(connections)
    contagion_brd(G, [0, 1], q)
    print("(4.1b) After Contagion BRD for q = " + str(q) + ":")
    G.print_values(True)

def run_contagion_multiple(n, k, q, log=True):
    connections = create_graph_from_connections([], "facebook_combined.txt")
    average_infected = 0
    max_infected = 0
    min_infected = 5000
    for x in range(n):
        if log:
            print("======" + str(x+1) + "======")
        G = Graph(connections)
        contagion_brd(G, random_list(k, 4039), q)
        infected = G.infected_values()
        if log:
            G.print_values()
            print("===============")
        average_infected += infected
        max_infected = max(max_infected, infected)
        min_infected = min(min_infected, infected)
    average_infected = average_infected/n
    return average_infected, max_infected, min_infected

def question_8_b():
    average_infected, max_infected, min_infected = run_contagion_multiple(100, 10, 0.1, False)
    print("Average Infected: " + str(average_infected) + " (" + str(round(average_infected/40.39, 2)) + "%)")
    print("Maximum Infected: " + str(max_infected) + " (" + str(round(max_infected/40.39, 2)) + "%)")
    print("Minimum Infected: " + str(min_infected) + " (" + str(round(min_infected/40.39, 2)) + "%)")

def question_8_c():
    # print("======== k=10 ========")
    for k in range(26):
        k_step = k*10
        for q in range(11):
            q_step = q/20
            average_infected, max_infected, min_infected = run_contagion_multiple(10, k_step, q_step, False)
            print("q=" + str(q_step) + "|k=" + str(k_step) + "| Average Infected: " + str(average_infected) + " (" + str(round(average_infected/40.39, 2)) + "%)")
    # print("======== q=0.5 ========")
    # for k in range(26):
    #     k_step = k*10
    #     average_infected, max_infected, min_infected = run_contagion_multiple(10, k_step, 0.5, False)
    #     print("k=" + str(k_step) + "| Average Infected: " + str(average_infected) + " (" + str(round(average_infected/40.39, 2)) + "%)")
    # print("======== q=0.15 ========")
    # for k in range(26):
    #     k_step = k*10
    #     average_infected, max_infected, min_infected = run_contagion_multiple(10, k_step, 0.15, False)
    #     print("k=" + str(k_step) + "| Average Infected: " + str(average_infected) + " (" + str(round(average_infected/40.39, 2)) + "%)")

# question_8_a()
# question_8_b()
question_8_c()