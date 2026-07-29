import sys
import traceback
from datetime import datetime

from core.config import DEBUG_MODE

RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
MAGENTA = "\033[95m"
CYAN = "\033[96m"
WHITE = "\033[97m"


def _timestamp():
    return datetime.now().strftime("%H:%M:%S")


def info(message):
    print(f"{DIM}{_timestamp()}{RESET} {CYAN}[INFO]{RESET} {message}")


def warn(message):
    print(f"{DIM}{_timestamp()}{RESET} {YELLOW}[WARN]{RESET} {message}")


def error(message):
    print(f"{DIM}{_timestamp()}{RESET} {RED}[ERROR]{RESET} {message}")


def debug(message):
    if DEBUG_MODE:
        print(f"{DIM}{_timestamp()}{RESET} {MAGENTA}[DEBUG]{RESET} {DIM}{message}{RESET}")
