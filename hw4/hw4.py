# Justin Liu
from collections import defaultdict

class DirectedGraph:
    def __init__(self, number_of_nodes):
        self.number_of_nodes = number_of_nodes
        self.graph = self.create_graph(number_of_nodes)
        self.graph_reverse = self.create_graph(number_of_nodes)
        pass
    
    def add_edge(self, origin_node, destination_node):
        if destination_node not in self.graph[origin_node]:
            self.graph[origin_node].append(destination_node)
        if origin_node not in self.graph_reverse[destination_node]:
            self.graph_reverse[destination_node].append(origin_node)
        pass
    
    def edges_from(self, origin_node):
        ''' This method shold return a list of all the nodes u such that the edge (origin_node,u) is 
        part of the graph.'''
        return self.graph[origin_node]

    def edges_to(self, origin_node):
        ''' This method shold return a list of all the nodes u such that the edge (u, origin_node) is 
        part of the graph.'''
        return self.graph_reverse[origin_node]
    
    def check_edge(self, origin_node, destination_node):
        ''' This method should return true is there is an edge between origin_node
        and destination_node, and false otherwise'''
        return destination_node in self.graph[origin_node]
    
    def number_of_nodes(self):
        ''' This method should return the number of nodes in the graph'''
        return self.number_of_nodes
    
    def create_graph(self, num_nodes):
        graph = defaultdict(list) 
        for i in range(num_nodes):
            graph[i] = []
        return graph
    
    def print(self):
        for node,neighbor_nodes in self.graph.items():
            print(node, neighbor_nodes)
        pass
    
def scaled_page_rank(graph, num_iter, eps = 1/7.0):
    ''' This method, given a directed graph, should run the epsilon-scaled page-rank
    algorithm for num-iter iterations and return a mapping (dictionary) between a node and its weight. 
    In the case of 0 iterations, all nodes should have weight 1/number_of_nodes'''    
    iter = num_iter
    num_nodes = graph.number_of_nodes
    
    new_score = 1/num_nodes
    
    eps_over_n = eps/num_nodes
    one_min_eps = 1 - eps
    
    scores = defaultdict(list) 
    for node in range(num_nodes):
        scores[node] = new_score
    
    while iter > 0:
        new_scores = []
        for node in range(num_nodes):
            sum_scores = 0
            for n_node in graph.edges_to(node):
                sum_scores += scores[n_node] / len(graph.edges_from(n_node))
            new_scores.append(eps_over_n + one_min_eps * sum_scores)
        
        for n, score in enumerate(new_scores):
            scores[n] = score
        iter -= 1
    
    return scores

def graph_15_1_left():
    ''' This method, should construct and return a DirectedGraph encoding the left example in fig 15.1
    Use the following indexes: A:0, B:1, C:2, Z:3 '''    
    graph = DirectedGraph(4)
    graph.add_edge(0, 1)
    graph.add_edge(0, 3)
    graph.add_edge(1, 2)
    graph.add_edge(2, 0)
    graph.add_edge(3, 3)
    return graph

def graph_15_1_right():
    ''' This method, should construct and return a DirectedGraph encoding the right example in fig 15.1
    Use the following indexes: A:0, B:1, C:2, Z1:3, Z2:4'''    
    graph = DirectedGraph(5)
    graph.add_edge(0, 1)
    graph.add_edge(0, 3)
    graph.add_edge(0, 4)
    graph.add_edge(1, 2)
    graph.add_edge(2, 0)
    graph.add_edge(3, 4)
    graph.add_edge(4, 3)
    return graph

def graph_15_2():
    ''' This method, should construct and return a DirectedGraph encoding example 15.2
        Use the following indexes: A:0, B:1, C:2, A':3, B':4, C':5'''
    graph = DirectedGraph(6)
    graph.add_edge(0, 1)
    graph.add_edge(1, 2)
    graph.add_edge(2, 0)
    graph.add_edge(3, 4)
    graph.add_edge(4, 5)
    graph.add_edge(5, 3)
    return graph

def extra_graph_1():
    ''' This method, should construct and return a DirectedGraph of your choice with at least 10 nodes'''    
    graph = DirectedGraph(10)
    graph.add_edge(0, 0)
    graph.add_edge(1, 0)
    graph.add_edge(2, 0)
    graph.add_edge(3, 0)
    graph.add_edge(4, 0)
    graph.add_edge(5, 0)
    graph.add_edge(6, 0)
    graph.add_edge(7, 0)
    graph.add_edge(8, 0)
    graph.add_edge(9, 0)
    graph.add_edge(9, 1)
    graph.add_edge(1, 2)
    graph.add_edge(2, 3)
    graph.add_edge(3, 4)
    graph.add_edge(4, 5)
    graph.add_edge(5, 6)
    graph.add_edge(6, 7)
    graph.add_edge(7, 8)
    graph.add_edge(8, 9)
    return graph

# This dictionary should contain the expected weights for each node when running the scaled page rank on the extra_graph_1 output
# with epsilon = 0.07 and num_iter = 20.
extra_graph_1_weights = {0: 0.8822428159108227, 1: 0.013084131565464101, 2: 0.013084131565464101, 3: 0.013084131565464101, 4: 0.013084131565464101, 5: 0.013084131565464101, 6: 0.013084131565464101, 7: 0.013084131565464101, 8: 0.013084131565464101, 9: 0.013084131565464101}

def extra_graph_2():
    ''' This method, should construct and return a DirectedGraph of your choice with at least 10 nodes'''    
    graph = DirectedGraph(10)
    for j in range(10):
        for i in range(10):
            if j != i:
                graph.add_edge(i, j)
    return graph

# This dictionary should contain the expected weights for each node when running the scaled page rank on the extra_graph_2 output
# with epsilon = 0.07 and num_iter = 20.
extra_graph_2_weights = {0: 0.1, 1: 0.1, 2: 0.1, 3: 0.1, 4: 0.1, 5: 0.1, 6: 0.1, 7: 0.1, 8: 0.1, 9: 0.1}


def facebook_graph(filename = "facebook_combined.txt"):
    ''' This method should return a DIRECTED version of the facebook graph as an instance of the DirectedGraph class.
    In particular, if u and v are friends, there should be an edge between u and v and an edge between v and u.'''  
    text_file_r = open(filename, "r")
    graph = DirectedGraph(4039)
    
    for x in text_file_r:
        nodepair = x.split()
        i = int(nodepair[0])
        j = int(nodepair[1])
        graph.add_edge(i,j)
        graph.add_edge(j,i)
    text_file_r.close()  
    return graph

def print_scores(scores):
    for node, score in scores.items():
        print(str(node) + ": " + str(round(score, 3)))
    pass

# The code necessary for your measurements for question 8b should go in this function.
# Please COMMENT THE LAST LINE OUT WHEN YOU SUBMIT (as it will be graded by hand and we do not want it to interfere
# with the automatic grader).
def question7b():
    def stats(graph, scores, num_samples = 1, facebook = False):
        num_nodes = graph.number_of_nodes
        sorted_scores = sorted(scores.items(), key = lambda x: x[1], reverse = True)
        sorted_edges_from = sorted(graph.graph.items(), key = lambda x: len(graph.edges_from(x[0])), reverse = True)
        sorted_edges_to = sorted(graph.graph.items(), key = lambda x: len(graph.edges_to(x[0])), reverse = True)
        

        if facebook:
            print("Top " + str(num_samples) + " Max Scores:")
            for i in range(num_samples):
                node, score = sorted_scores[i]
                print("(" + str(i + 1) + ") Node " + str(node) + " | Score: " + str(round(score, 3)) + " | Edges: " + str(len(graph.edges_from(node))))

            print("Top " + str(num_samples) + " Max Edges:")
            for i in range(num_samples):
                node, num = sorted_edges_to[i]
                print("(" + str(i + 1) + ") Node " + str(node) + " | Num Edges: " + str(len(num)))
            
            print("Top " + str(num_samples) + " Min Scores:")
            for i in range(num_samples):
                node, score = sorted_scores[num_nodes - i - 1]
                print("(" + str(i + 1) + ") Node " + str(node) + " | Score: " + str(round(score, 3)) + " | Edges: " + str(len(graph.edges_from(node))))
            
            print("Top " + str(num_samples) + " Min Edges:")
            for i in range(num_samples):
                node, num = sorted_edges_from[num_nodes - i - 1]
                print("(" + str(i + 1) + ") Node " + str(node) + " | Num Edges: " + str(len(num)))
        else:
            for i in range(num_samples):
                node, score = sorted_scores[i]
                print("(" + str(i) + ") Max Score: Node " + str(node) + " | Score: " + str(round(score, 3)) + " | Out: " + str(len(graph.edges_from(node))) + " | In: " + str(len(graph.edges_to(node))))

            for i in range(num_samples):
                node, num = sorted_edges_from[i]
                print("(" + str(i) + ") Max Out Edges: Node " + str(node) + " | Num: " + str(len(num)) + " | Out: " + str(len(graph.edges_from(node))) + " | In: " + str(len(graph.edges_to(node))))

            for i in range(num_samples):
                node, num = sorted_edges_to[i]
                print("(" + str(i) + ") Max In Edges: Node " + str(node) + " | Num: " + str(len(num)) + " | Out: " + str(len(graph.edges_from(node))) + " | In: " + str(len(graph.edges_to(node))))

            for i in range(num_samples):
                node, score = sorted_scores[num_nodes - i - 1]
                print("(" + str(i) + ") Min Score: Node " + str(node) + " | Score: " + str(round(score, 3)) + " | Out: " + str(len(graph.edges_from(node))) + " | In: " + str(len(graph.edges_to(node))))
            
            for i in range(num_samples):
                node, num = sorted_edges_from[num_nodes - i - 1]
                print("(" + str(i) + ") Min Out Edges: Node " + str(node) + " | Num: " + str(len(num)) + " | Out: " + str(len(graph.edges_from(node))) + " | In: " + str(len(graph.edges_to(node))))

            for i in range(num_samples):
                node, num = sorted_edges_to[num_nodes - i - 1]
                print("(" + str(i) + ") Min In Edges: Node " + str(node) + " | Num: " + str(len(num)) + " | Out: " + str(len(graph.edges_from(node))) + " | In: " + str(len(graph.edges_to(node))))

    print("graph_15_1_left:")
    graph = graph_15_1_left()
    scores_1 = scaled_page_rank(graph, 10)
    print_scores(scores_1)
    stats(graph, scores_1)
    
    print("graph_15_1_right:")
    graph = graph_15_1_right()
    scores_2 = scaled_page_rank(graph, 10)
    print_scores(scores_2)
    stats(graph, scores_2)
    
    print("graph_15_2:")
    graph = graph_15_2()
    scores_3 = scaled_page_rank(graph, 10)
    print_scores(scores_3)
    stats(graph, scores_3)
    
    print("extra_graph_1:")
    graph = extra_graph_1()
    scores_4 = scaled_page_rank(graph, 10)
    print_scores(scores_4)
    stats(graph, scores_4)
    
    print("extra_graph_2:")
    graph = extra_graph_2()
    scores_5 = scaled_page_rank(graph, 10)
    print_scores(scores_5)
    stats(graph, scores_5)

    print("facebook_graph:")
    graph = facebook_graph()
    scores_f = scaled_page_rank(graph, 10)
    stats(graph, scores_f, num_samples=10, facebook=True)
    # print_scores(scores_f)

    
    pass

# question7b()
