import os.path
import argparse
from configparser import ConfigParser


def get_source_file_paths(root_path, file_suffix=".java") -> str:
    file_paths = []
    for root, dirs, files in os.walk(root_path):
        file_paths += [os.path.join(root, file) for file in files if file.endswith(file_suffix)]

    return "\n".join(file_paths)


def get_parser():
    parser = argparse.ArgumentParser(description="NoOJBot, a code analyze bot powered by OpenAI API")

    parser.add_argument(
        "ppath",
        type=str,
        help="the path of project",
    )

    parser.add_argument(
        "--mpath", "-m",
        type=str,
        default=None,
        help="the path of metrics report",
    )

    parser.add_argument(
        "--dbg", "-d",
        action='store_true',
    )

    parser.add_argument(
        "--mmem", "-k",
        type=int,
        nargs='?',
        default=20,
        help="set the chat turn threshold",
    )

    return parser


def set_openai_key():
    cfg = ConfigParser()
    cfg.read("config.ini")
    config = dict(cfg.items("openai"))

    os.environ["OPENAI_API_KEY"] = config["openai_key"]
