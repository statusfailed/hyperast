# HyperAST

A (currently experimental) frontend to
[open-hypergraphs](https://github.com/statusfailed/open-hypergraphs/)
which hijacks python syntax to define a hypergraph.

For example, you write:

    @hypergraph
    def adder(x0, x1):
        y0 = x0 + x1 # sum
        y1 = x0 * x1 # carry
        return [y0, y1]

To get an open hypergraph representing a string diagram like this:

![adder diagram](./propaganda/adder.png)

In python syntax, variables serve as hypernodes while functions and python
operators are (labeled) hyperedges.
