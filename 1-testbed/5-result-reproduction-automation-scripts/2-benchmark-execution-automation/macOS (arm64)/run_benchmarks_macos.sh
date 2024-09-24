#!/bin/sh

cd .. &&

python ./benchmarks.py --host-platform macos --benchmark jetstream2 &&
python ./benchmarks.py --host-platform macos --benchmark motionmark &&
python ./benchmarks.py --host-platform macos --benchmark speedometer &&

sleep 15 &&

open -a Docker

sleep 60 &&

cd "../macOS (arm64)/x-version" &&

docker compose -f ./docker-compose-firefox-x-macos-automated-benchmarks.yml up &&

sleep 15 &&

docker compose -f ./docker-compose-firefox-x-macos-automated-benchmarks.yml down
