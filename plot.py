import matplotlib.pyplot as plt

from enum import Enum
from graph import Graph
from collections.abc import Iterable


class Color(Enum):
    RED   = "#ff6961"
    GREY  = "#f5f5f5"
    BLACK = "#d5d5d5"


def _points(graph: Graph, vertices: Iterable[int], color: Color, z = 0):
    x = []
    y = []

    for vertex in vertices:
        coord = graph.coords[vertex]
        x.append(coord.x)
        y.append(coord.y)

    plt.scatter(x, y, s = 15, c = color.value, zorder = z)


def vertices(graph: Graph):
    _points(graph, graph, Color.BLACK)
    plt.savefig("Vertices.png", dpi = 250)


def path(graph: Graph, dist: float, path: list[int], visited: set[int], title: str):
    plt.clf()

    plt.suptitle(f"{title}")
    plt.title(f"Distance: {dist :.2f}", fontsize = 5)

    # Plot vertices as points
    _points(graph, graph,   Color.GREY,  0)
    _points(graph, visited, Color.BLACK, 1)
    _points(graph, path,    Color.RED,   2)

    # Plot edges in the path as arrows
    for i in range(len(path) - 1):
        x, y = graph.coords[path[i]]

        neighbor = graph.coords[path[i + 1]]
        dx = neighbor.x - x
        dy = neighbor.y - y

        plt.arrow(x, y, dx, dy, length_includes_head = True, head_width = 0.01 * len(graph), head_length = 0.025 * len(graph), color = Color.RED.value, zorder = 3)

    plt.savefig(title + ".png", dpi = 250)
