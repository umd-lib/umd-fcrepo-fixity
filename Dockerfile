# Dockerfile for the fixity checking scro[t
#
# To build:
#
# docker build -t docker.lib.umd.edu/fcrepo-fixity:<VERSION> -f Dockerfile .
#
# where <VERSION> is the Docker image version to create.

FROM python:3.14.3-slim

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY process_fixitycandidates.py ./

ENTRYPOINT [ "python", "./process_fixitycandidates.py" ]
