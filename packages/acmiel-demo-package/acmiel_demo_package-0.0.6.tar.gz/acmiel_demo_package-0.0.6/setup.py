import os
import tempfile
from pathlib import Path

from setuptools import setup, find_packages


USER = os.getenv("USERNAME") or "sir"


def say_hi():
    tmpdir = Path(tempfile.gettempdir())
    hello_file = tmpdir / f"hello-{USER}.txt"
    hello_content = (
        f"Hello {USER}, thanks for attempting to install this package! 💛\n"
        "\n"
        "This is a benign example of arbitrary code execution at package install time.\n"
        "It doesn't do anything malicious, just attempts to demonstrate the concept.\n"
    )

    if not hello_file.exists():
        hello_file.write_text(hello_content + "\n")
        raise ValueError(f"There is a message for you in {hello_file} :-)")
    else:
        raise ValueError(hello_content)


if os.getenv("BUILDING_RELEASE") != "1":
    say_hi()

setup(
    name="acmiel-demo-package",
    version="0.0.6",
    long_description="Demo package to show why setup.py is scary.",
    long_description_content_type="text/x-rst",
    packages=find_packages(),
)
