from pathlib import Path
from tabulate import tabulate
import readline
from prompt_toolkit import prompt
from prompt_toolkit.key_binding import KeyBindings
import subprocess
import tempfile

configFile = Path(".py-commit.conf")
def multiline_input(message):
    return prompt(message,  multiline=True)

def gitmojis() -> (dict):
    emoji = {
  "art": {
    "emoji": "🎨",
    "description": "Improve structure / format of the code"
  },
  "zap": {
    "emoji": "⚡️",
    "description": "Improve performance"
  },
  "fire": {
    "emoji": "🔥",
    "description": "Remove code or files"
  },
  "bug": {
    "emoji": "🐛",
    "description": "Fix a bug"
  },
  "ambulance": {
    "emoji": "🚑️",
    "description": "Critical hotfix"
  },
  "sparkles": {
    "emoji": "✨",
    "description": "Introduce new features"
  },
  "memo": {
    "emoji": "📝",
    "description": "Add or update documentation"
  },
  "rocket": {
    "emoji": "🚀",
    "description": "Deploy stuff"
  },
  "lipstick": {
    "emoji": "💄",
    "description": "Add or update the UI and style files"
  },
  "tada": {
    "emoji": "🎉",
    "description": "Begin a project"
  },
  "white_check_mark": {
    "emoji": "✅",
    "description": "Add, update, or pass tests"
  },
  "lock": {
    "emoji": "🔒️",
    "description": "Fix security issues"
  },
  "bookmark": {
    "emoji": "🔖",
    "description": "Release / Version tags"
  },
  "rotating_light": {
    "emoji": "🚨",
    "description": "Fix compiler/linter warnings"
  },
  "construction": {
    "emoji": "🚧",
    "description": "Work in progress"
  },
  "arrow_down": {
    "emoji": "⬇️",
    "description": "Downgrade dependencies"
  },
  "arrow_up": {
    "emoji": "⬆️",
    "description": "Upgrade dependencies"
  },
  "pushpin": {
    "emoji": "📌",
    "description": "Pin dependencies to specific versions"
  },
  "construction_worker": {
    "emoji": "👷",
    "description": "Add or update CI build system"
  },
  "chart_with_upwards_trend": {
    "emoji": "📈",
    "description": "Add or update analytics or tracking code"
  },
  "recycle": {
    "emoji": "♻️",
    "description": "Refactor code"
  },
  "heavy_plus_sign": {
    "emoji": "➕",
    "description": "Add a dependency"
  },
  "heavy_minus_sign": {
    "emoji": "➖",
    "description": "Remove a dependency"
  },
  "wrench": {
    "emoji": "🔧",
    "description": "Add or update configuration files"
  },
  "hammer": {
    "emoji": "🔨",
    "description": "Add or update development scripts"
  },
  "globe_with_meridians": {
    "emoji": "🌐",
    "description": "Internationalization and localization"
  },
  "pencil2": {
    "emoji": "✏️",
    "description": "Fix typos"
  },
  "poop": {
    "emoji": "💩",
    "description": "Write bad code that needs to be improved"
  },
  "rewind": {
    "emoji": "⏪️",
    "description": "Revert changes"
  },
  "twisted_rightwards_arrows": {
    "emoji": "🔀",
    "description": "Merge branches"
  },
  "package": {
    "emoji": "📦️",
    "description": "Add or update compiled files or packages"
  },
  "alien": {
    "emoji": "👽️",
    "description": "Update code due to external API changes"
  },
  "truck": {
    "emoji": "🚚",
    "description": "Move or rename resources (e.g.: files, paths)"
  },
  "page_facing_up": {
    "emoji": "📄",
    "description": "Add or update license"
  },
  "boom": {
    "emoji": "💥",
    "description": "Introduce breaking changes"
  },
  "bento": {
    "emoji": "🍱",
    "description": "Add or update assets"
  },
  "wheelchair": {
    "emoji": "♿️",
    "description": "Improve accessibility"
  },
  "bulb": {
    "emoji": "💡",
    "description": "Add or update comments in source code"
  },
  "beers": {
    "emoji": "🍻",
    "description": "Write code drunkenly"
  },
  "card_file_box": {
    "emoji": "🗃️",
    "description": "Perform database related changes"
  },
  "loud_sound": {
    "emoji": "🔊",
    "description": "Add or update logs"
  },
  "mute": {
    "emoji": "🔇",
    "description": "Remove logs"
  },
  "busts_in_silhouette": {
    "emoji": "👥",
    "description": "Add or update contributor(s)"
  },
  "children_crossing": {
    "emoji": "🚸",
    "description": "Improve user experience / usability"
  },
  "building_construction": {
    "emoji": "🏗️",
    "description": "Make architectural changes"
  },
  "iphone": {
    "emoji": "📱",
    "description": "Work on responsive design"
  },
  "clown_face": {
    "emoji": "🤡",
    "description": "Mock things"
  },
  "egg": {
    "emoji": "🥚",
    "description": "Add or update an easter egg"
  },
  "see_no_evil": {
    "emoji": "🙈",
    "description": "Add or update .gitignore file"
  },
  "alembic": {
    "emoji": "⚗️",
    "description": "Perform experiments"
  },
  "mag": {
    "emoji": "🔍️",
    "description": "Improve SEO"
  },
  "label": {
    "emoji": "🏷️",
    "description": "Add or update types"
  },
  "seedling": {
    "emoji": "🌱",
    "description": "Add or update seed files"
  },
  "triangular_flag_on_post": {
    "emoji": "🚩",
    "description": "Add, update, or remove feature flags"
  },
  "goal_net": {
    "emoji": "🥅",
    "description": "Catch errors"
  },
  "dizzy": {
    "emoji": "💫",
    "description": "Add or update animations and transitions"
  },
  "wastebasket": {
    "emoji": "🗑️",
    "description": "Deprecate code that needs to be cleaned"
  },
  "passport_control": {
    "emoji": "🛂",
    "description": "Work on code related to authorization, roles and permissions"
  },
  "adhesive_bandage": {
    "emoji": "🩹",
    "description": "Simple fix for a non-critical issue"
  },
  "monocle_face": {
    "emoji": "🧐",
    "description": "Data exploration/inspection"
  },
  "coffin": {
    "emoji": "⚰️",
    "description": "Remove dead code"
  },
  "test_tube": {
    "emoji": "🧪",
    "description": "Add a failing test"
  },
  "bricks": {
    "emoji": "🧱",
    "description": "Infrastructure related changes"
  },
  "technologist": {
    "emoji": "🧑‍💻",
    "description": "Improve developer experience"
  },
  "money_with_wings": {
    "emoji": "💸",
    "description": "Add sponsors or money-related infrastructure"
  },
  "thread": {
    "emoji": "🧵",
    "description": "Add or update threading/concurrency code"
  },
  "safety_vest": {
    "emoji": "🦺",
    "description": "Add or update code related to validations"
  },
  "airplane": {
    "emoji": "✈️",
    "description": "Improve offline experience"
  }
}

    print("Select a Gitmoji")
    print("If you prefer, you can leave this field blank as it is optional.")

# Obtener la lista de emojis
    headers = ["Id", "Code", "Description", "Emoji"]
    rows = [
            [ 
                i,
                list(emoji.keys())[i],
                emoji[list(emoji.keys())[i]]["description"],
                emoji[list(emoji.keys())[i]]["emoji"],   
            ]
            for i in range(len(list(emoji.keys())))
            ]
    print(tabulate(rows, headers=headers))
    emojiSelected = int(input("emojiSelected> "))
    return emoji[list(emoji.keys())[emojiSelected]]["emoji"]
def checkScopeConfig(configFile) -> (list):
    if not configFile.exists():
        configFile.touch()
    with open(configFile, "r") as f:
        return [line.strip() for line in f if line.strip()]


def addScopeList(configFile):
    current = checkScopeConfig(configFile)
    while True:
        print(f"You currently have {len(current)} \"Scope(s)\" created:")
        print("To finish adding scopes, use the \"exit\" command.")
        if len(current) > 0:
            for i in range(len(current)):
                print(f"{i+1}. {current[i]}")
        scope = input("scope> ").strip().lower()
        if scope == "exit":
            break
        current.append(scope)
    with open(configFile,"w") as f:
        for scope in current:
            f.write(f"{scope}\n")
    print(checkScopeConfig(configFile))
    
def chooseScope() -> (str):
    scopeList = checkScopeConfig(configFile)
    print("Please select the scope number you wish to use.")
    for idx, name in enumerate(scopeList, 0):
        print(f"{idx}. {name}")
    try:
        scope = int(input("scopeNumber> "))
        print(f"The scope chosen was {scopeList[scope]}")
        return scopeList[scope]
    except:
        return ""

def typeSelector() -> str():
    types = {
  "feat": "A new feature for the user.",
  "fix": "A bug fix.",
  "docs": "Documentation-only changes.",
  "style": "Changes that do not affect the meaning of the code (white-space, formatting, etc).",
  "refactor": "A code change that neither fixes a bug nor adds a feature.",
  "perf": "A code change that improves performance.",
  "test": "Adding or correcting tests.",
  "build": "Changes that affect the build system or external dependencies.",
  "ci": "Changes to CI configuration files and scripts.",
  "chore": "Other changes that don't modify src or test files.",
  "revert": "Reverts a previous commit."
}
    print("Please choose one of the available types")
    rows = [[i, tipo, desc] for i, (tipo, desc) in enumerate(types.items(), 0)]
    print(tabulate(rows, headers=["ID","Type","Description"]))
    typeSelected = list(types.keys())[int(input("typeNumber> "))]
    return typeSelected
def boxify(text):
    lines = text.splitlines()
    width = max(len(line) for line in lines)
    top = f"╭{'─' * (width + 2)}╮"
    middle = [f"│ {line.ljust(width)} │" for line in lines]
    bottom = f"╰{'─' * (width + 2)}╯"
    return "\n".join([top] + middle + [bottom])
def make_commit(full_message: str):
    try:
        with tempfile.NamedTemporaryFile(mode="w+", delete=False) as tmp:
            tmp.write(full_message)
            tmp.flush()
            subprocess.run(["git", "commit", "-F", tmp.name], check=True)
        print("✅ Commit successfully created.")
    except subprocess.CalledProcessError as e:
        print("❌ Error during git commit.")
        print(e)
def commitMessageCreator() -> (str):
    commitMessage = ""
    scope = ""
    scopeList = checkScopeConfig(configFile)
    if len(scopeList) == 0:
        userOption = input("""[!]No scope found
[*]This is a optional field
[?]Would you like to create a new scope [y/N] """).lower()
        if userOption == "y":
            addScopeList(configFile)
            scope = chooseScope()
        else:
            print("Since you do not have any scope, this field will be left empty.")
    else:
        print(f"You currently have {len(scopeList)} scopes created")
        for i in scopeList:
            print(i)
        a = input("Would you like to add more? [y/n]").lower()
        if a == "y":
            addScopeList(configFile)
        scope = chooseScope()
    typeSelected = typeSelector()
    emoji = gitmojis()
    smessage = input("Short Message> ")
    
    body = multiline_input("Write your commit message (Enter for new line, ESC+Enter to submit):\n")

    commitMessage += f"{typeSelected}{f'({scope})' if scope else ''}: {emoji}{smessage}\n\n{body}"
    
    print("Commit Message generated")

    print(boxify(commitMessage))

    b = input("Would you like to change something? [y/n]").lower()
    if b == "y":
        commitMessageCreator()
    else:
        make_commit(commitMessage)

