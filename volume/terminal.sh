#!/usr/bin/env bash

if [[ -z $WORKDIR ]]; then
	pushd `dirname $0` > /dev/null
	WORKDIR=`pwd -P`
	popd > /dev/null
fi

export AVALON_MONGO=mongodb://127.0.0.1:27017
export PATH=$WORKDIR:$PATH

# Expose cross-platform libraries
export PYTHONPATH=$WORKDIR/bin/pythonpath:$PYTHONPATH

avalon --environment > tmp.sh
source tmp.sh
cat tmp.sh
rm tmp.sh
