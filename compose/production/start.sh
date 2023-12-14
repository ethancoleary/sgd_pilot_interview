#!/bin/bash

# Wait for postgres
wait-for-it $POSTGRES_HOST:$POSTGRES_PORT

# Start otree
otree prodserver 80

exec "$@"
