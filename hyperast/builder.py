from typing import Any, List, Tuple
from dataclasses import dataclass, field

################################################################################
# Hypegraph builder class

@dataclass
class Node:
    id: int
    label: Any = None

    # TODO: overload operators

@dataclass
class Edge:
    source: List[int]
    target: List[int]
    label: Any = None

@dataclass
class Builder:
    # a list of Node
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
    def target(self, s):
        assert (x <= n for x in s)        
        self._target= s

    def node(self, label=None):
        i = len(self.nodes)
        # TODO: pass a self ref to Node.
        node = Node(i, label=label)
        self.nodes.append(node)
        return node

    def _object_to_nodes(self, obj):
        # for integers (arities) return unlabeled nodes
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

    def operation(self, sources, source_type=None, target_type=None, label=None):
        e_sources, e_targets = self.edge(source_type, target_type, label)

        targets = [ self.node() for _ in range(len(e_targets)) ]
        for a, b in zip(sources, e_sources):
            self.unify(a, b)
        for a, b in zip(e_targets, targets):
            self.unify(a, b)

        return targets
