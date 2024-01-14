import asyncio
import shlex
from typing import Tuple

from git import Repo
from git.exc import GitCommandError, InvalidGitRepositoryError

import config

from ..logging import LOGGER


def install_req(cmd: str) -> Tuple[str, str, int, int]:
    async def install_requirements():
        args = shlex.split(cmd)
        process = await asyncio.create_subprocess_exec(
            *args,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await process.communicate()
        return (
            stdout.decode("utf-8", "replace").strip(),
            stderr.decode("utf-8", "replace").strip(),
            process.returncode,
            process.pid,
        )

    return asyncio.get_event_loop().run_until_complete(
        install_requirements()
    )


        from git import Repo, GitCommandError, InvalidGitRepositoryError
import config  # Importing the necessary config module
import logging  # Importing the logging module if it hasn't been already imported

# Assuming LOGGER is configured as per the logging module documentation
def git(name):
    LOGGER = logging.getLogger(__name)  # Assuming LOGGER is configured as per the logging module documentation

    REPO_LINK = config.UPSTREAM_REPO
    if config.GIT_TOKEN:
        GIT_USERNAME = REPO_LINK.split("com/")[1].split("/")[0]
        TEMP_REPO = REPO_LINK.split("https://")[1]
        UPSTREAM_REPO = (
            f"https://{GIT_USERNAME}:{config.GIT_TOKEN}@{TEMP_REPO}"
        )
    else:
        UPSTREAM_REPO = config.UPSTREAM_REPO

    try:
        repo = Repo()
        LOGGER.info(f"Git Client Found [VPS DEPLOYER]")
    except GitCommandError as e:
        LOGGER.error(f"Invalid Git Command: {e}")
        # Handle the GitCommandError exception

    except InvalidGitRepositoryError:
        repo = Repo.init()
        if "origin" in repo.remotes:
            origin = repo.remote("origin")
        else:
            origin = repo.create_remote("origin", UPSTREAM_REPO)
        origin.fetch()
        repo.create_head(
            config.UPSTREAM_BRANCH,
            origin.refs[config.UPSTREAM_BRANCH]
        )
        repo.heads[config.UPSTREAM_BRANCH].set_tracking_branch(
            origin.refs[config.UPSTREAM_BRANCH]
        )
        repo.heads[config.UPSTREAM_BRANCH].checkout(True)
        try:
            repo.create_remote("origin", config.UPSTREAM_REPO)
        except BaseException as e:
            LOGGER.error(f"Failed to create remote: {e}")
            # Handle the exception appropriately
        nrs = repo.remote("origin")
        nrs.fetch(config.UPSTREAM_BRANCH)
        try:
            nrs.pull(config.UPSTREAM_BRANCH)
        except GitCommandError as e:
            LOGGER.error(f"Failed to pull: {e}")
            repo.git.reset("--hard", "FETCH_HEAD")
            # Handle the GitCommandError appropriately
        install_req("pip3 install --no-cache-dir -r requirements.txt")
        LOGGER.info(f"Fetching updates from ™°‌ 🇭 🇦 🇷 🇸 🇭 🇺")
