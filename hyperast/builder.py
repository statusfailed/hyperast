from typing import Any, List, Tuple
from dataclasses import dataclass, field

################################################################################
# Hypegraph builder class

@dataclass
class Node:
    id: int
    label: Any = None
    builder: 'Builder' = None

    def __add__(self, other):
        raise NotImplementedError("TODO")

    def __mul__(self, other):
        raise NotImplementedError("TODO")

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
    def target(self, s):
        assert (x <= n for x in s)
        self._target= s

    def node(self, label=None):
        i = len(self.nodes)
        node = Node(i, label=label, builder=self)
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

    def operation(self, sources, target_type, source_type=None, label=None):
        """ Create an operation from its sources and a specified target type.
        Optionally specify:
            - edge label
            - source_type (whose length must match ``sources``.)

        NOTE: this creates twice as many nodes as we "need" - this lets us
        detect type errors when an operation's source/target doesn't match those
        passed in.
        """

        if source_type:
            assert len(sources) == len(source_type)
        else:
            source_type = [ self.nodes[i].label for i in sources ]

        # create an edge with the same number of sources/targets
        e_sources, e_targets = self.edge(source_type, target_type, label)

        # unify the boundary sources/targets with the edge sources/targets
        targets = [ self.node() for _ in range(len(e_targets)) ]
        for a, b in zip(sources, e_sources):
            self.unify(a, b)
        for a, b in zip(e_targets, targets):
            self.unify(a, b)

        return targets
