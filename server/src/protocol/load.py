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
            for file in listdir(dirname(abspath(__file__)) + "/commands/" + dir):
                if file != "__pycache__" and file.endswith(".py"):
                    commands[dir][file[:-3]] = getattr(__import__(f"src.protocol.commands.{dir}.{file[:-3]}", fromlist=[file[:-3]]), "main")
    return commands