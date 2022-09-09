import math
import random

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
        dest: int
        weight: float

        def __iter__(self): # Allow unpacking
            return iter((self.dest, self.weight))

        def __str__(self):
            return f"({self.dest}, {self.weight :.2f})"

        __repr__ = __str__


    def __init__(self, vertices: int, neighbors: int):
        # Generate the vertices x and y coordinates
        self.coords = [self.Coord(random.uniform(0, vertices), random.uniform(0, vertices)) for _ in range(vertices)]

        # Generate the vertices neighbors
        population = set(range(vertices))
        self.adj = [[self.Edge(dest, self.dist(vertex, dest)) for dest in random.sample(population - {vertex}, neighbors)] for vertex in range(vertices)]

    def __getitem__(self, key: int):
        return self.adj[key]

    def __len__(self):
        return len(self.coords)

    def dist(self, src: int, dest: int):
        """Returns the geometric distance from src to dest"""
        return math.sqrt((self.coords[dest].x - self.coords[src].x) ** 2 + (self.coords[dest].y - self.coords[src].y) ** 2)
