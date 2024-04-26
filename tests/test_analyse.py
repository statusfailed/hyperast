from hyperast.analyse import FunctionAnalysis

# Example code to test
import math
def wrap():
    import math as zerp # checking aliases and enclosing scopes work
    def foo(x):
        # foo uses two bound vars: "math" and "zerp"
        x
        y = math.log(1) + zerp.log(1)
        return [x, y]
    return foo


def test_analyse_foo():
    foo = wrap()
    a = FunctionAnalysis.from_function(foo)
    assert set(a.names) == {"x", "y", "math", "zerp"}
    assert a.bound() == { "math": math, "zerp": math }
