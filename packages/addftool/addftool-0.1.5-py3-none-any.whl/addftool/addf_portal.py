import argparse
from addftool.process import add_killer_args, killer_main


def get_args():
    parser = argparse.ArgumentParser(description="Addf's tool")

    subparsers = parser.add_subparsers(dest='command', help='Sub-command help')
    add_killer_args(subparsers)

    return parser.parse_args()


def main():
    args = get_args()
    if args.command == "kill":
        killer_main(args)
    else:
        print("Unknown command: ", args.command)


if __name__ == "__main__":
    main()
