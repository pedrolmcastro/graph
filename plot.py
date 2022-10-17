import matplotlib

import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

from graph import Graph


# Change rc font
matplotlib.rc("font", **{"family": "sans-serif", "sans-serif": ["Ubuntu"]})


def graph(graph: Graph):
    # Create ploted graph
    ploted = nx.DiGraph()
    labels = {}

    for vertex in graph:
        labels[vertex] = vertex
        ploted.add_node(vertex, pos = tuple(graph.coords[vertex]))

    fig, ax = plt.subplots(figsize = (10, 10))

    # Plot Vertices
    pos = nx.get_node_attributes(ploted, "pos")
    nx.draw_networkx_nodes(ploted, pos, node_size = 200, node_color = "gray", alpha = 0.4, ax = ax)
    nx.draw_networkx_labels(ploted, pos, labels, font_family = "sans-serif", font_size = 6, ax = ax)

    # Box
    ax.tick_params(left = True, bottom = True, labelleft = True, labelbottom = True)
    plt.title("Grafo")

    # Scale
    corr = int(graph.vertices * 0.05)
    fig.gca().set_aspect("equal", adjustable = "box")
    plt.xlim(0 - corr, graph.vertices + corr)
    plt.ylim(0 - corr, graph.vertices + corr)

    fig.savefig("Grafo.png", dpi = 250)


def path(graph: Graph, dist: float, path: list[int], visited: set[int], title: str):
    # Create ploted graph
    ploted = nx.DiGraph()
    labels = {}

    for vertex in path:
        labels[vertex] = vertex

    for vertex in visited | set(path):
        ploted.add_node(vertex, pos = tuple(graph.coords[vertex]))

    # Add edges
    for vertex, nxt in zip(path, path[1:]):
        adj = [item for item in graph[vertex] if item.neighbor == nxt][0]
        ploted.add_edge(vertex, nxt, weight = round(adj.weight, 2))

    fig, ax = plt.subplots(figsize = (10, 10))

    pos = nx.get_node_attributes(ploted, "pos")

    # Path vertices
    nx.draw_networkx_nodes(ploted, pos, nodelist = path, node_size = 600, node_color = range(len(path)), cmap = plt.cm.cool, alpha = 1, edgecolors = "black", ax = ax)
    nx.draw_networkx_labels(ploted, pos, labels, font_family = "sans-serif", font_size = 10, ax = ax)

    # Visited vertices
    nx.draw_networkx_nodes(ploted, pos, nodelist = visited, node_size = 200, node_color = "gray", alpha = 0.1, ax = ax)

    # Edges
    nx.draw_networkx_edges(ploted, pos, edgelist = ploted.edges, width = 0.5, edge_color = "black", ax = ax)
    nx.draw_networkx_edge_labels(ploted, pos, nx.get_edge_attributes(ploted, "weight"), font_family = "sans-serif", font_size = 8, ax = ax)

    # Legend
    cm = plt.cm.cool(range(256))
    legend = [
        mpatches.Patch(color = cm[0],  label = "Origem"),
        mpatches.Patch(color = cm[-1], label = "Destino"),
        mpatches.Patch(color = "gray", label = "Visitado"),
    ]

    # Box
    ax.tick_params(left = True, bottom = True, labelleft = True, labelbottom = True)
    plt.title(f"{title} [Distância {dist :.2f}]")
    plt.legend(handles = legend)

    # Scale
    corr = int(graph.vertices * 0.05)
    fig.gca().set_aspect("equal", adjustable = "box")
    plt.xlim(0 - corr, graph.vertices + corr)
    plt.ylim(0 - corr, graph.vertices + corr)

    fig.savefig(title + ".png", dpi = 250)
