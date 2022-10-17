import sys
import math
import plot
import time
import random
import search

from enum import Enum
from graph import Graph
from typing import Callable
from dataclasses import dataclass


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

    plot.graph(graph)

    for title, algo in {"DFS": search.dfs, "BFS": search.bfs, "Best First": search.bestfirst, "Dijkstra": search.dijkstra, "A": search.a, "A*": search.astar}.items():
        dist, path, visited = algo(graph, src, goal)
        plot.path(graph, dist, path, visited, title)


def measure():
    REPEAT = 20

    @dataclass
    class Result:
        timed: float = 0.0
        dist: float = 0.0
        path: int = 0
        visits: int = 0

        def __iadd__(self, other: "Result"):
            self.visits += other.visits
            self.timed += other.timed
            self.dist += other.dist
            self.path += other.path
            return self

        def __str__(self):
            return (
                f"Time:   {self.timed * 1000 / REPEAT :.2f}ms \n"
                f"Dist:   {self.dist / REPEAT :.2f}           \n"
                f"Path:   {self.path / REPEAT :.2f}           \n"
                f"Visits: {self.visits / REPEAT :.2f}         \n"
            )

    def randvertices():
        while True:
            src = random.randint(0, len(graph) - 1)
            goal = random.randint(0, len(graph) - 1)

            if reachable(graph, src, goal):
                return src, goal

    def timeit(algo: Callable[[Graph, int, int], tuple[float, list[int], set[int]]]):
        """Executes the algorithm and measures it's time"""
        start = time.time()
        dist, path, visited = algo(graph, src, goal)
        return Result(time.time() - start, dist, len(path), len(visited))

    for graph in (Graph(5000, 3), Graph(5000, 5), Graph(5000, 7)):
        stress(str(graph))
        results = {algo: Result() for algo in ("DFS", "BFS", "Best First", "Dijkstra", "A", "A*")}

        for _ in range(REPEAT):
            src, goal = randvertices()

            results["A"] += timeit(search.a)
            results["DFS"] += timeit(search.dfs)
            results["BFS"] += timeit(search.bfs)
            results["A*"] += timeit(search.astar)
            results["Dijkstra"] += timeit(search.dijkstra)
            results["Best First"] += timeit(search.bestfirst)

        for algo, result in results.items():
            print(algo)
            print(result)


def reachable(graph: Graph, src: int, goal: int):
    return search.astar(graph, src, goal)[0] != math.inf


def error(message: str):
    print("\033[31m", end = "") # Set font color to red
    print(f"Error: {message}!")
    print("\033[0m", end = "")  # Reset font color

def stress(message: str):
    print("\033[36m", end = "")  # Set font color to blue
    print(message, end = "\n\n")
    print("\033[0m", end = "")   # Reset font color


if __name__ == "__main__":
    main()
