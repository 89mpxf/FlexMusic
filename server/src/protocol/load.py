# Import dependencies
from importlib import import_module
from os.path import abspath, dirname, isdir
from os import listdir

@staticmethod
def load_commands() -> dict:
    commands = {}
    commands["meta"] = {}
    for dir in listdir(dirname(abspath(__file__)) + "/commands"):
        if dir != "__pycache__" and isdir(dirname(abspath(__file__)) + "/commands/" + dir):
            commands[dir] = {}
            commands["meta"][dir] = {}
            for file in listdir(dirname(abspath(__file__)) + "/commands/" + dir):
                if file != "__pycache__" and file.endswith(".py"):
                    command = __import__(f"src.protocol.commands.{dir}.{file[:-3]}", fromlist=[file[:-3]])
                    commands[dir][file[:-3]] = getattr(command, "main")
                    commands["meta"][dir][file[:-3]] = {}
                    try:
                        commands["meta"][dir][file[:-3]]["usage"] = getattr(command, "__usage")
                    except:
                        commands["meta"][dir][file[:-3]]["usage"] = ""
                    try:
                        commands["meta"][dir][file[:-3]]["help_text"] = getattr(command, "__help_text")
                    except:
                        commands["meta"][dir][file[:-3]]["help_text"] = "(No help text provided)"
    if "all" in commands:
        for mode in [mode for mode in commands if mode != "meta" and mode != "all"]:
            for command in commands["all"]:
                if command not in commands[mode]:
                    commands[mode][command] = commands["all"][command]
                    commands["meta"][mode][command] = commands["meta"]["all"][command]
    del commands["all"]
    del commands["meta"]["all"]
    return commands