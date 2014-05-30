from random import random


def read_file(file_name):
    graph = {}
    for line in open(file_name).readlines():
        (n1, n2) = [int(x) for x in line.strip().split('\t')]
        if n1 not in graph:
            graph[n1] = []
        graph[n1].append(n2)
        if n2 not in graph:
            graph[n2] = []
        graph[n2].append(n1)
    return graph


def uPCI(node):
    # TODO: calculate uPCI
    return int(random()*20)


def uPCI_for_every_node(graph):
    uPCIs = {}
    for node in graph:
        upci = uPCI(node)
        if upci not in uPCIs:
            uPCIs[upci] = []
        uPCIs[upci].append(node)
    return sorted(uPCIs.iteritems())


def get_most_influential_nodes(graph, number_of_nodes=1):
    influential_nodes = []
    for (upci, nodes) in uPCI_for_every_node(graph):
        influential_nodes += nodes
        if len(influential_nodes) >= number_of_nodes:
            break
    return influential_nodes[:number_of_nodes]


def main():
    graph = read_file("CA-CondMat.txt")
    print get_most_influential_nodes(graph, 10)

if __name__ == "__main__":
    main()
