from graph import Graph
from typing import Optional
from collections import deque


def dfs(graph: Graph, src: int, dest: int):
    path: list[int] = []
    visited: set[int] = set()

    def recursive(src: int, acc = 0.0) -> Optional[float]:
        path.append(src)
        visited.add(src)

        if src == dest:
            return acc

        for neighbor, weight in graph.adj[src]:
            if neighbor not in visited and (dist := recursive(neighbor, acc + weight)) is not None:
                return dist

        # Dead end path
        path.pop()
        return None

    return path, recursive(src)


def bfs(graph: Graph, src: int, dest: int):
    visited: set[int] = set()

    queue: deque[tuple[list[int], float]] = deque()
    queue.append(([src], 0.0))

    while queue:
        path, dist = queue.popleft()
        visited.add(path[-1])

        if path[-1] == dest:
            return path, dist

        for neighbor, weight in graph.adj[path[-1]]:
            if neighbor not in visited:
                queue.append((path + [neighbor], dist + weight))

    return [], None


def bestfirst(graph: Graph, src: int, dest: int):
    return NotImplemented


def dijkstra(graph: Graph, src: int, dest: int):
    return NotImplemented


def astar(graph: Graph, src: int, dest: int):
    return NotImplemented
