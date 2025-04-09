from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import sh

from .status import get_status


class Repo:
    def __init__(
        self, path: Path | str,
        *,
        user_name: str,
        user_email: str,
    ) -> None:
        self.__path: Path = Path(path).expanduser()

        self.__git = sh.bake(
            _cwd=self.__path,
            _env={
                "GIT_AUTHOR_NAME": user_name,
                "GIT_AUTHOR_EMAIL": user_email,
                "GIT_COMMITTER_NAME": user_name,
                "GIT_COMMITTER_EMAIL": user_email,
            } | os.environ,
        ).git

        if not (self.__path / ".git").is_dir():
            msg = "Specified path must be part of a Git repo."
            raise ValueError(msg)

    @staticmethod
    def init(
        path: Path | str,
        *,
        exist_ok: bool = True,
        **kwargs: Any,
    ) -> Repo:
        repo_path: Path = Path(path).expanduser()

        repo_path.mkdir(parents=True, exist_ok=True)

        if (repo_path / ".git").exists():
            if not exist_ok:
                msg = "Specified path is already a Git repo."
                raise RuntimeError(msg)
        else:
            sh.git(
                "init",
                _cwd=repo_path,
            )

        return Repo(repo_path, **kwargs)

    def is_clean(self) -> bool:
        status: dict[str, Any] | None = get_status(str(self.__path))
        if not status:
            msg = "Cannot get status of Git repo."
            raise RuntimeError(msg)

        return not (status["files"]["staged"] or status["files"]["unstaged"])

    def stage(self, *files: str) -> None:
        args: list[str] = ["--", *files] if files else ["."]

        self.__git(
            "add", *args,
        )

    def reset(self) -> None:
        self.__git(
            "reset",
        )

    def commit(self, message: str, *, stage_all: bool = True, background: bool = False) -> None:
        args: list[str] = ["--all"] if stage_all else []

        self.__git(
            "commit", *args, f"--message={message}",
            _bg=background,
        )

    def pull(self, *, rebase: bool = True, background: bool = False) -> None:
        if not self.is_clean():
            msg = "Repo is not clean."
            raise RuntimeError(msg)

        args: list[str] = ["--rebase=true"] if rebase else []

        self.__git(
            "pull", *args,
            _bg=background,
        )

    def push(self, *, background: bool = False) -> None:
        if not self.is_clean():
            msg = "Repo is not clean."
            raise RuntimeError(msg)

        self.__git(
            "push",
            _bg=background,
        )
