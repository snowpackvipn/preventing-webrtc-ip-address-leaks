#!/bin/sh

./benchmarks.py --host-platform windows --benchmark jetstream2 --web-browser-containerised --container-window-manager x &&
./benchmarks.py --host-platform windows --benchmark motionmark --web-browser-containerised --container-window-manager x &&
./benchmarks.py --host-platform windows --benchmark speedometer --web-browser-containerised --container-window-manager x