import os
import subprocess


def test_backup_restore():
    """Backup and restore works"""
    subprocess.call(
        [
            "docker", "run", "-d", "--rm",
            "--name", "avalon",
            "-p", "27017:27017",
            "-p", "445:445",
            "-p", "139:139",
            "getavalon/docker"
        ],
        shell=True
    )

    # Populate database
    subprocess.call(["avalon", "--import", "batman"], shell=True)

    # Backup
    result = subprocess.call(["avalon", "--backup"], shell=True)
    assert result == 0

    # Get backup
    backup_path = ""
    for f in os.listdir(os.getcwd()):
        if f.endswith(".zip"):
            backup_path = os.path.join(os.getcwd(), f)

    # Restore
    subprocess.call(["docker", "kill", "avalon"], shell=True)

    subprocess.call(
        [
            "docker", "run", "-d", "--rm",
            "--name", "avalon",
            "-p", "27017:27017",
            "-p", "445:445",
            "-p", "139:139",
            "getavalon/docker"
        ],
        shell=True
    )

    result = subprocess.call(["avalon", "--restore", backup_path], shell=True)
    assert result == 0
