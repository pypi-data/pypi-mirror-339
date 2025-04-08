import os
from pathlib import Path


def current() -> Path:
    return Path.cwd()


def define(workdir: str | None = None) -> Path:
    if not workdir:
        return current()
    elif workdir.startswith("/"):
        return Path(workdir)
    else:
        return current() / workdir
