import math
import heapq

from graph import Graph
from collections import deque


def traceback(parents: dict[int, int], dest: int):
    """Returns the path taken to dest"""
    path = []
    curr: int | None = dest

    while curr is not None:
        path.append(curr)
        curr = parents.get(curr)

    path.reverse()
    return path


def dfs(graph: Graph, src: int, dest: int):
    parents: dict[int, int] = {}
    visited: set[int] = set()
    stack = [(src, 0.0)]

    while stack:
        curr, dist = stack.pop()

        if curr == dest:
            return traceback(parents, dest), dist, visited

        if curr in visited: # Ignore redundant entries
            continue

        visited.add(curr)

        for neighbor, weight in graph[curr]:
            if neighbor not in visited:
                stack.append((neighbor, dist + weight))
                parents[neighbor] = curr

    return [], math.inf, visited


def bfs(graph: Graph, src: int, dest: int):
    parents: dict[int, int] = {}
    visited: set[int] = set()

    queue: deque[tuple[int, float]] = deque()
    queue.append((src, 0.0))

    while queue:
        curr, dist = queue.popleft()
        visited.add(curr)

        if curr == dest:
            return traceback(parents, dest), dist, visited

        for neighbor, weight in graph[curr]:
            if neighbor not in visited:
                queue.append((neighbor, dist + weight))
                parents[neighbor] = curr

    return [], math.inf, visited


def bestfirst(graph: Graph, src: int, dest: int):
    parents: dict[int, int] = {}
    visited: set[int] = set()
    queue = [(0.0, src)]

    while queue:
        dist, curr = heapq.heappop(queue)
        visited.add(curr)

        if curr == dest:
            return traceback(parents, dest), dist, visited

        for neighbor, weight in graph[curr]:
            if neighbor not in visited:
                heapq.heappush(queue, (dist + weight, neighbor))
                parents[neighbor] = curr

    return [], math.inf, visited


def dijkstra(graph: Graph, src: int, dest: int):
    parents: dict[int, int] = {}
    visited: set[int] = set()
    queue = [(0.0, src)]

    dists = [math.inf for _ in range(len(graph))]
    dists[src] = 0.0

    while queue:
        dist, curr = heapq.heappop(queue)
        visited.add(curr)

        if curr == dest:
            return traceback(parents, dest), dists[dest], visited

        if dist > dists[curr]: # Ignore redundant entries
            continue

        for neighbor, weight in graph[curr]:
            dist = dists[curr] + weight

            if dist < dists[neighbor]:
                dists[neighbor] = dist
                parents[neighbor] = curr
                heapq.heappush(queue, (dist, neighbor))

    return [], math.inf, visited


def astar(graph: Graph, src: int, dest: int):
    return NotImplemented
