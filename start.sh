#!/bin/bash
/usr/sbin/smbd -D
/usr/local/bin/docker-entrypoint.sh mongod
