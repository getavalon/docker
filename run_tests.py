import os
import subprocess

import pytest


# Setup environment for executable
os.environ["PATH"] += os.path.abspath(os.path.join(__file__, "..", "volume"))

# Build docker file
subprocess.call(["docker", "build", ".", "-t", "getavalon/docker"])

# Run tests
pytest.main(
    [os.path.abspath(os.path.join(__file__, "..", "tests"))]
)
