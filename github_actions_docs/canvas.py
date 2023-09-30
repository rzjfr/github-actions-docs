import re

from github_actions_docs.git import get_current_branch, get_latest_tag, get_remote_url


def generate_usage(
    inputs: list,
    uses_ref_override: str = "",
    action_path: str = "",
    action_filename: str = "action.yaml",
) -> str:
    """Generates usage section
    By default it tries to constuct the reference in following format:
    `{owner}/{repo}/.github/workflows/{filename}@{ref}`
    based on the git repository setting of the current folder. Otherwise
    it would be in `./.github/<actions|workflows>/{filename}` format.
    [(docs)](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions#jobsjob_iduses)

    Params:
        inputs: github actions inputs.
        uses_ref_override: overrides the ref section of `uses` section of if set.
        action_path: path of the github actions.
        action_filename: filename of the github actions.

    Returns:
        yaml in form of string can be used directly in the output file.
    """
    if remote_url := get_remote_url():
        ref = uses_ref_override or get_latest_tag() or get_current_branch()
        uses_result = f"{remote_url}{action_path}@{ref}"
    else:
        uses_result = f"./.github/{action_path}/{action_filename}"

    result = "- name: Example Usage\n"
    result += f"  uses: {uses_result}\n"
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
