import asyncio
import random
import re
import tarfile
import rio.project_config
import tempfile
from pathlib import Path
from typing import *  # type: ignore

import revel

import rio.cli
from rio.cli.rio_api import RioApi


def should_directory_likely_be_excluded(
    dir_path: Path,
) -> tuple[str, str] | None:
    """
    Some directories should very likely not be part of the user's project. This
    function looks at a directory, and if the directory should likely be
    excluded it returns a name and explanation of why. Returns `None` otherwise.
    """
    assert dir_path.is_dir(), dir_path

    # Virtual environments
    if (dir_path / "pyvenv.cfg").exists():
        return (
            "contain a python virtual environment",
            "Virtual environments contain a huge number of files which are typically created by `uv`, `venv`, `poetry`, `conda` or similar tools. These don't have to be included with your project and can easily be recreated later.",
        )

    # .git
    if dir_path.name == ".git":
        return (
            "be a git folder",
            "Git repositories contain the entire history of your project and typically aren't necessary to deploy your project.",
        )

    # node_modules
    if dir_path.name == "node_modules":
        return (
            "be npm's modules directory",
            "Node's package manager (npm) can store a vast number of files in these folders. These typically don't have to be included with your project and can easily be recreated later.",
        )

    # Build directories
    if dir_path.name in ("build", "dist"):
        return (
            "contain past build files",
            "Build directories can contain a large number of past build outputs and are not typically necessary to deploy your project.",
        )

    # All good, keep it
    return None


def list_files(
    proj: rio.project_config.RioProjectConfig,
    dir_path: Path,
) -> Iterable[Path]:
    """
    Recursively yield all files in the given directory, ignoring any files that
    are ignored by the project.

    Any directories that should likely be excluded are ignored, unless
    explicitly listed in an exception in the `.rioignore` file.

    Interacts with the terminal.

    All yielded paths are absolute.
    """
    assert dir_path.exists(), dir_path
    assert dir_path.is_dir(), dir_path

    dir_path = dir_path.resolve()

    for path in dir_path.iterdir():
        # Ignore files that are ignored by the project
        if not proj.file_is_path_of_project(path):
            continue

        # If this is a file, yield it
        if path.is_file():
            yield path
            continue

        # Is this a directory that the user likely doesn't want to include?
        exclude_reason = should_directory_likely_be_excluded(path)
        if (
            exclude_reason is not None
            and not proj.ignores.is_explicitly_included(path)
        ):
            appears_to, explanation = exclude_reason
            rel_path = path.relative_to(proj.project_directory)
            revel.warning(
                f'Excluding "{rel_path}". This directory appears to {appears_to}.'
            )
            revel.warning(explanation)
            revel.warning(
                f'If you do want to include it after all, add the following to your ".rioignore" file:'
            )
            revel.warning(f"!{rel_path}")
            revel.print()

            # Explicitly ignore this directory
            proj.rioignore_additions.extend(
                [
                    f"# Automatically excluded by Rio",
                    f"# This directory appears to {appears_to}",
                    f"/{rel_path}",
                    "",
                ]
            )
            continue

        # Recurse
        yield from list_files(proj, path)


def pack_up_project(
    proj: rio.project_config.RioProjectConfig,
    archive_path: Path,
) -> int:
    """
    Compresses all files in the project into an archive, displaying progress,
    and interacting with the terminal in general.

    Returns the size of the uncompressed files in bytes.
    """

    # Find all files which are part of the project
    revel.print("Scanning project")
    project_directory = proj.project_directory.resolve()
    files = set(list_files(proj, project_directory))

    # Make sure essential files are included
    essential_files = {
        project_directory / "rio.toml",
    }

    missing_files = essential_files - files

    if missing_files:
        raise NotImplementedError(
            "TODO: Ask the user whether these files should be included"
        )

    # Gather all files into a single archive
    #
    # Randomize the file order to ensure that the progress is somewhat uniform.
    # Hard drives hate him.
    revel.print("Creating app package")
    files = list(files)
    random.shuffle(files)
    total_size = 0

    with revel.ProgressBar() as bar:
        with tarfile.open(archive_path, "w:xz") as tar:
            for ii, file_path in enumerate(files):
                bar.progress = ii / len(files)

                # Add the file to the tarball
                relative_path = file_path.relative_to(project_directory)
                tar.add(file_path, arcname=relative_path)

                # Add the file size to the total
                total_size += file_path.stat().st_size

    return total_size


async def create_or_update_app(
    api: RioApi,
    proj: rio.project_config.RioProjectConfig,
) -> None:
    """
    Uploads the given archive file to the cloud, creating a new deployment.
    """
    # Get an app name
    try:
        name = proj.deploy_name
    except KeyError:
        revel.print(
            "What should your app be called? This name will be used as part of the URL."
        )
        revel.print(
            'For example, if you name your app "my-app", it will be deployed at `https://rio.dev/.../my-app`.'
        )

        name = input("App name: ")

        allowed_chars = "abcdefghijklmnopqrstuvwxyz0123456789-"
        normalized = re.sub("[^" + allowed_chars + "]", "-", name.lower())
        normalized = re.sub("-+", "-", normalized)

    # Make sure the user is logged in
    # TODO

    # Pack up the project
    revel.print_chapter("Packaging project")
    with tempfile.TemporaryDirectory() as tmp_dir:
        assert Path(tmp_dir).exists(), tmp_dir
        archive_path = Path(tmp_dir) / "packed-project.tar.xz"
        uncompressed_size_in_bytes = pack_up_project(proj, archive_path)
        compressed_size_in_bytes = archive_path.stat().st_size

        revel.print(
            f"Compressed size: {compressed_size_in_bytes / 1024 / 1024:.2f} MiB"
        )
        revel.print(
            f"Uncompressed size: {uncompressed_size_in_bytes / 1024 / 1024:.2f} MiB"
        )
        revel.print(
            f"Compression ratio: {uncompressed_size_in_bytes / compressed_size_in_bytes:.2f}x"
        )

        # Make sure the user has the ability to create this app
        # TODO:
        # - # of apps
        # - compressed size
        # - uncompressed size

        # Create the app
        await api.create_app(
            name=proj.name,
            packed_app=archive_path.open("rb"),
        )


async def _get_or_create_app(
    client: RioApi,
    proj: rio.project_config.RioProjectConfig,
) -> str:
    """
    Gets the app corresponding to this project. If the project doesn't have an
    app yet, creates a new one.

    This function interacts directly with the terminal should user input be
    required.
    """
    app_id = proj.deployment_app_id

    # If no app ID is stored with the project, there obviously isn't an
    # associated app.
    if app_id is None:
        pass

    # If an app ID is stored, make sure this app indeed exists on the API, and
    # this user has access to it.
    else:
        user_response = await client.get_user()

        for app in user_response["apps"]:
            if app["id"] == app_id:
                return app_id

    # No app ID was found, so create a new one
    project_nicename = (
        proj.project_directory.name.strip()
        .replace("-", " ")
        .replace("_", " ")
        .title()
    )

    app = await client.create_app(
        name=project_nicename,
        packed_app=None,  # TODO
        start_in_realm=None,
    )

    # Return the fresh app
    return app["id"]


async def deploy_app(
    client: RioApi,
    proj: rio.project_config.RioProjectConfig,
) -> None:
    """
    Deploys the app to the cloud.
    """
    # Every app in the cloud has a unique ID. The first time a project is
    # deployed, the app ID is created and stored in the `rio.toml`.
    #
    # Get this app's ID, either from the `rio.toml` or by creating a new app in
    # the API.


async def main() -> None:
    with rio.project_config.RioProjectConfig.try_locate_and_load() as proj:
        pack_up_project(
            proj,
            Path.home() / "Downloads" / "packed-project.tar.xz",
        )

    #     async with rio.cli.cli_instance.CliInstance() as cli:
    #         await create_or_update_app(None, proj)


if __name__ == "__main__":
    asyncio.run(main())
