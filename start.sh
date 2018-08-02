#!/usr/bin/env bash
docker run --name avalon-files -d --rm \
    -p 445:445 \
    avalon/files \
    -s "Avalon;/avalon;yes;yes;yes;all;none;all" \
    -u "avalon;default"
docker run --name avalon-database -d --rm \
    -v avalon-database:/data/db \
    -p 27017:27017 \
    avalon/database
docker run --name avalon-tracker -d --rm \
    -v avalon-tracker:/var/lib/postgresql \
    -v avalon-tracker:/opt/zou/zou/thumbnails \
    -p 80:80 \
    avalon/tracker
