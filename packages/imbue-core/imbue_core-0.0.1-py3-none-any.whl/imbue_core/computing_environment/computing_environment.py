from __future__ import annotations

import asyncio
import shlex
import time
from pathlib import Path
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Protocol
from typing import Sequence
from typing import TYPE_CHECKING
from typing import Tuple
from typing import Union
from uuid import uuid4

import anyio
from loguru import logger

from imbue_core.computing_environment.data_types import AnyPath
from imbue_core.computing_environment.data_types import FailedToMakeCommitError
from imbue_core.computing_environment.data_types import PatchApplicationError
from imbue_core.computing_environment.data_types import RunCommandError
from imbue_core.section import Section

# Import the types needed for file modes
if TYPE_CHECKING:
    # for proper file mode typing
    from _typeshed import OpenBinaryModeReading
    from _typeshed import OpenBinaryModeWriting
    from _typeshed import OpenTextModeReading
    from _typeshed import OpenTextModeWriting


class ComputingEnvironment(Protocol):
    """Protocol defining the interface for a computing environment.

    This protocol specifies the required methods for interacting with a computing
    environment, including running commands and file operations.
    """

    async def run_command(
        self,
        command: Sequence[str],
        check: bool = True,
        secrets: Optional[List[Any]] = None,
        cwd: Optional[AnyPath] = None,
        is_error_logged: bool = True,
    ) -> str:
        ...

    async def run_git(
        self,
        command: Sequence[str],
        check: bool = True,
        cwd: Optional[AnyPath] = None,
        is_error_logged: bool = True,
        is_stripped: bool = True,
        retry_on_git_lock_error: bool = True,
    ) -> str:
        ...

    async def write_file(
        self,
        relative_path: AnyPath,
        content: Optional[Union[str, bytes]],
        cwd: Optional[AnyPath] = None,
        mode: Union[OpenTextModeWriting, OpenBinaryModeWriting] = "w",
        mkdir_if_missing: bool = True,
    ) -> None:
        ...

    async def read_file(
        self,
        relative_path: AnyPath,
        cwd: Optional[AnyPath] = None,
        mode: Union[OpenTextModeReading, OpenBinaryModeReading] = "r",
        mkdir_if_missing: bool = True,
    ) -> Union[str, bytes]:
        ...

    async def delete_file(
        self,
        relative_path: AnyPath,
        cwd: Optional[AnyPath] = None,
    ) -> None:
        ...


def _get_temp_patch_file() -> anyio.Path:
    # this is a bad idea because it triggers the file watcher
    # patch_file = (self.base_path / str(uuid4())).with_suffix(".patch")
    patch_file = (Path("/tmp") / uuid4().hex).with_suffix(".patch")
    return anyio.Path(patch_file)


async def apply_patch_without_git(computing_environment: ComputingEnvironment, diff: str) -> None:
    if diff.strip() == "":
        return
    patch_file = _get_temp_patch_file()
    try:
        await computing_environment.write_file(patch_file, diff)
        await computing_environment.run_command(("bash", "-c", f"patch -p1 < {patch_file}"))
    except RunCommandError as e:
        raise PatchApplicationError(f"Failed to apply patch: {e}") from e
    finally:
        await computing_environment.delete_file(patch_file)


async def is_repo_dirty(computing_environment: ComputingEnvironment) -> bool:
    """Check if the repo has any uncommitted changes."""
    return bool(await computing_environment.run_git(("status", "--porcelain")))


async def assert_repo_is_clean(computing_environment: ComputingEnvironment) -> None:
    """Assert that the repo has no uncommitted changes."""
    assert not await is_repo_dirty(
        computing_environment
    ), "You have untracked files. Please address them before using this script (this is to prevent accidentally adding large files unintentionally)"


async def get_branch_name(get_branch_name: ComputingEnvironment, is_error_logged: bool = True) -> str:
    """Get the name of the current branch."""
    return await get_branch_name.run_git(("symbolic-ref", "--short", "HEAD"), is_error_logged=is_error_logged)


async def rename_branch(
    computing_environment: ComputingEnvironment, old_name: str, new_name: str, force_if_exists: bool = True
) -> None:
    """Rename the given branch."""
    if force_if_exists:
        await computing_environment.run_git(("branch", "-M", old_name, new_name))
    else:
        await computing_environment.run_git(("branch", "-m", old_name, new_name))


async def get_branch_description(computing_environment: ComputingEnvironment, branch_name: str) -> str:
    """Get the description of the given branch."""
    try:
        return await computing_environment.run_git(
            ("config", f"branch.{branch_name}.description"), is_error_logged=False
        )
    except RunCommandError as e:
        if e.returncode == 1:
            # no description set
            return ""
        raise


async def is_branch_exists(computing_environment: ComputingEnvironment, branch_name: str) -> bool:
    """Check if the given branch exists."""
    result = await computing_environment.run_git(
        ("rev-parse", "--verify", "--quiet", branch_name), is_error_logged=False, check=False
    )
    return result.strip() != ""


async def is_detached_head(computing_environment: ComputingEnvironment) -> bool:
    """Check if the current HEAD is detached."""
    result = await computing_environment.run_git(("rev-parse", "--abbrev-ref", "HEAD"), is_error_logged=False)
    return result.strip() == "HEAD"


async def set_branch_description(
    computing_environment: ComputingEnvironment, branch_name: str, description: str
) -> None:
    """Set the description of the given branch."""
    await computing_environment.run_git(("config", f"branch.{branch_name}.description", description))


async def get_branch_commit(computing_environment: ComputingEnvironment, branch_name: str) -> str:
    """Get the commit of the given branch."""
    return await computing_environment.run_git(("rev-parse", branch_name))


async def is_branch_child_of_branch(
    computing_environment: ComputingEnvironment, child_branch_name: str, parent_branch_name: str
) -> bool:
    """Check if the given branch is a child of the parent branch."""
    try:
        await computing_environment.run_git(
            ("merge-base", "--is-ancestor", parent_branch_name, child_branch_name), is_error_logged=False
        )
        return True
    except RunCommandError as e:
        if e.stderr.strip() == "" and e.returncode == 1:
            # we expect this command to give an empty stderr and a return code of 1
            # if the child branch is not an ancestor of the parent branch
            return False
        raise


async def is_commit_on_branch(
    computing_environment: ComputingEnvironment, commit_hash: str, branch_name: str, local_only: bool = True
) -> bool:
    """Check if the given commit is on the given branch."""
    if local_only:
        result = await computing_environment.run_git(("branch", "--contains", commit_hash))
    else:
        result = await computing_environment.run_git(("branch", "-a", "--contains", commit_hash))
    return branch_name in result.splitlines()


async def fetch_branch(computing_environment: ComputingEnvironment, branch_name: str) -> None:
    """Fetch the given branch from the remote."""
    await computing_environment.run_git(("fetch", "origin", branch_name))


async def is_branch_present(computing_environment: ComputingEnvironment, branch_name: str) -> bool:
    """Check if branch with given name is present."""
    result = await computing_environment.run_git(("branch",))
    return branch_name in result.splitlines()


async def create_reset_and_checkout_branch(computing_environment: ComputingEnvironment, branch_name: str) -> str:
    """Create new branch with given name."""
    return await computing_environment.run_git(("switch", "-C", branch_name))


async def switch_branch(computing_environment: ComputingEnvironment, branch_name: str) -> str:
    """Switch to branch with given name."""
    return await computing_environment.run_git(("switch", branch_name))


async def delete_branch(computing_environment: ComputingEnvironment, branch_name: str, delete_remote: bool) -> str:
    """Delete branch with given name."""
    result = await computing_environment.run_git(("branch", "-D", branch_name))
    if delete_remote:
        result = await computing_environment.run_git(("push", "origin", "--delete", branch_name))
    return result


async def update_branch_to_hash(computing_environment: ComputingEnvironment, branch_name: str, git_hash: str) -> None:
    """Update the given branch to reference the given git hash."""
    # here we do it without checking out the branch
    await computing_environment.run_git(("branch", "-f", branch_name, git_hash))


async def switch_and_create_branch_if_needed(computing_environment: ComputingEnvironment, branch_name: str) -> str:
    """Switch to new branch, creating it if it doesn't already exist."""
    if await is_branch_present(computing_environment, branch_name):
        await switch_branch(computing_environment, branch_name)
    else:
        await create_reset_and_checkout_branch(computing_environment, branch_name)
    return await get_branch_name(computing_environment)


async def merge_branches(
    computing_environment: ComputingEnvironment,
    base_branch_name: str,
    merge_branch_name: str,
    is_moving_to_base_branch: bool = True,
) -> str:
    """Merge `merge_branch_name` into `base_branch_name`."""
    await switch_branch(computing_environment, base_branch_name)
    await computing_environment.run_git(("merge", merge_branch_name))
    if not is_moving_to_base_branch:
        await switch_branch(computing_environment, "-")
    return await get_branch_name(computing_environment)


async def get_merge_base(computing_environment: ComputingEnvironment, branch_name: str, target_branch: str) -> str:
    """Get the merge base of the given branch and target branch.

    The merge base is the most recent commit that is on both branches.
    """
    return await computing_environment.run_git(["merge-base", branch_name, target_branch], is_error_logged=False)


async def checkout_hash(computing_environment: ComputingEnvironment, git_hash: str) -> str:
    """Checkout given git hash."""
    return await computing_environment.run_git(("checkout", git_hash))


async def force_add(computing_environment: ComputingEnvironment, *paths: str) -> None:
    """Force-add the specified paths to the git index."""
    await computing_environment.run_git(("add", "-f", *paths))


async def git_add(computing_environment: ComputingEnvironment, *paths: str) -> None:
    """Add the specified paths to the git index."""
    await computing_environment.run_git(("add", *paths))


async def make_commit(
    computing_environment: ComputingEnvironment,
    commit_message: str,
    allow_empty: bool = False,
    amend: bool = False,
    commit_time: Optional[str] = None,
) -> str:
    if commit_message.strip() == "":
        commit_message = "No commit message provided"
    with Section(f"committing changes with message:\n{commit_message}"):
        if commit_time is None:
            time_args = ""
        else:
            time_args = f'GIT_AUTHOR_DATE="{commit_time}" GIT_COMMITTER_DATE="{commit_time}" '

        commit_message = shlex.quote(commit_message)
        no_changes_message = "No changes to commit"
        amend_args = "--amend " if amend else ""
        if allow_empty or amend:
            bash_command = f"""git add . && {time_args}git commit {amend_args}--allow-empty -m {commit_message} > /dev/null && git rev-parse HEAD"""
        else:
            bash_command = f"""git add . && ( git status | grep -q "nothing to commit" && echo "{no_changes_message}" ) || ( {time_args}git commit {amend_args}-m {commit_message} > /dev/null && git rev-parse HEAD )"""
        stdout = (await computing_environment.run_command(["bash", "-c", bash_command])).strip()
        if stdout == no_changes_message:
            raise FailedToMakeCommitError(f"Failed to make commit with message: {commit_message}. {bash_command=}")
        new_git_hash = stdout
        return new_git_hash


async def get_tree_hash_for_commit(computing_environment: ComputingEnvironment, commit: str) -> str:
    """Get the tree hash for the given commit."""
    return await computing_environment.run_git(["rev-parse", commit + "^{tree}"])


async def git_push(computing_environment: ComputingEnvironment, branch_name: str) -> str:
    """Push changes to remote branch with given name."""
    return await computing_environment.run_git(("push", "origin", branch_name))


async def force_push(computing_environment: ComputingEnvironment, branch_name: str) -> str:
    """Push changes to remote branch with given name."""
    return await computing_environment.run_git(("push", "--force", "origin", branch_name))


async def force_push_commit_with_retry(
    computing_environment: ComputingEnvironment, commit: str, branch_name: str, timeout: float = 30.0
) -> None:
    start_time = asyncio.get_event_loop().time()
    sleep_time = 0.5
    while True:
        try:
            await force_push_commit(computing_environment, commit, branch_name)
            break
        except Exception as exc:
            if asyncio.get_event_loop().time() - start_time > timeout:
                logger.error(f"Timeout reached: Could not force push {commit} to {branch_name} in {timeout} seconds.")
                raise TimeoutError(f"Timeout reached: Could not force push {commit} to {branch_name}.") from exc
            logger.info(f"Force push of {commit} to {branch_name} failed; trying again...")
            await asyncio.sleep(sleep_time)
            sleep_time *= 2


async def force_push_commit(computing_environment: ComputingEnvironment, commit: str, branch_name: str) -> None:
    try:
        await computing_environment.run_git(["push", "-f", "origin", f"{commit}:{branch_name}"], is_error_logged=False)
    except RunCommandError as e:
        if "fatal: bad object" in e.stderr:
            # TODO (danielmewes): We're retrying failed fetches here. However, there is also a separate
            #   force_push_commit_with_retry method that retries the entire force_push_commit.
            #   We should probably try the fetch only once, and then rely on the outer
            #   force_push_commit_with_retry to retry the entire force_push_commit call when retrying is =
            #   desired?
            NUM_TRIES = 3
            for _ in range(NUM_TRIES):
                try:
                    await computing_environment.run_git(["fetch", "origin", commit], is_error_logged=False)
                except RunCommandError as fetch_e:
                    if "not our ref" in fetch_e.stderr:
                        # FIXME: actually, this has been getting worse... I suspect perhaps rate limiting or something? We are checking thing out much more than usual...
                        await asyncio.sleep(2)
                    else:
                        raise fetch_e
                else:
                    start_time = time.time()
                    while time.time() - start_time < 10:
                        try:
                            await computing_environment.run_git(["push", "-f", "origin", f"{commit}:{branch_name}"])
                        except RunCommandError as repush_e:
                            if "not our ref" in repush_e.stderr:
                                # FIXME: actually, this has been getting worse... I suspect perhaps rate limiting or something? We are checking thing out much more than usual...
                                await asyncio.sleep(2)
                            else:
                                raise repush_e
                        else:
                            return
                    raise Exception(f"Could not force push commit {commit}")
            raise Exception(f"Could not fetch commit {commit} to force push it")
        else:
            raise


async def get_staged_files(computing_environment: ComputingEnvironment) -> Tuple[str, ...]:
    """Get list of all files in repo that are currently staged."""
    result = await computing_environment.run_git(("diff", "--name-only", "--cached"))
    return tuple(result.splitlines())


async def get_unstaged_files(computing_environment: ComputingEnvironment) -> Tuple[str, ...]:
    """Get list of all files in repo that are currently unstaged."""
    result = await computing_environment.run_git(("diff", "--name-only"))
    return tuple(result.splitlines())


async def restore_all_staged_files(computing_environment: ComputingEnvironment) -> None:
    """Restore all staged files."""
    await computing_environment.run_git(("restore", "--staged", "."))


async def restore_all_unstaged_changes(computing_environment: ComputingEnvironment) -> None:
    """Restore all unstaged changes."""
    await computing_environment.run_git(("restore", "."))


async def apply_patch_via_git_with_conflict_markers(
    computing_environment: ComputingEnvironment, git_diff: str, is_error_logged: bool = True
) -> None:
    """Apply a diff to repo with conflict markers."""
    if git_diff.strip() == "":
        return
    if not git_diff.endswith("\n"):
        # git requires a newline at the end of the patch
        git_diff += "\n"
    patch_file = _get_temp_patch_file()
    try:
        await computing_environment.write_file(patch_file, git_diff)
        await computing_environment.run_command(
            ["bash", "-c", f"git add . && git apply --verbose {patch_file} || git apply -3 --verbose {patch_file}"],
            is_error_logged=is_error_logged,
        )
    except RunCommandError as e:
        raise PatchApplicationError(f"Failed to apply patch: {e}") from e
    finally:
        await computing_environment.delete_file(patch_file)


async def is_repo_conflicted(computing_environment: ComputingEnvironment) -> bool:
    output = await computing_environment.run_git(["status"], is_error_logged=False, check=False)
    if "Unmerged paths:" in output:
        return True
    return False


async def get_head_hash(computing_environment: ComputingEnvironment) -> str:
    """Get the hash of the current HEAD commit."""
    git_hash = await computing_environment.run_git(["rev-parse", "HEAD"])
    assert len(git_hash) == 40, f"Expected 40-character git hash, got {git_hash}"
    return git_hash


async def get_parent_commit_hash(computing_environment: ComputingEnvironment, commit_hash: str) -> str:
    """Get the parent commit hash of the given commit hash."""
    git_hash = await computing_environment.run_git(["rev-parse", f"{commit_hash}^"])
    assert len(git_hash) == 40, f"Expected 40-character git hash, got {git_hash}"
    return git_hash


async def get_nth_commit_ago(
    computing_environment: ComputingEnvironment, commit_hash: str, n: int, is_error_logged: bool = True
) -> str:
    """Get the nth commit ago of the given commit hash."""
    git_hash = await computing_environment.run_git(
        ["rev-parse", f"{commit_hash}~{n}"], is_error_logged=is_error_logged
    )
    assert len(git_hash) == 40, f"Expected 40-character git hash, got {git_hash}"
    return git_hash


async def get_initial_repo_commit_hash(computing_environment: ComputingEnvironment, commit_hash: str = "HEAD") -> str:
    """Get the initial commit hash of the repo."""
    # --max-parents=0: only consider commits with no parents
    # --date-order: sort by date (newest first)
    output = await computing_environment.run_git(["rev-list", "--max-parents=0", commit_hash, "--date-order"])
    # assume the oldest commit with no parents is the initial repo commit
    all_root_commits = output.splitlines()
    root_commit = all_root_commits[-1]
    assert len(root_commit) == 40, f"Expected 40-character git hash, got {root_commit}"
    return root_commit


async def get_upto_nth_commit_ago(computing_environment: ComputingEnvironment, commit_hash: str, n: int) -> str:
    """Get the commit hash of the upto nth commit ago of the given commit hash.

    If the commit history is shorter than n, it will return the first commit.
    """
    try:
        return await get_nth_commit_ago(computing_environment, commit_hash, n, is_error_logged=False)
    except RunCommandError as e:
        if "unknown revision or path not in the working tree" in e.stderr:
            return await get_initial_repo_commit_hash(computing_environment)
        raise e


async def get_commit_message(computing_environment: ComputingEnvironment, commit_hash: str) -> str:
    """Get the commit message of the given commit hash."""
    return await computing_environment.run_git(["log", "-1", "--pretty=%B", commit_hash])


async def get_commit_count_between_hashes(
    computing_environment: ComputingEnvironment, old_hash: str, new_hash: str
) -> int:
    """Get the number of commits between two hashes."""
    output = await computing_environment.run_git(["rev-list", "--count", f"{old_hash}..{new_hash}"])
    return int(output.strip())


async def fetch_and_checkout_hash(
    computing_environment: ComputingEnvironment, git_hash: str, is_error_logged: bool = True
) -> None:
    await computing_environment.run_command(
        ["bash", "-c", f"git fetch origin {git_hash} && git checkout {git_hash}"],
        is_error_logged=is_error_logged,
    )


async def fetch_ref_and_checkout_hash(
    computing_environment: ComputingEnvironment, ref: str, git_hash: str, is_error_logged: bool = True
) -> None:
    await computing_environment.run_command(
        ["bash", "-c", f"git fetch origin {ref} && git checkout {git_hash}"],
        is_error_logged=is_error_logged,
    )


async def wait_for_git_hash_to_checkout(
    computing_environment: ComputingEnvironment, git_hash: str, timeout: float = 20.0
) -> None:
    with Section(f"checking out git hash {git_hash}"):
        # boo, I hate this - but not sure how else to wait for the git hash to be available
        # we could track when our own agents have finished doing pushes for a given hash, but it's probably so much more complicated that it's not really worth it
        # and even if we did that, there's no guarantee that you wouldn't need this anyway due to slight inconsistency in the remote service (eg gitlab or github)
        start_time = asyncio.get_event_loop().time()
        while True:
            try:
                await fetch_and_checkout_hash(computing_environment, git_hash, is_error_logged=False)
                break
            except RunCommandError as exc:
                if asyncio.get_event_loop().time() - start_time > timeout:
                    logger.error(f"Timeout reached: Git hash {git_hash} is not available after {timeout} seconds.")
                    logger.error(exc.stdout)
                    raise TimeoutError(f"Timeout reached: Git hash {git_hash} is not available.") from exc
                logger.info(f"Waiting for git hash {git_hash} to be available...")
                await asyncio.sleep(0.5)


async def wait_for_git_hash_with_ref_to_checkout(
    computing_environment: ComputingEnvironment, git_hash: str, ref: str, timeout: float = 20.0
) -> None:
    with Section(f"checking out git hash {git_hash} with ref {ref}"):
        # boo, I hate this - but not sure how else to wait for the git hash to be available
        # we could track when our own agents have finished doing pushes for a given hash, but it's probably so much more complicated that it's not really worth it
        # and even if we did that, there's no guarantee that you wouldn't need this anyway due to slight inconsistency in the remote service (eg gitlab or github)
        start_time = asyncio.get_event_loop().time()
        while True:
            try:
                await fetch_ref_and_checkout_hash(computing_environment, ref, git_hash, is_error_logged=False)
                break
            except RunCommandError as exc:
                if asyncio.get_event_loop().time() - start_time > timeout:
                    logger.error(f"Timeout reached: Git hash {git_hash} is not available after {timeout} seconds.")
                    logger.error(exc.stdout)
                    raise TimeoutError(f"Timeout reached: Git hash {git_hash} is not available.") from exc
                logger.info(f"Waiting for git hash {git_hash} to be available...")
                await asyncio.sleep(0.5)


async def force_checkout_git_hash_immediate_on_branch(
    computing_environment: ComputingEnvironment, git_hash: str, branch_name: str
) -> None:
    # Here we clear any uncommited changes, then change branch, before checking out the new hash
    # We need to do these three steps so we don't affect the currently checked out branch
    command = f"git reset --hard && git checkout -B {branch_name} && git reset --hard {git_hash}"
    logger.debug(f"Running command: {command}")
    await computing_environment.run_command(
        [
            "bash",
            "-c",
            command,
        ],
    )


async def get_git_folder_paths(computing_environment: ComputingEnvironment) -> Tuple[str, ...]:
    """Get the paths of all the git folders in the repo."""
    result = await computing_environment.run_command(["ls", ".git"])
    return tuple(result.splitlines())


async def apply_patch_via_git(computing_environment: ComputingEnvironment, git_diff: str) -> None:
    """Apply a diff to repo."""
    if git_diff.strip() == "":
        return
    patch_file = _get_temp_patch_file()
    await computing_environment.write_file(patch_file, git_diff)
    # NOTE: --allow-empty is necessary because the patch may be empty, or result in no changes
    #  update (2024-11-22) --allow-empty is not available in the git version in our devcontainers
    #  so we have to do a janky error check below
    try:
        await computing_environment.run_git(("apply", "--verbose", str(patch_file)))
    except RunCommandError as e:
        raise PatchApplicationError(f"Failed to apply patch: {e}") from e
    finally:
        await computing_environment.delete_file(patch_file)


async def get_git_diff(
    computing_environment: ComputingEnvironment, staged: bool = False, is_error_logged: bool = True
) -> str:
    """Get the diff for the current repo state."""
    # make sure `is_stripped=False` otherwise patch can be invalid
    if staged:
        return await computing_environment.run_git(
            ["diff", "--staged"], is_stripped=False, is_error_logged=is_error_logged
        )
    return await computing_environment.run_git(["diff"], is_stripped=False, is_error_logged=is_error_logged)


async def get_diff_between_hashes(computing_environment: ComputingEnvironment, old_hash: str, new_hash: str) -> str:
    """Get the diff between two git hashes."""
    # make sure `is_stripped=False` otherwise patch can be invalid
    return await computing_environment.run_git(["diff", old_hash, new_hash], is_stripped=False)


async def get_patch_for_commit(computing_environment: ComputingEnvironment, commit_hash: str) -> str:
    """Get the patch for a given commit hash."""
    return await computing_environment.run_git(["show", "--pretty=format:", "--patch", commit_hash], is_stripped=False)


async def get_untracked_files(computing_environment: ComputingEnvironment) -> Tuple[str, ...]:
    """Get the untracked files in the repo."""
    result = await computing_environment.run_git(["ls-files", "--others", "--exclude-standard"], is_error_logged=False)
    return tuple([line.strip() for line in result.splitlines() if line.strip()])


async def get_staged_unstaged_and_combined_diffs(
    computing_environment: ComputingEnvironment,
) -> Tuple[str, str, str]:
    # FIXME: make sure the combined diff is ALWAYS the combination of the staged and unstaged diffs
    """Get the staged diff, the unstaged diff, and the combined diff"""
    unstaged_diff = await get_git_diff(computing_environment, staged=False)
    staged_diff = await get_git_diff(computing_environment, staged=True)
    combined_diff = await computing_environment.run_git(["diff", "HEAD"], is_stripped=False)
    return staged_diff, unstaged_diff, combined_diff


async def get_unmerged_blob_hashes(computing_environment: ComputingEnvironment) -> Tuple[str, ...]:
    """Get the blob hashes of all the unmerged files in the repo."""
    result = await computing_environment.run_command(
        ["bash", "-c", "git ls-files --unmerged | awk '{print $2}' | sort -u"], check=False
    )
    return tuple(line.strip() for line in result.splitlines() if line.strip() != "")


async def get_staged_blob_hashes(computing_environment: ComputingEnvironment) -> Tuple[str, ...]:
    """Get the blob hashes of all the staged files in the repo."""
    staged_blob_hashes = await computing_environment.run_command(
        [
            "bash",
            "-c",
            'staged_blobs=$(git diff --cached --name-only --diff-filter=ACMRT | while read file; do git ls-files --stage "$file" | awk \'{print $2}\'; done); echo "$staged_blobs"',
        ]
    )
    return tuple(line.strip() for line in staged_blob_hashes.splitlines() if line.strip() != "")


async def get_blob_content_by_hash(computing_environment: ComputingEnvironment, blob_hash: str) -> bytes:
    """Get the content of a blob by its hash."""
    result = await computing_environment.run_git(["cat-file", "-p", blob_hash], is_stripped=False)
    return result.encode("utf-8")


async def get_unmerged_and_staged_blob_contents_by_hash(
    computing_environment: ComputingEnvironment,
) -> Dict[str, bytes]:
    """Get the contents of all the unmerged and staged blobs in the repo."""
    unmerged_blob_hashes = await get_unmerged_blob_hashes(computing_environment)
    staged_blob_hashes = await get_staged_blob_hashes(computing_environment)
    all_relevant_blob_hashes = unmerged_blob_hashes + staged_blob_hashes
    blob_content_tasks_by_hash = {
        blob_hash: get_blob_content_by_hash(computing_environment, blob_hash) for blob_hash in all_relevant_blob_hashes
    }
    blob_contents = await asyncio.gather(*blob_content_tasks_by_hash.values())
    return {
        blob_hash: blob_content for blob_hash, blob_content in zip(blob_content_tasks_by_hash.keys(), blob_contents)
    }


async def write_blob_content(computing_environment: ComputingEnvironment, blob_hash: str, blob_content: bytes) -> None:
    """Write the content of a blob to the repo."""
    # write the blob content to a temp file
    temp_file = anyio.Path(f"/tmp/{blob_hash}")
    try:
        await computing_environment.write_file(temp_file, blob_content, mode="wb")
        # write the blob to the repo
        result = await computing_environment.run_git(["hash-object", "-w", str(temp_file)])
        assert result.strip() == blob_hash, f"Expected blob hash {blob_hash}, got {result.strip()}"
    finally:
        await computing_environment.delete_file(temp_file)


async def write_blob_content_by_hash(
    computing_environment: ComputingEnvironment, blob_content_by_hash: Dict[str, bytes]
) -> None:
    """Write the content of all the blobs to the repo."""
    tasks = []
    for blob_hash, blob_content in blob_content_by_hash.items():
        tasks.append(write_blob_content(computing_environment, blob_hash, blob_content))
    await asyncio.gather(*tasks)


async def get_modified_files_with_conflicts(computing_environment: ComputingEnvironment) -> Tuple[str, ...]:
    """Get the modified files with conflicts."""
    commands = ["diff --check --staged", "diff --check"]
    conflicted_files = set()
    for command in commands:
        result = await computing_environment.run_git(command.split(), check=False, is_error_logged=False)
        # output is of the form:
        # test.txt:2: leftover conflict marker

        for line in result.splitlines():
            parts = line.split(":", maxsplit=1)
            if len(parts) == 2:
                file_path, message = parts
                if "leftover conflict marker" in message.strip():
                    conflicted_files.add(file_path)
    return tuple(conflicted_files)


async def get_conflicted_pathnames(computing_environment: ComputingEnvironment) -> Tuple[str, ...]:
    """Get the pathnames of all the conflicted files in the repo."""
    result = await computing_environment.run_git(["diff", "--name-only", "--diff-filter=U"])
    return tuple(result.splitlines())


async def get_conflicted_contents_by_path(computing_environment: ComputingEnvironment) -> Dict[str, bytes]:
    """Get the contents of all the conflicted files in the repo."""
    conflicted_files = await get_conflicted_pathnames(computing_environment)
    conflicted_contents_by_path: Dict[str, bytes] = {}
    for file_path in conflicted_files:
        content = await computing_environment.read_file(file_path, mode="rb")
        assert isinstance(content, bytes), f"Expected bytes, got {type(content)}"
        conflicted_contents_by_path[file_path] = content
    return conflicted_contents_by_path


async def get_modified_pathnames(computing_environment: ComputingEnvironment) -> Tuple[str, ...]:
    """Get the pathnames of all the modified files in the repo."""
    result = await computing_environment.run_command(["bash", "-c", "git status --porcelain | awk '{print $2}'"])
    return tuple(result.splitlines())


async def get_modified_file_contents_by_path(computing_environment: ComputingEnvironment) -> Dict[str, bytes]:
    """Get the contents of all the modified files in the repo."""
    modified_pathnames = await get_modified_pathnames(computing_environment)
    modified_file_contents_by_path: Dict[str, bytes] = {}
    for pathname in modified_pathnames:
        content = await computing_environment.read_file(pathname, mode="rb")
        assert isinstance(content, bytes), f"Expected bytes, got {type(content)}"
        modified_file_contents_by_path[pathname] = content
    return modified_file_contents_by_path


async def get_repo_url(computing_environment: ComputingEnvironment) -> str:
    repo_url = await computing_environment.run_git(["remote", "get-url", "origin"])
    if repo_url.startswith("git@"):
        # convert ssh url to https
        repo_url = repo_url.replace(":", "/")
        repo_url = f"https://{repo_url[4:]}"
    if "https://oauth2:" in repo_url:
        # remove the oauth2 prefix
        # repo_url is something like https://oauth2:{token}@gitlab.com/.../.git
        # change it to https://gitlab.com/.../.git
        suffix = repo_url.split("@")[-1]
        repo_url = "https://" + suffix
    return repo_url


async def get_main_branch_name_for_repo(
    computing_environment: ComputingEnvironment, default_branch: Optional[str] = None
) -> str:
    """Get the name of the main branch for the repo.

    Attempts to detect whether the repository uses 'main', 'master', or another name
    as its primary branch by checking for common branch names in order of preference.
    """
    possible_main_branches = ["main", "master", "trunk", "development"]

    if default_branch is not None and default_branch not in possible_main_branches:
        possible_main_branches.insert(0, default_branch)

    try:
        # First check if any of the common main branch names exist
        # and return the first one that does
        for branch in possible_main_branches:
            if await is_branch_exists(computing_environment, branch):
                return branch

        # If we couldn't find a common main branch, try to determine the default branch
        # This gets the branch that HEAD points to in a newly cloned repo
        default_remote_branch = await computing_environment.run_git(
            ["symbolic-ref", "refs/remotes/origin/HEAD"], is_error_logged=False
        )
        if default_remote_branch:
            # Format is typically refs/remotes/origin/main, so extract the last part
            default_remote_branch = default_remote_branch.strip().split("/")[-1]
            return default_remote_branch
    except RunCommandError as e:
        logger.error(f"Error detecting main branch: {e}")
        raise e
    raise ValueError("Could not detect main branch for repo.")
