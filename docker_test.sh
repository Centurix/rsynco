#!/bin/bash
docker run -it --volume=/home/chris/Projects/PycharmProjects/rsynco:/localDebugRepo --workdir="/localDebugRepo" --memory=4g --memory-swap=4g --memory-swappiness=0 --entrypoint=/bin/bash python:3.5.1
