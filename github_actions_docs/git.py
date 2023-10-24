import subprocess

from github_actions_docs.errors import GithubActionsDocsError


class Git:
    """Basic git commands"""

    def __init__(self):
        self._run_command("git")

    def _run_command(self, command: str = "git status") -> str | None:
        try:
            return (
                subprocess.check_output(command.split(), stderr=subprocess.DEVNULL)
                .decode("ascii")
                .strip("'\" \n")
            )
        except FileNotFoundError:
            raise GithubActionsDocsError(f"{command} is not an executable.")
        except subprocess.CalledProcessError:
            return None
        raise GithubActionsDocsError(f"Unkown git issue running: {command}")

    @property
    def latest_tag(self) -> str | None:
        result = self._run_command(
            "git for-each-ref --sort=-version:refname --format '%(refname)' refs/tags --count=1"
        )
        try:
            return result.split("/")[2]
        except (IndexError, AttributeError):
            return None
        raise GithubActionsDocsError("unkown git issue getting latest git tag")

    @property
    def remote_url(self) -> str | None:
        result = self._run_command("git ls-remote --get-url origin")
        try:
            return "/".join(result.replace(":", "/").split("/")[-2:]).rstrip(".git")
        except (IndexError, AttributeError):
            return None
        raise GithubActionsDocsError("unkown git issue getting git remote url")

    @property
    def current_branch(self) -> str | None:
        return self._run_command("git rev-parse --abbrev-ref HEAD")

    @property
    def revision_short_hash(self) -> str:
        return self._run_command("git rev-parse --short HEAD")
