import os
import subprocess

import nose


root = os.path.abspath(os.path.join(__file__, ".."))

# Setup environment for executable
os.environ["PATH"] += os.pathsep + os.path.join(root, "volume")
os.environ["AVALON_MONGO"] = "mongodb://192.168.99.100:27017"

# Build and run docker file
subprocess.call(["docker", "kill", "avalon"])
subprocess.call(["docker", "build", ".", "-t", "getavalon/docker"], cwd=root)
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

# Run tests
nose.main(
    [os.path.abspath(os.path.join(__file__, "..", "tests"))]
)
