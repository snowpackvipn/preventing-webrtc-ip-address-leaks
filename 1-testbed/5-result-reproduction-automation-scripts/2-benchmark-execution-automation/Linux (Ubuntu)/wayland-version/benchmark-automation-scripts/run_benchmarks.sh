#!/bin/sh

./benchmarks.py --host-platform linux --linux-host-window-manager wayland --benchmark jetstream2 --web-browser-containerised --container-window-manager wayland &&
./benchmarks.py --host-platform linux --linux-host-window-manager wayland --benchmark motionmark --web-browser-containerised --container-window-manager wayland &&
./benchmarks.py --host-platform linux --linux-host-window-manager wayland --benchmark speedometer --web-browser-containerised --container-window-manager wayland
