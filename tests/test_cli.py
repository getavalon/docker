import os
import subprocess

import pymongo


def test_backup_restore():
    """Backup and restore works"""

    # Populate database
    result = subprocess.call(["avalon", "--import", "batman"], shell=True)
    assert result == 0, "Importing failed"

    # Backup
    result = subprocess.call(["avalon", "--backup"], shell=True)
    assert result == 0, "Backup failed"

    # Get backup
    backup_path = ""
    for f in os.listdir(os.getcwd()):
        if f.endswith(".zip"):
            backup_path = os.path.join(os.getcwd(), f)

    # Wipe database
    client = pymongo.MongoClient(os.environ["AVALON_MONGO"])
    client.drop_database("avalon")

    # Restore database
    result = subprocess.call(["avalon", "--restore", backup_path], shell=True)
    assert result == 0, "Restoring failed"

    # Clean up
    client = pymongo.MongoClient(os.environ["AVALON_MONGO"])
    client.drop_database("avalon")
    os.remove(backup_path)
