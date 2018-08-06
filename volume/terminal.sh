#!/usr/bin/env bash

if [[ -z $WORKDIR ]]; then
	pushd `dirname $0` > /dev/null
	WORKDIR=`pwd -P`
	popd > /dev/null
fi

export PATH=$WORKDIR:$PATH

avalon --environment > tmp.sh
source tmp.sh
rm tmp.sh
