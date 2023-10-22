import argparse
import logging
import pathlib
import re
import sys

from importlib_metadata import metadata

from github_actions_docs.canvas import (
    find_table_of_contents,
    generate_usage,
    replace_tags,
    update_style,
)
from github_actions_docs.configs import DOCS_TEMPLATES
from github_actions_docs.errors import (
    GithubActionsDocsError,
    GithubActionsDocsSchemaError,
)
from github_actions_docs.parser import parse_yaml

__version__ = metadata("github-actions-docs")["Version"]
logging.basicConfig(stream=sys.stdout, level=logging.WARNING)


def generate_docs(
    file_paths: list,
    output_mode: str = "inject",
    docs_filename: str = "README.md",
    uses_ref_override: str = "",
) -> int:
    """
    Params:
        file_paths: list of files requires to be evaluated
        output_mode: inject to the existing docs_filename or create new based on the
            DOCS_TEMPLATE_ACTION
        docs_filename: name of the markdown file which will be created next to the
            input file.
        uses_ref_override: If empty tries to use the latest git tag and then
            branch name.

    Returns:
        exit code, 1 if any of input files has been changed, 0 if no change.
    """
    changed_files = []
    for path in file_paths:
        logging.debug(f"evaluating: {path}")

        yaml_path = pathlib.Path(path)
        try:
            parsed_yaml = parse_yaml(yaml_path)
        except (GithubActionsDocsError, GithubActionsDocsSchemaError) as e:
            logging.debug(f"ignoring invalid file: {path}\n  reason: {e}")
            continue  # it's not a valid github action or reusable workflow file

        action_path = f"/{yaml_path.parent}"
        action_filename = (
            f"/{yaml_path.name}" if parsed_yaml["runs"] == "reusable workflow" else ""
        )
        action_type = parsed_yaml["runs"]
        action_name = parsed_yaml["name"]
        parsed_yaml["usage"] = generate_usage(
            parsed_yaml["inputs"]["content"],
            parsed_yaml["runs"],
            uses_ref_override,
            action_path,
            action_filename,
            action_name,
        )
        docs_items = update_style(parsed_yaml)
        changed_file = create_or_update_docs_file(
            docs_items,
            yaml_path,
            docs_filename,
            output_mode,
            action_type,
            action_name,
        )
        changed_files.append(changed_file)
        if changed_file:
            logging.error(f"changed file: {yaml_path}")
    logging.debug(f"number of changed files: {sum(changed_files)}/{len(file_paths)}")
    return 1 if any(changed_files) else 0


def create_or_update_docs_file(
    docs_items: dict,
    yaml_path: pathlib.PosixPath,
    docs_filename: str,
    output_mode: str,
    action_type: str,
    action_name: str,
    tag_prefix: str = "GH_DOCS",
) -> bool:
    """
    Returns:
        True if the file has been updated
    """
    file_changed = False
    docs_path = yaml_path.parent.joinpath(docs_filename)
    if action_type not in DOCS_TEMPLATES:
        template = DOCS_TEMPLATES["generic"].format(prefix=tag_prefix)
    else:
        template = DOCS_TEMPLATES[action_type].format(prefix=tag_prefix)

    # Create file based on the template
    create_file_from_template = not docs_path.is_file() or output_mode == "replace"
    if create_file_from_template:
        with open(docs_path, "w") as f:
            f.write(template)
            file_changed = True

    # Read file
    with open(docs_path, "r") as f:
        content = f.read()

    # Append the template if none of the valid tags already exist
    valid_tag_exists = re.search(rf"<!--\s(BEGIN_)?{tag_prefix}(_.+)\s-->", content)
    if not valid_tag_exists and output_mode == "inject":
        with open(docs_path, "a+") as f:
            f.write(re.sub("#.+\n", "", template, count=1))
            f.flush()
            f.seek(0)
            file_changed = True
            content = f.read()

    if action_type == "reusable workflow":
        item_id = (
            re.sub(r"[^a-z\d\s]", "", docs_items["name"].lower())
            .replace(" ", "_")
            .upper()
        )
        # Add if item_id wich represents the respective action does not exist
        if item_id not in content:
            with open(docs_path, "a+") as f:
                f.write(
                    "\n"
                    + DOCS_TEMPLATES["reusable workflow item"]
                    .format(prefix=tag_prefix)
                    .replace("ITEM_ID", item_id)
                )
                f.flush()
                f.seek(0)
                file_changed = True
                content = f.read()
        # Update table of contents
        existing_table_of_contents = find_table_of_contents(content)
        if docs_items["contents_table_item"] not in existing_table_of_contents:
            table_of_contents = (
                existing_table_of_contents + docs_items["contents_table_item"]
            )
        else:
            table_of_contents = existing_table_of_contents
        docs_items["contents_table_item"] = "\n\n" + table_of_contents.lstrip("\n")

    for item in docs_items.keys():
        content = replace_tags(content, item, docs_items[item], tag_prefix)
        if action_type == "reusable workflow":
            content = replace_tags(
                content, f"{item}_{item_id}", docs_items[item], tag_prefix
            )

    # Check if anything has changed
    with open(docs_path, "r") as f:
        old_content = f.read()

    if change_status := (not old_content == content) or file_changed:
        logging.info(f"generating: {docs_path}")
        with open(docs_path, "w") as f:
            f.write(content.lstrip())
    else:
        logging.debug(f"no changes made: {docs_path}")
    return change_status


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
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    exit_code = generate_docs(
        file_paths=args.input_files_path,
        output_mode=args.output_mode,
        docs_filename=args.docs_filename,
        uses_ref_override=args.uses_ref_override,
    )
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
