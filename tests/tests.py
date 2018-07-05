import os

import subprocess
from avalon import io


def test_drop():
    """Dropping database works."""
    subprocess.call(["avalon", "--import", "batman"], shell=True)
    subprocess.call(["avalon", "--drop", "batman"], shell=True)

    os.environ["AVALON_PROJECT"] = "batman"
    io.install()
    msg = "Dropping project \"batman\" did not work."
    assert io.find_one({"type": "project", "name": "batman"}) is None, msg
