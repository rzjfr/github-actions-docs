import re

from github_actions_docs.git import Git


class UpdateDocsStyle:
    def __init__(
        self, parsed_yaml: dict, yaml_path: str, uses_ref_override: str = ""
    ) -> None:
        self.action_path = f"/{yaml_path.parent}"
        self.action_filename = (
            f"/{yaml_path.name}" if parsed_yaml["runs"] == "reusable workflow" else ""
        )
        self.action_name = parsed_yaml["name"]
        self.action_type = parsed_yaml["runs"]
        self.inputs = parsed_yaml["inputs"]["content"]
        self.docs = parsed_yaml
        self._update_docs_usage(uses_ref_override)
        self._update_docs_style()

    def _update_docs_usage(self, uses_ref_override: str = "") -> str:
        """Generates usage section
        By default it tries to constuct the reference in following format:
        `{owner}/{repo}/.github/workflows/{filename}@{ref}`
        based on the git repository setting of the current folder. Otherwise
        it would be in `./.github/<actions|workflows>/{filename}` format.
        [(docs)](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions#jobsjob_iduses)

        Args:
            inputs: github actions inputs.
            uses_ref_override: overrides the ref section of `uses` section of if set.
            action_path: path of the github actions.
            action_filename: filename of the github actions.

        Returns:
            yaml in form of string can be used directly in the output file.
        """
        git = Git()
        if remote_url := git.remote_url:
            ref = uses_ref_override or git.latest_tag or git.current_branch
            uses_result = f"{remote_url}{self.action_path}{self.action_filename}@{ref}"
        else:
            uses_result = f"./.github/{self.action_path}{self.action_filename}"
        result = ""
        if self.action_type == "reusable workflow":
            result += "jobs:\n"
            result += "  call-workflow:\n"
            indentation = 4
        else:
            result += f"- name: {self.action_name}\n"
            indentation = 2
        result += f"{' '*indentation}uses: {uses_result}\n"
        if self.inputs:
            result += f"{' '*indentation}with:\n"
            for item in self.inputs:
                result += f"{' '*(indentation+2)}{item[0]}: {item[-1]}\n"
        self.docs["usage"] = result

    def _update_table_style(self, key: str) -> None:
        """Replaces section designated by `key` to be markdown tables."""
        if self.docs.get(key) and self.docs[key]["content"]:
            table = create_table(
                self.docs[key]["header"],
                self.docs[key]["content"],
            )
            self.docs[key] = f"\n\n{table}\n"
        else:
            self.docs[key] = f"\n\nThis item does not have any {key}.\n\n"

    def _update_docs_style(self) -> None:
        """Replaces raw values with the processes ones."""
        for item in ["inputs", "outputs", "secrets"]:
            self._update_table_style(item)
        self.docs["runs"] = f"`{self.docs['runs']}`"
        self.docs["description"] = f"\n\n{self.docs['description'].strip()}\n\n"
        self.docs["usage"] = f"\n\n```yaml\n{self.docs['usage']}```\n\n"
        if default := self.docs.get("default"):
            self.docs["default"] = default.lower
        if table_item := self.docs.get("contents_table_item"):
            sanitized = re.sub(r"[^a-z\d\s]", "", table_item.lower()).replace(" ", "-")
            self.docs["contents_table_item"] = f"- [{table_item}](#{sanitized})\n"


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
