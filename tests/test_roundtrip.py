#pylint:disable = missing-function-docstring,missing-docstring,invalid-name

import random
from hyperast import hypergraph
from hyperast.builder import Builder

from examples.ast import FunctionDefinition
from examples.polycirc.primitive import add, mul
from examples.polycirc.codegen import FUNCTION_TEMPLATE, to_python

def test_adder():

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
    #pylint:disable = no-member
    h = builder.to_open_hypergraph()
    my_callable, source_code = to_python(FunctionDefinition.from_open_hypergraph(h))
    expected_source_code = FUNCTION_TEMPLATE.format(
            fn_name="fn",
            args="x0, x1",
            assignments="\n".join(["    x2 = x0 + x1","    x3 = x0 * x1"]),
            returns="x2, x3")
    assert expected_source_code == source_code
    N_MAX = 50
    for _ in range(100):
        c = random.randint(0,N_MAX**2)
        a = c//N_MAX
        b = c % N_MAX
        assert my_callable(a,b) == [a*b,a+b]
