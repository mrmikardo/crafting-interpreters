import sys

# Lifted from sysexits.h
EX_USAGE = 64


def run_file(path: str) -> None:
    pass


def run_prompt() -> None:
    pass

def main() -> None:
    if len(sys.argv) > 1:
        print('Usage: plox [script]')
        sys.exit(EX_USAGE)
    elif len(sys.argv) == 1:
        run_file(sys.argv[0])
    else:
        run_prompt()


        
