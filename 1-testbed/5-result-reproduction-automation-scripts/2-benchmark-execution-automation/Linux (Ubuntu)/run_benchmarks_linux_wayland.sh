#!/bin/sh

sudo systemctl stop docker.service &&
sudo systemctl stop docker.socket &&
sudo systemctl stop containerd.service &&

sleep 15 &&

cd .. &&

sudo -u $USER ./benchmarks.py --host-platform linux --linux-host-window-manager wayland --benchmark jetstream2 &&
sudo -u $USER ./benchmarks.py --host-platform linux --linux-host-window-manager wayland --benchmark motionmark &&
sudo -u $USER ./benchmarks.py --host-platform linux --linux-host-window-manager wayland --benchmark speedometer &&

sleep 15 &&

sudo systemctl start docker.service &&
sudo systemctl start docker.socket &&
sudo systemctl start containerd.service &&

echo "From /preventing-webrtc-ip-address-leaks/5-experiment-automation-scripts/2-automate-benchmark-execution/Linux (Ubuntu)/wayland-version, launch manually this command"
echo ""
echo "UID=\$(id -u) GID=\$(id -g) RENDER_GID=\$(getent group render | cut -d: -f3) docker compose -f ./docker-compose-firefox-wayland-linux-automated-benchmarks.yml up"
