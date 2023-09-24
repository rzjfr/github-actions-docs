import argparse
import pathlib
import re
import sys

import git
import yaml
from importlib_metadata import metadata
from tabulate import tabulate

__version__ = metadata("github-actions-docs")["Version"]


DOCS_TEMPLATE = """
# <!-- GH_DOCS_NAME -->
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
                inputs[item]["description"],
                f"`{inputs[item].get('required', 'true')}`",
                f"`{inputs[item].get('default', '-')}`",
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
                outputs[item]["description"],
            ]
        )
    result["outputs"] = {
        "header": ["parameter", "description"],
        "content": output_content,
    }

    try:
        result["runs"] = f"`{yaml_content['runs']['using']}`"
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
    inputs_table = tabulate(
        parsed_yaml["inputs"]["content"],
        parsed_yaml["inputs"]["header"],
        tablefmt="github",
    )
    parsed_yaml["inputs"] = f"\n{inputs_table}\n"

    outputs_table = tabulate(
        parsed_yaml["outputs"]["content"],
        parsed_yaml["outputs"]["header"],
        tablefmt="github",
    )
    parsed_yaml["outputs"] = f"\n{outputs_table}\n"

    parsed_yaml["usage"] = f"\n```yaml\n{parsed_yaml['usage']}\n```\n"

    return parsed_yaml


def replace_tag(content, tag_name, tag_value, tag_prefix="GH_DOCS"):
    # Update tags
    content = re.sub(
        rf"(<!-- BEGIN_{tag_prefix}_{tag_name.upper()} -->)(.*)(<!-- END_{tag_prefix}_{tag_name.upper()} -->)",
        rf"\1{tag_value}\3",
        content,
    )
    # Generate
    content = re.sub(
        rf"<!-- {tag_prefix}_{tag_name.upper()} -->",
        f"<!-- BEGIN_{tag_prefix}_{tag_name.upper()} -->{tag_value}<!-- END_{tag_prefix}_{tag_name.upper()} -->",
        content,
    )
    return content


def generate_docs(docs_file: str = "README.md") -> int:
    args = _build_parser().parse_args()
    print(args)
    for path in args.path:
        # Prepare
        yaml_path = pathlib.Path(path)
        parsed_yaml = parse_yaml(yaml_path)
        action_path = (
            f"/{yaml_path.parent}" if parsed_yaml["runs"] == "composit" else ""
        )
        parsed_yaml["usage"] = generate_usage(
            parsed_yaml["inputs"]["content"], action_path
        )

        docs_items = update_style(parsed_yaml)
        print(docs_items)

        # Generate
        docs_path = yaml_path.parent.joinpath(docs_file)
        if not docs_path.is_file() or args.output_mode == "replace":
            with open(docs_path, "w") as f:
                f.write(DOCS_TEMPLATE)

        with open(docs_path, "r") as f:
            content = f.read()

        for item in docs_items.keys():
            content = replace_tag(content, item, docs_items[item])

        print(content)

    return 1


def inject_docs() -> None:
    pass


def replace_docs() -> None:
    pass


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
        nargs=1,
        type=str,
        help="Path of a github reusable workflow or composite action file.",
    )
    return parser


def main():
    # try:
    # sys.exit(generate_docs())
    # except Exception as e:
    # sys.stderr.write("github-actions-docs: " + str(e) + "\n")
    # sys.exit(1)
    generate_docs()
    sys.exit(1)


if __name__ == "__main__":
    # <!-- BEGIN_GH_DOCS -->
    main()
