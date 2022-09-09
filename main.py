import search

from graph import Graph


# TODO: Timing and profiling
# TODO: Better path visualization


def main():
    vertices = int(input("Vertices:  "))
    neighbors = int(input("Neighbors: "))

    print()


    graph = Graph(vertices, neighbors)

    print("Coords\n" + '\n'.join(f"{i}: {coord}" for i, coord in enumerate(graph.coords)), end = "\n\n")
    print("Edges\n" + '\n'.join(f"{i}: {adj}" for i, adj in enumerate(graph.adj)), end = "\n\n")


    path, dist, _ = search.dfs(graph, 0, vertices - 1)
    print(f"DFS: {path} ({dist or 0.0 :.2f})")

    path, dist, _ = search.bfs(graph, 0, vertices - 1)
    print(f"BFS: {path} ({dist or 0.0 :.2f})")

    path, dist, _ = search.bestfirst(graph, 0, vertices - 1)
    print(f"Best First: {path} ({dist or 0.0 :.2f})")


if __name__ == "__main__":
    main()
    print()
