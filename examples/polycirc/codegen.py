""" Python codegen (emit strings) """
from typing import Tuple, Callable

from examples.ast import Apply, FunctionDefinition
#pylint:disable=wildcard-import,unused-wildcard-import
from examples.polycirc.signature import *

FUNCTION_TEMPLATE = """
def {fn_name}({args}):
{assignments}
    return [{returns}]
    """

#pylint:disable=too-many-return-statements
def op_to_expr(a: Apply):
    """
    single simple python line
    """
    lhs = a.lhs
    rhs = a.rhs
    lhs_str = ", ".join(f"x{i}" for i in a.lhs)
    match a.op:
        case Constant(x):
            return str(x)
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


def _to_function(code: str, name: str):
    # Create a local dictionary to execute the code and capture the function definition
    env = {}
    #pylint:disable=exec-used
    exec(code, {}, env)

    # Retrieve the function object using its name from the local dictionary
    return env[name]

def to_python(fn: FunctionDefinition, fn_name='fn') -> Tuple[Callable, str]:
    """
    FunctionDef -> python code for it and the function itself
    """
    args = ", ".join(f"x{i}" for i in fn.args)
    returns = ", ".join(f"x{i}" for i in fn.returns)
    assignments = "\n".join(f"    {op_to_expr(a)}" for a in fn.body)
    code = FUNCTION_TEMPLATE.format(
            fn_name=fn_name,
            args=args,
            assignments=assignments,
            returns=returns)

    return _to_function(code, fn_name), code
