#!/usr/bin/env bash
pushd `dirname $0` > /dev/null
DIRNAME=`pwd -P`
popd > /dev/null

export AVALON_MONGO=mongodb://127.0.0.1:27017
export PATH=$DIRNAME:$PATH

# Expose Python libraries
export PYTHONPATH=$DIRNAME/git/avalon-core
export PYTHONPATH=$DIRNAME/git/avalon-launcher:$PYTHONPATH
export PYTHONPATH=$DIRNAME/git/mindbender-config:$PYTHONPATH
export PYTHONPATH=$DIRNAME/git/pyblish-base:$PYTHONPATH
export PYTHONPATH=$DIRNAME/git/pyblish-qml:$PYTHONPATH
export PYTHONPATH=$DIRNAME/git/cgwire-gazu:$PYTHONPATH

# Expose cross-platform libraries
export PYTHONPATH=$DIRNAME/bin/pythonpath:$PYTHONPATH
