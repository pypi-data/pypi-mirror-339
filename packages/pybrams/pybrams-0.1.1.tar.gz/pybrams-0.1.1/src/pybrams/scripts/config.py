from pybrams.utils import Config
import json
import shutil


def setup_args(subparsers):
    subparser_config = subparsers.add_parser("config")
    subparser_config_subparsers = subparser_config.add_subparsers(
        dest="config_cmd", required=True
    )

    subparser_config_subparsers.add_parser("show", help="show configuration")
    subparser_config_subparsers.add_parser(
        "copy", help="copy default configuration into current directory"
    )


def run(args):
    if args.config_cmd == "show":
        print(json.dumps(Config._config, indent=4))
    elif args.config_cmd == "copy":
        shutil.copy(Config._default_config_path, Config._user_defined_config_path)
