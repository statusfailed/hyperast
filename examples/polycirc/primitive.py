""" The basic interface for building polynomial circuits """
# These are helpers which wrap each operation, and remove some work from the user.
# For example, they can write `add(a, b)` instead of manually having to...
#   - create an edge with a label
#   - specify source/target arity
#   - unify its nodes with the interfaces
#
# Note that in cases of operations with variable arity, we'd need to pass in a
# coarity manually, e.g.,
#   def spider(*args, coarity=0): ...
# or
#   def spider(*args, target=[explicit, type, here, ...]): ...

# TODO: add a get_context() function to allow these to get the builder
#   without going via @hypergraph.
# we can then rely on @hypergraph to annotate user context

#pylint:disable = missing-function-docstring,invalid-name

from hyperast import operation
from examples.polycirc.signature import Add, Mul

def add(x0, x1):
    # TODO: get context explicitly
    # NOTE: source_type can specify only arity
    return operation([x0, x1], source_type=2, target_type=1, label=Add())

def mul(x0, x1):
    return operation([x0, x1], source_type=2, target_type=1, label=Mul())
