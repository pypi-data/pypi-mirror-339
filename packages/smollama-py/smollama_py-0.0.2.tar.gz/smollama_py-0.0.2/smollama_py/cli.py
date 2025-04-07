import argparse
import eel
import sys
import os

public = os.path.join(os.path.dirname(__file__), "public")
# Initialize the Eel app
eel.init(public)


def create_parser():
    parser = argparse.ArgumentParser(description="A python app to serve smOllama")
    parser.add_argument(
        "-m", "--mode", choices=["chrome", "electron", "edge", "msie"], default="chrome"
    )
    return parser


def cli():
    "A python app to serve smOllama"
    parser = create_parser()
    args = parser.parse_args()
    mycommand(args)


def close(a, b):
    sys.exit(0)


def mycommand(args):
    try:
        eel.start("index.html", size=(800, 600), close_callback=close)
    except KeyboardInterrupt:
        sys.exit(0)
