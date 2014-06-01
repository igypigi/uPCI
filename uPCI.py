import matplotlib.cm as cm
import matplotlib.pyplot as plt


u = 1


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


def compute_upci(graph, node):
    neighbours_degree = []
    for neighbour in graph[node]:
        neighbours_degree.append(len(graph[neighbour]))
    neighbours_degree.sort(reverse=True)

    for neighbour_degree in neighbours_degree:
        k = -0
        e = +0
        for d in neighbours_degree:
            if d > neighbour_degree:
                k += 1
            elif d == neighbour_degree:
                e += 1
        if k <= u * neighbour_degree <= k + e:
            return neighbour_degree
    return -1


def upci_for_every_node(graph):
    upcis = {}
    for node in graph:
        upci = compute_upci(graph, node)
        if upci not in upcis:
            upcis[upci] = []
        upcis[upci].append(node)
    return sorted(upcis.iteritems())


def get_most_influential_nodes_upci(graph, number_of_nodes=1):
    influential_nodes = []
    for (upci, nodes) in upci_for_every_node(graph):
        influential_nodes += nodes
        if len(influential_nodes) >= number_of_nodes:
            break
    return influential_nodes[:number_of_nodes]


def main():
    graph = read_file("ca-AstroPh.txt")
    #print get_most_influential_nodes_upci(graph, 10)
    upci_nodes = upci_for_every_node(graph)
    x = []
    y = []
    for (upci, nodes) in upci_nodes:
        for node in nodes:
            x.append(upci/2)
            y.append(len(graph[node]))
    plt.plot(x, y, 'ro')
    plt.yscale('log')
    plt.axis([0, 120, 0, 1000])
    plt.show()


if __name__ == "__main__":
    main()
