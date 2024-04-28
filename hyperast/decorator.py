from typing import List, Tuple, Callable
from dataclasses import dataclass, field

################################################################################
# inspection functions
import inspect

def arity(f: Callable):
    sig = inspect.signature(f)
    positional_args = sum(
        1 for param in sig.parameters.values()
        if param.kind in [param.POSITIONAL_ONLY, param.POSITIONAL_OR_KEYWORD] and param.default is param.empty
    )
    return positional_args

################################################################################
# Hypegraph builder class

@dataclass
class Builder:
    nodes: List = field(default_factory=list)
    edges: List = field(default_factory=list)

    # a quotienting of hypernodes
    quotient: List[Tuple[int, int]] = field(default_factory=list)

    _source: List[int] = field(default_factory=list)
    _target: List[int] = field(default_factory=list)

    @property
    def source(self):
        return self._source

    @source.setter
    def source(self, s):
        assert (x <= n for x in s)        
        self._source = s

    @property
    def target(self):
        return self._target

    @target.setter
    def target(self, s):
        assert (x <= n for x in s)        
        self._target= s

    def node(self, label=None):
        i = len(self.nodes)
        self.nodes.append((i, label))
        return i

    def edge(self, targets, label=None):
        i = len(self.edges)
        # TODO!
        self.edges.append(None)
        return i 

    def unify(self, *args):
        n = len(self.nodes)
        assert all(x < n for x in args)
        self.quotient.extend(*args)

################################################################################
# Interface module

# a global builder variable.
# when None, the hypergraph decorator will initialize it, call a function, then set back to None
# when a Builder, it will be
builder = None

def node(*args, **kwargs):
    global builder
    return builder.node(*args, **kwargs)

def edge(*args, **kwargs):
    global builder
    return builder.edge(*args, **kwargs)

def unify(*args):
    """ Unify a number of variables """
    pass

# decorator
def hypergraph(f: Callable):
    def hypergraph_wrapper(*args, **kwargs):
        global builder

        if builder is None:
            # this is the top-level invocation of @hypergraph when builder is
            # unset, so we have to create it.
            builder = Builder()

            # called without the *args (nodes); we need to create them
            if len(args) > 0:
                raise ValueError("Functions annotated with @hypergraph should be called without positional args")
            source = [ builder.node() for x in range(arity(f)) ]
            builder.source = source
            target = f(*source, **kwargs) # get targets by running the function
            builder.target = target

            # finally, unset builder and return
            result = builder
            builder = None
            return result
        else:
            # In this branch, we're in a nested call, so we use the existing
            # builder which is already set
            target = f(*args, **kwargs)
            return target

    return hypergraph_wrapper
