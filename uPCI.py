import pickle
import matplotlib.pyplot as plt


u = 1


def save_obj(obj, name ):
    with open(name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


def load_obj(name ):
    with open(name + '.pkl', 'r') as f:
        return pickle.load(f)


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


def decompose_graph(graph, kshell):
    nodes_to_remove = [-1]
    removed_nodes = []
    # If nodes were removed, repeat process
    while len(nodes_to_remove) > 0:
        nodes_to_remove = []
        for node in graph:
            # If node with kshell connections exists remove it
            if len(graph[node]) <= kshell:
                nodes_to_remove.append(node)
        # Add only non deleted nodes to new graph
        if len(nodes_to_remove) > 0:
            new_graph = {}
            for node in graph:
                # Add node
                if node not in nodes_to_remove:
                    new_graph[node] = []
                    # Add connections
                    for connection in graph[node]:
                        if connection not in nodes_to_remove:
                            new_graph[node].append(connection)
            graph = new_graph
            removed_nodes += nodes_to_remove
    return graph, removed_nodes


def kshell_for_every_node(graph):
    kshells = {}
    kshell = 0
    while len(graph) > 0:
        graph, removed_nodes = decompose_graph(graph, kshell)
        kshells[kshell] = removed_nodes
        kshell += 1
    return sorted(kshells.iteritems())


def draw_upci(graph):
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


def draw_kshell(graph):
    kshell_nodes = load_obj('kshell')
    #kshell_nodes = kshell_for_every_node(graph)
    #save_obj(kshell_nodes, 'kshell')
    x = []
    y = []
    for (kshell, nodes) in kshell_nodes:
        for index, node in enumerate(nodes):
            x.append(kshell / 2)
            y.append(len(graph[node]))
    plt.plot(x, y, 'ro')
    plt.yscale('log')
    plt.axis([0, 60, 0, 1000])
    plt.show()


def main():
    graph = read_file("ca-AstroPh.txt")
    #print get_most_influential_nodes_upci(graph, 10)

    # Draw uPCI
    #draw_upci(graph)

    # Draw k-shell
    draw_kshell(graph)

if __name__ == "__main__":
    main()
