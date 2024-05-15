#pylint:disable = missing-function-docstring,missing-docstring,unused-import,too-few-public-methods,invalid-name

from dataclasses import dataclass
from enum import Enum, auto

################################################################################
# Signature

# Polynomial circuits over finite semirings.
#   Generating objects: {*} (we use None)
#   Generating operations:
#
# Semirings
#       0 : 0 → 1
#       1 : 0 → 1
#       + : 2 → 1
#       - : 1 → 1       # unary negate
#       * : 2 → 1
#
# Cartesian
#       Δ : 1 → 2
#       ! : 1 → 0
#
# Polynomial circuits
#       s : 0 → 1

# In general, ops are only labels. They don't have types assigned - this comes later.
class Op:
    pass

# constants are special; they have some data associated with them.
@dataclass
class Constant(Op):
    x: int

class Add(Op):
    pass
class Neg(Op):
    pass
class Mul(Op):
    pass
class Copy(Op):
    pass
class Discard(Op):
    pass

operation = Add | Neg | Mul | Constant | Copy | Discard
