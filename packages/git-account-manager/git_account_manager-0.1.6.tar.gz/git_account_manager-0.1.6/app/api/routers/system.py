import os
import platform
import shutil
import subprocess
from tkinter import Tk, filedialog

from fastapi import APIRouter, HTTPException

from app.models import FolderResponse

# Configure DPI Awareness for Windows
if platform.system() == "Windows":
    try:
        from ctypes import windll

        windll.shcore.SetProcessDpiAwareness(1)
    except Exception as e:
        print(f"Could not set DPI awareness: {e}")

router = APIRouter(
    prefix="/system",
    tags=["System"],
    responses={404: {"description": "Not found"}},
)


@router.post("/folder-select", response_model=FolderResponse)
async def trigger_folder_dialog():
    """Opens a native folder selection dialog on the server."""
    try:
        root = Tk()
        root.withdraw()
        root.call("wm", "attributes", ".", "-topmost", True)

        selected_path = filedialog.askdirectory(title="Select Git Repository Directory")
        root.destroy()

        if selected_path:
            selected_path = os.path.abspath(selected_path)
            return FolderResponse(status="success", path=selected_path)
        else:
            return FolderResponse(status="cancelled", message="Folder selection cancelled.")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/check-prerequisites")
async def check_prerequisites():
    """
    Check if all required system prerequisites are installed.

    This endpoint verifies if Git and SSH are installed and available on the system.

    Returns:
        dict: Status of each prerequisite
    """
    git_installed = shutil.which("git") is not None
    ssh_installed = shutil.which("ssh") is not None

    # Additional checks to verify git works
    git_version = None
    if git_installed:
        try:
            result = subprocess.run(["git", "--version"], capture_output=True, text=True, check=False)
            git_version = result.stdout.strip() if result.returncode == 0 else None
        except Exception:
            git_installed = False

    # Additional check to verify ssh works
    ssh_version = None
    if ssh_installed:
        try:
            result = subprocess.run(["ssh", "-V"], capture_output=True, text=True, check=False)
            # SSH version is typically printed to stderr
            ssh_version = result.stderr.strip() if result.stderr else result.stdout.strip()
        except Exception:
            ssh_installed = False

    return {
        "git": git_installed,
        "ssh": ssh_installed,
        "details": {
            "git_version": git_version,
            "ssh_version": ssh_version,
            "platform": platform.system(),
            "python_version": platform.python_version(),
        },
    }
