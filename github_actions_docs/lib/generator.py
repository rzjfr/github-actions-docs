import difflib
import logging
import pathlib
import re
import tempfile

from github_actions_docs.config import DOCS_TEMPLATES
from github_actions_docs.errors import (
    GithubActionsDocsError,
    GithubActionsDocsSchemaError,
)
from github_actions_docs.lib.parser import GithubActions
from github_actions_docs.lib.styler import UpdateDocsStyle
from pygments import highlight
from pygments.formatters import Terminal256Formatter
from pygments.lexers import DiffLexer, MarkdownLexer


def generate_docs(
    file_paths: list,
    output_mode: str = "inject",
    docs_filename: str = "README.md",
    usage_ref_override: str = "",
    tag_prefix: str = "GH_DOCS",
    ignore: bool = False,
    dry_run: bool = False,
    show_diff: bool = False,
    generation_mode="inline",
) -> int:
    """
    Args:
        file_paths: list of files requires to be evaluated
        output_mode: inject to the existing docs_filename or create new based on the
            DOCS_TEMPLATE_ACTION
        docs_filename: name of the markdown file which will be created next to the
            input file.
        usage_ref_override: If empty tries to use the latest git tag and then
            branch name.
        tag_prefix: sections are designated by comments in markdown file. This
            parameter controls the prefix of those comments.
        ignore: continue if any one of the input files are not a valid github
            action or a workflow.

    Returns:
        exit code, 1 if any of input files has been changed, 0 if no change.
    """
    if dry_run:
        docs_path = pathlib.Path(tempfile.mkdtemp())
    changed_files = []
    for path in file_paths:
        logging.debug(f"evaluating: {path}")
        try:
            github_actions = GithubActions(path)
            parsed_yaml = github_actions.parse()
            action_type = parsed_yaml["runs"]
        except (GithubActionsDocsError, GithubActionsDocsSchemaError, KeyError) as e:
            if not ignore:
                logging.error(f"ignoring invalid file: {path}\n  reason: {e}")
                return 1
            logging.debug(f"ignoring invalid file: {path}\n  reason: {e}")
            continue  # it's not a valid github action or reusable workflow file

        UpdateDocsStyle(parsed_yaml, github_actions.yaml_path, usage_ref_override)

        # Setup output
        existing_docs_path = github_actions.yaml_path.parent.joinpath(docs_filename)
        existing_file_content = ""
        if existing_docs_path.is_file():
            with open(existing_docs_path, "r") as f:
                existing_file_content = f.read()
        if dry_run:
            docs_path = docs_path.joinpath(f"{hash(path)}_{docs_filename}")
            if existing_docs_path.is_file():
                with open(docs_path, "w") as f:
                    f.write(existing_file_content)
        else:
            docs_path = github_actions.yaml_path.parent.joinpath(docs_filename)
        # Generate changed file
        changed_file = create_or_update_docs_file(
            parsed_yaml,
            github_actions.yaml_path,
            docs_filename,
            output_mode,
            action_type,
            docs_path,
            tag_prefix,
        )
        changed_files.append(changed_file)
        # Generate output
        with open(docs_path, "r") as f:
            new_file_content = f.read()
        if dry_run:
            if not show_diff:
                print(new_file_content)
                logging.info(f"file would have been written in: {existing_docs_path}")
        if show_diff:
            diff = "".join(
                difflib.unified_diff(
                    existing_file_content.splitlines(keepends=True),
                    new_file_content.splitlines(keepends=True),
                    n=10,
                )
            )
            if not diff:
                print("No changes to the existing file!")
            else:
                print(highlight(diff, DiffLexer(), Terminal256Formatter()))
        if changed_file:
            logging.info(f"changed for file: {github_actions.yaml_path}")
        else:
            logging.info(f"no change: {github_actions.yaml_path}")
    logging.debug(f"number of changed files: {sum(changed_files)}/{len(file_paths)}")
    return 1 if any(changed_files) else 0


def create_or_update_docs_file(
    docs_items: dict,
    yaml_path: str,
    docs_filename: str,
    output_mode: str,
    action_type: str,
    docs_path: pathlib.Path,
    tag_prefix: str = "GH_DOCS",
) -> bool:
    """
    Returns:
        True if the file has been updated
    """
    file_changed = False
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


def replace_tags(
    content: str, tag_name: str, tag_value: str, tag_prefix: str = "GH_DOCS"
) -> str:
    """ """
    identifier = f"{tag_prefix}_{tag_name.upper()}"
    # Update tags
    content = re.sub(
        rf"(<!-- BEGIN_{identifier} -->)(.*)(<!-- END_{identifier} -->)",
        rf"\1{tag_value}\3",
        content,
        flags=re.DOTALL,
    )
    # Generate
    content = re.sub(
        rf"<!-- {identifier} -->",
        f"<!-- BEGIN_{identifier} -->{tag_value}<!-- END_{identifier} -->",
        content,
    )
    return content


def find_table_of_contents(content: str, tag_prefix: str = "GH_DOCS") -> str:
    """ """
    identifier = f"{tag_prefix}_CONTENTS_TABLE_ITEM"
    if result := re.search(
        rf"(<!-- BEGIN_{identifier} -->)(.*)(<!-- END_{identifier} -->)",
        content,
        flags=re.DOTALL,
    ):
        return result.group(2)
    else:
        return ""
