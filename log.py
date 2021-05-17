from enum import Enum
import threading

class Severity(Enum):
    INFO = '\033[96m'
    UPDATE = '\033[92m'
    DELETE = '\033[95m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'

ENDC = '\033[0m'
BOLD = '\033[1m'

logLock = threading.Lock()

def log(severity: Severity, source, *values, separator=' '):
    heading = f"{BOLD}{severity.value}({severity.name}){ENDC}{severity.value} {source.ljust(16)} : "
    print(heading, *values, ENDC, sep=separator)

def logc(severity: Severity, source, *values, separator=' '):
    with logLock:
        log(severity, source, *values, separator)
