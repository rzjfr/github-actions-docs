import yaml

from github_actions_docs.errors import (
    GithubActionsDocsError,
    GithubActionsDocsSchemaError,
)


def parse_yaml(yaml_path: str) -> dict:
    """validates and parses action file to extract the relevant information"""
    if not yaml_path.is_file():
        raise GithubActionsDocsError(f"file {yaml_path} does not exist")
    if not (yaml_path.suffix == ".yaml" or yaml_path.suffix == ".yml"):
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
