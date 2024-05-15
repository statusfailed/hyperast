#pylint:disable=missing-function-docstring,missing-docstring,invalid-name,pointless-statement

from hyperast.analyse import FunctionAnalysis

# Example code to test
#pylint:disable=wrong-import-order
import math
def wrap():
    #pylint:disable=import-outside-toplevel,reimported
    import math as zerp # checking aliases and enclosing scopes work
    def my_foo(x):
        # foo uses two bound vars: "math" and "zerp"
        x
        y = math.log(1) + zerp.log(1)
        return [x, y]
    return my_foo


def test_analyse_foo():
    our_foo = wrap()
    a = FunctionAnalysis.from_function(our_foo)
    assert set(a.names) == {"x", "y", "math", "zerp"}
    assert a.bound() == { "math": math, "zerp": math }
