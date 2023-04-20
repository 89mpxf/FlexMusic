def version(compat_signature: tuple[str, int, int, int]):
    print(f"{compat_signature[0]} (v{compat_signature[1]}.{compat_signature[2]}.{compat_signature[3]})")
    return 0