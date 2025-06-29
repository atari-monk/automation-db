from pathlib import Path
import argparse
from automation_db.automation_service import run_automation


def get_path_interactively():
    while True:
        path_input = input("Enter path (or 'q' to quit): ").strip()
        if path_input.lower() == 'q':
            exit(0)
        path = Path(path_input)
        if path.exists():
            return path
        print(f"Path '{path}' doesn't exist")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', type=str, help='Path for automation service')
    args = parser.parse_args()

    if args.path:
        path = Path(args.path)
        if not path.exists():
            print(f"Path '{path}' not found")
            path = get_path_interactively()
    else:
        path = get_path_interactively()

    print(f"Using path: {path}")
    run_automation(path)


if __name__ == '__main__':
    main()