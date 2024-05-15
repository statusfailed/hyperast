""" Static extraction of various data from .... """
from typing import Callable, List
import ast
import inspect
from dataclasses import dataclass

#pylint:disable = missing-function-docstring,missing-class-docstring

def fn_closure(f):
    """ Return a mapping of variables in f which are bound by a closure """
    freevars = f.__code__.co_freevars or []
    closure = f.__closure__ or []
    return { var: cell.cell_contents for var, cell in zip(freevars, closure) }

def fn_globals(f):
    """ Return a mapping of variables in f which are bound as globals """
    return dict(f.__globals__)

def bindings(f):
    """ Return a mapping k → v of variable names k to their bound values v. """
    d = fn_globals(f)
    d.update(fn_closure(f)) # closed variables override globals
    return d

def unindent(source_lines):
    """ Unindent source so it can be parsed to AST """
    # Find the minimum indentation (exclude empty lines)
    min_indent = min(
        len(line) - len(line.lstrip())
        for line in source_lines
        if line.strip()
    )

    # Strip minimum indentation
    stripped_source = [line[min_indent:] if len(line) > min_indent else line
                       for line in source_lines]
    return ''.join(stripped_source)

def to_ast(f):
    """ Try to turn a function f into its (unindented) source code & AST """
    # NB: throws OSError if source for a function can't be found.
    source_lines, _ = inspect.getsourcelines(f)
    source = unindent(source_lines)
    return source, ast.parse("".join(source))


# Visit all names in an AST and store them
# TODO: record both name id and its context (Load/Store)
class NameExtractor(ast.NodeVisitor):
    def __init__(self):
        self.names = []

    #pylint:disable=invalid-name
    def visit_Name(self, node):
        self.names.append(node.id)
        self.generic_visit(node)

def extract_names(tree):
    # Create an instance of the visitor and walk the AST
    extractor = NameExtractor()
    extractor.visit(tree)

    # Return the list of extracted names
    return extractor.names

@dataclass
class FunctionAnalysis:
    f: Callable
    source: str
    fs_ast: ast.AST
    names: List[ast.Name]
    bindings: dict
    names: List[str]

    @staticmethod
    def from_function(f: Callable):
        source, f_ast = to_ast(f)
        names = extract_names(f_ast)
        return FunctionAnalysis(
            f=f,
            source=source,
            names=names,
            fs_ast=f_ast,
            bindings=bindings(f))

    def bound(self):
        return { k: v for k, v in self.bindings.items() if k in set(self.names) }
