from ruamel.yaml import YAML

from github_actions_docs.errors import (
    GithubActionsDocsError,
    GithubActionsDocsSchemaError,
)

# https://docs.github.com/en/actions/creating-actions/metadata-syntax-for-github-actions#inputsinput_iddefault
GHA_ACTION_REQUIRED_FIELDS = {"name", "description", "runs"}
# https://docs.github.com/en/actions/using-workflows/reusing-workflows
GHA_WORKFLOW_REQUIRED_FIELDS = {"name", "on", "jobs"}

GH_DOCS_WORKFLOWS_TITLE = "Reusable Workflows"
GH_DOCS_WORKFLOWS_TABLE_OF_CONTENT_TITLE = "List of workflows"


def find_gh_actions_type(yaml_path: str) -> tuple[str, dict]:
    """
    Returns:
      tuple of action type and the content of input yaml file as a dict
    """
    if not yaml_path.is_file():
        raise GithubActionsDocsError(f"file {yaml_path} does not exist")
    if yaml_path.suffix not in [".yaml", ".yml"]:
        raise GithubActionsDocsError(f"expected .yaml instead of {yaml_path.suffix}.")
    with open(yaml_path, "r") as f:
        yaml = YAML(typ="unsafe", pure=True)
        yaml_content = yaml.load(f)
    if not type(yaml_content) == dict:
        raise GithubActionsDocsError("file doesn't seem to be a valid yaml file.")

    if "on" in yaml_content.keys() and ("workflow_call" in yaml_content["on"].keys()):
        action_type = "workflow"
        if not GHA_WORKFLOW_REQUIRED_FIELDS <= set(yaml_content.keys()):
            raise GithubActionsDocsSchemaError(
                list(GHA_WORKFLOW_REQUIRED_FIELDS), "top level"
            )
    else:
        action_type = "action"
        if not GHA_ACTION_REQUIRED_FIELDS <= set(yaml_content.keys()):
            raise GithubActionsDocsSchemaError(
                list(GHA_ACTION_REQUIRED_FIELDS), "top level"
            )
    return (action_type, yaml_content)


def construct_gha_action_content(yaml_content: dict) -> dict:
    result = {}
    inputs, inputs_content = yaml_content.get("inputs", {}), []
    for item in inputs.keys():
        if "description" not in inputs[item].keys():
            raise GithubActionsDocsSchemaError(["description"], f".inputs.{item}")
        inputs_content.append(
            [
                item,
                inputs[item]["description"].replace("\n", ""),
                f"{inputs[item].get('required', True)}".lower(),
                f"\"{inputs[item].get('default', '')}\"".lower(),
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


def construct_gha_workflow_content(yaml_content: dict) -> dict:
    result = {}
    result["runs"] = "reusable workflow"
    inputs, inputs_content = yaml_content["on"]["workflow_call"].get("inputs", {}), []
    for item in inputs.keys():
        item_type = f"{inputs[item].get('type', 'string')}"
        if item_type == "boolean":
            item_default = f"{inputs[item].get('default', '')}".lower()
        else:
            item_default = f"\"{inputs[item].get('default', '')}\""
        inputs_content.append(
            [
                item,
                inputs[item].get("description", "").replace("\n", ""),
                item_type,
                f"{inputs[item].get('required', True)}".lower(),
                item_default,
            ]
        )
    result["inputs"] = {
        "header": ["parameter", "description", "type", "required", "default"],
        "content": inputs_content,
    }
    secrets, secrets_content = (
        yaml_content["on"]["workflow_call"].get("secrets", {}),
        [],
    )
    for item in secrets.keys():
        secrets_content.append(
            [
                item,
                secrets[item].get("description", "").replace("\n", ""),
                f"{secrets[item].get('required', True)}",
            ]
        )
    result["secrets"] = {
        "header": ["parameter", "description", "required"],
        "content": secrets_content,
    }
    outputs, output_content = yaml_content["on"]["workflow_call"].get("outputs", {}), []
    for item in outputs.keys():
        output_content.append(
            [
                item,
                outputs[item].get("description", "").replace("\n", ""),
            ]
        )
    result["outputs"] = {
        "header": ["parameter", "description"],
        "content": output_content,
    }
    return result


def parse_yaml(yaml_path: str) -> dict:
    """validates and parses action file to extract the relevant information"""

    action_type, yaml_content = find_gh_actions_type(yaml_path)
    result = {}
    result["name"] = yaml_content["name"]
    result["description"] = yaml_content.get(
        "description", f"[{yaml_path}]({yaml_path.name})"
    )

    if action_type == "action":
        result.update(construct_gha_action_content(yaml_content))
    else:
        result["title"] = GH_DOCS_WORKFLOWS_TITLE
        result["contents_table_item"] = result["name"]
        result["contents_table_title"] = GH_DOCS_WORKFLOWS_TABLE_OF_CONTENT_TITLE
        result.update(construct_gha_workflow_content(yaml_content))
    return result
