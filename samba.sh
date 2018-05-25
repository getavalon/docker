#!/usr/bin/env bash
docker run \
	-ti \
	--rm \
	-d \
	-p 139:139 \
	-p 445:445 \
	--name avalon-samba \
	--volumes-from avalon-docker \
	dperson/samba \
	    -s "Avalon;/avalon;yes;no;yes;all;none;all" \
	    -u "myuser;mypass"
