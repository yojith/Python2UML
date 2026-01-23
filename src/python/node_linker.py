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
                        dot.edge(node.name, parent.id, arrowhead="empty", tailport="s", headport="n", xlabel="inherits")

            # Check associations via attributes
            for f in node.body:
                if isinstance(f, ast.FunctionDef):
                    for n in f.body:
                        if isinstance(n, ast.AnnAssign):
                            if isinstance(n.annotation, ast.Name):
                                print(f"{node.name} has an association with {n.annotation.id}")
                                if n.annotation.id in node_set:
                                    dot.edge(node.name, n.annotation.id, arrowhead="vee", headport="e", tailport="w", label="has a")
                        elif isinstance(n, ast.Assign):
                            for target in n.targets:
                                if isinstance(target, ast.Attribute):
                                    if isinstance(n.value, ast.Name):
                                        print(f"{node.name} has an association with {n.value.id}")
                                        if n.value.id in node_set:
                                            dot.edge(node.name, n.value.id, arrowhead="vee", headport="e", tailport="w", label="has a")
