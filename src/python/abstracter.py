"""
This file takes a python source file and converts it into an abstract syntax tree (AST).
"""

import ast


def abstract_code(filepath: str) -> ast.AST:
    """
    Turns a python file into an abstract syntax tree

    :param filepath: Path to the python file
    :type filepath: str
    :return: Returns an abstract syntax tree
    :rtype: AST
    """
    print(f"Reading file: {filepath}")
    with open(filepath, "r", encoding="utf-8") as file:
        code = file.read()
        tree = ast.parse(code)
        print("...Converted to AST")
    return tree


def main():
    """
    Test the abstract_code function on a sample file.
    """
    filepath = "src/test/example3.py"
    tree = abstract_code(filepath)
    print(ast.dump(tree, indent=4))


if __name__ == "__main__":
    main()
