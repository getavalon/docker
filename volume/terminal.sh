#!/usr/bin/env bash

if [[ -z $WORKDIR ]]; then
	pushd `dirname $0` > /dev/null
	WORKDIR=`pwd -P`
	popd > /dev/null
fi

export AVALON_MONGO=mongodb://127.0.0.1:27017
export AVALON_CORE=$WORKDIR/git/avalon-core
export AVALON_LAUNCHER=$WORKDIR/git/avalon-launcher
export PATH=$WORKDIR:$PATH

# Expose Python libraries
export PYTHONPATH=$AVALON_CORE
export PYTHONPATH=$AVALON_LAUNCHER:$PYTHONPATH
export PYTHONPATH=$WORKDIR/git/mindbender-config:$PYTHONPATH
export PYTHONPATH=$WORKDIR/git/pyblish-base:$PYTHONPATH
export PYTHONPATH=$WORKDIR/git/pyblish-qml:$PYTHONPATH
export PYTHONPATH=$WORKDIR/git/cgwire-gazu:$PYTHONPATH

# Expose cross-platform libraries
export PYTHONPATH=$WORKDIR/bin/pythonpath:$PYTHONPATH
