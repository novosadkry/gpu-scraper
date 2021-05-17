from enum import Enum
from datetime import datetime

import threading

class Severity(Enum):
    INFO = '\033[96m'
    UPDATE = '\033[92m'
    REMOVE = '\033[95m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'

ENDC = '\033[0m'
BOLD = '\033[1m'
SEP = f'{ENDC}{BOLD}>>{ENDC}'

logLock = threading.Lock()

def log(severity: Severity, source, *values, separator=' '):
    COLOR = severity.value

    time = datetime.now()
    time = time.strftime("%Y-%m-%d %H:%M:%S")

    heading = \
        f"{BOLD}{time} {SEP} " \
        f"{BOLD}{COLOR}{severity.name.ljust(7)} {SEP} " \
        f"{BOLD}{COLOR}{source.ljust(16)} {SEP} {COLOR}" \

    print(heading, *values, ENDC, sep=separator)

def logc(severity: Severity, source, *values, separator=' '):
    with logLock:
        log(severity, source, *values, separator)
