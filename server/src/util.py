from time import process_time

def log(source: str, message: str):
    print(f"[{process_time():0>12.4f}][{source}] {message}")