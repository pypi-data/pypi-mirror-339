# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright The Geneva Authors

# a module for automatically inspecting path and capturing the local env

import base64
import logging
import site
import tempfile
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import emoji

from geneva.packager.uploader import Uploader
from geneva.packager.zip import WorkspaceZipper
from geneva.tqdm import tqdm

_LOG = logging.getLogger(__name__)


def _maybe_pyproject() -> Path | None:
    """
    Inspect the current working directory and return the path to the
    source root if it's in a python project.
    """

    # don't resolve because we could be inside a link
    cwd = Path.cwd().absolute()
    assert cwd.root == "/", "cwd is not absolute"

    root = Path("/")
    cur = cwd

    while not list(cur.glob("pyproject.toml")) and (cur := cur.parent) != root:
        ...

    # TODO: use the packaging tool configured in pyproject.toml
    # to determine the source root
    if list(cur.glob("pyproject.toml")):
        return cur / "src"

    return None


def _maybe_src() -> Path | None:
    """
    Inspect the current working directory and return the path to the
    source root if it's in a python project.
    """

    # don't resolve because we could be inside a link
    cwd = Path.cwd().absolute()
    assert cwd.root == "/", "cwd is not absolute"

    root = Path("/")
    cur = cwd

    while not list(cur.glob("src")) and (cur := cur.parent) != root:
        ...

    if list(cur.glob("src")):
        return cur / "src"

    return None


def _maybe_python_repo() -> Path | None:
    """
    Inspect the current working directory and return the path to the
    source root if it's in a python project.
    """

    return _maybe_pyproject() or _maybe_src()


def _find_workspace() -> Path:
    """
    Inspect the current working directory and return the path to the
    source root if it's in a python project. If we can not find a
    python source root, return the current working directory.
    """

    return _maybe_python_repo() or Path.cwd()


def get_paths_to_package() -> list[Path]:
    """
    Inspect the current working directory and return the path to the
    source root if it's in a python project. If we can not find a
    python source root, return the current working directory.
    """

    paths = sorted(
        {
            Path(p).resolve().absolute()
            for p in [
                _find_workspace(),
                Path.cwd(),
                *site.getsitepackages(),
            ]
        }
    )

    _LOG.info("found paths to package: %s", paths)

    return paths


def package_local_env_into_zips(output_dir: Path | str) -> list[list[Path]]:
    """
    Package the local environment into zip files.

    return a list of the paths to the zip files.
    """

    paths = get_paths_to_package()

    zips = []

    for p in paths:
        if not p.exists():
            _LOG.warning("path %s does not exist", p)
            continue

        if not p.is_dir():
            _LOG.warning("path %s is not a directory", p)
            continue

        _LOG.info("packaging %s", p)

        path_b32 = base64.b32encode(p.as_posix().encode()).decode()

        zip_path, _ = WorkspaceZipper(
            p,
            output_dir,
            file_name=f"{path_b32}.zip",
        ).zip()

        zips.append(zip_path)

    return zips


def upload_local_env(
    *,
    zip_output_dir: Path | str | None = None,
    uploader: Uploader | None = None,
) -> list[list[str]]:
    zip_output_dir = zip_output_dir or tempfile.mkdtemp()

    zips = package_local_env_into_zips(zip_output_dir)
    uploader = uploader or Uploader.get()

    sizes = []
    with ThreadPoolExecutor(max_workers=8) as executor:
        res = []
        for zip_paths in zips:
            res.append([])
            for zip_path in zip_paths:
                fut = executor.submit(
                    uploader.upload,
                    zip_path,
                )
                sizes.append(zip_path.stat().st_size)
                res[-1].append(fut)

        with tqdm(
            total=sum(sizes), unit="B", unit_scale=True, unit_divisor=1024, smoothing=0
        ) as pbar:
            pbar.set_description(emoji.emojize(":rocket: uploading zips"))
            for i in range(len(res)):
                uploaded_uris = []
                for p in as_completed(res[i]):
                    pbar.update(sizes.pop(0))
                    uploaded_uris.append(p.result())
                res[i] = uploaded_uris

    return res
