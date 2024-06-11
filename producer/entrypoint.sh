#!/bin/bash

set -ex

# Wait until Kafka comes online
sleep 5

python /producer-app/main.py