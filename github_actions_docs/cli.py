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
        help="More verbosity in logging.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show content of the generated docs instead of writing it.",
    )
    parser.add_argument(
        "--show-diff",
        action="store_true",
        help="Show diff between existing file and the newly generated one.",
    )
    parser.add_argument(
        "--ignore",
        action="store_true",
        help="Silently ignore the invalid files.",
    )
    parser.add_argument(
        "--tag-prefix",
        type=str,
        default="GH_DOCS",
        help="Prefix used for the tags in the output.",
    )
    parser.add_argument(
        "--output-mode",
        nargs="?",
        choices=["replace", "inject"],
        default="inject",
        help="Method of output to file.",
    )
    parser.add_argument(
        "--generation-mode",
        nargs="?",
        choices=["inline", "block"],
        default="inline",
        help="Whether to create tags inline (more flexibility but more noise).",
    )
    parser.add_argument(
        "--docs-filename",
        type=str,
        default="README.md",
        help="Creates or updates output on the same path as the input.",
    )
    parser.add_argument(
        "--usage-ref-override",
        type=str,
        default="",
        help="Override the uses reference in usage section.\
                By default latest tag or current branch name will be used.",
    )
    parser.add_argument(
        "input_files_path",
        nargs="+",
        type=str,
        help="Path of github action or reusable workflow file(s).",
    )
    return parser
