# Import dependencies
from time import process_time
from datetime import datetime

def log(source: str, message: str):
    print(f"[{process_time():0>12.4f}][{source}] {message}")

def print_with_time(message: str):
    print(f"[{datetime.now().strftime('%a %d, %H:%M:%S')}] {message}")