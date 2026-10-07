# -------------------------------------------------
# EDIT THIS FILE TO IMPLEMENT TASK B.
# Kruskal's algorithm.
#
# __author__ = 'your_name_here'
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
    # IMPLEMENT ME! (Task B)
    # Return the chosen connections and their total firewalls. The empty
    # return below is a valid placeholder so the program runs before you
    # start: it finds no tree.
    return [], 0
