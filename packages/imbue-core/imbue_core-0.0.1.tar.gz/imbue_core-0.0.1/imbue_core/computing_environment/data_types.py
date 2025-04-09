from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Union

import anyio

# Use AnyPath type to match Sanctum
AnyPath = Union[Path, str, anyio.Path]


class RunCommandError(subprocess.CalledProcessError):
    """Custom exception for errors encountered during Git commands."""

    def __str__(self) -> str:
        return f"Command `{self.cmd}` returned non-zero exit status {self.returncode}.\nOutput: {self.stdout}\nError: {self.stderr}"


class PatchApplicationError(Exception):
    """Custom exception for errors encountered during patch application."""


class FailedToMakeCommitError(Exception):
    """Custom exception for errors encountered during commit creation."""
