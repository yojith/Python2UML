"""
Generate a UML diagram from an abstract syntax tree (AST) of Python code.
"""

import ast
from graphviz import Digraph
from abstracter import abstract_code


def create_nodes(ast_tree: ast.AST, dot: Digraph) -> None:
    """
    Create nodes in the UML diagram for each class in the AST.

    :param ast_tree: The abstract syntax tree
    :type ast_tree: AST
    :param dot: The Graphviz Digraph object
    :type dot: Digraph
    """
    for node in ast.walk(ast_tree):

        if isinstance(node, ast.ClassDef):
            method_string_list = _get_methods(node)
            attribute_string_list = _get_attributes(node)

            dot.node(node.name, shape="record", label=f"{{{node.name}|{"\\l".join(attribute_string_list)}\\l|{"\\l".join(method_string_list)}\\l}}")


def _get_methods(node: ast.ClassDef) -> list[str]:
    """
    Extract methods from a class node.

    :param node: The class definition node
    :type node: ClassDef
    :return: List of method names
    :rtype: list[str]
    """
    methods_list = [n for n in node.body if isinstance(n, ast.FunctionDef)]
    method_string_list = []

    for method in methods_list:
        if method.name == "__init__":
            method_string = f"+ {node.name}("
        else:
            if method.name[0] == "_":
                method_string = f"- {method.name}("
            else:
                method_string = f"+ {method.name}("

        for arg in method.args.args:
            if arg.arg != "self":
                type_name = ""
                if arg.annotation:
                    if isinstance(arg.annotation, ast.Name):
                        type_name = f": {arg.annotation.id}"
                method_string += f"{arg.arg}{type_name}"
        method_string += ")"

        if method.returns:
            if isinstance(method.returns, ast.Name):
                method_string += f": {method.returns.id}"
            elif isinstance(method.returns, ast.Constant):
                if method.returns.value is not None:
                    method_string += f": {method.returns.value}"
        method_string_list.append(method_string)

    return method_string_list


def _get_attributes(node: ast.ClassDef) -> list[str]:
    """
    Extract attributes from a class node.

    :param node: The class definition node
    :type node: ClassDef
    :return: List of attribute names
    :rtype: list[str]
    """
    attribute_string_list = []

    for f in node.body:
        if isinstance(f, ast.FunctionDef):
            for n in f.body:
                if isinstance(n, ast.AnnAssign):
                    if isinstance(n.target, ast.Attribute):
                        if n.target.attr[0] == "_":
                            attribute_string = f"- {n.target.attr}"
                        else:
                            attribute_string = f"+ {n.target.attr}"
                        if isinstance(n.annotation, ast.Name):
                            attribute_string += f": {n.annotation.id}"
                        attribute_string_list.append(attribute_string)

                elif isinstance(n, ast.Assign):
                    for target in n.targets:
                        if isinstance(target, ast.Attribute):
                            if target.attr[0] == "_":
                                attribute_string = f"- {target.attr}"
                            else:
                                attribute_string = f"+ {target.attr}"
                            attribute_string_list.append(attribute_string)

    return attribute_string_list


def parse_ast(ast_tree: ast.AST, filename: str) -> None:
    """
    Parses the AST and generates a UML diagram.

    :param ast_tree: The abstract syntax tree to parse
    :type ast_tree: AST
    """
    dot = Digraph(comment="UML Diagram")
    create_nodes(ast_tree, dot)
    # link_nodes(ast_tree, dot)
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
