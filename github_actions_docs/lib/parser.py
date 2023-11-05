import pathlib

from github_actions_docs.config import (
    GH_DOCS_WORKFLOWS_TABLE_OF_CONTENT_TITLE,
    GH_DOCS_WORKFLOWS_TITLE,
    GHA_ACTION_REQUIRED_FIELDS,
    GHA_WORKFLOW_REQUIRED_FIELDS,
)
from github_actions_docs.errors import (
    GithubActionsDocsError,
    GithubActionsDocsSchemaError,
)
from ruamel.yaml import YAML


class GithubActions:
    def __init__(self, yaml_path: str) -> None:
        self.yaml_path = pathlib.Path(yaml_path)
        # validate file
        if not self.yaml_path.is_file():
            raise GithubActionsDocsError(f"file {yaml_path} does not exist")
        if self.yaml_path.suffix not in [".yaml", ".yml"]:
            raise GithubActionsDocsError(f"{self.yaml_path.suffix} not accepted.")
        # load content
        with open(yaml_path, "r") as f:
            yaml = YAML(pure=True)
            self.yaml_content = yaml.load(f)
        # validate content
        if not self.yaml_content:
            raise GithubActionsDocsError("file doesn't seem to be a valid yaml file.")
        # find action type
        self.action_type = self._find_action_type()

    def parse(self) -> dict:
        """validates and parses action file to extract the relevant information"""

        result = {}
        result["name"] = self.yaml_content["name"]
        result["description"] = self.yaml_content.get(
            "description", f"[{self.yaml_path}]({self.yaml_path.name})"
        )
        if self.action_type == "action":
            result.update(self._parse_action())
        else:
            result.update(self._parse_workflow())
            result["title"] = GH_DOCS_WORKFLOWS_TITLE
            result["contents_table_item"] = result["name"]
            result["contents_table_title"] = GH_DOCS_WORKFLOWS_TABLE_OF_CONTENT_TITLE
        return result

    def _find_action_type(self) -> str:
        yaml_content_keys = set(self.yaml_content.keys())
        if "on" in yaml_content_keys and (
            "workflow_call" in self.yaml_content["on"].keys()
        ):
            action_type = "workflow"
            if not GHA_WORKFLOW_REQUIRED_FIELDS <= yaml_content_keys:
                raise GithubActionsDocsSchemaError(
                    list(GHA_WORKFLOW_REQUIRED_FIELDS), "top level"
                )
        else:
            action_type = "action"
            if not GHA_ACTION_REQUIRED_FIELDS <= yaml_content_keys:
                raise GithubActionsDocsSchemaError(
                    list(GHA_ACTION_REQUIRED_FIELDS), "top level"
                )
        return action_type

    def _parse_action(self) -> dict:
        result = {}
        inputs, inputs_content = self.yaml_content.get("inputs", {}), []
        for item, value in inputs.items():
            if "description" not in value.keys():
                raise GithubActionsDocsSchemaError(["description"], f".inputs.{item}")
            comment = ""
            if all_comments := value.ca.items.get("description"):
                comment = " ".join([i.value for i in all_comments if i])
            inputs_content.append(
                [
                    item,
                    f"{value['description']}{comment}".replace("\n", "").strip(),
                    f"{value.get('required', True)}".lower(),
                    f"\"{value.get('default', '')}\"".lower(),
                ]
            )
        result["inputs"] = {
            "header": ["parameter", "description", "required", "default"],
            "content": inputs_content,
        }

        outputs, output_content = self.yaml_content.get("outputs", {}), []
        for item, value in outputs.items():
            if "description" not in value.keys():
                raise GithubActionsDocsSchemaError(["description"], f".outputs.{item}")
            output_content.append(
                [
                    item,
                    value["description"].replace("\n", ""),
                ]
            )
        result["outputs"] = {
            "header": ["parameter", "description"],
            "content": output_content,
        }
        try:
            result["runs"] = f"{self.yaml_content['runs']['using']}"
        except KeyError:
            raise GithubActionsDocsSchemaError(["using"], ".runs")
        return result

    def _parse_workflow(self) -> dict:
        result = {}
        result["runs"] = "reusable workflow"
        inputs, inputs_content = (
            self.yaml_content["on"]["workflow_call"].get("inputs", {}),
            [],
        )
        for item, value in inputs.items():
            description = value.get("description", "")
            if all_comments := value.ca.items.get("description"):
                description += " ".join([i.value for i in all_comments if i])
            item_type = f"{value.get('type', 'string')}"
            item_default = f"\"{value.get('default', '')}\""
            if item_type == "boolean":
                item_default = item_default.lower()
            inputs_content.append(
                [
                    item,
                    description.replace("\n", "").strip(),
                    item_type,
                    f"{value.get('required', True)}".lower(),
                    item_default,
                ]
            )
        result["inputs"] = {
            "header": ["parameter", "description", "type", "required", "default"],
            "content": inputs_content,
        }
        secrets, secrets_content = (
            self.yaml_content["on"]["workflow_call"].get("secrets", {}),
            [],
        )
        for item, value in secrets.items():
            secrets_content.append(
                [
                    item,
                    value.get("description", "").replace("\n", ""),
                    f"{value.get('required', True)}".lower(),
                ]
            )
        result["secrets"] = {
            "header": ["parameter", "description", "required"],
            "content": secrets_content,
        }
        outputs, output_content = (
            self.yaml_content["on"]["workflow_call"].get("outputs", {}),
            [],
        )
        for item, value in outputs.items():
            output_content.append(
                [
                    item,
                    value.get("description", "").replace("\n", ""),
                ]
            )
        result["outputs"] = {
            "header": ["parameter", "description"],
            "content": output_content,
        }
        return result
