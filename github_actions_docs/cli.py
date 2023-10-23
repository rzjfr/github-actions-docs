import argparse


def build_args_parser(description: str, version: str) -> argparse.ArgumentParser:
    """
    Returns:
        An ArgumentParser instance for the CLI.
    """
    parser = argparse.ArgumentParser(
        prog="github-actions-docs",
        description=description,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--version",
        action="version",
        version=version,
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="print out file names while processing.",
    )
    parser.add_argument(
        "--silent",
        action="store_true",
        help="continue on parse error.",
    )
    parser.add_argument(
        "--tag-prefis",
        type=str,
        default="GH_DOCS",
        help="Prefix used for the tags in the output.",
    )
    parser.add_argument(
        "--output-mode",
        nargs="?",
        choices=["replace", "inject"],
        default="inject",
        help="output to file method",
    )
    parser.add_argument(
        "--docs-filename",
        type=str,
        default="README.md",
        help="creates or updates output on the same path as the input.",
    )
    parser.add_argument(
        "--uses-ref-override",
        type=str,
        default="",
        help="Override the uses reference in usage section.\
                By default latest tag or current branch name will be used.",
    )
    parser.add_argument(
        "input_files_path",
        nargs="+",
        type=str,
        help="Path of a github reusable workflow or composite action file.",
    )
    return parser
