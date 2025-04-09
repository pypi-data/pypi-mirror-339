from typing import Any

from colors import color

from .status import get_status


def __get_branch_prompt(
    branch: str | None,
    *,
    has_remote: bool,
    ahead: int,
    behind: int,
) -> str:
    if branch is None:
        return color("(detached)", fg="red")

    prompt: str = color(branch, fg=(
        "green" if has_remote else "cyan"
    ))

    if has_remote:
        remote_flags: str = ""

        if ahead > 0:
            remote_flags += color('↑', fg="blue", style="bold")
        if behind > 0:
            remote_flags += color('↓', fg="yellow", style="bold")

        if remote_flags:
            prompt += remote_flags

    return prompt


def __get_local_flags(
    *,
    staged: bool,
    unstaged: bool,
    untracked: bool,
) -> str:
    local_flags: str = ""

    if staged:
        local_flags += color('+', fg="green", style="bold")
    if unstaged:
        local_flags += color('*', fg="red", style="bold")
    if untracked:
        local_flags += color('?', fg="cyan", style="bold")

    if local_flags:
        return ':' + local_flags

    return ""


def get_prompt() -> str:
    status: dict[str, Any] | None = get_status()
    if status is None:
        return ""

    branch: str | None = status["branch"]["head"]
    has_remote: bool = status["branch"]["upstream"] is not None
    ahead: int = status["commits"]["ahead"]
    behind: int = status["commits"]["behind"]
    staged = bool(status["files"]["staged"])
    unstaged = bool(status["files"]["unstaged"])
    untracked = bool(status["files"]["untracked"])

    return __get_branch_prompt(
        branch,
        has_remote=has_remote,
        ahead=ahead,
        behind=behind,
    ) + __get_local_flags(
        staged=staged,
        unstaged=unstaged,
        untracked=untracked,
    )


def print_prompt() -> None:
    print(get_prompt(), end="")
