import subprocess

from github_actions_docs.errors import GithubActionsDocsError


def run_git_command(command: str = "git status") -> str | None:
    try:
        return (
            subprocess.check_output(command.split(), stderr=subprocess.DEVNULL)
            .decode("ascii")
            .strip("'\" \n")
        )
    except subprocess.CalledProcessError:
        return None
    raise GithubActionsDocsError(f"Unkown git issue running: {command}")


def get_latest_tag() -> str | None:
    result = run_git_command(
        "git for-each-ref --sort=-creatordate --format '%(refname)' refs/tags --count=1"
    )
    try:
        return result.split("/")[2]
    except (IndexError, AttributeError):
        return None
    raise GithubActionsDocsError("unkown git issue getting latest git tag")


def get_remote_url() -> str | None:
    result = run_git_command("git ls-remote --get-url origin")
    try:
        return result.split(":")[1].rstrip(".git")
    except (IndexError, AttributeError):
        return None
    raise GithubActionsDocsError("unkown git issue getting git remote url")


def get_current_branch() -> str | None:
    return run_git_command("git rev-parse --abbrev-ref HEAD")


def get_git_revision_short_hash() -> str:
    return run_git_command("git rev-parse --short HEAD")
