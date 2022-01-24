# Fixity Image for umd-fcrepo-docker

A Docker image for running the "process_fixitycandidates.py" script, to
perform fixity checks.

[Dockerfile](Dockerfile)

To perform fixity checks, use the command:

```bash
docker run docker.lib.umd.edu/fcrepo-fixity <SCRIPT_ARGS>
```

where <SCRIPT_ARGS> are the arguments to pass to the script.

For example, when running against the Docker stack on a Mac:

```bash
docker run docker.lib.umd.edu/fcrepo-fixity --server host.docker.internal:61613
```

Multiple command line options can be provided to the script, i.e.:

```bash
docker run docker.lib.umd.edu/fcrepo-fixity --server host.docker.internal:61613 --age P6M
```
