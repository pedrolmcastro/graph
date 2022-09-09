import search

from graph import Graph


# TODO: Timing and profiling
# TODO: Better path visualization


def main():
    vertices = int(input("Vertices:  "))
    neighbors = int(input("Neighbors: "))

    print()


    graph = Graph(vertices, neighbors)
    src, dest = 0, vertices - 1

    # print("Coords\n" + '\n'.join(f"{i}: {coord}" for i, coord in enumerate(graph.coords)), end = "\n\n")
    # print("Edges\n" + '\n'.join(f"{i}: {adj}" for i, adj in enumerate(graph.adj)), end = "\n\n")


    path, dist, _ = search.dfs(graph, src, dest)
    print(f"DFS: {path} ({dist :.2f})")

    path, dist, _ = search.bfs(graph, src, dest)
    print(f"BFS: {path} ({dist :.2f})")

    path, dist, _ = search.bestfirst(graph, src, dest)
    print(f"Best First: {path} ({dist :.2f})")

    path, dist, _ = search.dijkstra(graph, src, dest)
    print(f"Dijkstra: {path} ({dist :.2f})")


if __name__ == "__main__":
    main()
    print()
