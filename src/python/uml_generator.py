"""
Generate a UML diagram from an abstract syntax tree (AST) of Python code.
"""

import ast
from graphviz import Digraph

from node_generator import create_nodes
from node_linker import link_nodes
from abstracter import abstract_code


def parse_ast(ast_tree: ast.AST, filename: str) -> None:
    """
    Parses the AST and generates a UML diagram.

    :param ast_tree: The abstract syntax tree to parse
    :type ast_tree: AST
    """
    dot = Digraph(comment="UML Diagram", graph_attr={"splines": "ortho", "nodesep": "1.0", "ranksep": "1.2"})

    nodes = create_nodes(ast_tree, dot)
    link_nodes(ast_tree, dot, nodes)
    print(dot.directory)
    dot.render(f"output/{filename}", format="svg")


def main(filepath: str):
    """
    Test the parse_ast function on a sample AST.
    """
    tree = abstract_code(filepath)
    filename = filepath.split("/")[-1].split(".")[0]
    parse_ast(tree, filename)


if __name__ == "__main__":
    main("src/test/example1.py")
    main("src/test/example2.py")
    main("src/test/example3.py")
