"""Console script for ccob."""

import logging
import os
import pathlib

import typer
from rich.console import Console

from ccob import __version__

app = typer.Typer()
console = Console()

logging.basicConfig(level=logging.INFO, format="[*] %(message)s")


@app.command()
def main(
    offline: bool = typer.Option(None, "--offline", help="Offline mode"),
) -> None:
    """Console script for ccob."""
    console.print(f"ccob v{__version__}")

    if offline:
        ccob_dir = pathlib.Path("~/.cookiecutters/ccob").expanduser()
        if not ccob_dir.is_dir():
            logging.error(f"{ccob_dir.parent}目录下未找到ccob, 请下载后解压到该目录")
            return
        os.system(" ".join(["uvx", "cookiecutter", "ccob"]))

    os.system(" ".join(["uvx", "cookiecutter", "https://gitee.com/gooker_young/ccob.git"]))


if __name__ == "__main__":
    app()
