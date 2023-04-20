switches = {
    "--auth-manager": "Launches the FlexMusic server authentication manager",
    "--debug": "Launch the FlexMusic server in debug mode",
    "--help": "Display this help message",
    "--version": "Display the FlexMusic server version"
}

def help(compat_signature: tuple[str, int, int, int]) -> int:
    print("")
    print(f"{compat_signature[0]} v{compat_signature[1]}.{compat_signature[2]}.{compat_signature[3]}")
    print("Supported options: ")
    print("")
    print("\n".join([str(key.ljust(max([len(key) for key in switches.keys()])) + " " + value) for key, value in switches.items()]))
    print("")
    print("Please note: options do not stack and are loaded alphabetically.")
    print("For further help, please visit https://github.com/89mpxf/FlexMusic.")
    print("")
    return 0