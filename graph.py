import random
import math

from dataclasses import dataclass


class Graph:
    @dataclass(repr = False)
    class Coord:
        x: float
        y: float

        def __iter__(self): # Allow unpacking
            return iter((self.x, self.y))

        def __str__(self):
            return f"({self.x :.2f}, {self.y :.2f})"

        __repr__ = __str__


    @dataclass(repr = False)
    class Edge:
        neighbor: int
        weight: float

        def __iter__(self): # Allow unpacking
            return iter((self.neighbor, self.weight))

        def __str__(self):
            return f"({self.neighbor}, {self.weight :.2f})"

        __repr__ = __str__


    def __init__(self, vertices: int, neighbors: int):
        self.vertices = vertices
        self.neighbors = neighbors

        # Generate the vertices x and y coordinates
        self.coords = [self.Coord(random.uniform(0, vertices), random.uniform(0, vertices)) for _ in range(vertices)]

        # Generate the vertices neighbors
        population = set(range(vertices))
        self.adj = [[self.Edge(neighbor, self.dist(vertex, neighbor)) for neighbor in random.sample(population - {vertex}, neighbors)] for vertex in range(vertices)]

    def __str__(self):
        return f"Graph with {self.vertices} vertices and {self.neighbors} neighbors"

    def __len__(self):
        return self.vertices

    def __getitem__(self, key: int):
        return self.adj[key]

    def __iter__(self):
        return iter(range(self.vertices))


    def dist(self, src: int, goal: int):
        """Returns the geometric distance from src to goal"""
        return math.sqrt((self.coords[goal].x - self.coords[src].x) ** 2 + (self.coords[goal].y - self.coords[src].y) ** 2)
