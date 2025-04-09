"""Utility abstractions for interacting with git repositories."""
from __future__ import annotations

import asyncio
import contextlib
import functools
import hashlib
import shlex
import shutil
import subprocess
import sys
from asyncio.subprocess import PIPE
from asyncio.subprocess import STDOUT
from contextlib import asynccontextmanager
from io import StringIO
from pathlib import Path
from types import TracebackType
from typing import Any
from typing import AsyncGenerator
from typing import AsyncIterator
from typing import Dict
from typing import List
from typing import Mapping
from typing import Optional
from typing import Self
from typing import Sequence
from typing import TYPE_CHECKING
from typing import TextIO
from typing import Tuple
from typing import Type
from typing import Union

import anyio
import attr
from loguru import logger

from imbue_core.async_utils import sync
from imbue_core.async_utils import sync_contextmanager_func
from imbue_core.cattrs_serialization import serialize_to_json
from imbue_core.common import TEMP_DIR
from imbue_core.computing_environment.computing_environment import apply_patch_via_git
from imbue_core.computing_environment.computing_environment import assert_repo_is_clean
from imbue_core.computing_environment.computing_environment import get_head_hash
from imbue_core.computing_environment.computing_environment import git_add
from imbue_core.computing_environment.computing_environment import is_repo_dirty
from imbue_core.computing_environment.computing_environment import make_commit
from imbue_core.computing_environment.computing_environment import restore_all_staged_files
from imbue_core.computing_environment.computing_environment import restore_all_unstaged_changes
from imbue_core.computing_environment.data_types import AnyPath
from imbue_core.computing_environment.data_types import RunCommandError
from imbue_core.frozen_utils import empty_mapping
from imbue_core.secrets_utils import get_secret
from imbue_core.testing_utils import async_temp_dir

if TYPE_CHECKING:
    # for proper file mode typing
    from _typeshed import OpenBinaryMode
    from _typeshed import OpenBinaryModeReading
    from _typeshed import OpenBinaryModeWriting
    from _typeshed import OpenTextMode
    from _typeshed import OpenTextModeReading
    from _typeshed import OpenTextModeWriting

PYTHON_EXTENSION = ".py"


@attr.s(auto_attribs=True, frozen=True, kw_only=True)
class GitRepo:
    git_user_name: str
    git_user_email: str


@attr.s(auto_attribs=True, frozen=True, kw_only=True)
class GitRepoSnapshot(GitRepo):
    git_hash: str
    git_branch: str
    git_diff: Optional[str]

    @functools.cached_property
    def reference_hash(self) -> str:
        hash_fn = hashlib.md5()
        hash_fn.update(serialize_to_json(self).encode("UTF-8"))
        return hash_fn.hexdigest()


@attr.s(auto_attribs=True, frozen=True, kw_only=True)
class RemoteGitRepoSnapshot(GitRepoSnapshot):
    git_repo_url: str


@attr.s(auto_attribs=True, frozen=True, kw_only=True)
class LocalGitRepoSnapshot(GitRepoSnapshot):
    git_repo_path: str
    # the relative paths of any untracked files in the repo
    git_untracked_files: Optional[Tuple[str, ...]]


@attr.s(auto_attribs=True, frozen=True, kw_only=True)
class GitCommitSnapshot:
    contents_by_path: Mapping[str, str]
    commit_message: str
    # ex: "2023-05-15T14:30:00"
    # used for GIT_AUTHOR_DATE and GIT_COMMITTER_DATE
    commit_time: str


@attr.s(auto_attribs=True, frozen=True, kw_only=True)
class FullLocalGitRepo(GitRepo):
    main_history: Tuple[GitCommitSnapshot, ...]
    # the relative paths of any currently untracked files in the repo, and their content
    untracked_file_content_by_path: Mapping[str, str] = attr.ib(factory=empty_mapping)
    git_branch: str = "main"
    git_diff: Optional[str] = None


def get_git_repo_root() -> Path:
    """Gets a Path to the current git repo root, assuming that our cwd is somewhere inside the repo."""
    completed_process = subprocess.run(
        ("git", "rev-parse", "--show-toplevel"),
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
    )
    root_dir = Path(completed_process.stdout.decode().strip())
    assert root_dir.is_dir(), f"{root_dir} must be a directory"
    return root_dir


def get_git_repo_root_from_path(path: Path) -> Path:
    """Gets a Path to the git repo root for the given path."""
    if path.is_file():
        path = path.parent
    completed_process = subprocess.run(
        ["git", "-C", path, "rev-parse", "--show-toplevel"],
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
    )
    root_dir = Path(completed_process.stdout.decode().strip())
    assert root_dir.is_dir(), f"{root_dir} must be a directory"
    return root_dir


REPO_LOCKS: Dict[Path, asyncio.Lock] = {}


@attr.s(auto_attribs=True, frozen=True)
class LocalGitRepo:
    base_path: Path

    @classmethod
    def build_from_cwd(cls) -> Self:
        """Create a `LocalGitRepo` instance from the current working directory."""
        return cls(get_git_repo_root())

    async def run_git(
        self,
        command: Sequence[str],
        check: bool = True,
        cwd: Optional[AnyPath] = None,
        is_error_logged: bool = True,
        is_stripped: bool = True,
        retry_on_git_lock_error: bool = True,
    ) -> str:
        """Run a git command in the repo.

        Example:
        ```
        git_repo.run_git("status")
        ```
        """
        absolute_path = self.base_path.absolute()
        if absolute_path not in REPO_LOCKS:
            REPO_LOCKS[absolute_path] = asyncio.Lock()
        async with REPO_LOCKS[absolute_path]:
            max_retries = 50 if retry_on_git_lock_error else 1
            retry_count = 0
            retry_delay = 0.1  # seconds
            while True:
                try:
                    result = await self.run_command(
                        ["git"] + list(command), check=check, is_error_logged=is_error_logged, cwd=cwd
                    )
                    if is_stripped:
                        return result.strip()
                    return result
                except RunCommandError as e:
                    error_message = str(e)
                    if "fatal: Unable to create" in error_message and ".git/index.lock': File exists" in error_message:
                        if retry_count >= max_retries:
                            raise
                        await asyncio.sleep(retry_delay)
                        retry_count += 1
                    else:
                        raise

    sync_run_git = sync(run_git)

    async def run_command(
        self,
        command: Sequence[str],
        check: bool = True,
        secrets: Optional[List[Any]] = None,
        cwd: Optional[AnyPath] = None,
        is_error_logged: bool = True,
    ) -> str:
        """Run a command in the repo.

        Note, this can be used to run any command, not just git.
        """
        command_string = shlex.join(command)
        proc = await asyncio.create_subprocess_exec(
            *command,
            cwd=cwd or self.base_path,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        # note, need to be carefull not to strip() lines since whitespace may be important (e.g. for diffs)
        # return joined lines since mostly we only use the output for logging, and this way we arn't
        # passing around lots of lists. Also it's easy to parse by lines if needed
        stdout_bytes, stderr_bytes = await proc.communicate()
        stdout = stdout_bytes.decode("UTF-8")
        stderr = stderr_bytes.decode("UTF-8")
        if check and proc.returncode != 0:
            error_message = f"command run from cwd={self.base_path} failed with exit code {proc.returncode} and stdout:\n{stdout}\nstderr:\n{stderr}"
            if is_error_logged:
                logger.error(f"command attempted: '{command_string}' from cwd={self.base_path}")
                logger.error(f"error message: {error_message}")
            # this should not be None, but do this to satisfy type checker, int or None we throw the same error
            returncode = proc.returncode or -1
            raise RunCommandError(
                cmd=command_string,
                stderr=stderr,
                returncode=returncode,
            )
        return stdout

    @contextlib.asynccontextmanager
    async def _open_file(
        self,
        relative_path: AnyPath,
        cwd: Optional[AnyPath] = None,
        mode: Union[OpenTextMode, OpenBinaryMode] = "r",
        mkdir_if_missing: bool = True,
    ) -> AsyncGenerator[anyio.AsyncFile[Any], None]:
        logger.trace(f"opening file {relative_path} in cwd {cwd} with mode {mode}")
        if cwd is not None:
            sb_file_path = str(Path(cwd) / relative_path)
        else:
            sb_file_path = str(self.base_path / relative_path)

        if mkdir_if_missing:
            parent_dir = anyio.Path(sb_file_path).parent
            await parent_dir.mkdir(parents=True, exist_ok=True)

        f: Optional[anyio.AsyncFile[Any]] = None
        try:
            f = await anyio.Path(sb_file_path).open(mode=mode)
            yield f
        finally:
            if f is not None:
                await f.aclose()

    async def write_file(
        self,
        relative_path: AnyPath,
        content: Optional[Union[str, bytes]],
        cwd: Optional[AnyPath] = None,
        mode: Union[OpenTextModeWriting, OpenBinaryModeWriting] = "w",
        mkdir_if_missing: bool = True,
    ) -> None:
        if content is None:
            await self.delete_file(relative_path, cwd=cwd)
            return

        async with self._open_file(relative_path, cwd=cwd, mode=mode, mkdir_if_missing=mkdir_if_missing) as f:
            logger.trace(f"writing to file {relative_path} in cwd {cwd} with mode {mode}")
            await f.write(content)

    async def delete_file(self, relative_path: AnyPath, cwd: Optional[AnyPath] = None) -> None:
        logger.trace(f"deleting the file {relative_path} in cwd {cwd}")
        if cwd is not None:
            sb_file_path = str(Path(cwd) / relative_path)
        else:
            sb_file_path = str(self.base_path / relative_path)
        await anyio.Path(sb_file_path).unlink()

    async def read_file(
        self,
        relative_path: AnyPath,
        cwd: Optional[AnyPath] = None,
        mode: Union[OpenTextModeReading, OpenBinaryModeReading] = "r",
        mkdir_if_missing: bool = True,
    ) -> Union[str, bytes]:
        async with self._open_file(relative_path, cwd=cwd, mode=mode, mkdir_if_missing=mkdir_if_missing) as f:
            logger.trace(f"reading file {relative_path} in cwd {cwd} with mode {mode}")
            content = await f.read()
            assert isinstance(content, str) or isinstance(content, bytes)
            return content

    async def head_hash(self) -> str:
        """Get the hash of the current HEAD commit."""
        return await get_head_hash(self)

    async def is_git_repo(self) -> bool:
        """Check that repo is valid git repo."""
        return await anyio.Path(self.base_path / ".git").exists()

    sync_is_git_repo = sync(is_git_repo)

    async def assert_clean(self) -> None:
        await assert_repo_is_clean(self)

    sync_assert_clean = sync(assert_clean)

    async def configure_git(
        self,
        git_user_name: Optional[str] = None,
        git_user_email: Optional[str] = None,
        initial_commit_message: str = "initial commit",
        is_recreating: bool = False,
    ) -> None:
        """Configure git repo with user name and email."""
        if is_recreating:
            if await self.is_git_repo():
                await asyncio.to_thread(shutil.rmtree, self.base_path / ".git")

        # order here is important
        # ref https://stackoverflow.com/questions/11656761/git-please-tell-me-who-you-are-error?noredirect=1
        await self.run_git(("init",))
        if git_user_name:
            await self.run_git(("config", "user.name", f"'{git_user_name}'"))
        if git_user_email:
            await self.run_git(("config", "user.email", f"'{git_user_email}'"))
        await self.run_git(("add", "."))
        await self.run_git(("commit", "-m", f"'{initial_commit_message}'"))
        branch_name = await self.run_git(("symbolic-ref", "HEAD"))
        if not branch_name == "refs/heads/main":
            # rename master to main for consistency
            await self.run_git(("branch", "-m", "master", "main"))

    sync_configure_git = sync(configure_git)

    @asynccontextmanager
    async def temporary_commit(
        self, tag_prefix: str, commit_message: str, raise_on_head_hash_change: bool = False
    ) -> AsyncIterator[str]:
        """Context manager to make a temporary commit and tag in the repo."""
        await self.run_git(("commit", "-am", commit_message, "--allow-empty"))
        head_hash = await self.head_hash()
        tag = f"{tag_prefix}/{head_hash}"
        await self.run_git(("tag", tag))
        await self.run_git(("push", "origin", tag))
        try:
            yield head_hash
        finally:
            # This is susceptible to a race condition (if the user makes a commit between the time we check the head hash and the time we reset the state).
            # So it's important to keep any block that uses this context manager short - make the commit, copy it to the controller, and work there. Don't hold the repo hostage.
            current_head_hash = await self.head_hash()
            if current_head_hash != head_hash and raise_on_head_hash_change:
                raise AssertionError(
                    f"Head hash has changed from {head_hash} to {current_head_hash} since the temporary commit was made. Giving up on resetting git state, please address this manually."
                )
            else:
                await self.run_git(("reset", "HEAD~"))

    sync_temporary_commit = sync_contextmanager_func(temporary_commit)

    async def copy_repo(self, new_repo_path: Path, exists_ok: bool = True) -> "LocalGitRepo":
        """Make a full copy of this repo in a new directory.

        Note, this will copy all the files in the repo into a new local directory, but will not handle
        configuring the new directory as a git repo.
        """
        if await anyio.Path(new_repo_path).exists():
            if not exists_ok:
                raise FileExistsError(
                    f"New repo path '{new_repo_path} already exists. Set `exists_ok=True` if you are happy overwriting it, otherwise select new path."
                )
            await asyncio.to_thread(shutil.rmtree, new_repo_path)
        await asyncio.to_thread(
            shutil.copytree,
            self.base_path,
            new_repo_path,
            dirs_exist_ok=True,
            ignore=shutil.ignore_patterns(".git", ".gitsecret"),
        )
        return LocalGitRepo(new_repo_path)

    sync_copy_repo = sync(copy_repo)

    async def get_snapshot_info(self) -> GitRepoSnapshot:
        """Get general snapshot of the current state of the git repo."""
        async with asyncio.TaskGroup() as tg:
            git_branch_task = tg.create_task(self.run_git(("rev-parse", "--abbrev-ref", "HEAD")))
            git_hash_task = tg.create_task(self.run_git(("rev-parse", "HEAD")))
            git_unstaged_diff_task = tg.create_task(self.run_git(("diff",), is_stripped=False))
            git_staged_diff_task = tg.create_task(self.run_git(("diff", "--staged"), is_stripped=False))
            git_user_name_task = tg.create_task(self.run_git(("config", "user.name")))
            git_user_email_task = tg.create_task(self.run_git(("config", "user.email")))
            await asyncio.gather(
                *[
                    git_branch_task,
                    git_hash_task,
                    git_unstaged_diff_task,
                    git_staged_diff_task,
                    git_user_name_task,
                    git_user_email_task,
                ]
            )
            git_branch = git_branch_task.result()
            current_git_hash = git_hash_task.result()
            # get the current diff (changes the user has made)
            git_staged_diff = git_staged_diff_task.result()
            git_diff = git_staged_diff
            git_unstaged_diff = git_unstaged_diff_task.result()
            if git_unstaged_diff.strip() != "":
                git_diff += git_unstaged_diff

            git_user_email = git_user_email_task.result()
            git_user_name = git_user_name_task.result()

            return GitRepoSnapshot(
                git_hash=current_git_hash,
                git_diff=git_diff,
                git_branch=git_branch,
                git_user_name=git_user_name,
                git_user_email=git_user_email,
            )

    async def get_remote_snapshot(self) -> RemoteGitRepoSnapshot:
        """Get a snapshot of the current state of the git repo on remote."""
        # run a bunch of commands in parallel to generate the necessary information
        async with asyncio.TaskGroup() as tg:
            general_snapshot_task = tg.create_task(self.get_snapshot_info())
            repo_url_task = tg.create_task(self.run_git(("config", "--get", "remote.origin.url")))
            # we have to push so that this commit can be fetched later in the process
            git_push_task = tg.create_task(self.run_git(("push", "origin", "HEAD")))
            await asyncio.gather(
                *[
                    general_snapshot_task,
                    repo_url_task,
                    git_push_task,
                ]
            )
            # figure out the remote url
            repo_url = repo_url_task.result()
            # convert to https if necessary
            if repo_url and repo_url.startswith("git@"):
                https_repo_url = repo_url.replace(":", "/").replace("git@", "https://")
            else:
                https_repo_url = repo_url
            general_snapshot = general_snapshot_task.result()
            return RemoteGitRepoSnapshot(
                git_repo_url=https_repo_url,
                git_hash=general_snapshot.git_hash,
                git_diff=general_snapshot.git_diff,
                git_branch=general_snapshot.git_branch,
                git_user_email=general_snapshot.git_user_email,
                git_user_name=general_snapshot.git_user_name,
            )

    async def get_local_snapshot(self) -> LocalGitRepoSnapshot:
        """Get a snapshot of the current state of the git repo locally."""
        # run a bunch of commands in parallel to generate the necessary information
        async with asyncio.TaskGroup() as tg:
            general_snapshot_task = tg.create_task(self.get_snapshot_info())
            git_untracked_files_task = tg.create_task(self.run_git(("ls-files", "--others", "--exclude-standard")))
            await asyncio.gather(
                *[
                    general_snapshot_task,
                    git_untracked_files_task,
                ]
            )
            # relative path to any untracked files in repo (that are not in excluded files, etc)
            untracked_files_result = git_untracked_files_task.result()
            if untracked_files_result not in (None, ""):
                untracked_files = tuple(untracked_files_result.splitlines())
            else:
                untracked_files = None

            general_snapshot = general_snapshot_task.result()
            return LocalGitRepoSnapshot(
                git_repo_path=str(self.base_path),
                git_hash=general_snapshot.git_hash,
                git_diff=general_snapshot.git_diff,
                git_branch=general_snapshot.git_branch,
                git_untracked_files=untracked_files,
                git_user_email=general_snapshot.git_user_email,
                git_user_name=general_snapshot.git_user_name,
            )

    async def is_path_in_repo(self, file_path: Union[str, Path, anyio.Path]) -> bool:
        """Check whether a given file path is within this repo.

        FIXME: It doesn't seem entirely necessary to enumerate all of the files with a particular extension
               just to check if a single file (whose path we know) is in the repo.
        """
        if isinstance(file_path, (str, Path)):
            file_path = anyio.Path(file_path)
        extension = file_path.suffix
        return file_path in await self.get_all_files_by_extension(extension=extension)

    async def _get_file_path(self, file_path: Union[str, Path]) -> anyio.Path:
        path = anyio.Path(file_path)
        if not path.is_absolute():
            path = anyio.Path(self.base_path / path)
        assert await path.exists(), f"File {path} does not exist."
        return path

    async def safely_read_file_from_repo(self, file_path: Union[str, Path]) -> str:
        """Safely read file from repo."""
        path = await self._get_file_path(file_path)
        assert await self.is_path_in_repo(path), f"File {path} is not in repo."
        return await path.read_text()

    sync_safely_read_file_from_repo = sync(safely_read_file_from_repo)

    async def get_all_files_by_extension(self, extension: str = PYTHON_EXTENSION) -> Tuple[Path, ...]:
        """Get absolute path of all files in the repo with given extension."""
        paths: List[Path] = []
        async for path in anyio.Path(self.base_path).rglob(f"*{extension}"):
            paths.append(Path(path))
        return tuple(paths)


@attr.s(auto_attribs=True, frozen=True, kw_only=True)
class WritableLocalGitRepo(LocalGitRepo):
    """A Local Git Repo with support for modifying files and reseting to an initial state.

    Note, this does not handle creating a copy of an existing repo, or anything. Rather it adds some additional
    functionality for actually writing to files in the repo. For the creation of a separate copy of an existing
    repo which supports making changes without affecting the main repo see the `temp_writable_local_git_repo` context
    manager.

    It is also recommended the `build_from_repo` function when creating a WritableLocalGitRepo, as this will
    make sure that any untracked and uncommited changes are managed correctly.
    """

    initial_git_hash: str
    stash_git_hash: Optional[str]

    @classmethod
    async def build_from_repo(cls, repo: LocalGitRepo) -> "WritableLocalGitRepo":
        """Create a writable repo from an local repo."""
        init_hash = await repo.head_hash()
        if await is_repo_dirty(repo):
            await repo.run_git(("add", "."))
            stash_hash = await make_commit(repo, "stashing uncommited and untracked changes")
        else:
            stash_hash = None

        return cls(base_path=repo.base_path, initial_git_hash=init_hash, stash_git_hash=stash_hash)

    async def _setup(self) -> None:
        init_hash = await self.head_hash()
        expected_hash = self.stash_git_hash or self.initial_git_hash
        assert init_hash == expected_hash, "git repo is not currently at expected commit"
        assert await self.is_git_repo(), f"{self.base_path} is not a git repo"
        await self.assert_clean()

    async def reset(self) -> None:
        """Reset the repo to the state it was in when this class was created."""
        await restore_all_staged_files(self)
        await restore_all_unstaged_changes(self)
        if self.stash_git_hash:
            # hard to reset to commit with stashed untracked and uncommited changes
            await self.run_git(("reset", "--hard", self.stash_git_hash))
            # soft reset to return to initial commit but keep the untracked and uncommited changes
            await self.run_git(("reset", "--soft", self.initial_git_hash))
            # unstage untracked and uncommited changes
            await restore_all_staged_files(self)
        else:
            await self.run_git(("reset", "--hard", self.initial_git_hash))
            await self.run_git(("clean", "-f"))
            await self.run_git(("checkout", self.initial_git_hash))

        current_git_hash = await self.head_hash()
        assert (
            current_git_hash == self.initial_git_hash
        ), f"base branch changed, current git hash ({current_git_hash}) != initial git hash ({self.initial_git_hash})"
        await self.assert_clean()

    async def apply_change_to_file(self, file_path: Union[str, Path], new_contents: str) -> None:
        """Apply change to a single file."""
        path = await self._get_file_path(file_path)
        assert await self.is_path_in_repo(path), f"File {path} is not in repo."
        await path.write_text(new_contents)
        await git_add(self, str(path))

    async def __aenter__(self) -> "WritableLocalGitRepo":
        await self._setup()
        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        await self.reset()


async def checkout_repo(
    repo_snapshot: Union[LocalGitRepoSnapshot, RemoteGitRepoSnapshot],
    destination_path: Path,
) -> LocalGitRepo:
    """Checks out an existing repo into a directory in the fastest way possible.

    Uses a snapshot of the existing repo to checkout a specific commit and branch, and apply any uncommited changes.
    Will checkout from a remote or local repo depending on the type of snapshot.

    Note, checking out from a remote repo requires that the necessary git permissions, etc are configured.

    See here: https://stackoverflow.com/questions/31278902/how-to-shallow-clone-a-specific-commit-with-depth-1
    """
    anyio_path = anyio.Path(destination_path)
    assert (
        await anyio_path.is_dir()
    ), f"Destination for repo checkout must be a directory. {destination_path} is not a directory."
    if not await anyio_path.exists():
        destination_path.mkdir(parents=True)
    async for _ in anyio_path.iterdir():
        raise Exception(f"Destination for repo checkout must be an empty directory. {destination_path} is not empty.")

    remote_address: Optional[str] = None
    if isinstance(repo_snapshot, RemoteGitRepoSnapshot):
        token = get_secret("GIT_TOKEN")
        assert token is not None, "Must set GIT_TOKEN environment variable to clone git repos"
        env = {"GIT_TOKEN": token}

        repo_url = repo_snapshot.git_repo_url
        assert repo_url.startswith("https://"), "Only https git urls are supported"
        if repo_url.startswith("https://oauth2"):
            raise Exception("Wait no, that doesn't make sense--that will hardcode the oauth token into the DB")
        remote_address = repo_url.replace("https://", f"https://oauth2:{token}@", 1)
    elif isinstance(repo_snapshot, LocalGitRepoSnapshot):
        remote_address = repo_snapshot.git_repo_path
        env = None
    assert remote_address is not None, "Remote address not found"

    new_repo = LocalGitRepo(destination_path)
    await new_repo.run_git(("init",))
    await new_repo.run_git(("config", "user.name", f"'{repo_snapshot.git_user_name}'"))
    await new_repo.run_git(("config", "user.email", f"'{repo_snapshot.git_user_email}'"))
    await new_repo.run_git(("remote", "add", "origin", str(remote_address)))
    await get_lines_from_process(f"git fetch --depth 1 origin {repo_snapshot.git_hash}", cwd=destination_path, env=env)
    await new_repo.run_git(("checkout", "FETCH_HEAD"))

    if repo_snapshot.git_diff:
        # apply any diffs from between git_hash and repo snapshot state of repo being checked out
        await apply_patch_via_git(new_repo, repo_snapshot.git_diff)

    return new_repo


async def create_repo(
    full_repo: FullLocalGitRepo,
    destination_path: Path,
) -> LocalGitRepo:
    """Creates an entire repo history locally from scratch. Much faster and more reliable than checking from remote."""
    anyio_path = anyio.Path(destination_path)
    assert (
        await anyio_path.is_dir()
    ), f"Destination for repo checkout must be a directory. {destination_path} is not a directory."
    if not await anyio_path.exists():
        destination_path.mkdir(parents=True)
    async for _ in anyio_path.iterdir():
        raise Exception(f"Destination for repo creation must be an empty directory. {destination_path} is not empty.")

    # create the empty repo
    new_repo = LocalGitRepo(destination_path)
    await new_repo.run_git(("init",))
    await new_repo.run_git(("checkout", "-b", "main"))
    if full_repo.git_branch != "main":
        await new_repo.run_git(("branch", "-m", "main", full_repo.git_branch))
    await new_repo.run_git(("config", "user.name", f"'{full_repo.git_user_name}'"))
    await new_repo.run_git(("config", "user.email", f"'{full_repo.git_user_email}'"))

    # put the history in
    for commit in full_repo.main_history:
        await _write_files_in_parallel(new_repo, commit.contents_by_path)
        await make_commit(new_repo, commit.commit_message, commit_time=commit.commit_time)

    if full_repo.git_diff:
        # apply any diffs from between git_hash and repo snapshot state of repo being checked out
        await apply_patch_via_git(new_repo, full_repo.git_diff)

    if full_repo.untracked_file_content_by_path:
        # make sure the untracked file contents are there
        await _write_files_in_parallel(new_repo, full_repo.untracked_file_content_by_path)

    return new_repo


async def _write_files_in_parallel(repo: LocalGitRepo, content: Mapping[str, str]) -> None:
    async with asyncio.TaskGroup() as tg:
        tasks = [tg.create_task(repo.write_file(file_path, content)) for file_path, content in content.items()]
        await asyncio.gather(*tasks)


async def copy_files_from_one_repo_to_another(
    src_repo_path: Path, dst_repo_path: Path, relative_file_paths: Sequence[Union[str, Path]]
) -> None:
    """Copies files from src to dst repo using the relative file paths."""
    for relative_path in relative_file_paths:
        src_file_path = src_repo_path / relative_path
        dst_file_path = anyio.Path(dst_repo_path / relative_path)
        # make sure necessary directories exist in destination
        await dst_file_path.parent.mkdir(parents=True, exist_ok=True)
        await asyncio.to_thread(shutil.copy2, src_file_path, dst_file_path)


@asynccontextmanager
async def temp_writable_local_git_repo(existing_repo: LocalGitRepo) -> AsyncIterator[WritableLocalGitRepo]:
    """Context manager to create a writable version of an existing git repo.

    Under the hood this will create a copy of the existing repo in a temporary directory in the fastest way possible.
    """
    async with async_temp_dir(TEMP_DIR) as writable_repo_path:
        repo_snapshot = await existing_repo.get_local_snapshot()

        cloned_repo = await checkout_repo(
            repo_snapshot=repo_snapshot,
            destination_path=writable_repo_path,
        )

        # copy any untracked files into new writable repo
        if repo_snapshot.git_untracked_files is not None:
            await copy_files_from_one_repo_to_another(
                src_repo_path=existing_repo.base_path,
                dst_repo_path=writable_repo_path,
                relative_file_paths=repo_snapshot.git_untracked_files,
            )

        yield await WritableLocalGitRepo.build_from_repo(cloned_repo)


@asynccontextmanager
async def get_writable_local_git_repo(
    existing_repo: LocalGitRepo, writable_repo_path: Path, is_removing_repo: bool = True
) -> AsyncIterator[WritableLocalGitRepo]:
    anyio_path = anyio.Path(writable_repo_path)
    try:
        repo_snapshot = await existing_repo.get_local_snapshot()
        if not await anyio_path.exists():
            await anyio_path.mkdir(parents=True)
        cloned_repo = await checkout_repo(
            repo_snapshot=repo_snapshot,
            destination_path=writable_repo_path,
        )
        # copy any untracked files into new writable repo
        if repo_snapshot.git_untracked_files is not None:
            await copy_files_from_one_repo_to_another(
                src_repo_path=existing_repo.base_path,
                dst_repo_path=writable_repo_path,
                relative_file_paths=repo_snapshot.git_untracked_files,
            )
        yield await WritableLocalGitRepo.build_from_repo(cloned_repo)
    finally:
        if is_removing_repo:
            if await anyio_path.exists():
                await asyncio.to_thread(shutil.rmtree, writable_repo_path)


async def get_repo_snapshot() -> GitRepoSnapshot:
    return await LocalGitRepo.build_from_cwd().get_snapshot_info()


async def get_git_repo_reference_hash() -> str:
    return (await get_repo_snapshot()).reference_hash


def get_repo_url_from_folder(repo_path: Path) -> str:
    try:
        repo_url = subprocess.check_output(
            ["git", "remote", "get-url", "origin"], cwd=repo_path, universal_newlines=True
        ).strip()
    except subprocess.CalledProcessError as e:
        raise e
    else:
        if repo_url.startswith("git@"):
            # convert ssh url to https
            repo_url = repo_url.replace(":", "/")
            repo_url = f"https://{repo_url[4:]}"
        if "https://oauth2:" in repo_url:
            # remove the oauth2 prefix
            # repo_url is something like https://oauth2:{token}@gitlab.com/.../.git
            # change it to https://gitlab.com/.../.git
            # This will happen if repo was originallycloned using oauth2
            suffix = repo_url.split("@")[-1]
            repo_url = "https://" + suffix
        return repo_url


def get_repo_base_path() -> Path:
    working_directory = Path(__file__).parent
    try:
        return Path(
            _run_command_and_capture_output(["git", "rev-parse", "--show-toplevel"], cwd=working_directory).strip()
        )
    except subprocess.CalledProcessError as e:
        try:
            return working_directory.parents[1]
        except IndexError:
            raise UnableToFindRepoBase() from e


def _run_command_and_capture_output(args: Sequence[str], cwd: Optional[Path] = None) -> str:
    arg_str = " ".join(shlex.quote(arg) for arg in args)
    print(f"Running command: {arg_str}", file=sys.stderr)
    with subprocess.Popen(args, text=True, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT) as proc:
        with StringIO() as output:
            _handle_output(proc, output, sys.stderr)
            if proc.wait() != 0:
                raise subprocess.CalledProcessError(proc.returncode, cmd=args, output=output.getvalue())
            return output.getvalue()


class UnableToFindRepoBase(Exception):
    """Raised when the base of the repository cannot be found."""


def _handle_output(process: subprocess.Popen[str], *files: TextIO) -> None:
    process_stdout = process.stdout
    assert process_stdout is not None
    while True:
        output = process_stdout.read(1)
        if output:
            for f in files:
                f.write(output)
        elif process.poll() is not None:
            break


def get_diff_without_index(diff: str) -> str:
    new_lines = []
    for line in diff.splitlines():
        if line.startswith("index "):
            # We replace index lines with "index 0000000..0000000 100644" because:
            # - `0000000..0000000` ensures no real object hashes are referenced, making the diff neutral.
            # - `100644` is the standard file mode for non-executable files in git diffs, ensuring compatibility.
            # - This keeps the diff format valid while removing specific index information.
            new_lines.append("index 0000000..0000000 100644")
        else:
            new_lines.append(line)
    return "\n".join(new_lines).strip()


def is_diffs_without_index_equal(diff_1: str, diff_2: str) -> bool:
    return get_diff_without_index(diff_1) == get_diff_without_index(diff_2)


# Copy-pasted from imbue to avoid moving the whole hammers machinery over to imbue-core.
async def get_lines_from_process(shell_command: str, is_exit_code_validated: bool = True, **kwargs) -> List[str]:
    p = await asyncio.create_subprocess_shell(shell_command, stdin=PIPE, stdout=PIPE, stderr=STDOUT, **kwargs)
    lines = [x.decode("UTF-8") for x in (await p.communicate())[0].splitlines()]
    if is_exit_code_validated:
        joined_lines = "\n".join(lines)
        assert (
            p.returncode == 0
        ), f"command failed: {shell_command}\nwith output:\n{joined_lines} with exit code {p.returncode}"
    return lines
