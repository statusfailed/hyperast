# HyperAST

A (currently experimental) frontend to
[open-hypergraphs](https://github.com/statusfailed/open-hypergraphs/)
which hijacks python syntax to define a hypergraph.

For example, you write:

    def adder(x0, x1):
        y0 = x0 + x1 # sum
        y1 = x0 * x1 # carry
        return [y0, y1]

Variables serve as hypernodes. Functions and python operators are (labeled) hyperedges. The result is an
open hypergraph (i.e., a string diagram) like this:

![adder diagram](./propaganda/adder.png)
