#pylint:disable = missing-function-docstring,missing-docstring,missing-docstring

import ast
from typing import Any, List, Tuple
from dataclasses import dataclass, field

import numpy as np
from open_hypergraphs import FiniteFunction, IndexedCoproduct, Hypergraph, OpenHypergraph

################################################################################
# Hypegraph builder class

@dataclass
class Node:
    id: int
    label: Any = None
    # don't print the Builder in __repr__, this will recurse forever.
    builder: 'Builder' = field(repr=False, default=None)

    def __add__(self, other):
        return self.builder.operation([self, other], 1, label=ast.Add())

    def __mul__(self, other):
        return self.builder.operation([self, other], 1, label=ast.Mul())

@dataclass
class Edge:
    source: List[int]
    target: List[int]
    label: Any = None

@dataclass
class Builder:
    # a list of Node (wrapped because we need to __add__ and __mul__ etc. nodes)
    nodes: List = field(default_factory=list)

    # a list of Edge
    edges: List[Edge] = field(default_factory=list)

    # a quotienting of hypernodes
    quotient: List[Tuple[int, int]] = field(default_factory=list)

    _source: List[int] = field(default_factory=list)
    _target: List[int] = field(default_factory=list)

    @property
    def source(self):
        return self._source

    @source.setter
    def source(self, s):
        assert (x <= n for x in s)
        self._source = s

    @property
    def target(self):
        return self._target

    @target.setter
    def target(self, t):
        assert (x <= n for x in t)
        self._target = t

    def node(self, label=None):
        i = len(self.nodes)
        node = Node(i, label=label, builder=self)
        self.nodes.append(node)
        return node

    def _object_to_nodes(self, obj):
        # for integers (arities) return unlabeled nodes
        #pylint:disable=unidiomatic-typecheck
        if type(obj) is int:
            return [ self.node() for _ in range(obj) ]

        # otherwise label according to obj
        return [ self.node(label=x) for x in obj ]

    # create a hyperedge and its associated nodes
    def edge(self, source_type, target_type, label=None):
        sources = self._object_to_nodes(source_type)
        targets = self._object_to_nodes(target_type)
        e = Edge(sources, targets, label=label)
        self.edges.append(e)
        return e.source, e.target

    def unify(self, *args):
        n = len(self.nodes)
        assert all(x.id < n for x in args)
        self.quotient.append(args) # each element is a clique to be unified

    # Mid-level interface
    def var(self, *args, **kwargs):
        return self.edge(*args, **kwargs)

    def operation(self, sources: List[Node], target_type, source_type=None, label=None):
        """ Create an operation from its sources and a specified target type.
        Optionally specify:
            - edge label
            - source_type (whose length must match ``sources``.)

        NOTE: this creates twice as many nodes as we "need" - this lets us
        detect type errors when an operation's source/target doesn't match those
        passed in.
        """

        if source_type is None:
            source_type = [ node.label for node in sources ]

        # create an edge with the same number of sources/targets
        e_sources, e_targets = self.edge(source_type, target_type, label)

        if len(e_sources) != len(sources):
            raise ValueError(
                "operation had arity {len(e_sources)} but was given {len(sources)} args")

        # unify the boundary sources/targets with the edge sources/targets
        targets = [ self.node() for _ in range(len(e_targets)) ]
        for a, b in zip(sources, e_sources):
            self.unify(a, b)
        for a, b in zip(e_targets, targets):
            self.unify(a, b)

        return targets

    def to_coequalizer(self):
        """
        Represent the unification graph as a pair of
        parallel arrows representing source and target
        """
        # f, g : N → N
        f, g = to_graph_pairs(len(self.nodes), self.quotient)

        # Quotient the tensored hypergraph H by the coequalizer of f and g to merge nodes.
        q = f.coequalizer(g)
        return q

    def to_open_hypergraph(self) -> 'OpenHypergraph':
        # Unquotiented hypergraph
        nw = len(self.nodes)
        #pylint:disable=invalid-name
        H = Hypergraph(
            # TODO: FIXME: Just create the IndexedCoproducts directly; don't use from_list
            #pylint:disable=line-too-long
            s = IndexedCoproduct.from_list(nw,
                                           [ FiniteFunction(nw,np.array([a.id for a in x.source], dtype=np.uint32))
                                            for x in self.edges ]),
            #pylint:disable=line-too-long
            t = IndexedCoproduct.from_list(nw,
                                           [ FiniteFunction(nw, np.array([a.id for a in x.target], dtype=np.uint32))
                                            for x in self.edges ]),
            w = FiniteFunction(None, np.array([ w.label for w in self.nodes ], dtype='O')),
            x = FiniteFunction(None, np.array([ x.label for x in self.edges ], dtype='O')))

        q = self.to_coequalizer()
        #pylint:disable=invalid-name
        Q = H.coequalize_vertices(q)

        # compute resulting sources and targets under q
        s = FiniteFunction(nw, np.array([ a.id for a in self.source ], dtype=np.uint32))
        t = FiniteFunction(nw, np.array([ a.id for a in self.target ], dtype=np.uint32))
        s = s >> q
        t = t >> q
        return OpenHypergraph(s, t, Q)

def cliques_to_pairs(cliques):
    """ Turn a list of cliques into a list of pairs """
    for clique in cliques:
        if len(clique) == 0:
            continue
        i = clique[0] # the first item is representative
        for j in clique[1:]:
            yield (j, i)

def to_graph_pairs(num_nodes, cliques):
    sources, targets = zip(*cliques_to_pairs(cliques))
    sources = np.array([a.id for a in sources], dtype=np.uint32)
    targets = np.array([a.id for a in targets], dtype=np.uint32)
    s = FiniteFunction(num_nodes, sources)
    t = FiniteFunction(num_nodes, targets)
    return s, t
