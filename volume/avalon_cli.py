"""Avalon Command-line Interface

This module contains a CLI towards Avalon and all of what
is bundled together in this distribution.

- https://github.com/getavalon/docker

dependencies:
    - Python 2.6+ or 3.6+
    - PyQt5

example:
    $ avalon --help

overrides:
    avalon takes into account dependencies bundled
    together with this distribution, but these can be
    overridden via environment variables.

    # Database
    - AVALON_MONGO=mongodb://localhost:27017
    - AVALON_DB=avalon

    # Dependencies
    - AVALON_PYTHONPATH=absolute/path

    # Enable additional output
    - AVALON_DEBUG=True

    # Which Avalon config to use
    - AVALON_CONFIG=polly

    # Examples repository
    - AVALON_EXAMPLES=absolute/path

"""

import os
import sys
import shutil
import tempfile
import platform
import contextlib
import subprocess
import json
import time
import datetime
import zipfile
import importlib

REPO_DIR = os.path.dirname(os.path.abspath(__file__))
AVALON_DEBUG = bool(os.getenv("AVALON_DEBUG"))

init = """\
from avalon import api, shell
api.install(shell)
"""


@contextlib.contextmanager
def install():
    tempdir = tempfile.mkdtemp()
    usercustomize = os.path.join(tempdir, "usercustomize.py")

    with open(usercustomize, "w") as f:
        f.write(init)

    os.environ["PYTHONVERBOSE"] = "True"
    os.environ["PYTHONPATH"] = os.pathsep.join([
        tempdir, os.environ["PYTHONPATH"]
    ])

    try:
        yield
    finally:
        shutil.rmtree(tempdir)


def _check_pyqt5():
    try:
        __import__("PyQt5")
    except ImportError:
        print("Sorry, PyQt5 seems to be missing from your system.")
        sys.exit(1)


def _install(root=None):
    for key, value in get_environment(root).items():
        os.environ[key] = value

    config = os.environ["AVALON_CONFIG"]
    if subprocess.call([sys.executable, "-c", "import %s" % config]) != 0:
        print("ERROR: config not found, check your PYTHONPATH.")
        sys.exit(1)


def get_environment(root):
    environment = {}

    # Copy AVALON_PYTHONPATH to PYTHONPATH
    environment["PYTHONPATH"] = os.environ.get("AVALON_PYTHONPATH", "")

    # Need to add all paths from PYTHONPATH to sys.path for import testing
    for path in environment["PYTHONPATH"].split(os.pathsep):
        sys.path.append(path)

    # Adding dependencies from submodules if missing
    dependencies = [
        ("pyblish", "pyblish-base"),
        ("pyblish_qml", "pyblish-qml"),
        ("avalon", "avalon-core"),
        ("launcher", "avalon-launcher"),
        ("gazu", "cgwire-gazu")
    ]
    for dependency, name in dependencies:
        try:
            importlib.import_module(dependency)
        except ImportError:
            environment["PYTHONPATH"] += (
                os.pathsep + os.path.join(REPO_DIR, "git", name)
            )

    environment["PATH"] = os.pathsep.join([
        # Expose "avalon", overriding existing
        os.path.join(REPO_DIR),

        os.environ["PATH"],

        # Add generic binaries
        os.path.join(REPO_DIR, "bin"),

        # Add OS-level dependencies
        os.path.join(REPO_DIR, "bin", platform.system().lower()),
    ])

    # Third-party dependencies for Avalon
    path = os.path.join(REPO_DIR, "bin", "pythonpath")
    environment["PYTHONPATH"] += os.pathsep + path

    # Override default configuration by setting this value.
    if "AVALON_CONFIG" not in os.environ:
        environment["AVALON_CONFIG"] = "polly"
        environment["PYTHONPATH"] += (
            os.pathsep + os.path.join(REPO_DIR, "git", "mindbender-config")
        )

    if root is not None:
        environment["AVALON_PROJECTS"] = root
    else:
        try:
            root = os.environ["AVALON_PROJECTS"]
        except KeyError:
            root = os.path.join(
                os.getenv(
                    "AVALON_EXAMPLES",
                    os.path.join(
                        os.path.dirname(os.path.abspath(__file__)),
                        "git",
                        "avalon-examples"
                    )
                ),
                "projects"
            )
            environment["AVALON_PROJECTS"] = root

    try:
        config = os.environ["AVALON_CONFIG"]
    except KeyError:
        config = "polly"
        environment["AVALON_CONFIG"] = config

    # AVALON_MONGO
    path = "mongodb://127.0.0.1:27017"
    if platform.system().lower() == "windows":
        path = "mongodb://192.168.99.100:27017"

    environment["AVALON_MONGO"] = os.environ.get("AVALON_MONGO", path)

    return environment


def forward(args, silent=False, cwd=None):
    """Pass `args` to the Avalon CLI, within the Avalon Setup environment

    Arguments:
        args (list): Command-line arguments to run
            within the active environment

    """

    if AVALON_DEBUG:
        print("avalon.py: Forwarding '%s'.." % " ".join(args))

    popen = subprocess.Popen(
        args,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True,
        bufsize=1,
        cwd=cwd
    )

    # Blocks until finished
    while True:
        line = popen.stdout.readline()
        if line != '':
            if not silent or AVALON_DEBUG:
                sys.stdout.write(line)
        else:
            break

    if AVALON_DEBUG:
        print("avalon.py: Finishing up..")

    popen.wait()
    return popen.returncode


def update(cd):
    """Update Avalon to the latest version"""

    script = (
        # Discard any ad-hoc changes
        ("Resetting..", ["git", "reset", "--hard"]),
        ("Downloading..", ["git", "pull", "origin", "master"]),

        # In case there are new submodules since last pull
        ("Looking for submodules..", ["git", "submodule", "init"]),

        ("Updating submodules..",
            ["git", "submodule", "update", "--recursive"]),
    )

    for message, args in script:
        print(message)
        returncode = forward(args, silent=True, cwd=cd)
        if returncode != 0:
            sys.stderr.write("Could not update, try running "
                             "it again with AVALON_DEBUG=True\n")
            return returncode

    print("All done")


def backup(dst=None):
    """Outputs a zip file of the data in all the projects."""
    import pymongo
    from bson import json_util

    directory = tempfile.mkdtemp()

    timestamp = datetime.datetime.fromtimestamp(time.time()).strftime(
        "%Y%m%d%H%M%S"
    )

    # Collect all projects data in Mongo
    client = pymongo.MongoClient(os.environ["AVALON_MONGO"])
    db = client["avalon"]

    for name in db.collection_names():
        filename = "{0}_{1}.json".format(name, timestamp)

        with open(os.path.join(directory, filename), "w") as f:
            project_data = db[name].find()
            for data in json.loads(json_util.dumps(project_data)):
                f.write(json.dumps(data) + "\n")

    # Collect all data in zip file
    dst = dst or "Avalon_{0}".format(timestamp)
    dst = dst.rsplit(".zip", 1)[0]
    zip_path = os.path.join(os.getcwd(), dst)
    shutil.make_archive(zip_path, "zip", directory)

    # Clean up
    shutil.rmtree(directory)


def drop(db):
    import pymongo

    client = pymongo.MongoClient(os.environ["AVALON_MONGO"])
    client["avalon"][db].drop()
    print("Successfully dropped %s" % db)


def restore(zip_path):
    """Restores data from backups.

    Arguments:
        path (str): Path to backup zip files.

    """
    import pymongo
    from bson import json_util

    directory = tempfile.mkdtemp()

    # Unzip backup
    zip_ref = zipfile.ZipFile(zip_path, "r")
    zip_ref.extractall(directory)
    zip_ref.close()

    # Insert data from json seralized projects
    for f in os.listdir(directory):
        file_path = os.path.join(directory, f)
        project_data = []
        project_name = ""
        with open(file_path) as file_data:
            for line in file_data:
                data = json_util.loads(line)
                if "type" in data and data["type"] == "project":
                    project_name = data["name"]
                project_data.append(data)

        client = pymongo.MongoClient(os.environ["AVALON_MONGO"])
        db = client["avalon"]
        project = db[project_name]
        project.insert_many(project_data).inserted_ids

    # Clean up
    shutil.rmtree(directory)


def main():
    import argparse

    parser = argparse.ArgumentParser(usage=__doc__)
    parser.add_argument("--root", help="Projects directory")
    parser.add_argument("--import", dest="import_", action="store_true",
                        help="Import an example project into the database")
    parser.add_argument("--export", action="store_true",
                        help="Export a project from the database")
    parser.add_argument("--build", action="store_true",
                        help="Build one of the bundled example projects")
    parser.add_argument("--update", action="store_true",
                        help="Update Avalon Setup to the latest version")
    parser.add_argument("--init", action="store_true",
                        help="Establish a new project in the "
                             "current working directory")
    parser.add_argument("--load", nargs="?", default=False,
                        help="Load project at the current working directory")
    parser.add_argument("--save", action="store_true",
                        help="Save project from the current working directory")
    parser.add_argument("--ls", action="store_true",
                        help="List all projects in database")
    parser.add_argument("--forward",
                        help="Run arbitrary command from setup environment")
    parser.add_argument("--publish", action="store_true",
                        help="Publish from current working directory, "
                             "or supplied --root")
    parser.add_argument("--backup", nargs='?',
                        help="Create a backup in current working directory.")
    parser.add_argument("--restore",
                        help="Restore a project or a folder or projects.")
    parser.add_argument("--drop", help="Delete database")
    parser.add_argument(
        "--environment",
        action="store_true",
        help="Print Avalon environment command."
    )

    kwargs, args = parser.parse_known_args()

    _install(root=kwargs.root)

    cd = os.path.dirname(os.path.abspath(__file__))
    examplesdir = os.getenv("AVALON_EXAMPLES",
                            os.path.join(cd, "git", "avalon-examples"))

    if kwargs.import_:
        fname = os.path.join(examplesdir, "import.py")
        returncode = forward(
            [sys.executable, "-u", fname] + args)

    elif kwargs.export:
        fname = os.path.join(examplesdir, "export.py")
        returncode = forward(
            [sys.executable, "-u", fname] + args)

    elif kwargs.build:
        fname = os.path.join(examplesdir, "build.py")
        returncode = forward(
            [sys.executable, "-u", fname] + args)

    elif kwargs.init:
        returncode = forward([
            sys.executable, "-u", "-m",
            "avalon.inventory", "--init"])

    elif kwargs.load:
        returncode = forward(
            [
                sys.executable,
                "-u",
                "-m",
                "avalon.inventory",
                "--load",
                kwargs.load
            ]
        )

    elif kwargs.load is None:
        returncode = forward(
            [sys.executable, "-u", "-m", "avalon.inventory", "--load"]
        )

    elif kwargs.save:
        returncode = forward([
            sys.executable, "-u", "-m",
            "avalon.inventory", "--save"])

    elif kwargs.ls:
        returncode = forward([
            sys.executable, "-u", "-m",
            "avalon.inventory", "--ls"])

    elif kwargs.update:
        returncode = update(cd)

    elif kwargs.forward:
        returncode = forward(kwargs.forward.split())

    elif kwargs.publish:
        os.environ["PYBLISH_HOSTS"] = "shell"

        with install():
            returncode = forward([
                sys.executable, "-u", "-m", "pyblish", "gui"
            ] + args, silent=True)

    elif kwargs.backup:
        returncode = 0
        try:
            backup(kwargs.backup)
        except Exception:
            raise

    elif kwargs.restore:
        returncode = 0
        try:
            restore(kwargs.restore)
        except Exception:
            raise

    elif kwargs.drop:
        returncode = 0
        try:
            drop(kwargs.drop)
        except Exception:
            raise

    elif kwargs.environment:
        returncode = 0
        try:
            cmd = ""
            environment = get_environment(kwargs.root)
            environment["AVALON_PYTHONPATH"] = environment["PYTHONPATH"]
            for key, value in environment.items():
                if platform.system().lower() == "windows":
                    cmd += r"set {0}={1}& ".format(key, value)
                else:
                    cmd += r"export {0}={1} && ".format(key, value)

            # Trim command
            if platform.system().lower() == "windows":
                cmd = cmd[:-2]
            else:
                cmd = cmd[:-4]

            print(cmd)
        except Exception:
            raise

    else:
        _check_pyqt5()
        root = os.environ["AVALON_PROJECTS"]
        returncode = forward([
            sys.executable, "-u", "-m", "launcher", "--root", root
        ] + args)

    sys.exit(returncode)


if __name__ == '__main__':
    main()
