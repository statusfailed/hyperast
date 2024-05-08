from hyperast import hypergraph

from examples.ast import FunctionDefinition
from examples.polycirc.primitive import add, mul
from examples.polycirc.codegen import to_python

@hypergraph
def adder(x0, x1):
    # NOTE: Internally each operation node generated here needs to be tagged that it came from the "adder" function.
    # 'add' and 'mul' are primitives that *don't* do this tagging.
    # TODO: FIXME: don't want to have to unpack singleton lists!
    [s] = add(x0, x1) # sum
    [c] = mul(x0, x1) # carry
    return [s, c]

builder = adder()
print(builder)

h = builder.to_open_hypergraph()
print(to_python(FunctionDefinition.from_open_hypergraph(h)))
