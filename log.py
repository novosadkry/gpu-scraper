from enum import Enum

class Severity(Enum):
    INFO = '\033[96m'
    UPDATE = '\033[92m'
    DELETE = '\033[95m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'

ENDC = '\033[0m'
BOLD = '\033[1m'

def log(severity: Severity, *values, separator=' '):
    heading = f"{BOLD}{severity.value}({severity.name}){ENDC}{severity.value}"
    print(heading, *values, ENDC, sep=separator)