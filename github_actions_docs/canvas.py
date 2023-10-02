import re

from github_actions_docs.git import get_current_branch, get_latest_tag, get_remote_url


def generate_usage(
    inputs: list,
    action_type: str,
    uses_ref_override: str = "",
    action_path: str = "",
    action_filename: str = "",
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
        uses_result = f"{remote_url}{action_path}{action_filename}@{ref}"
    else:
        uses_result = f"./.github/{action_path}{action_filename}"

    result = ""
    if action_type == "reusable workflow":
        result += "jobs:\n"
        result += "  call-workflow:\n"
        indentation = 4
    else:
        result += "- name: Example Usage\n"
        indentation = 2
    result += f"{' '*indentation}uses: {uses_result}\n"
    if inputs:
        result += f"{' '*indentation}with:\n"
        for item in inputs:
            result += f"{' '*(indentation+2)}{item[0]}: {item[-1]}\n"

    return result


def update_table_style(parsed_yaml: dict, key: str) -> dict:
    if parsed_yaml.get(key) and parsed_yaml[key]["content"]:
        table = create_table(
            parsed_yaml[key]["header"],
            parsed_yaml[key]["content"],
        )
        parsed_yaml[key] = f"\n\n{table}\n"
    else:
        parsed_yaml[key] = f"\n\nThis item does not have any {key}.\n\n"
    return parsed_yaml


def update_style(parsed_yaml: dict) -> dict:
    for item in ["inputs", "outputs", "secrets"]:
        parsed_yaml = update_table_style(parsed_yaml, item)

    parsed_yaml["runs"] = f"`{parsed_yaml['runs']}`"

    parsed_yaml["description"] = f"\n\n{parsed_yaml['description'].strip()}\n\n"

    parsed_yaml["usage"] = f"\n\n```yaml\n{parsed_yaml['usage']}```\n\n"
    if parsed_yaml.get("default"):
        parsed_yaml["default"] = parsed_yaml["default"].lower
        if parsed_yaml.get("type"):
            parsed_yaml["default"] = parsed_yaml["default"].strip("'\"")

    if table_item := parsed_yaml.get("contents_table_item"):
        sanitized = re.sub(r"[^a-z\d\s]", "", table_item.lower()).replace(" ", "-")
        parsed_yaml["contents_table_item"] = f"- [{table_item}](#{sanitized})\n"

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
