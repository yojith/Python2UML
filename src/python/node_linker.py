"""
This file links nodes for a UML diagram from a python AST.
"""

import ast
from graphviz import Digraph


def link_nodes(ast_tree: ast.AST, dot: Digraph, node_set: set[str]) -> None:
    """
    Link nodes in the UML diagram based on class inheritance, association, etc.

    :param ast_tree: The abstract syntax tree
    :type ast_tree: ast.AST
    :param dot: The Graphviz Digraph object
    :type dot: Digraph
    :param node_set: Set of node names created
    :type node_set: set[str]
    """
    for node in ast.walk(ast_tree):
        if isinstance(node, ast.ClassDef):
            # Check inheritance
            for parent in node.bases:
                if isinstance(parent, ast.Name):
                    if parent.id in node_set:
                        print(f"{node.name} inherits from {parent.id}")
                        dot.edge(parent.id, node.name, arrowhead="onormal", headport="n", tailport="s")

            # Check associations via attributes
            for f in node.body:
                if isinstance(f, ast.FunctionDef):
                    # Check for parameters in each function for aggregation
                    for arg in f.args.args:
                        if arg.arg != "self":
                            if arg.annotation and isinstance(arg.annotation, ast.Name):
                                print(f"{node.name} has an association with {arg.annotation.id}")
                                if arg.annotation.id in node_set:
                                    dot.edge(node.name, arg.annotation.id, arrowhead="normal", headport="n", tailport="s")

                    for n in f.body:

                        # Check for annotated assignment
                        if isinstance(n, ast.AnnAssign):
                            if isinstance(n.annotation, ast.Name):
                                print(f"{node.name} has an association with {n.annotation.id}")
                                if n.annotation.id in node_set:
                                    dot.edge(node.name, n.annotation.id, arrowhead="normal", headport="s", tailport="n")

                        # Check for instantiation in assignment value (composition)
                        elif isinstance(n, ast.Assign):
                            # Check for instantiation in assignment value
                            if isinstance(n.value, ast.Call):
                                if isinstance(n.value.func, ast.Name):
                                    print(f"{node.name} has an association with {n.value.func.id}")
                                    if n.value.func.id in node_set:
                                        dot.edge(node.name, n.value.func.id, arrowhead="normal", headport="s", tailport="n")
