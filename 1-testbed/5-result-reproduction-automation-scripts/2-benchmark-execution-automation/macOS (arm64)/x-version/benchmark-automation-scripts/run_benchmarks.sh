#!/bin/sh

./benchmarks.py --host-platform macos --benchmark jetstream2 --web-browser-containerised --container-window-manager x &&
./benchmarks.py --host-platform macos --benchmark motionmark --web-browser-containerised --container-window-manager x &&
./benchmarks.py --host-platform macos --benchmark speedometer --web-browser-containerised --container-window-manager x
