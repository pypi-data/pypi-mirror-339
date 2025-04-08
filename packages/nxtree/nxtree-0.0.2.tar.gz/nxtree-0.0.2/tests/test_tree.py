import networkx as nx
import pytest
from src.nxtree import Tree
from src.nxtree import NotALeaf


def test_invalid_initialization():
    with pytest.raises(nx.NotATree):
        Tree([(0, 1), (1, 0)])

def test_valid_initialization():
    Tree([('root', 'child'), ('child', 'grandchild')])

def test_empty_initialization():
    Tree()


# def test_illegal_mutation():
#     with pytest.raises(nx.NotATree):
#         Tree().add_nodes_from()

# terminology borrowed from grafting (horticultural technique)
y_tree = Tree([('+', 'a', {'pos': 'L'}), ('+', 'b', {'pos': 'R'})])

dot_tree = nx.Graph()
dot_tree.add_node(0)
dot_tree = Tree(dot_tree)

def test_to_str():
    assert str(y_tree) == '(a+b)'

def test_graft():
    # terminology borrowed from grafting (horticultural technique)
    scion = dot_tree.copy()

    stock = y_tree.copy()
    stock.graft('a', scion)

    expectation = Tree([('+', 0, {'pos': 'L'}), ('+', 'b', {'pos': 'R'})])
    assert stock == expectation

def test_graft_not_a_tree():
    cycle = nx.DiGraph([(0, 1), (1, 0)])
    stock = y_tree.copy()
    with pytest.raises(nx.NotATree):
        stock.graft('a', cycle)

def test_graft_invalid_node():
    stock = y_tree.copy()
    scion = dot_tree.copy()
    with pytest.raises(nx.NodeNotFound):
        stock.graft('c', scion)

def test_graft_not_a_leaf():
    stock = y_tree.copy()
    scion = dot_tree.copy()
    with pytest.raises(NotALeaf):
        stock.graft('+', scion)

def test_graft_id_overlap():
    stock = y_tree.copy()
    scion = Tree([('a', '+')])
    with pytest.raises(Exception):
        stock.graft('b', scion)

depth_3_tree = Tree([('a', 'b'), ('a', 'c'), ('b', 'd'), ('b', 'e')])

def test_leaves():
    assert depth_3_tree.leaves 