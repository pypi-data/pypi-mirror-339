import os


def add_sync_args(subparsers):
    process_killer_parser = subparsers.add_parser('sync', help='download and sync folder from master node to other nodes')

    process_killer_parser.add_argument("--from_blob_url", help="download from blob url to master node before sync", type=str, default="")
    process_killer_parser.add_argument("--sas_token", help="sas token for blob url", type=str, default="")
    process_killer_parser.add_argument("--tool", help="tool name", type=str, default="torch_nccl", choices=["torch_nccl", "rsync"])
    process_killer_parser.add_argument("--hostfile", help="host file, sync file from node-0 to others", type=str, default="")

    # distributed downloader from blob
    process_killer_parser.add_argument("--donwload_nodes", help="download nodes, default is node-0", type=int, default=1)

    process_killer_parser.add_argument("folder", nargs='?', help="the folder need to sync", type=str, default="")


def sync_main(args):
    print(args)
    exit(0)
    if args.source == "" or args.target == "":
        print("Please provide source and target folder")
        return

    # check if source is a folder
    if not os.path.isdir(args.source):
        print(f"Source {args.source} is not a folder")
        return

    # check if target is a folder
    if not os.path.isdir(args.target):
        print(f"Target {args.target} is not a folder")
        return

    # check if source and target are the same
    if os.path.abspath(args.source) == os.path.abspath(args.target):
        print(f"Source and target are the same")
        return

    # sync source to target
    command = f"rsync -avz --delete {args.source} {args.target}"
    os.system(command)
