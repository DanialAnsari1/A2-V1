# -------------------------------------------------
# EDIT THIS FILE TO IMPLEMENT TASK B.
# Kruskal's algorithm.
#
# __author__ = 'Danial Ansari (s4119075)'
# __project__ = "Neuromancer: Hacking with Graphs"
# __copyright__ = 'Copyright 2026, RMIT University'
# -------------------------------------------------

from graph.graph import Graph
from graph.edge import Edge
from mst.merge_sort import merge_sort
from mst.union_find import UnionFind


def kruskals(graph: Graph) -> tuple[list[Edge], int]:
    """
    Computes a minimum spanning tree of a connected graph using
    Kruskal's algorithm.

    Considers every connection from lightest to heaviest and keeps a
    connection whenever its two endpoints are not already linked by
    the connections kept so far. Stops once the tree holds every
    vertex.

    You are given two tools to use: merge_sort (mst/merge_sort.py) to
    order the connections, and UnionFind (mst/union_find.py) to decide
    whether two vertices are already linked.

    @param graph: The graph to span. Must be connected.
    @returns: A tuple of:
              - list[Edge]: the connections chosen for the tree.
              - int: the total number of firewalls across the tree.

    HINT: get_edges gives every connection; sort them, then add a
    connection only when its endpoints are not already joined.
    """
    vertices = graph.get_vertices()
    n = len(vertices)
    if n <= 1:
        return [], 0                      # nothing to connect

    # Lines 1-2: every connection once, lightest first.
    edges = merge_sort(graph.get_edges())

    # Lines 3-4: every vertex starts in its own group (MAKE-SET).
    groups = UnionFind(vertices)

    # Line 5: the tree holds |V| - 1 connections when complete.
    tree: list[Edge] = []
    total = 0

    # Lines 6-12: keep an edge only if it joins two different groups,
    # i.e. it does not close a cycle.
    for edge in edges:
        if groups.find(edge.u) != groups.find(edge.v):
            groups.union(edge.u, edge.v)
            tree.append(edge)
            total += edge.weight
            if len(tree) == n - 1:
                break                     # tree spans every vertex

    return tree, total
