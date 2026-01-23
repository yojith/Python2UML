"""
This file creates nodes for a UML diagram from a python AST.
"""

import ast
from graphviz import Digraph


def create_nodes(ast_tree: ast.AST, dot: Digraph) -> set[str]:
    """
    Create nodes in the UML diagram for each class in the AST.

    :param ast_tree: The abstract syntax tree
    :type ast_tree: AST
    :param dot: The Graphviz Digraph object
    :type dot: Digraph
    :return: Set of node names created
    :rtype: set[str]
    """
    node_set = set()
    for node in ast.walk(ast_tree):

        if isinstance(node, ast.ClassDef):
            attribute_string_list = _get_attributes(node)
            method_string_list = _get_methods(node)

            html_attributes = "".join([f'{attribute}<BR ALIGN="LEFT"/>' for attribute in attribute_string_list])
            html_methods = "".join([f'{method}<BR ALIGN="LEFT"/>' for method in method_string_list])

            html_string = f"""<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" CELLPADDING="6">
            <TR><TD>{node.name}</TD></TR>
            <TR><TD ALIGN="LEFT">{html_attributes}</TD></TR>
            <TR><TD ALIGN="LEFT">{html_methods}</TD></TR>
            </TABLE>>"""

            dot.node(node.name, shape="plaintext", label=html_string, margin="0")
            node_set.add(node.name)

    return node_set


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

        method_parameters = []
        for arg in method.args.args:
            if arg.arg != "self":
                type_name = ""
                if arg.annotation:
                    if isinstance(arg.annotation, ast.Name):
                        type_name = f": {arg.annotation.id}"
                method_parameters.append(f"{arg.arg}{type_name}")
        method_string += ", ".join(method_parameters) + ")"

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
