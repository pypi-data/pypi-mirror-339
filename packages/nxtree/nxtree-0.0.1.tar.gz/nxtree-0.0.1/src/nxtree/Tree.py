import networkx as nx
from random import random

class NotALeaf(Exception):
    pass

class Tree(nx.DiGraph):
    def _not_a_tree():
        raise(nx.NotATree)
    
    @staticmethod
    def _ensure_tree(G):
        try:
            if not nx.is_tree(G):
                raise(nx.NotATree)
        except nx.NetworkXPointlessConcept:
            return # is_tree errors on empty graphs, but Tree allows them

    def _unlock_mutation(self):
        self.add_nodes_from = super().add_nodes_from
        self.add_edges_from = super().add_edges_from
    
    def _lock_mutation(self):
        self.add_nodes_from = self._not_a_tree
        self.add_edges_from = self._not_a_tree

    def __init__(self, incoming_graph_data=None, expand_binary_ops=True, **attr):
        self.expand_binary_ops = expand_binary_ops
        
        # DiGraph calls these functions..
        self._unlock_mutation()
        super().__init__(incoming_graph_data, **attr)
        self._lock_mutation()
        # ..but no other code is allowed to
        for edge in self.edges:
            if 'pos' not in self.edges[edge]:
                self.edges[edge]['pos'] = random()


        self._ensure_tree(self)
    

    def add_node(self, node_for_adding, **attr):
        self._not_a_tree()
    
    def add_nodes_from(self, nodes_for_adding, **attr):
        self._not_a_tree()
    
    def remove_node(self, n):
        self._not_a_tree()
    
    def remove_nodes_from(self, nodes):
        self._not_a_tree()
    
    def add_edge(self, u_of_edge, v_of_edge, **attr):
        self._not_a_tree()
    
    def add_edges_from(self, ebunch_to_add, **attr):
        self._not_a_tree()
    
    def remove_edge(self, u, v):
        self._not_a_tree()
    
    def remove_edges_from(self, ebunch):
        self._not_a_tree()
    
    def add_weighted_edges_from(self, ebunch_to_add, weight="weight", **attr):
        self._not_a_tree()
    
    def update(self, edges=None, nodes=None):
        self._not_a_tree()
    
    def clear_edges(self):
        self._not_a_tree()

    # copied from superclass
    def copy(self, as_view=False):
        if as_view is True:
            return nx.graphviews.generic_graph_view(self)
        G = Tree()
        G._unlock_mutation()
        G.graph.update(self.graph)
        G.add_nodes_from((n, d.copy()) for n, d in self._node.items())
        G.add_edges_from(
            (u, v, datadict.copy())
            for u, nbrs in self._adj.items()
            for v, datadict in nbrs.items()
        )
        G._lock_mutation()
        return G

    def children(self, node):
        return list(sorted(
            self.successors(node),
            key=lambda child: str(self[node][child]['pos'])
        ))

    def _to_str(self, node):
        children = self.children(node)
        if len(children) == 0:
            return str(node)
        if len(children) == 1:
            return f'{node}({self._to_str(children[0])})'
        if self.expand_binary_ops and len(children) == 2:
            return f'({self._to_str(children[0])}{node}{self._to_str(children[1])})'
        return f'{node}({','.join(self._to_str(child) for child in children)})'

    def __str__(self):
        return self._to_str(self.root)
    
    def __eq__(self, other):
        return str(self) == str(other)
    
    def __hash__(self):
        return hash(str(self))
    
    def __contains__(self, other):
        return str(other) in str(self)
    
    @property
    def leaves(self):
        return [n for n in self.nodes if not list(self.successors(n))]

    @property
    def root(self):
        return [n for n in self.nodes() if not list(self.predecessors(n))][0]
    
    @property
    def depth(self):
        return 1 + max(nx.shortest_path_length(
            self,
            source=self.root,
            target=leaf
        ) for leaf in self.leaves)
    
    def subtree(self, node):
        return Tree(nx.subgraph(self, {node} | nx.descendants(self, node)))

    def graft(self, leaf, other: 'Tree'):
        self._ensure_tree(other)

        if not leaf in self:
            raise(nx.NodeNotFound)
        
        if list(self.successors(leaf)):
            print(list(self.successors(leaf)))
            raise(NotALeaf)
        
        self._unlock_mutation()
        super().update(other)
        self._lock_mutation()
        if leaf != self.root:
            super().add_edge(next(self.predecessors(leaf)), other.root, pos=random())
        super().remove_node(leaf)


        self._ensure_tree(self) # Fails if other has overlapping node IDs