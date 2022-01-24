# umd-fcrepo-fixity

Tool to perform regular fixity checking.

## process_fixitycandidates.py Script

Reads messages from a candidate queue, and sends messages to a fixity queue.

### Configuration

Environment variables:

|Name             |Purpose                                     |Default Value            |
|-----------------|--------------------------------------------|-------------------------|
|`FIXITY_DEST`    |STOMP destination to send fixity requests to|`/queue/fixity`          |
|`CANDIDATE_DEST` |STOMP destination to read candidates from   |`/queue/fixitycandidates`|

Command-line usage:

```
usage: process_fixitycandidates.py [-h] [--age AGE] [--number NUMBER]
                                   [--server SERVER] [--timeout TIMEOUT]

optional arguments:
  -h, --help            show this help message and exit
  --age AGE, -a AGE     only process messages older than this age, expressed
                        as an ISO8601 duration. Default is 3 months ("P3M")
  --number NUMBER, -n NUMBER
                        maximum number of messages to process before exiting.
                        Default is 7000
  --server SERVER, -s SERVER
                        STOMP server IP address and port to connect to.
                        Default is "127.0.0.1:61613"
  --timeout TIMEOUT, -t TIMEOUT
                        time in seconds to wait without receiving any messages
                        before exiting. Default is 30
```

## Docker

A Docker image is available for running the "process_fixitycandidates.py"
script, to perform fixity checks.

[Dockerfile](Dockerfile)

### Building

```bash
docker build -t docker.lib.umd.edu/fcrepo-fixity .
```

### Running

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
