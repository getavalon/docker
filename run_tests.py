import os
import subprocess

import pytest


root = os.path.abspath(os.path.join(__file__, ".."))

# Setup environment for executable
os.environ["PATH"] += os.pathsep + os.path.join(root, "volume")

# Build docker file
subprocess.call(["docker", "build", ".", "-t", "getavalon/docker"], cwd=root)

# Run tests
pytest.main(
    [os.path.abspath(os.path.join(__file__, "..", "tests"))]
)
