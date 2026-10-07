# -------------------------------------------------
# EDIT THIS FILE TO IMPLEMENT TASK A.
# Adjacency list implementation of the Graph ABC.
#
# __author__ = 'your_name_here'
# __project__ = "Neuromancer: Hacking with Graphs"
# __copyright__ = 'Copyright 2026, RMIT University'
# -------------------------------------------------

from graph.graph import Graph
from graph.vertex import Vertex
from graph.edge import Edge


class LinkedListNode:
    """
    A single entry in the linked list used by the AdjacencyList.

    Each entry stores a neighbouring vertex, the number of firewalls
    on the connection to that neighbour, and a pointer to the next
    entry in the chain. The chain for a given vertex, followed to
    its end, is that vertex's adjacency list.
    """

    def __init__(self, neighbour: Vertex, weight: int,
                 next_node: 'LinkedListNode | None' = None) -> None:
        """
        Initialises a LinkedListNode.

        @param neighbour: The neighbouring vertex this entry records.
        @param weight: The number of firewalls on the connection.
        @param next_node: The next entry in the chain, or None if this
                          is the last entry.
        @returns: None
        """
        self.neighbour = neighbour
        self.weight = weight
        self.next = next_node

    def __repr__(self) -> str:
        """
        Renders this entry and the remainder of its chain.

        @returns: A string of the form '(d1, 3) -> (d4, 2) -> None'.
        """
        return f"({self.neighbour}, {self.weight}) -> {self.next!r}"


class AdjacencyList(Graph):
    """
    An adjacency list representation of The Fold.

    The structure is an array of linked lists: one chain per vertex,
    where each entry in a vertex's chain records one real connection.
    Only connections that actually exist are stored.
    """

    def __init__(self) -> None:
        """
        Initialises an empty adjacency list graph. Internally keeps
        one chain head per vertex (initially None) plus the vertex
        objects themselves.

        @returns: None
        """
        self._heads: list[LinkedListNode | None] = []
        self._vertices: list[Vertex] = []
        self._index_of: dict[int, int] = {}   # vertex.index -> slot
        self._num_edges: int = 0

    def _pos(self, vertex: Vertex) -> int | None:
        """
        Looks up the slot of a vertex in the array of chains.

        @param vertex: The vertex to look up.
        @returns: The slot as an integer, or None if unknown.
        """
        return self._index_of.get(vertex.index)

    def _find_node(self, slot: int, neighbour: Vertex) -> LinkedListNode | None:
        """
        Walks one chain looking for the entry that records a given
        neighbour.

        @param slot: The slot whose chain should be walked.
        @param neighbour: The neighbour to look for.
        @returns: The matching LinkedListNode, or None if the chain
                  holds no entry for that neighbour.
        """
        node = self._heads[slot]
        while node is not None:
            if node.neighbour == neighbour:
                return node
            node = node.next
        return None

    def _delete_node(self, slot: int, neighbour: Vertex) -> bool:
        """
        Unlinks the entry for a given neighbour from one chain,
        re-joining the chain around it.

        @param slot: The slot whose chain should be edited.
        @param neighbour: The neighbour whose entry is to be removed.
        @returns: True if an entry was found and unlinked; False if
                  the chain holds no entry for that neighbour.
        """
        # IMPLEMENT ME! (needed by remove_edge, Task A.2)
        # Unlink the entry for `neighbour` from the chain at `slot`,
        # re-joining the chain around it. Return True if you removed an
        # entry, False if the chain had none for that neighbour.
        # HINT: track the previous node so you can bypass the one you
        # remove; the head (no previous node) is the case to watch.
        return False

    def add_vertex(self, vertex: Vertex) -> bool:
        """
        Adds a vertex with an empty chain.

        @param vertex: The vertex to add.
        @returns: True if added; False if a vertex with the same index
                  already exists.
        """
        if vertex.index in self._index_of:
            return False
        self._index_of[vertex.index] = len(self._vertices)
        self._vertices.append(vertex)
        self._heads.append(None)
        return True

    def add_edge(self, u: Vertex, v: Vertex, weight: int) -> bool:
        """
        Adds an undirected connection by prepending a new entry to
        both u's chain and v's chain.

        @param u: The first vertex.
        @param v: The second vertex.
        @param weight: The number of firewalls (must be at least 1).
        @returns: True if added; False if either vertex is unknown,
                  u equals v, the weight is below 1, or the connection
                  already exists.
        """
        # IMPLEMENT ME! (Task A.1)
        # Add an undirected connection: update BOTH u's and v's chains.
        # Return True on success; return False if a vertex is unknown,
        # u == v, weight < 1, or the connection already exists.
        # HINT: _pos gives a vertex's slot; _find_node checks whether a
        # connection is already there.
        return False

    def remove_edge(self, u: Vertex, v: Vertex) -> bool:
        """
        Removes a connection by unlinking the matching entry from
        both chains.

        @param u: The first vertex.
        @param v: The second vertex.
        @returns: True if the connection existed and was removed;
                  False otherwise.
        """
        # IMPLEMENT ME! (Task A.2)
        # Remove the connection from BOTH chains. Return True if it
        # existed and was removed, False otherwise.
        # HINT: _delete_node (which you implement above) unlinks one
        # entry from one chain.
        return False

    def update_edge_weight(self, u: Vertex, v: Vertex, weight: int) -> bool:
        """
        Changes the number of firewalls recorded for an existing
        connection, in both chains.

        @param u: The first vertex.
        @param v: The second vertex.
        @param weight: The new number of firewalls (must be at least 1).
        @returns: True if the connection existed and was updated;
                  False otherwise.
        """
        # IMPLEMENT ME! (Task A.3 --- change weight)
        # Update the firewalls on an existing connection in BOTH chains.
        # Return True if it existed and was updated, False otherwise.
        # HINT: changing a weight is not the same as adding a fresh
        # connection --- find the existing entry rather than prepending.
        return False

    def get_vertices(self) -> list[Vertex]:
        """
        Returns all vertices in insertion order.

        @returns: A list of Vertex objects.
        """
        return list(self._vertices)

    def get_edges(self) -> list[Edge]:
        """
        Walks every chain and returns each connection exactly once
        (a connection is emitted only from the endpoint with the
        smaller slot).

        @returns: A list of Edge objects.
        """
        edges: list[Edge] = []
        for slot, head in enumerate(self._heads):
            node = head
            while node is not None:
                other = self._pos(node.neighbour)
                if other is not None and slot < other:
                    edges.append(Edge(self._vertices[slot],
                                      node.neighbour, node.weight))
                node = node.next
        return edges

    def get_neighbours(self, vertex: Vertex) -> list[tuple[Vertex, int]]:
        """
        Walks one chain and returns each entry as a
        (neighbour, weight) pair.

        @param vertex: The vertex whose neighbours are to be returned.
        @returns: A list of (neighbour, weight) tuples; empty if the
                  vertex is unknown.
        """
        # IMPLEMENT ME! (Task A.5)
        # Return a (neighbour, weight) tuple for every entry in this
        # vertex's chain; an empty list if the vertex is unknown.
        # HINT: walk the chain from its head, following .next to the end.
        return []

    def has_edge(self, u: Vertex, v: Vertex) -> bool:
        """
        Checks whether a connection exists between two vertices.

        @param u: The first vertex.
        @param v: The second vertex.
        @returns: True if a connection exists.
        """
        return self.get_edge_weight(u, v) != 0

    def get_edge_weight(self, u: Vertex, v: Vertex) -> int:
        """
        Walks u's chain looking for v.

        @param u: The first vertex.
        @param v: The second vertex.
        @returns: The number of firewalls, or 0 if no connection
                  exists or either vertex is unknown (matching the
                  matrix's behaviour).
        """
        # IMPLEMENT ME! (Task A.4 --- get weight)
        # Return the firewalls on the connection u--v, or 0 if there is
        # none or either vertex is unknown (matching the matrix).
        # HINT: _find_node searches one chain for a given neighbour.
        return 0

    def num_vertices(self) -> int:
        """
        @returns: The number of vertices as an integer.
        """
        return len(self._vertices)

    def num_edges(self) -> int:
        """
        @returns: The number of connections as an integer, each
                  counted once.
        """
        return self._num_edges

    def __repr__(self) -> str:
        """
        Renders every chain on its own line, for use with the
        print_struct configuration option.

        @returns: A multi-line string picture of the structure.
        """
        out = ""
        for slot, v in enumerate(self._vertices):
            out += f"[{slot}] {v.name}: {self._heads[slot]!r}\n"
        return out
