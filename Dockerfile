FROM ubuntu:17.10

COPY volume /avalon

# Expose avalon to external containers
VOLUME /avalon
