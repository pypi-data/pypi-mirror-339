from shutil import which as w
import subprocess


def checkGitInstall() -> (bool):
    if w("git") is not None:
        return True
    else:
        return False
def checkGitInit() -> (bool):
    try:
        subprocess.run(
            ["git", "-C", ".", "rev-parse", "--is-inside-work-tree"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True
        )
        return True
    except subprocess.CalledProcessError:
        return False
def gitAdd() -> (bool):
    try:
        subprocess.run(
            ["git", "add", "."],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True
        )
        return True
    except subprocess.CalledProcessError:
        return False


def checkWorkingTree() -> (bool):
    result = subprocess.run(
        ["git", "status", "--porcelain"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    return result.stdout.strip() == ""

def checkGit() -> (bool):
    return checkGitInstall() and checkGitInit()

