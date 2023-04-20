import platform
from platform import system, release, python_version_tuple, python_implementation, python_compiler

def box(lines: list[str]) -> list[str]:
    _ret = []
    width = max([len(line) for line in lines])
    for line in range(len(lines) + 4):
        if line in [0, len(lines) + 3]:
            _ret.append("#" * int(width+4))
        elif line in [1, len(lines) + 2]:
            _ret.append("#" + " " * int(width+2) + "#")
        else:
            _ret.append("# " + lines[line-2] + " " * int(width - len(lines[line-2])) + " #")
    return _ret

def splash(config: dict, compat_signature: tuple[str, int, int, int], debug: bool = False):
    lines = []
    _pyver = python_version_tuple()
    lines.append(f"{compat_signature[0]} (v{compat_signature[1]}.{compat_signature[2]}.{compat_signature[3]})")
    lines.append(f"Now listening for connections on: {config['host']}:{config['port']}")
    lines.append("")
    lines.append(f"Press ENTER for realtime server information.")
    lines.append(f"Press CTRL+C to exit.")
    lines.append("")
    lines.append(f"Operating System: {system()} {release()}")
    lines.append(f"Python Version: {python_implementation()} {_pyver[0]}.{_pyver[1]}.{_pyver[2]} ({python_compiler()})")
    lines.append("")
    lines.append("https://github.com/89mpxf/FlexMusic")
    lines = box(lines)
    print(*lines, sep='\n')
