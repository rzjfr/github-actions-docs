import argparse
import pathlib
import sys

from importlib_metadata import metadata

from github_actions_docs.canvas import generate_usage, replace_tags, update_style
from github_actions_docs.errors import GithubActionsDocsError
from github_actions_docs.parser import parse_yaml

__version__ = metadata("github-actions-docs")["Version"]


DOCS_TEMPLATE = """# <!-- GH_DOCS_NAME -->

<!-- GH_DOCS_DESCRIPTION -->

> [!NOTE]
> This action is a <!-- GH_DOCS_RUNS --> action.

## Inputs

<!-- GH_DOCS_INPUTS -->

## Outputs

<!-- GH_DOCS_OUTPUTS -->

## Usage

<!-- GH_DOCS_USAGE -->
"""


def generate_docs(
    file_paths: list,
    output_mode: str = "inject",
    verbose: bool = False,
    docs_filename: str = "README.md",
    uses_ref_override: str = "",
) -> int:
    """
    Params:
        file_paths: list of files requires to be evaluated
        output_mode: inject to the existing docs_filename or create new based on the
            DOCS_TEMPLATE
        verbose: more logs
        docs_filename: name of the markdown file which will be created next to the
            input file.
        uses_ref_override: If empty tries to use the latest git tag and then
            branch name.

    Returns:
        exit code, 1 if any of input files has been changed, 0 if no change.
    """
    changed_files = []
    for path in file_paths:
        if verbose:
            print(f"evaluating: {path}")

        yaml_path = pathlib.Path(path)
        try:
            parsed_yaml = parse_yaml(yaml_path)
        except GithubActionsDocsError:
            if verbose:
                print(f"ignoring invalid file: {path}")
            continue  # it's not a valid github action or reusable workflow file

        action_path = (
            f"/{yaml_path.parent}" if parsed_yaml["runs"] == "composite" else ""
        )
        parsed_yaml["usage"] = generate_usage(
            parsed_yaml["inputs"]["content"],
            uses_ref_override,
            action_path,
            yaml_path.name,
        )

        docs_items = update_style(parsed_yaml)

        docs_path = yaml_path.parent.joinpath(docs_filename)
        if not docs_path.is_file() or output_mode == "replace":
            with open(docs_path, "w") as f:
                f.write(DOCS_TEMPLATE)

        with open(docs_path, "r") as f:
            content = f.read()

        for item in docs_items.keys():
            content = replace_tags(content, item, docs_items[item])

        with open(docs_path, "r") as f:
            old_content = f.read()

        if change_status := not old_content == content:
            with open(docs_path, "w") as f:
                print(f"generating: {docs_path}")
                f.write(content.lstrip())
        elif verbose:
            print(f"no changes made: {docs_path}")

        changed_files.append(change_status)

    if verbose:
        print(f"number of changed files: {sum(changed_files)}/{len(file_paths)}")

    return 1 if any(changed_files) else 0


def _build_args_parser() -> argparse.ArgumentParser:
    """
    Returns:
        An ArgumentParser instance for the CLI.
    """
    parser = argparse.ArgumentParser(
        prog="github-actions-docs",
        description=metadata("github-actions-docs")["Description"],
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s {}".format(__version__),
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="print out file names while processing.",
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


def main():
    """main"""
    args = _build_args_parser().parse_args()
    exit_code = generate_docs(
        file_paths=args.input_files_path,
        output_mode=args.output_mode,
        verbose=args.verbose,
        docs_filename=args.docs_filename,
        uses_ref_override=args.uses_ref_override,
    )
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
