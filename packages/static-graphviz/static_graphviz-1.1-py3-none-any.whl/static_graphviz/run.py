"""
Entry point for running the ffmpeg executable.
"""

import os
import stat
import subprocess
import sys
import zipfile
from datetime import datetime
from pathlib import Path

import requests  # type: ignore
from filelock import FileLock, Timeout
from progress.bar import Bar  # type: ignore
from progress.spinner import Spinner  # type: ignore

TIMEOUT = 10 * 60  # Wait upto 10 minutes to validate install
# otherwise break the lock and install anyway.

SELF_DIR = os.path.abspath(os.path.dirname(__file__))
LOCK_FILE = os.path.join(SELF_DIR, "lock.file")


PLATFORM_ZIP_FILES = {
    "win32": "https://github.com/zackees/static-graphviz/raw/refs/heads/main/bins/windows_10_cmake_Release_Graphviz-12.2.1-win32.zip",
    "darwin": "NOT VALID YET",
    "linux": "https://github.com/zackees/static-graphviz/raw/refs/heads/main/bins/ubuntu_22.04_graphviz-12.2.1-debs.tar.xz",
}


def check_system() -> None:
    """Friendly error if there's a problem with the system configuration."""
    if sys.platform not in PLATFORM_ZIP_FILES:
        raise OSError(f"Please implement static_ffmpeg for {sys.platform}")


def get_platform_http_zip() -> str:
    """Return the download link for the current platform"""
    check_system()
    return PLATFORM_ZIP_FILES[sys.platform]


def get_platform_dir() -> str:
    """Either get the executable or raise an error"""
    check_system()
    return os.path.join(SELF_DIR, "bin", sys.platform)


def download_file(url: str, local_path: str) -> str:
    """Downloads a file to the give path."""
    # NOTE the stream=True parameter below
    print(f"Downloading {url} -> {local_path}")
    chunk_size = (1024 * 1024) // 4
    with requests.get(url, stream=True, timeout=TIMEOUT) as req:
        req.raise_for_status()
        spinner: Spinner | Bar = Spinner("graphviz: ")
        size = -1
        try:
            size = int(req.headers.get("content-length", 0))
            spinner = Bar("graphviz: ", max=size, suffix="%(percent).1f%% - %(eta)ds")
        except ValueError:
            pass
        with open(local_path, "wb") as file_d:
            with spinner as spinner:
                for chunk in req.iter_content(chunk_size):
                    file_d.write(chunk)
                    spinner.next(len(chunk))
            sys.stdout.write(f"\nDownload of {url} -> {local_path} completed.\n")
    return local_path


def get_or_fetch_platform_executables_else_raise(
    fix_permissions=True, download_dir=None
) -> Path:
    """Either get the executable or raise an error"""
    lock = FileLock(LOCK_FILE, timeout=TIMEOUT)  # pylint: disable=E0110
    try:
        with lock.acquire():
            return _get_or_fetch_platform_executables_else_raise_no_lock(
                fix_permissions=fix_permissions, download_dir=download_dir
            )
    except Timeout:
        sys.stderr.write(
            f"{__file__}: Warning, could not acquire lock at {LOCK_FILE}\n"
        )
        return _get_or_fetch_platform_executables_else_raise_no_lock(
            fix_permissions=fix_permissions, download_dir=download_dir
        )


def _search_for_dot_exe(exe_dir: str) -> Path:
    """Search for the dot executable in the given directory."""
    for root, _, files in os.walk(exe_dir):
        for file in files:
            if file in ["dot", "dot.exe"]:
                return Path(root) / file
    raise FileNotFoundError(f"dot executable not found in {exe_dir}")


def _get_or_fetch_platform_executables_else_raise_no_lock(
    fix_permissions=True, download_dir=None
) -> Path:
    """Either get the executable or raise an error, internal api"""
    exe_dir = download_dir if download_dir else get_platform_dir()
    installed_crumb = os.path.join(exe_dir, "installed.crumb")
    if not os.path.exists(installed_crumb):
        # All zip files store their platform executables in a folder
        # like "win32" or "darwin" or "linux" inside the executable. So root
        # the install one level up from that same directory.
        install_dir = os.path.dirname(exe_dir)
        os.makedirs(exe_dir, exist_ok=True)
        url = get_platform_http_zip()
        local_zip = exe_dir + ".zip"
        download_file(url, local_zip)
        print(f"Extracting {local_zip} -> {install_dir}")
        with zipfile.ZipFile(local_zip, mode="r") as zipf:
            zipf.extractall(install_dir)
        try:
            os.remove(local_zip)
        except OSError as err:
            print(f"{__file__}: Error could not remove {local_zip} because of {err}")
        with open(installed_crumb, "wt") as filed:  # pylint: disable=W1514
            filed.write(f"installed from {url} on {str(datetime.now())}")

    dot_exe = _search_for_dot_exe(exe_dir)

    # dot_exe = os.path.join(exe_dir, "dot")
    # if sys.platform == "win32":
    #     dot_exe = f"{dot_exe}.exe"
    # for exe in [dot_exe]:
    #     if (
    #         fix_permissions
    #         and sys.platform != "win32"
    #         and (not os.access(exe, os.X_OK) or not os.access(exe, os.R_OK))
    #     ):
    #         # Set bits for execution and read for all users.
    #         exe_bits = stat.S_IXOTH | stat.S_IXUSR | stat.S_IXGRP
    #         read_bits = stat.S_IRUSR | stat.S_IRGRP | stat.S_IXGRP
    #         os.chmod(exe, exe_bits | read_bits)
    #         assert os.access(exe, os.X_OK), f"Could not execute {exe}"
    #         assert os.access(exe, os.R_OK), f"Could not get read bits of {exe}"
    # return Path(dot_exe)
    if fix_permissions:
        # Set bits for execution and read for all users.
        exe_bits = stat.S_IXOTH | stat.S_IXUSR | stat.S_IXGRP
        read_bits = stat.S_IRUSR | stat.S_IRGRP | stat.S_IXGRP
        os.chmod(dot_exe, exe_bits | read_bits)
        assert os.access(dot_exe, os.X_OK), f"Could not execute {dot_exe}"
        assert os.access(dot_exe, os.R_OK), f"Could not get read bits of {dot_exe}"
    return dot_exe


def main_static_dot() -> None:
    """Entry point for running static_ffmpeg, which delegates to ffmpeg."""
    dot_exe = get_or_fetch_platform_executables_else_raise()
    rtn: int = subprocess.call([str(dot_exe)] + sys.argv[1:])
    sys.exit(rtn)


def main_print_paths() -> None:
    """Entry point for printing ffmpeg paths"""
    dot_exe = get_or_fetch_platform_executables_else_raise()
    print(f"DOT={dot_exe}")
    sys.exit(0)


if __name__ == "__main__":
    get_or_fetch_platform_executables_else_raise()
