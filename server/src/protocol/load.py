# Import dependencies
from importlib import import_module
from os.path import abspath, dirname, isdir
from os import listdir

@staticmethod
def load_commands() -> dict:
    commands = {}
    for dir in listdir(dirname(abspath(__file__)) + "/commands"):
        if dir != "__pycache__" and isdir(dirname(abspath(__file__)) + "/commands/" + dir):
            commands[dir] = {}
            commands[dir]["meta"] = {}
            for file in listdir(dirname(abspath(__file__)) + "/commands/" + dir):
                if file != "__pycache__" and file.endswith(".py"):
                    command = __import__(f"src.protocol.commands.{dir}.{file[:-3]}", fromlist=[file[:-3]])
                    commands[dir][file[:-3]] = getattr(command, "main")
                    commands[dir]["meta"][file[:-3]] = {}
                    try:
                        commands[dir]["meta"][file[:-3]]["usage"] = getattr(command, "__usage")
                    except:
                        commands[dir]["meta"][file[:-3]]["usage"] = ""
                    try:
                        commands[dir]["meta"][file[:-3]]["help_text"] = getattr(command, "__help_text")
                    except:
                        commands[dir]["meta"][file[:-3]]["help_text"] = "(No help text provided)"
    return commands