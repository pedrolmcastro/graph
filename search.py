import math
import heapq

from graph import Graph
from typing import Callable
from collections import deque


class Stack:
    def __init__(self):
        self.stack: list[tuple[float, int]] = []

    def __len__(self):
        return len(self.stack)

    def insert(self, dist: float, vertex: int):
        self.stack.append((dist, vertex))

    def remove(self):
        return self.stack.pop()

class Queue:
    def __init__(self):
        self.queue: deque[tuple[float, int]] = deque()

    def __len__(self):
        return len(self.queue)

    def insert(self, dist: float, vertex: int):
        self.queue.append((dist, vertex))

    def remove(self):
        return self.queue.popleft()

class PriorityQueue:
    def __init__(self):
        self.queue: list[tuple[float, int]] = []

    def __len__(self):
        return len(self.queue)

    def insert(self, dist: float, vertex: int):
        heapq.heappush(self.queue, (dist, vertex))

    def remove(self):
        return heapq.heappop(self.queue)


def traceback(parents: dict[int, int], goal: int):
    """Returns the path taken to goal"""
    path = []
    curr: int | None = goal

    while curr is not None:
        path.append(curr)
        curr = parents.get(curr)

    path.reverse()
    return path


def search(graph: Graph, src: int, goal: int, agenda: Stack | Queue | PriorityQueue):
    parents: dict[int, int] = {}
    visited: set[int] = set()

    agenda.insert(0.0, src)

    while agenda:
        dist, curr = agenda.remove()

        if curr == goal:
            return dist, traceback(parents, goal), visited

        if curr in visited: # Ignore redundant entries
            continue

        visited.add(curr)

        for neighbor, weight in graph[curr]:
            if neighbor not in visited:
                agenda.insert(dist + weight, neighbor)
                parents[neighbor] = curr

    return math.inf, [], visited


def dfs(graph: Graph, src: int, goal: int):
    return search(graph, src, goal, Stack())

def bfs(graph: Graph, src: int, goal: int):
    return search(graph, src, goal, Queue())

def bestfirst(graph: Graph, src: int, goal: int):
    return search(graph, src, goal, PriorityQueue())


def astar(graph: Graph, src: int, goal: int, heuristic: Callable[[int, int], float]):
    parents: dict[int, int] = {}
    visited: set[int] = set()

    queue = [(0.0, 0.0, src)]

    dists = [math.inf for _ in range(len(graph))]
    dists[src] = 0.0

    while queue:
        _, dist, curr = heapq.heappop(queue)
        visited.add(curr)

        if curr == goal:
            return dists[goal], traceback(parents, goal), visited

        if dist > dists[curr]: # Ignore redundant entries
            continue

        for neighbor, weight in graph[curr]:
            dist = dists[curr] + weight

            if dist < dists[neighbor]:
                dists[neighbor] = dist
                parents[neighbor] = curr
                heapq.heappush(queue, (dist + heuristic(neighbor, goal), dist, neighbor))

    return math.inf, [], visited

def dijkstra(graph: Graph, src: int, goal: int):
    return astar(graph, src, goal, lambda curr, goal: 0)
