import os
import re
import getpass
import shutil

from avalon import io, api, lib


def get_regex_files(items):
    """Traverse the pattern items to find files with regex expressions.
    Usage:
        >>> items = [
                "C:\\",
                "Program Files",
                "djv-[0-9].[0-9].[0-9]-Windows-64",
                "bin",
                "djv_view.exe"
            ]
        >>> get_regex_files(items)
        [
            "C:\\Program Files\\djv-1.1.0-Windows-64\\bin\\djv_view.exe",
            "C:\\Program Files\\djv-1.0.0-Windows-64\\bin\\djv_view.exe"
        ]
    """
    # Find files from patterns
    files = []
    for root, dirnames, filenames in os.walk(items[0], topdown=True):

        level_items = root.split(os.sep)
        # Remove blank levels like "C:\" which returns two levels.
        for item in level_items:
            if not item:
                del level_items[level_items.index(item)]

        level = len(level_items)
        # Match whole, not partial string.
        pattern = "^" + items[level] + "$"

        # Do not search invalid directories.
        for i in reversed(range(len(dirnames))):
            if not re.match(pattern, dirnames[i]):
                del dirnames[i]

        # Collect all valid file paths
        for f in filenames:
            if re.match(pattern, f):
                files.append(os.path.join(root, f))

    return files


class Application(api.Action):

    executable = None
    args = []

    def is_compatible(self, session):
        if self.executable is None:
            return False

        required = ["AVALON_PROJECTS",
                    "AVALON_PROJECT",
                    "AVALON_SILO",
                    "AVALON_ASSET",
                    "AVALON_TASK"]
        missing = [x for x in required if x not in session]
        if missing:
            self.log.debug("Missing keys: %s" % (missing,))
            return False

        # Find patterns in project config.
        project = io.find_one({"type": "project"})
        patterns = []
        for app in project["config"]["apps"]:
            if "regex" in app:
                patterns.append(app["regex"])

        if not patterns:
            return False

        # If a pattern find a match in the executable path, display the action.
        for pattern in patterns:
            if re.findall(pattern, self.executable):
                return True

    def get_workdir(self, session):
        project = io.find_one({"type": "project"})
        template = project["config"]["template"]["work"]
        return template.format(
            **{
                "root": session["AVALON_PROJECTS"],
                "project": session["AVALON_PROJECT"],
                "silo": session["AVALON_SILO"],
                "asset": session["AVALON_ASSET"],
                "task": session["AVALON_TASK"],
                "app": session["AVALON_APP"],
                "user": session.get("AVALON_USER", getpass.getuser())
            }
        )

    def initialize(self, environment):
        """Initialize work directory"""

        if not os.path.exists(environment["AVALON_WORKDIR"]):
            os.makedirs(environment["AVALON_WORKDIR"])

    def environ(self, session):
        """Build application environment"""

        env = os.environ.copy()
        return env

    def launch(self, environment):
        return lib.launch(
            executable=self.executable,
            args=self.args,
            environment=environment,
            cwd=environment["AVALON_WORKDIR"]
        )

    def process(self, session, **kwargs):
        """Process the full Application action"""

        environment = self.environ(session)

        if kwargs.get("initialize", True):
            self.initialize(environment)

        if kwargs.get("launch", True):
            return self.launch(environment)


class Nuke(Application):

    color = "yellow"

    def environ(self, session):
        """Build application environment"""

        session["AVALON_APP"] = "nuke"

        env = os.environ.copy()
        env["AVALON_WORKDIR"] = self.get_workdir(session)
        return env


class Maya(Application):
    """Maya Action
    """

    color = "#4ae8dd"

    def environ(self, session):
        """Build application environment"""

        session["AVALON_APP"] = "maya"

        env = os.environ.copy()
        env["AVALON_WORKDIR"] = self.get_workdir(session)

        env["MAYA_DISABLE_CLIC_IPM"] = "Yes"  # Disable the AdSSO process
        env["MAYA_DISABLE_CIP"] = "Yes"  # Shorten time to boot
        env["MAYA_DISABLE_CER"] = "Yes"
        env["PYMEL_SKIP_MEL_INIT"] = "Yes"
        env["LC_ALL"] = "C"  # Mute color management warnings
        env["PYTHONPATH"] += os.pathsep + os.path.abspath(
            os.path.join(api.__file__, "..", "..", "setup", "maya")
        )

        return env

    def initialize(self, environment):
        """Initialize work directory"""

        if not os.path.exists(environment["AVALON_WORKDIR"]):
            os.makedirs(environment["AVALON_WORKDIR"])

        # Create default directories
        dirs = ["scenes", "data", "renderData/shaders", "images"]
        for dir in dirs:
            path = os.path.join(environment["AVALON_WORKDIR"], dir)
            if not os.path.exists(path):
                os.makedirs(path)

        # Create workspace file
        shutil.copy(
            os.path.abspath(
                os.path.join(api.__file__, "..", "..", "res", "workspace.mel")
            ),
            os.path.join(environment["AVALON_WORKDIR"], "workspace.mel")
        )


def register():
    # Register all available Nuke applications.
    pattern_items = [
        "C:\\",
        "Program Files",
        r"Nuke[0-9]+\.[0-9]v[0-9]",
        r"Nuke[0-9]+\.[0-9]\.exe",
    ]
    paths = get_regex_files(pattern_items)

    for path in paths:
        name = re.findall(r"Nuke[0-9]+\.[0-9]v[0-9]", path)[0]

        # Nuke
        application_name = name.replace("Nuke", "Nuke\n")
        class_obj = type(
            application_name,
            (Nuke,),
            {
                "name": application_name,
                "executable": path
            }
        )
        api.register_plugin(api.Action, class_obj)

        # NukeX
        application_name = name.replace("Nuke", "NukeX\n")
        class_obj = type(
            application_name,
            (Nuke,),
            {
                "name": application_name,
                "executable": path,
                "args": ["--nukex"]
            }
        )
        api.register_plugin(api.Action, class_obj)

        # NukeAssist
        application_name = name.replace("Nuke", "NukeAssist\n")
        class_obj = type(
            application_name,
            (Nuke,),
            {
                "name": application_name,
                "executable": path,
                "args": ["--nukeassist"]
            }
        )
        api.register_plugin(api.Action, class_obj)

        # Hiero
        application_name = name.replace("Nuke", "Hiero\n")
        class_obj = type(
            application_name,
            (Nuke,),
            {
                "name": application_name,
                "executable": path,
                "args": ["--hiero"]
            }
        )
        api.register_plugin(api.Action, class_obj)

        # HieroPlayer
        application_name = name.replace("Nuke", "HieroPlayer\n")
        class_obj = type(
            application_name,
            (Nuke,),
            {
                "name": application_name,
                "executable": path,
                "args": ["--player"]
            }
        )
        api.register_plugin(api.Action, class_obj)

        # NukeStudio
        application_name = name.replace("Nuke", "NukeStudio\n")
        class_obj = type(
            application_name,
            (Nuke,),
            {
                "name": application_name,
                "executable": path,
                "args": ["--studio"]
            }
        )
        api.register_plugin(api.Action, class_obj)

    # Register all available Maya applications.
    pattern_items = [
        "C:\\",
        "Program Files",
        "Autodesk",
        r"Maya[0-9]{4}",
        "bin",
        "maya.exe"
    ]
    paths = get_regex_files(pattern_items)

    for path in paths:
        name = re.findall(r"Maya[0-9]{4}", path)[0].replace("Maya", "Maya\n")
        class_obj = type(
            name,
            (Maya,),
            {
                "name": name,
                "executable": path
            }
        )
        api.register_plugin(api.Action, class_obj)
