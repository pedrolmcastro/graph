import sys
import math
import search

from enum import Enum
from graph import Graph


class Mode(Enum):
    DISPLAY = "display"
    MEASURE = "measure"


def main():
    mode = sys.argv[1].lower() if len(sys.argv) > 1 else Mode.DISPLAY.value

    if mode == Mode.DISPLAY.value:
        display()
    elif mode == Mode.MEASURE.value:
        measure()
    else:
        error(f"Unknown execution mode '{mode}'")


def display():
    # TODO: Graphic path

    def reachable(graph: Graph, src: int, goal: int):
        return search.astar(graph, src, goal, lambda curr, goal: graph.dist(curr, goal))[0] != math.inf

    def readgraph():
        while True:
            try:
                vertices = int(input("Vertices: "))
                neighbors = int(input("Neighbors: "))
            except Exception:
                error("Invalid integer")
            else:
                if vertices < 2:
                    error("Number of vertices must be greater or equal to 2")
                elif neighbors < 1 or neighbors >= vertices:
                    error("Number of neighbors must be between 1 and vertices - 1")
                else:
                    return Graph(vertices, neighbors)

    def readvertices():
        while True:
            try:
                src = int(input("Source: "))
                goal = int(input("Goal: "))
            except Exception:
                error("Invalid integer")
            else:
                if src < 0 or src >= len(graph):
                    error("Source must be between 0 and vertices - 1")
                elif goal < 0 or goal >= len(graph):
                    error("Goal must be between 0 and vertices - 1")
                elif not reachable(graph, src, goal):
                    error("Goal unreachable from source")
                else:
                    return src, goal

    graph = readgraph()
    src, goal = readvertices()

    print()
    print(graph)
    print(f"Path from {src} to {goal}", end = "\n\n")

    dist, path, _ = search.dfs(graph, src, goal)
    print(f"DFS: {path} ({dist :.2f})")

    dist, path, _ = search.bfs(graph, src, goal)
    print(f"BFS: {path} ({dist :.2f})")

    dist, path, _ = search.bestfirst(graph, src, goal)
    print(f"Best First: {path} ({dist :.2f})")

    dist, path, _ = search.dijkstra(graph, src, goal)
    print(f"Dijkstra: {path} ({dist :.2f})")

    dist, path, _ = search.astar(graph, src, goal, lambda curr, goal: graph.dist(curr, goal))
    print(f"A*: {path} ({dist :.2f})")


def measure():
    # TODO: Timing and profiling
    pass


def error(message: str):
    print("\033[31m", end = "") # Set font color to red
    print(f"Error: {message}!")
    print("\033[0m", end = "")  # Reset font color


if __name__ == "__main__":
    main()
