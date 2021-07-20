# Container image that runs your code
FROM tjozsa/conduit

# Copies your code file from your action repository to the filesystem path `/` of the container
COPY entrypoint.sh /usr/bin/bash


