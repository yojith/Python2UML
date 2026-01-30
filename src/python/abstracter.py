"""
This file takes a python source file and converts it into an abstract syntax tree (AST).
"""

import ast


def abstract_files(*files: str) -> list[ast.AST]:
    """
    Convert Python source files into their corresponding ASTs.

    :param files: Paths to the Python source files
    :type files: str
    :return: List of ASTs for the provided files
    :rtype: list[AST]
    """
    tree_list = []
    for filepath in files:
        print(f"Reading file: {filepath}")
        with open(filepath, "r", encoding="utf-8") as file:
            code = file.read()
            tree_list.append(ast.parse(code))
            print("...Converted to AST")
    return tree_list


def main():
    """
    Test the abstract_code function on a sample file.
    """
    files = ["src/test/example3.py"]
    tree = abstract_files(*files)
    print(ast.dump(tree[0], indent=4))


if __name__ == "__main__":
    main()
