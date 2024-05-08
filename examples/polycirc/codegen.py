""" Python codegen (emit strings) """

from examples.ast import Apply, FunctionDefinition
from examples.polycirc.signature import *

FUNCTION_TEMPLATE = """
def {fn_name}({args}):
{assignments}
    return [{returns}]
    """

def op_to_expr(a: Apply):
    lhs = a.lhs
    rhs = a.rhs
    lhs_str = ", ".join(f"x{i}" for i in a.lhs)
    match a.op:
        case Constant(x): return str(x)
        case Add():
            assert len(rhs) == 2
            return f"{lhs_str} = x{rhs[0]} + x{rhs[1]}"
        case Neg():
            return f"{lhs_str} = -x{rhs[0]}"
        case Mul():
            assert len(rhs) == 2
            return f"{lhs_str} = x{rhs[0]} * x{rhs[1]}"
        case Copy():
            assert len(rhs) == 1
            assert len(lhs) == 2
            return f"{lhs_str} = x{rhs[0]}"
        case Discard():
            return f"# discard x{rhs[0]}" # dummy statement
        case _:
            return "Unknown operation"


def to_python(fn: FunctionDefinition, fn_name='fn'):
    args = ", ".join(f"x{i}" for i in fn.args)
    returns = ", ".join(f"x{i}" for i in fn.returns)
    assignments = "\n".join(f"    {op_to_expr(a)}" for a in fn.body)
    return FUNCTION_TEMPLATE.format(
            fn_name=fn_name,
            args=args,
            assignments=assignments,
            returns=returns)
