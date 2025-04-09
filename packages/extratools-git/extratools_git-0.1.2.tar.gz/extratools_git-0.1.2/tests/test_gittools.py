from extratools_gittools.status import parse_status


def test_parse_status_initial() -> None:
    output = """
# branch.oid (initial)
# branch.head main
""".strip()

    assert parse_status(output) == {
        "oid": "(initial)",
        "branch": {
            "head": "main",
            "upstream": None,
        },
        "commits": {
            "ahead": 0,
            "behind": 0,
        },
        "files": {
            "staged": [],
            "unstaged": [],
            "untracked": [],
        },
    }


def test_parse_status_staged() -> None:
    output = """
# branch.oid (initial)
# branch.head main
1 A. N... 000000 100644 100644 0000000000000000000000000000000000000000 f3bbb159c01181339498739c8d0c240344abf803 LICENSE
""".strip()  # noqa: E501

    assert parse_status(output) == {
        "oid": "(initial)",
        "branch": {
            "head": "main",
            "upstream": None,
        },
        "commits": {
            "ahead": 0,
            "behind": 0,
        },
        "files": {
            "staged": [
                "LICENSE",
            ],
            "unstaged": [],
            "untracked": [],
        },
    }


def test_parse_status_unstaged() -> None:
    output = """
# branch.oid (initial)
# branch.head main
1 .M N... 000000 100644 100644 0000000000000000000000000000000000000000 f3bbb159c01181339498739c8d0c240344abf803 LICENSE
""".strip()  # noqa: E501

    assert parse_status(output) == {
        "oid": "(initial)",
        "branch": {
            "head": "main",
            "upstream": None,
        },
        "commits": {
            "ahead": 0,
            "behind": 0,
        },
        "files": {
            "staged": [],
            "unstaged": [
                "LICENSE",
            ],
            "untracked": [],
        },
    }


def test_parse_status_staged_unstaged() -> None:
    output = """
# branch.oid (initial)
# branch.head main
1 AM N... 000000 100644 100644 0000000000000000000000000000000000000000 f3bbb159c01181339498739c8d0c240344abf803 LICENSE
""".strip()  # noqa: E501

    assert parse_status(output) == {
        "oid": "(initial)",
        "branch": {
            "head": "main",
            "upstream": None,
        },
        "commits": {
            "ahead": 0,
            "behind": 0,
        },
        "files": {
            "staged": [
                "LICENSE",
            ],
            "unstaged": [
                "LICENSE",
            ],
            "untracked": [],
        },
    }


def test_parse_status_untracked() -> None:
    output = """
# branch.oid (initial)
# branch.head main
? README.md
""".strip()

    assert parse_status(output) == {
        "oid": "(initial)",
        "branch": {
            "head": "main",
            "upstream": None,
        },
        "commits": {
            "ahead": 0,
            "behind": 0,
        },
        "files": {
            "staged": [],
            "unstaged": [],
            "untracked": [
                "README.md",
            ],
        },
    }


def test_parse_status_upstream() -> None:
    output = """
# branch.oid 19d6f23b52c565b61f4532f6154ecc000d2d0524
# branch.head main
# branch.upstream origin/main
# branch.ab +0 -0
""".strip()

    assert parse_status(output) == {
        "oid": "19d6f23b52c565b61f4532f6154ecc000d2d0524",
        "branch": {
            "head": "main",
            "upstream": "origin/main",
        },
        "commits": {
            "ahead": 0,
            "behind": 0,
        },
        "files": {
            "staged": [],
            "unstaged": [],
            "untracked": [],
        },
    }


def test_parse_status_behind() -> None:
    output = """
# branch.oid 1bd851ae2c067354194ee6f5a44aa7cf954a22ec
# branch.head main
# branch.upstream origin/main
# branch.ab +0 -1
""".strip()

    assert parse_status(output) == {
        "oid": "1bd851ae2c067354194ee6f5a44aa7cf954a22ec",
        "branch": {
            "head": "main",
            "upstream": "origin/main",
        },
        "commits": {
            "ahead": 0,
            "behind": 1,
        },
        "files": {
            "staged": [],
            "unstaged": [],
            "untracked": [],
        },
    }


def test_parse_status_ahead() -> None:
    output = """
# branch.oid 198adc95d6f983eca1ccb3eb4b1c7efc735a0c93
# branch.head main
# branch.upstream origin/main
# branch.ab +1 -0
""".strip()

    assert parse_status(output) == {
        "oid": "198adc95d6f983eca1ccb3eb4b1c7efc735a0c93",
        "branch": {
            "head": "main",
            "upstream": "origin/main",
        },
        "commits": {
            "ahead": 1,
            "behind": 0,
        },
        "files": {
            "staged": [],
            "unstaged": [],
            "untracked": [],
        },
    }
