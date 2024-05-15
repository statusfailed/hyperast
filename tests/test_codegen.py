#pylint:disable = missing-function-docstring,missing-docstring,invalid-name

import random

from examples.ast import FunctionDefinition, Apply, DEBUGGING_WITHOUT_OPEN_HYPERGRAPH
from examples.polycirc.codegen import to_python, FUNCTION_TEMPLATE
from examples.polycirc.signature import Add, Discard, Mul

if DEBUGGING_WITHOUT_OPEN_HYPERGRAPH:
    #pylint:disable=too-few-public-methods
    class FiniteFunction:
        pass
else:
    from open_hypergraphs import FiniteFunction

def test_adder():
    # TODO : FIXME irrelevant for this test but provide the FiniteFunction here
    # this test only uses the operation, lhs and rhs
    def dummy_source() -> FiniteFunction:
        return None
    add_node = Apply(op=Add, source=dummy_source(), target=dummy_source(), rhs=[0,1], lhs=[2])
    mul_node = Apply(op=Mul, source=dummy_source(), target=dummy_source(), rhs=[0,1], lhs=[3])
    mul_node_2 = Apply(op=Mul, source=dummy_source(), target=dummy_source(), rhs=[1,0], lhs=[4])
    discard_node = Apply(op=Discard, source=dummy_source(), target=dummy_source(), rhs=[4], lhs=[])
    functiondef = FunctionDefinition(args=[0,1],
                                     body=[add_node,mul_node,mul_node_2,discard_node],
                                     returns=[3,2])
    my_callable, source_code = to_python(functiondef, fn_name='fn')
    expected_source_code = FUNCTION_TEMPLATE.format(
            fn_name="fn",
            args="x0, x1",
            assignments="\n".join(["    x2 = x0 + x1",
                                   "    x3 = x0 * x1",
                                   "    x4 = x1 * x0",
                                   "    # discard x4"]),
            returns="x3, x2")
    assert expected_source_code == source_code
    N_MAX = 50
    for _ in range(100):
        rand_num = random.randint(0,N_MAX**2)
        rand_a = rand_num//N_MAX
        rand_b = rand_num % N_MAX
        assert my_callable(rand_a,rand_b) == [rand_a*rand_b,rand_a+rand_b]
