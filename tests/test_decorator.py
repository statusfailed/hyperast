from hyperast.decorator import Builder, hypergraph, node, edge

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

def test_discrete():
    builder = discrete()
    assert type(builder) is Builder
    assert len(builder.nodes) == 1
    assert len(builder.edges) == 0

def test_identity():
    builder = identity()
    assert type(builder) is Builder
    assert len(builder.nodes) == 1
    assert len(builder.edges) == 0
    assert len(builder.source) == 1
    assert len(builder.target) == 1

def test_nested_identity():
    builder = nested_identity()
    assert type(builder) is Builder
    assert len(builder.nodes) == 1
    assert len(builder.edges) == 0
    assert len(builder.source) == 1
    assert len(builder.target) == 1


# TESTS
#   - setting source/target with out-of-range value fails
