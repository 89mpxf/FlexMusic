from platform import system

def splash(config: dict, compat_signature: tuple[str, int, int, int], debug: bool = False):
    splash_width = 50
    print(f"#{'':#^50}#")
    print(f"#{'': ^50}#")
    print(f"#{'FlexMusic Media Server': ^50}#")
    print(f"#{f'{compat_signature[0]} ({compat_signature[1]}.{compat_signature[2]}.{compat_signature[3]})': ^50}#")
    print(f"#{'': ^50}#")
    print(f"#{'Now listening for connections on:': ^50}#")
    print(f"#{str(config['host'] + ':' + str(config['port'])): ^50}#")
    print(f"#{'': ^50}#")
    print(f"#{'https://github.com/89mpxf/FlexMusic': ^50}#")
    print(f"#{'': ^50}#")
    print(f"#{'':#^50}#")
