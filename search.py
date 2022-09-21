import math
import heapq

from graph import Graph
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


def traceback(parents: dict[int, int], dest: int):
    """Returns the path taken to dest"""
    path = []
    curr: int | None = dest

    while curr is not None:
        path.append(curr)
        curr = parents.get(curr)

    path.reverse()
    return path


def search(graph: Graph, src: int, dest: int, agenda: Stack | Queue | PriorityQueue):
    parents: dict[int, int] = {}
    visited: set[int] = set()

    agenda.insert(0.0, src)

    while agenda:
        dist, curr = agenda.remove()

        if curr == dest:
            return dist, traceback(parents, dest), visited

        if curr in visited: # Ignore redundant entries
            continue

        visited.add(curr)

        for neighbor, weight in graph[curr]:
            if neighbor not in visited:
                agenda.insert(dist + weight, neighbor)
                parents[neighbor] = curr

    return math.inf, [], visited


def dfs(graph: Graph, src: int, dest: int):
    return search(graph, src, dest, Stack())

def bfs(graph: Graph, src: int, dest: int):
    return search(graph, src, dest, Queue())

def bestfirst(graph: Graph, src: int, dest: int):
    return search(graph, src, dest, PriorityQueue())


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
            return dists[dest], traceback(parents, dest), visited

        if dist > dists[curr]: # Ignore redundant entries
            continue

        for neighbor, weight in graph[curr]:
            dist = dists[curr] + weight

            if dist < dists[neighbor]:
                dists[neighbor] = dist
                parents[neighbor] = curr
                heapq.heappush(queue, (dist, neighbor))

    return math.inf, [], visited


def astar(graph: Graph, src: int, dest: int):
    return NotImplemented
