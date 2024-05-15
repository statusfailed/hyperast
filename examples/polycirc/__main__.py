#pylint:disable = missing-function-docstring,missing-docstring,invalid-name

from hyperast import hypergraph
from hyperast.builder import Builder

from examples.ast import FunctionDefinition
from examples.polycirc.primitive import add, mul
from examples.polycirc.codegen import to_python


@hypergraph
def adder(x0, x1):
    # NOTE: Internally each operation node generated here needs to be tagged
    # that it came from the "adder" function.
    # 'add' and 'mul' are primitives that *don't* do this tagging.
    # TODO: FIXME: don't want to have to unpack singleton lists!
    [s] = add(x0, x1) # sum
    [c] = mul(x0, x1) # carry
    return [s, c]

#pylint:disable = no-value-for-parameter
builder : Builder = adder()
print(builder)

#pylint:disable = no-member
h = builder.to_open_hypergraph()
f, code = to_python(FunctionDefinition.from_open_hypergraph(h))
print(code)
print(f"{f(2, 3)=}")
