# MIT license

import os
import subprocess
import time
from importlib.metadata import PackageNotFoundError, version

import typer
from rich.console import Console
from rich.text import Text
from typing_extensions import Annotated

# Create Rich console
console = Console()

app = typer.Typer(
    help="git-multi-status shows uncommitted, untracked and unpushed changes in multiple Git repositories."
)
app.debug = False  # Default debug state


def debug(*args, **kwargs):
    """Print debug messages if debug mode is enabled"""
    if app.debug:
        console.print(*args, **kwargs)


def debug_callback(ctx: typer.Context, value: bool):
    """Callback to set debug mode on the app instance"""
    app.debug = value
    return value


def run_git_command(git_dir, work_tree, *args):
    """Run a git command and return its output."""
    cmd = ["git"]
    if work_tree:
        cmd.extend(["--work-tree", work_tree])
    if git_dir:
        cmd.extend(["--git-dir", git_dir])
    cmd.extend(args)

    debug(f"Running git command: {' '.join(cmd)}")

    try:
        output = subprocess.check_output(cmd, stderr=subprocess.DEVNULL).decode("utf-8").strip()
        debug(f"Command output: {output}")
        return output
    except subprocess.CalledProcessError as e:
        debug(f"Command failed with return code: {e.returncode}")
        return ""


def find_git_repos(start_dir, depth, warn_not_repo):
    """Find all git repositories up to a certain depth. Use 0 for no depth, -1 for unlimited."""
    debug(f"Searching for git repos in: {start_dir}")
    debug(f"Depth: {depth}")

    git_dirs = []

    if depth == 0:
        # Only check if the start_dir itself is a git repo
        git_path = os.path.join(start_dir, ".git")
        debug(f"Checking for .git in: {git_path}")
        if os.path.isdir(git_path):
            git_dirs.append(start_dir)
        elif warn_not_repo:
            text = Text()
            text.append(f"{start_dir}: ")
            text.append("Not a git repository", style="yellow")
            console.print(text)
        return git_dirs

    for root, dirs, _ in os.walk(start_dir, followlinks=True):
        debug(f"Checking directory: {root}")
        debug(f"Subdirectories: {dirs}")

        if ".git" in dirs:
            git_dirs.append(root)
        elif warn_not_repo:
            text = Text()
            text.append(f"{root}: ")
            text.append("Not a git repository", style="yellow")
            console.print(text)

        # Calculate current depth
        rel_path = os.path.relpath(root, start_dir)
        current_depth = len(rel_path.split(os.sep)) if rel_path != "." else 0

        # Stop recursion if we've reached max depth
        if depth > 0 and current_depth >= depth:
            dirs.clear()  # This stops os.walk from going deeper

    return git_dirs


def print_status(proj_dir, cur_branch, status_text, status_style):
    """Print a status message with rich formatting."""
    text = Text()
    text.append(f"{proj_dir}{cur_branch}: ")
    text.append(status_text, style=status_style)
    console.print(text)


def check_repo(
    proj_dir,
    exclude_ok,
    do_fetch,
    throttle,
    flatten,
    show_branch,
    no_push,
    no_pull,
    no_upstream,
    no_uncommitted,
    no_untracked,
    no_stashes,
):
    """Check the status of a git repository."""
    git_dir = os.path.join(proj_dir, ".git")
    git_conf = os.path.join(git_dir, "config")

    # Check if the repo is safe (ownership)
    if os.path.isdir(git_dir):
        try:
            git_dir_owner = os.stat(git_dir).st_uid
            current_user_id = os.getuid()

            if current_user_id != git_dir_owner:
                text = Text()
                text.append(f"{proj_dir}: ")
                text.append("Unsafe ownership, owned by someone else. Skipping.", style="purple bold")
                console.print(text)
                return False
        except OSError:
            text = Text()
            text.append(f"{proj_dir}: ")
            text.append("Could not check ownership. Skipping.", style="purple bold")
            console.print(text)
            return False

    # Check git config for this project to see if we should ignore this repo
    try:
        ignore = run_git_command(git_dir, None, "config", "-f", git_conf, "--bool", "mgitstatus.ignore")
        if ignore == "true":
            return True
    except Exception:
        pass

    # Check if repo is locked
    if os.path.exists(os.path.join(git_dir, "index.lock")):
        text = Text()
        text.append(f"{proj_dir}: ")
        text.append("Locked. Skipping.", style="red bold")
        console.print(text)
        return False

    # Do a 'git fetch' if requested
    if do_fetch:
        run_git_command(git_dir, os.path.dirname(git_dir), "fetch", "-q")

    # Refresh the index, or we might get wrong results
    run_git_command(git_dir, os.path.dirname(git_dir), "update-index", "-q", "--refresh")

    # Get current branch
    cur_branch = ""
    if show_branch:
        branch = run_git_command(git_dir, None, "rev-parse", "--abbrev-ref", "HEAD")
        cur_branch = f" ({branch})"

    # Find all remote branches that have been checked out
    needs_push_branches = []
    needs_pull_branches = []
    needs_upstream_branches = []

    # Find all branch refs
    refs_dir = os.path.join(git_dir, "refs", "heads")
    branch_refs = []

    if os.path.isdir(refs_dir):
        for root, _, files in os.walk(refs_dir):
            for file in files:
                ref_path = os.path.join(root, file)
                rel_path = os.path.relpath(ref_path, refs_dir)
                if os.path.isfile(ref_path):
                    branch_refs.append(rel_path)

    for ref_head in branch_refs:
        # Check if this branch is tracking an upstream
        upstream = run_git_command(
            git_dir, None, "rev-parse", "--abbrev-ref", "--symbolic-full-name", f"{ref_head}@{{u}}"
        )

        if upstream:
            # Branch is tracking a remote branch
            cnt_ahead_behind = run_git_command(
                git_dir, None, "rev-list", "--left-right", "--count", f"{ref_head}...{upstream}"
            )
            if cnt_ahead_behind:
                cnt_ahead, cnt_behind = cnt_ahead_behind.split()

                if int(cnt_ahead) > 0:
                    needs_push_branches.append(ref_head)
                if int(cnt_behind) > 0:
                    needs_pull_branches.append(ref_head)

                # Check if this branch is a branch off another branch and if it needs to be updated
                rev_local = run_git_command(git_dir, None, "rev-parse", "--verify", ref_head)
                rev_remote = run_git_command(git_dir, None, "rev-parse", "--verify", upstream)
                rev_base = run_git_command(git_dir, None, "merge-base", ref_head, upstream)

                if rev_local and rev_remote and rev_base:
                    if rev_local != rev_remote:
                        if rev_local == rev_base:
                            needs_pull_branches.append(ref_head)
                        if rev_remote == rev_base:
                            needs_push_branches.append(ref_head)
        else:
            # Branch does not have an upstream
            needs_upstream_branches.append(ref_head)

    # Remove duplicates
    needs_push_branches = list(set(needs_push_branches))
    needs_pull_branches = list(set(needs_pull_branches))
    needs_upstream_branches = list(set(needs_upstream_branches))

    # Find out if there are unstaged, uncommitted or untracked changes
    # The original script used exit codes, but we need to handle this differently in Python
    # For these git commands, an empty output means success (no changes)
    unstaged_output = run_git_command(git_dir, os.path.dirname(git_dir), "diff-index", "HEAD", "--")
    unstaged = 1 if unstaged_output else 0

    uncommitted_output = run_git_command(git_dir, os.path.dirname(git_dir), "diff-files", "--ignore-submodules", "--")
    uncommitted = 1 if uncommitted_output else 0

    untracked = run_git_command(git_dir, os.path.dirname(git_dir), "ls-files", "--exclude-standard", "--others")

    # Get stashes
    old_dir = os.getcwd()
    os.chdir(os.path.dirname(git_dir))
    stashes = run_git_command(git_dir, None, "stash", "list")
    stash_count = len(stashes.splitlines()) if stashes else 0
    os.chdir(old_dir)

    debug(f"UNSTAGED: {unstaged}")
    debug(f"UNCOMMITTED: {uncommitted}")
    debug(f"UNTRACKED: {untracked}")
    debug(f"STASHES: {stash_count}")

    # Build up the status string
    is_ok = True
    status_parts = []

    # Check for needs_push
    if needs_push_branches and not no_push:
        push_status = f"Needs push ({','.join(needs_push_branches)})"
        if flatten:
            print_status(proj_dir, cur_branch, push_status, "yellow bold")
        else:
            status_parts.append((push_status, "yellow bold"))
        is_ok = False

    # Check for needs_pull
    if needs_pull_branches and not no_pull:
        pull_status = f"Needs pull ({','.join(needs_pull_branches)})"
        if flatten:
            print_status(proj_dir, cur_branch, pull_status, "blue bold")
        else:
            status_parts.append((pull_status, "blue bold"))
        is_ok = False

    # Check for needs_upstream
    if needs_upstream_branches and not no_upstream:
        upstream_status = f"Needs upstream ({','.join(needs_upstream_branches)})"
        if flatten:
            print_status(proj_dir, cur_branch, upstream_status, "purple bold")
        else:
            status_parts.append((upstream_status, "purple bold"))
        is_ok = False

    # Check for uncommitted changes
    if (unstaged != 0 or uncommitted != 0) and not no_uncommitted:
        uncommitted_status = "Uncommitted changes"
        if flatten:
            print_status(proj_dir, cur_branch, uncommitted_status, "red bold")
        else:
            status_parts.append((uncommitted_status, "red bold"))
        is_ok = False

    # Check for untracked files
    if untracked and not no_untracked:
        untracked_status = "Untracked files"
        if flatten:
            print_status(proj_dir, cur_branch, untracked_status, "cyan bold")
        else:
            status_parts.append((untracked_status, "cyan bold"))
        is_ok = False

    # Check for stashes
    if stash_count and not no_stashes:
        stashes_status = f"{stash_count} stashes"
        if flatten:
            print_status(proj_dir, cur_branch, stashes_status, "yellow bold")
        else:
            status_parts.append((stashes_status, "yellow bold"))
        is_ok = False

    # If everything is OK
    if is_ok:
        ok_status = "ok"
        if flatten and not exclude_ok:
            print_status(proj_dir, cur_branch, ok_status, "green bold")
        else:
            status_parts.append((ok_status, "green bold"))

    # Print non-flattened output
    if not flatten and (not is_ok or not exclude_ok):
        text = Text()
        text.append(f"{proj_dir}{cur_branch}: ")

        for i, (status, style) in enumerate(status_parts):
            text.append(status, style=style)
            if i < len(status_parts) - 1:
                text.append(" ")

        console.print(text)

    # Throttle if requested
    if do_fetch and throttle:
        time.sleep(throttle)

    return is_ok


def version_callback(value: bool):
    try:
        __version__ = version("git-multi-status")
    except PackageNotFoundError:
        __version__ = "dev"

    if value:
        print(__version__)
        raise typer.Exit()


@app.command()
def main(
    dir: Annotated[str, typer.Argument(..., help="Dir to scan")] = ".",
    warn_not_repo: Annotated[bool, typer.Option("-w", help="Warn about dirs that are not Git repositories")] = False,
    exclude_ok: Annotated[bool, typer.Option("-e", "--no-ok", help="Exclude repos that are 'ok'")] = False,
    do_fetch: Annotated[bool, typer.Option("-f", help="Do a 'git fetch' on each repo (slow for many repos)")] = False,
    throttle: Annotated[
        int, typer.Option("--throttle", help="Wait SEC seconds between each 'git fetch' (-f option)")
    ] = 0,
    depth: Annotated[
        int, typer.Option("-d", "--depth", help="Scan depth: 0=no recursion, -1=unlimited, >0=max depth")
    ] = 2,
    flatten: Annotated[bool, typer.Option("--flatten", help="Show only one status per line")] = False,
    show_branch: Annotated[bool, typer.Option("-b", help="Show currently checked out branch")] = False,
    no_push: Annotated[bool, typer.Option("--no-push", help="Limit output: hide push status")] = False,
    no_pull: Annotated[bool, typer.Option("--no-pull", help="Limit output: hide pull status")] = False,
    no_upstream: Annotated[bool, typer.Option("--no-upstream", help="Limit output: hide upstream status")] = False,
    no_uncommitted: Annotated[
        bool, typer.Option("--no-uncommitted", help="Limit output: hide uncommitted changes")
    ] = False,
    no_untracked: Annotated[bool, typer.Option("--no-untracked", help="Limit output: hide untracked files")] = False,
    no_stashes: Annotated[bool, typer.Option("--no-stashes", help="Limit output: hide stashes")] = False,
    _: Annotated[bool, typer.Option("-v", "--version", callback=version_callback, is_eager=True)] = None,
    __: Annotated[bool, typer.Option("--debug", help="Enable debug output", callback=debug_callback)] = False,
):
    """
    git-multi-status shows uncommitted, untracked and unpushed changes in multiple Git repositories.
    """

    # Convert relative path to absolute path based on current working directory
    start_dir = os.path.abspath(dir)

    debug(f"Starting directory: {start_dir}")
    debug(f"Current working directory: {os.getcwd()}")

    # Process directory using absolute path
    repos = find_git_repos(start_dir, depth, warn_not_repo)

    debug(f"Found repositories: {repos}")

    all_repos_ok = True  # Track if all repos are OK

    for repo in repos:
        if os.path.isdir(os.path.join(repo, ".git")):
            repo_ok = check_repo(
                repo,
                exclude_ok,
                do_fetch,
                throttle,
                flatten,
                show_branch,
                no_push,
                no_pull,
                no_upstream,
                no_uncommitted,
                no_untracked,
                no_stashes,
            )
            all_repos_ok = all_repos_ok and repo_ok

    return typer.Exit(code=0 if all_repos_ok else 1)


if __name__ == "__main__":
    app()
