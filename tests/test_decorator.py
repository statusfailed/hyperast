#pylint:disable=missing-function-docstring,missing-docstring,invalid-name,unused-variable

from hyperast.decorator import Builder, hypergraph, node, edge, operation, unify

################################################################################
# Discrete hypergraphs, identity maps, twists, etc.

@hypergraph
def discrete():
    x = node()
    return []

@hypergraph
def identity(x):
    return [x]

@hypergraph
def nested_identity(x):
    return identity(x)

@hypergraph
def twist(x, y):
    return [y, x]

def test_discrete():
    builder = discrete()
    #pylint:disable=unidiomatic-typecheck
    assert type(builder) is Builder
    #pylint:disable=no-member
    assert len(builder.nodes) == 1
    #pylint:disable=no-member
    assert len(builder.edges) == 0

def test_identity():
    #pylint:disable=no-value-for-parameter
    builder = identity()
    #pylint:disable=unidiomatic-typecheck
    assert type(builder) is Builder
    #pylint:disable=no-member
    assert len(builder.nodes) == 1
    #pylint:disable=no-member
    assert len(builder.edges) == 0
    #pylint:disable=no-member
    assert len(builder.source) == 1
    #pylint:disable=no-member
    assert len(builder.target) == 1

def test_nested_identity():
    #pylint:disable=no-value-for-parameter
    builder = nested_identity()
    #pylint:disable=unidiomatic-typecheck
    assert type(builder) is Builder
    #pylint:disable=no-member
    assert len(builder.nodes) == 1
    #pylint:disable=no-member
    assert len(builder.edges) == 0
    #pylint:disable=no-member
    assert len(builder.source) == 1
    #pylint:disable=no-member
    assert len(builder.target) == 1

def test_twist():
    #pylint:disable=no-value-for-parameter
    builder = twist()
    #pylint:disable=no-member
    assert [ node.id for node in builder.source ] == [0, 1]
    #pylint:disable=no-member
    assert [ node.id for node in builder.target ] == [1, 0]

################################################################################
# Test unification

@hypergraph
def two_unified():
    x = node()
    y = node()
    unify(x, y)

def test_unify():
    builder = two_unified()
    assert len(builder.nodes) == 2 # TODO! should be 8!
    assert len(builder.edges) == 0
    assert len(builder.quotient) == 1
    assert builder.quotient == [(builder.nodes[0], builder.nodes[1])]
    assert builder.source == []
    assert builder.target == []


################################################################################
# Test operations

# test creating an edge without assigning it to the boundary
@hypergraph
def mimo_edge():
    source_type = ['A₀', 'A₁']
    target_type = ['B₀', 'B₁']
    sources, targets = edge(source_type, target_type, label='mimo')
    return []

# "builder.edge" is a very low-level interface; it only adds the edge, but
# doesn't connect it to any other nodes.
def test_mimo_edge():
    builder = mimo_edge()
    # TODO: this should be 8? Let's do these by quotienting.
    #pylint:disable=no-member
    assert len(builder.nodes) == 4 # TODO! should be 8!
    #pylint:disable=no-member
    assert len(builder.edges) == 1
    #pylint:disable=no-member
    assert builder.source == []
    #pylint:disable=no-member
    assert builder.target == []

# OTOH, "op" is a more "function-like" interface:
#pylint:disable=dangerous-default-value
@hypergraph
def mimo_operation(x0, x1, source_type=['A₀', 'A₁']):
    y0, y1 = operation([x0, x1], target_type=['B₀', 'B₁'], source_type=source_type, label='mimo')
    return [y0, y1]

# 'op' is a higher level interface that creates both the edge,
#   and copies of nodes for each input and output.
#   these copies are passed as input args, and returned as output args.
def test_mimo_operation():
    #pylint:disable=no-value-for-parameter
    builder = mimo_operation()
    #pylint:disable=no-member
    assert len(builder.nodes) == 8
    #pylint:disable=no-member
    assert len(builder.edges) == 1
    # NOTE: these two assertions are very implementation dependent!
    assert [ x.id for x in builder.source ] == [0, 1] # created first
    assert [ x.id for x in builder.target ] == [6, 7] # created last

def test_mimo_operation_untyped():
    #pylint:disable=no-value-for-parameter
    builder = mimo_operation(source_type=None)
    #pylint:disable=no-member
    assert len(builder.nodes) == 8
    #pylint:disable=no-member
    assert len(builder.edges) == 1
    # NOTE: these two assertions are very implementation dependent!
    assert [ x.id for x in builder.source ] == [0, 1] # created first
    assert [ x.id for x in builder.target ] == [6, 7] # created last
