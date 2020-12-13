# Justin Liu
# include any code you need for your assignment in this file or in auxiliary
# files that can be imported here. 
import math
import random
from collections import defaultdict

# given number of nodes n and probability p, output a random graph 
# as specified in homework
def create_graph(n, p):
    connect_dict = defaultdict(list) # a dict where each node is linked to list of connected nodes
    for i in range(n):
        connect_dict[i] = []
    for i in range(n):
        for j in range(i + 1, n):
            if random.random() <= p:
                connect_dict[i].append(j)
                connect_dict[j].append(i)
    return connect_dict

# given a graph G and nodes i,j, output the length of the shortest
# path between i and j in G.
def shortest_path(G, i, j):
    visited = [False for node in G] # boolean array to hold visited nodes
    path_queue = [[i]] # use a queue to hold next path+nodes to look for in BFS
    if i == j: # ... for cases where the starting is the end node
        return 0

    while path_queue: # while queue isn't empty
        curr_path = path_queue.pop(0) # retrieve next path
        curr_node = curr_path[-1] # and the newest node on that path

        for neighbor_node in G[curr_node]: # for all neighbor nodes
            if not visited[neighbor_node]: # that haven't been visited
                new_path = curr_path.copy() 
                new_path.append(neighbor_node) # add them onto this path
                
                path_queue.append(new_path) # store this new path for further exploration

                if neighbor_node == j: # if we reach the target node
                    return len(new_path) - 1 # output path length

        visited[curr_node] = True # finally set this node to visited
    return math.inf # this is triggered when no path is found

def print_graph(G):
    for node,neighbor_nodes in G.items():
        print(node, neighbor_nodes)

def rand_node_pair(range): # makes sure that two randomly generate nodes aren't equal.
    node1 = random.randrange(range)
    node2 = random.randrange(range)
    while node1 == node2:
        node2 = random.randrange(range)
    return [node1, node2]

def question_8_c():
    graph = create_graph(1000, 0.1)

    text_file = open("avg_shortest_path.txt", "w")
    average_shortest = 0.0

    for num in range(1000):
        nodes = rand_node_pair(1000)
        shortest = shortest_path(graph, *nodes)
        average_shortest += shortest
        text_line = "(" + str(nodes[0]) + "," + str(nodes[1]) + "," + str(shortest) + ")"
        text_file.write(text_line + "\n")

    average_shortest = average_shortest / 1000.0
    print(average_shortest)
    text_file.close()

def question_8_d():
    

    text_file = open("varying_p.txt", "w")

    disconnected_graph = False
    while not disconnected_graph:
        text_file.close()
        text_file = open("varying_p.txt", "w")
        p = 0.01 # 0.01
        graph = create_graph(1000, p)
        average_shortest = 0.0
        text_file.write("================== p:" + str(p) + " ==================" + "\n")

        for num in range(1000):
            nodes = rand_node_pair(1000)
            shortest = shortest_path(graph,*nodes)
            if shortest == math.inf:
                disconnected_graph = True
            average_shortest += shortest
            text_line = "(" + str(nodes[0]) + "," + str(nodes[1]) + "," + str(shortest) + ")"
            text_file.write(text_line + "\n")

        if not disconnected_graph:
            average_shortest = average_shortest / 1000.0
            print(p, average_shortest)


    for inc in range(1,4): 
        p = (inc + 1) * 0.01 # 0.02 to 0.04
        graph = create_graph(1000, p)
        average_shortest = 0.0
        text_file.write("================== p:" + str(p) + " ==================" + "\n")

        for num in range(1000):
            nodes = rand_node_pair(1000)
            shortest = shortest_path(graph,*nodes)
            average_shortest += shortest
            text_line = "(" + str(nodes[0]) + "," + str(nodes[1]) + "," + str(shortest) + ")"
            text_file.write(text_line + "\n")
        
        average_shortest = average_shortest / 1000.0
        print(p, average_shortest)

    for inc in range(10): 
        p = (inc + 1) * 0.05 # 0.05 to 0.5
        graph = create_graph(1000, p)
        average_shortest = 0.0
        text_file.write("================== p:" + str(p) + " ==================" + "\n")

        for num in range(1000):
            nodes = rand_node_pair(1000)
            shortest = shortest_path(graph,*nodes)
            average_shortest += shortest
            text_line = "(" + str(nodes[0]) + "," + str(nodes[1]) + "," + str(shortest) + ")"
            text_file.write(text_line + "\n")
        
        average_shortest = average_shortest / 1000.0
        print(p, average_shortest)

    text_file.close()

def question_9_a():
    text_file_r = open("facebook_combined.txt", "r")
    graph = defaultdict(list) 

    for i in range(4039):
        graph[i] = []
    
    for x in text_file_r:
        nodepair = x.split()
        i = int(nodepair[0])
        j = int(nodepair[1])
        graph[j].append(i)
        graph[i].append(j)
    text_file_r.close()

    text_file_w = open("fb_shortest_path.txt", "w")
    average_shortest = 0.0

    for num in range(1000):
        nodes = rand_node_pair(4039)
        shortest = shortest_path(graph, *nodes)
        average_shortest += shortest
        text_line = "(" + str(nodes[0]) + "," + str(nodes[1]) + "," + str(shortest) + ")"
        text_file_w.write(text_line + "\n")

    average_shortest = average_shortest / 1000.0
    print(average_shortest)
    text_file_w.close()

def question_9_c():
    graph = create_graph(4039, 0.011)

    average_shortest = 0.0

    for num in range(1000):
        nodes = rand_node_pair(4039)
        shortest = shortest_path(graph, *nodes)
        average_shortest += shortest

    average_shortest = average_shortest / 1000.0
    print(average_shortest)


# question_8_c()
# question_8_d()
# question_9_a()
# question_9_c()