#!/bin/bash
pushd `dirname $0` > /dev/null
DIRNAME=`pwd -P`
popd > /dev/null
export AVALON_MONGO=mongodb://192.168.99.100:27017
python -u $DIRNAME/avalon_cli.py $*
