from pathlib import Path
from typing import Any

import sh


def get_status(path: str = '.') -> dict[str, Any] | None:
    try:
        output: str = sh.git(
            "status", "--short", "--branch", "--porcelain=2",
            _cwd=Path(path).expanduser(),
        )
    except Exception:
        return None

    return {
        "path": path,
        **parse_status(output),
    }


def parse_status(output: str) -> dict[str, Any]:
    oid: str | None = None

    head: str | None = None
    upstream: str | None = None

    ahead: int = 0
    behind: int = 0

    staged: list[str] = []
    unstaged: list[str] = []
    untracked: list[str] = []

    for line in output.rstrip('\n').splitlines():
        vals: list[str] = line.split(' ')

        match vals[0]:
            case '#':
                match vals[1]:
                    case "branch.oid":
                        oid = vals[2]
                    case "branch.head":
                        branch = vals[2]
                        if branch != "(detached)":
                            head = branch
                    case "branch.upstream":
                        branch = vals[2]
                        if branch != "(detached)":
                            upstream = branch
                    case "branch.ab":
                        ahead, behind = [abs(int(x)) for x in vals[2:]]
            case '?':
                untracked.append(vals[1])
            case '!':
                pass
            case _:
                path: str = vals[-1]

                stage_flags: str = vals[1]
                if stage_flags[0] != '.':
                    staged.append(path)
                if stage_flags[1] != '.':
                    unstaged.append(path)

                submodule_flags: str = vals[2]
                if submodule_flags[0] == 'S' and submodule_flags[3] == 'U':
                    untracked.append(path)

    return {
        "oid": oid,
        "branch": {
            "head": head,
            "upstream": upstream,
        },
        "commits": {
            "ahead": ahead,
            "behind": behind,
        },
        "files": {
            "staged": staged,
            "unstaged": unstaged,
            "untracked": untracked,
        },
    }
