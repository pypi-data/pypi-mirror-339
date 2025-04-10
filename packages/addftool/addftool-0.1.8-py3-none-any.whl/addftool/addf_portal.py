import argparse
from addftool.process import add_killer_args, killer_main
from addftool.sync import add_sync_args, sync_main
from addftool.deploy import add_deploy_args, deploy_main


def get_args():
    parser = argparse.ArgumentParser(description="Addf's tool")

    subparsers = parser.add_subparsers(dest='command', help='Sub-command help')
    add_killer_args(subparsers)
    add_sync_args(subparsers)
    add_deploy_args(subparsers)

    return parser.parse_args()


def main():
    args = get_args()
    if args.command == "kill":
        killer_main(args)
    elif args.command == "sync":
        sync_main(args)
    elif args.command == "deploy":
        deploy_main(args)
    else:
        print("Unknown command: ", args.command)


if __name__ == "__main__":
    main()
