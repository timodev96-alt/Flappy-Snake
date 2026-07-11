import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SCRIPTS_DIR = ROOT / "Scripts"
ENTRY = SCRIPTS_DIR / "main.py"
DIST_DIR = ROOT / "dist"
BUILD_DIR = ROOT / "build"
APP_NAME = "FlappySnake"


def ensure_pyinstaller():
    try:
        import PyInstaller  # noqa: F401
    except ImportError:
        print("PyInstaller not found. Installing it now...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])


def get_add_data_arg(source_dir: Path):
    return f"{source_dir}{os.pathsep}{source_dir.name}"


def build():
    ensure_pyinstaller()

    if DIST_DIR.exists():
        shutil.rmtree(DIST_DIR)
    if BUILD_DIR.exists():
        shutil.rmtree(BUILD_DIR)

    cmd = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--noconfirm",
        "--clean",
        "--name",
        APP_NAME,
        "--onefile",
        "--windowed",
        "--distpath",
        str(DIST_DIR),
        "--workpath",
        str(BUILD_DIR),
        "--paths",
        str(SCRIPTS_DIR),
        "--collect-data",
        "pygame",
        "--add-data",
        get_add_data_arg(ROOT / "Graphics"),
        "--add-data",
        get_add_data_arg(ROOT / "Sound Effects"),
        str(ENTRY),
    ]

    print("Building executable with:")
    print(" ".join(cmd))
    subprocess.check_call(cmd)

    exe_path = DIST_DIR / f"{APP_NAME}.exe"
    if exe_path.exists():
        print(f"\nBuild complete: {exe_path}")
    else:
        print("\nBuild finished, but the executable was not found. Please inspect the output above.")


if __name__ == "__main__":
    build()
