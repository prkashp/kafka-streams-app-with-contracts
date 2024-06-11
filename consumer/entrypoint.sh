#!/bin/bash

set -ex

# Wait until Kafka comes online
sleep 5

python consumer-app/main.py