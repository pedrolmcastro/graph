import sys
import math
import time
import random
import search

from enum import Enum
from graph import Graph
from typing import Callable


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

    dist, path, _ = search.dfs(graph, src, goal)
    print(f"DFS: {path} ({dist :.2f})")

    dist, path, _ = search.bfs(graph, src, goal)
    print(f"BFS: {path} ({dist :.2f})")

    dist, path, _ = search.bestfirst(graph, src, goal)
    print(f"Best First: {path} ({dist :.2f})")

    dist, path, _ = search.dijkstra(graph, src, goal)
    print(f"Dijkstra: {path} ({dist :.2f})")

    dist, path, _ = search.astar(graph, src, goal)
    print(f"A*: {path} ({dist :.2f})")


def measure():
    REPEAT = 20

    def randvertices():
        while True:
            src = random.randint(0, len(graph) - 1)
            goal = random.randint(0, len(graph) - 1)

            if reachable(graph, src, goal):
                return src, goal

    def timeit(algo: Callable[[Graph, int, int], tuple[float, list[int], set[int]]]):
        """Executes the algorithm and measures it's time"""
        start = time.time()
        dist, path, _ = algo(graph, src, goal)
        return time.time() - start, dist, len(path)

    def accumulate(algo: str, timed: float, dist: float, path: int):
        """Accumulates the algorithm results in the dict"""
        if algo not in results:
            results[algo] = [0.0, 0.0, 0]

        results[algo][0] += timed
        results[algo][1] += dist
        results[algo][2] += path

    for graph in (Graph(5000, 3), Graph(5000, 5), Graph(5000, 7)):
        stress(str(graph))
        results: dict[str, list[float, float, int]] = {}

        for _ in range(REPEAT):
            src, goal = randvertices()

            accumulate("DFS", *timeit(search.dfs))
            accumulate("BFS", *timeit(search.bfs))
            accumulate("Best First", *timeit(search.bestfirst))
            accumulate("Dijkstra", *timeit(search.dijkstra))
            accumulate("A*", *timeit(search.astar))

        for algo, (timed, dist, path) in results.items():
            print(
                f"{algo}                               \n"
                f"Time: {timed * 1000 / REPEAT :.2f}ms \n"
                f"Dist: {dist / REPEAT :.2f}           \n"
                f"Path: {path / REPEAT :.2f}           \n"
            )


def reachable(graph: Graph, src: int, goal: int):
    return search.astar(graph, src, goal)[0] != math.inf


def error(message: str):
    print("\033[31m", end = "") # Set font color to red
    print(f"Error: {message}!")
    print("\033[0m", end = "")  # Reset font color

def stress(message: str):
    print("\033[36m", end = "") # Set font color to blue
    print(message, end = "\n\n")
    print("\033[0m", end = "")  # Reset font color


if __name__ == "__main__":
    main()
