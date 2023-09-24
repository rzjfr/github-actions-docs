import argparse
import pathlib
import re
import sys

import git
import yaml
from importlib_metadata import metadata

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


class GithubActionsDocsError(Exception):
    """Parent class for user errors or input errors.

    Exceptions of this type are handled by the command line tool
    and result in clear error messages, as opposed to backtraces.
    """


class GithubActionsDocsSchemaError(GithubActionsDocsError):
    """Schema errors"""

    def __init__(self, required_fields, field):
        message = f"{required_fields} are required inside {field}.\n\
https://docs.github.com/en/actions/creating-actions/metadata-syntax-for-github-actions"
        super().__init__(message)


def parse_yaml(yaml_path: str) -> dict:
    """validates and parses action file to extract the relevant information"""
    if not yaml_path.is_file():
        raise GithubActionsDocsError(f"file {yaml_path} does not exist")
    if not yaml_path.suffix == ".yaml":
        raise GithubActionsDocsError(f"expected .yaml instead of {yaml_path.suffix}.")
    with open(yaml_path, "r") as f:
        yaml_content = yaml.safe_load(f)

    if not type(yaml_content) == dict:
        raise GithubActionsDocsError("file doesn't seem to be a valid action file.")

    result = {}
    gh_actions_required_fields = {"name", "description", "runs"}
    if not gh_actions_required_fields <= set(yaml_content.keys()):
        raise GithubActionsDocsSchemaError(
            list(gh_actions_required_fields), "top level"
        )

    result["name"] = yaml_content["name"]
    result["description"] = yaml_content["description"]

    inputs, inputs_content = yaml_content.get("inputs", {}), []
    for item in inputs.keys():
        if "description" not in inputs[item].keys():
            raise GithubActionsDocsSchemaError(["description"], f".inputs.{item}")
        inputs_content.append(
            [
                item,
                inputs[item]["description"].replace("\n", ""),
                f"{inputs[item].get('required', True)}",
                f"\"{inputs[item].get('default', '')}\"",
            ]
        )
    result["inputs"] = {
        "header": ["parameter", "description", "required", "default"],
        "content": inputs_content,
    }

    outputs, output_content = yaml_content.get("outputs", {}), []
    for item in outputs.keys():
        if "description" not in outputs[item].keys():
            raise GithubActionsDocsSchemaError(["description"], f".outputs.{item}")
        output_content.append(
            [
                item,
                outputs[item]["description"].replace("\n", ""),
            ]
        )
    result["outputs"] = {
        "header": ["parameter", "description"],
        "content": output_content,
    }

    try:
        result["runs"] = f"{yaml_content['runs']['using']}"
    except KeyError:
        raise GithubActionsDocsSchemaError(["using"], ".runs")

    return result


def generate_usage(inputs: list, composit_action_path: str = "") -> str:
    repo = git.Repo(".")
    tags = sorted(repo.tags, key=lambda t: t.commit.committed_datetime)
    latest_tag = str(tags[-1]) if tags else "main"
    if repo.remotes:
        repo_ref = "/".join(repo.remotes[0].url.split("/")[3:])
    else:
        repo_ref = "owner/repoitory_name"
    result = "- name: Example Usage\n"
    result += f"  uses: {repo_ref}{composit_action_path}@{latest_tag}\n"
    result += "  with:\n"
    for item in inputs:
        result += f"    {item[0]}: {item[3]}\n"

    return result


def update_style(parsed_yaml: dict) -> dict:
    if parsed_yaml["inputs"]["content"]:
        inputs_table = create_table(
            parsed_yaml["inputs"]["header"],
            parsed_yaml["inputs"]["content"],
        )
        parsed_yaml["inputs"] = f"\n\n{inputs_table}\n"
    else:
        parsed_yaml["inputs"] = "\n\nThis Action does not have any inputs.\n\n"

    if parsed_yaml["outputs"]["content"]:
        outputs_table = create_table(
            parsed_yaml["outputs"]["header"],
            parsed_yaml["outputs"]["content"],
        )
        parsed_yaml["outputs"] = f"\n\n{outputs_table}\n"
    else:
        parsed_yaml["outputs"] = "\n\nThis Action does not have any outputs.\n\n"

    parsed_yaml["runs"] = f"`{parsed_yaml['runs']}`"

    parsed_yaml["description"] = f"\n\n{parsed_yaml['description'].strip()}\n\n"

    parsed_yaml["usage"] = f"\n\n```yaml\n{parsed_yaml['usage']}```\n\n"

    return parsed_yaml


def create_table(data_header: list, data_content) -> str:
    """creates markdown tabels"""
    transposed_data = list(zip(data_header, *data_content))
    column_size = [len(max(i, key=len)) for i in transposed_data]
    separator = ["-" * i for i in column_size]
    data = [data_header, separator, *data_content]
    result = ""
    for row in data:
        result += (
            "".join([f"| {row[i]: <{column_size[i]}} " for i in range(len(row))])
            + "|\n"
        )

    return result


def replace_tag(
    content: str, tag_name: str, tag_value: str, tag_prefix: str = "GH_DOCS"
) -> str:
    """ """
    # Update tags
    content = re.sub(
        rf"(<!-- BEGIN_{tag_prefix}_{tag_name.upper()} -->)(.*)(<!-- END_{tag_prefix}_{tag_name.upper()} -->)",
        rf"\1{tag_value}\3",
        content,
        flags=re.DOTALL,
    )
    # Generate
    content = re.sub(
        rf"<!-- {tag_prefix}_{tag_name.upper()} -->",
        f"<!-- BEGIN_{tag_prefix}_{tag_name.upper()} -->{tag_value}<!-- END_{tag_prefix}_{tag_name.upper()} -->",
        content,
    )
    return content


def generate_docs(docs_file: str = "README.md") -> int:
    """ """
    args = _build_parser().parse_args()
    failed = False
    for path in args.path:
        # Prepare
        yaml_path = pathlib.Path(path)
        try:
            parsed_yaml = parse_yaml(yaml_path)
        except GithubActionsDocsError:
            continue
        action_path = (
            f"/{yaml_path.parent}" if parsed_yaml["runs"] == "composite" else ""
        )
        parsed_yaml["usage"] = generate_usage(
            parsed_yaml["inputs"]["content"], action_path
        )

        docs_items = update_style(parsed_yaml)

        # Generate
        docs_path = yaml_path.parent.joinpath(docs_file)
        if not docs_path.is_file() or args.output_mode == "replace":
            with open(docs_path, "w") as f:
                f.write(DOCS_TEMPLATE)

        with open(docs_path, "r") as f:
            content = f.read()

        for item in docs_items.keys():
            content = replace_tag(content, item, docs_items[item])

        with open(docs_path, "r") as f:
            old_content = f.read()

        if not old_content == content:
            failed = True
            with open(docs_path, "w") as f:
                print(f"generating: {docs_path}")
                f.write(content.lstrip())

    return 1 if failed else 0


def _build_parser() -> argparse.ArgumentParser:
    """
    returns:
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
        "path",
        nargs="+",
        type=str,
        help="Path of a github reusable workflow or composite action file.",
    )
    return parser


def main():
    sys.exit(generate_docs())


if __name__ == "__main__":
    # <!-- BEGIN_GH_DOCS -->
    main()
