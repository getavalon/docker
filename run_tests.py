import os
import subprocess

import nose


root = os.path.abspath(os.path.join(__file__, ".."))

# Setup environment for executable
os.environ["PATH"] += os.pathsep + os.path.join(root, "volume")

# Build docker file
subprocess.call(["docker", "build", ".", "-t", "getavalon/docker"], cwd=root)

# Run tests
nose.main(
    [os.path.abspath(os.path.join(__file__, "..", "tests"))]
)
