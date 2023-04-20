from platform import system, release, python_version_tuple, python_implementation, python_compiler

def version(compat_signature: tuple[str, int, int, int]):
    _pyver = python_version_tuple()
    print(f"Server Version: {compat_signature[0]} (v{compat_signature[1]}.{compat_signature[2]}.{compat_signature[3]})")
    print(f"Operating System: {system()} {release()}")
    print(f"Python Version: {python_implementation()} {_pyver[0]}.{_pyver[1]}.{_pyver[2]} ({python_compiler()})")
    return 0