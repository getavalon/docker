import os

import subprocess
import pymongo


def test_drop():
    """Dropping database works."""
    subprocess.call(["avalon", "--import", "batman"], shell=True)
    subprocess.call(["avalon", "--drop", "batman"], shell=True)

    client = pymongo.MongoClient(os.environ["AVALON_MONGO"])
    db = client["avalon"]
    msg = "Dropping project \"batman\" did not work."
    assert "batman" not in db.collection_names(), msg
