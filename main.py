import sys


def run_file(filename: str) -> None:
    print(f"run_file() ({filename})")


def run_prompt() -> None:
    print("run_prompt()")


def main():
    if len(sys.argv) > 2:
        print("Usage: python main.py <filename>")
        sys.exit(64)
    elif len(sys.argv) == 2:
        filename = sys.argv[1]
        run_file(filename)
    else:
        run_prompt()


if __name__ == "__main__":
    main()
