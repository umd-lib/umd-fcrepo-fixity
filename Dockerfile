# Dockerfile for the fixity checking scro[t
#
# To build:
#
# docker build -t docker.lib.umd.edu/fcrepo-fixity:<VERSION> -f Dockerfile .
#
# where <VERSION> is the Docker image version to create.

FROM python:3.14.9-slim

WORKDIR /usr/src/app

COPY process_fixitycandidates.py ./

RUN pip install --no-cache-dir --requirements-from-script process_fixitycandidates.py

ENTRYPOINT [ "python", "./process_fixitycandidates.py" ]
