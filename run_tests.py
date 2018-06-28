import os

import nose


root = os.path.abspath(os.path.join(__file__, ".."))
os.chdir(root)

# Setup environment for executable
os.environ["PATH"] += os.pathsep + os.path.join(root, "volume")
os.environ["AVALON_MONGO"] = "mongodb://192.168.99.100:27017"
os.environ["AVALON_DEBUG"] = "True"

# Run tests
nose.main([os.path.join(root, "tests")])
