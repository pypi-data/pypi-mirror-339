from .commit import commitMessageCreator
from .git import checkGit, checkWorkingTree, gitAdd

def main():
    if checkGit():
        if not checkWorkingTree():
            answer = input("""[!] There are untracked files.
[?] Run "git add ."? [y/n] """).lower()
            if answer == "y":
                gitAdd()
        commitMessageCreator()
    else:
        print("❌ Git not initialized.")

