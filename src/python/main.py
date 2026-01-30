"""
This file provides the interface to use the uml converter
"""

import argparse
from uml_generator import generate_uml_from_files


def parse_arguments() -> tuple[str, tuple[str]]:
    """
    Parse command line arguments.
    :return: Tuple of the output file, and tuple of paths
    :rtype: tuple[str, tuple[str]]
    """
    parser = argparse.ArgumentParser(description="Generate UML diagrams from Python files")
    parser.add_argument("-o", "--output", default="uml_diagram", help="Output file name (default: uml_diagram)")
    parser.add_argument("-p", "--paths", nargs="+", required=True, help="Python file paths to analyze")
    
    args = parser.parse_args()
    return args.output, tuple(args.paths)


def main():
    """
    Main function to generate UML diagram from command line arguments.
    """
    output_file, file_paths = parse_arguments()
    generate_uml_from_files(output_file, *file_paths)

if __name__ == "__main__":
    main()
