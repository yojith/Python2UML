"""
Generate a UML diagram from an abstract syntax tree (AST) of Python code.
"""

import ast
from graphviz import Digraph
from pathlib import Path
from tkinter import filedialog
from tkinter import Tk

from node_generator import create_nodes
from node_linker import link_nodes
from abstracter import abstract_files


def create_dot() -> Digraph:
    """
    Create a Graphviz Digraph object for the UML diagram.

    :return: A Graphviz Digraph object
    :rtype: Digraph
    """
    dot = Digraph(comment="UML Diagram", graph_attr={"splines": "ortho", "nodesep": "1.0", "ranksep": "1.2"})
    return dot


def parse_ast(ast_tree_list: list[ast.AST], dot: Digraph) -> None:
    """
    Parses the AST and generates a UML diagram. Updates the provided Digraph object.

    :param ast_tree_list: The abstract syntax tree to parse
    :type ast_tree_list: list[AST]
    :param dot: The Graphviz Digraph object to update
    :type dot: Digraph
    """
    nodes = set()
    for ast_tree in ast_tree_list:
        nodes.update(create_nodes(ast_tree, dot))
    [link_nodes(ast_tree, dot, nodes) for ast_tree in ast_tree_list]
    print(dot.directory)


def save_uml(dot: Digraph, output_path: str, file_extenstion: str = "svg") -> None:
    """
    Saves the UML diagram to a file.
    :param dot: The Graphviz Digraph object
    :type dot: Digraph
    :param output_file: The output file name (without extension)
    :type output_file: str
    :param file_extenstion: The file extension/format (default: "svg")
    :type file_extenstion: str
    """

    if file_extenstion not in ["svg", "png", "pdf", "jpg", "jpeg"]:
        raise ValueError(f"Unsupported file extension: {file_extenstion}")

    if Path(output_path).suffix:
        file_extenstion = Path(output_path).suffix[1:]
        output_path = str(Path(output_path).with_suffix(""))

    dot.render(output_path, format=file_extenstion, cleanup=True)


def generate_uml_from_files(output: str, *paths: str) -> None:
    """
    Generates a UML diagram from Python source files.

    :param paths: Paths to the Python source files
    :type paths: str
    """
    dot = create_dot()
    filepaths = []
    for path in paths:
        # check if file is a folder
        if Path(path).is_dir():
            python_files = Path(path).rglob("*.py")
            filepaths.extend([str(file) for file in python_files])
        elif Path(path).is_file() and Path(path).suffix == ".py":
            filepaths.append(path)
        else:
            raise FileNotFoundError(f"Path {path} does not exist.")

    ast_tree = abstract_files(*filepaths)
    parse_ast(ast_tree, dot)
    save_uml(dot, output)


def main():
    """
    Test the parse_ast function on a sample AST.
    """
    generate_uml_from_files("output/example1", "src/test/example1.py")
    generate_uml_from_files("output/example2", "src/test/example2.py")
    generate_uml_from_files("output/example3", "src/test/example3.py")
    generate_uml_from_files("output/example4", "src/test/example4")


if __name__ == "__main__":
    main()
