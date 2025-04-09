"""
Entry point for running the ffmpeg executable.
"""

import os
import stat
import sys
import tarfile
import zipfile
from datetime import datetime
from pathlib import Path

import requests  # type: ignore
from filelock import FileLock, Timeout
from progress.bar import Bar  # type: ignore
from progress.spinner import Spinner


class CustomBar(Bar):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.output = sys.stderr  # or use any stream-like object


class CustomSpinner(Spinner):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.output = sys.stderr


TIMEOUT = 10 * 60  # Wait upto 10 minutes to validate install
# otherwise break the lock and install anyway.

SELF_DIR = os.path.abspath(os.path.dirname(__file__))
LOCK_FILE = os.path.join(SELF_DIR, "lock.file")


PLATFORM_ZIP_FILES = {
    "win32": "https://github.com/zackees/static-graphviz/raw/refs/heads/main/bins/windows_10_cmake_Release_Graphviz-12.2.1-win32.zip",
    "darwin": "NOT VALID YET",
    "linux": "https://github.com/zackees/static-graphviz/raw/refs/heads/main/bins/graphviz_libraries_executables-12.2.1.tar.xz",
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
    print_stderr(f"Downloading {url} -> {local_path}")
    chunk_size = (1024 * 1024) // 4
    with requests.get(url, stream=True, timeout=TIMEOUT) as req:
        req.raise_for_status()
        spin: CustomSpinner | CustomBar = CustomSpinner("graphviz: ")
        size = -1
        try:
            size = int(req.headers.get("content-length", 0))
            spin = CustomBar(
                "graphviz: ", max=size, suffix="%(percent).1f%% - %(eta)ds"
            )
        except ValueError:
            pass
        with open(local_path, "wb") as file_d:
            with spin as spin:
                for chunk in req.iter_content(chunk_size):
                    file_d.write(chunk)
                    spin.next(len(chunk))
            sys.stderr.write(f"\nDownload of {url} -> {local_path} completed.\n")
            sys.stderr.flush()
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


def print_stderr(*args, **kwargs) -> None:
    """Print to stderr"""
    sys.stderr.write(f"{__file__}: ")
    print(*args, file=sys.stderr, **kwargs)
    sys.stderr.flush()


def _get_or_fetch_platform_executables_else_raise_no_lock(
    fix_permissions=True, download_dir: str | None = None
) -> Path:
    """Either get the executable or raise an error, internal api"""
    exe_dir = download_dir if download_dir else get_platform_dir()
    installed_crumb = os.path.join(exe_dir, "installed.crumb")
    if not os.path.exists(installed_crumb):
        # All archives store their platform executables in a folder such as "win32", "darwin", or "linux".
        # So install one level up from that folder.
        install_dir = os.path.dirname(exe_dir)
        os.makedirs(exe_dir, exist_ok=True)

        # Choose the correct download URL and archive name based on the platform
        if sys.platform.startswith("linux"):
            url = get_platform_http_zip()  # Returns the URL for the tar.xz file
            local_archive = exe_dir + ".tar.xz"
            download_file(url, local_archive)
            print_stderr(f"Extracting {local_archive} -> {install_dir}")
            with tarfile.open(local_archive, mode="r:xz") as tar:
                tar.extractall(install_dir)
        else:
            url = get_platform_http_zip()
            local_archive = exe_dir + ".zip"
            download_file(url, local_archive)
            print_stderr(f"Extracting {local_archive} -> {install_dir}")
            with zipfile.ZipFile(local_archive, mode="r") as zipf:
                zipf.extractall(install_dir)
        try:
            os.remove(local_archive)
        except OSError as err:
            print_stderr(
                f"{__file__}: Error could not remove {local_archive} because of {err}"
            )
        with open(installed_crumb, "wt") as filed:
            filed.write(f"installed from {url} on {str(datetime.now())}")
    dot_exe = _search_for_dot_exe(os.path.dirname(exe_dir))

    if sys.platform == "linux":
        # add the LD path to the binary
        ld_path = os.path.dirname(dot_exe)
        prev_ld_path = os.environ.get("LD_LIBRARY_PATH", "")
        if ld_path not in prev_ld_path:
            full_path = f"{ld_path}"
            if prev_ld_path:
                full_path += ":" + prev_ld_path
            os.environ["LD_LIBRARY_PATH"] = full_path
    if fix_permissions and sys.platform != "win32":
        # Set execute permissions and read bits for all users.
        exe_bits = stat.S_IXOTH | stat.S_IXUSR | stat.S_IXGRP
        read_bits = stat.S_IRUSR | stat.S_IRGRP | stat.S_IRGRP
        os.chmod(dot_exe, exe_bits | read_bits)
        assert os.access(dot_exe, os.X_OK), f"Could not execute {dot_exe}"
        assert os.access(dot_exe, os.R_OK), f"Could not get read bits of {dot_exe}"
    return dot_exe
