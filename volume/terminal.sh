#!/usr/bin/env bash

if [[ -z $WORKDIR ]]; then
	pushd `dirname $0` > /dev/null
	WORKDIR=`pwd -P`
	popd > /dev/null
fi

export AVALON_MONGO=mongodb://127.0.0.1:27017
export PATH=$WORKDIR:$PATH
