<small><i>This README is a copy of [section 2 - Raw data on the performance evaluation of the containerised solution](../README.md#2-raw-data-on-the-performance-evaluation-of-the-containerised-solution) from the `3-raw-data/README.md` file.</i></small>

## Table of contents

[2. Raw data on the performance evaluation of the containerised solution](#2-raw-data-on-the-performance-evaluation-of-the-containerised-solution)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[2.1. Reminder about the client configurations](#21-reminder-about-the-client-configurations)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[2.2. Data organisation](#22-data-organisation)  


## 2. Raw data on the performance evaluation of the containerised solution

### 2.1. Reminder about the client configurations

Our containerised solution, initially designed for **Linux**, was later ported to **macOS** and **Windows** to demonstrate its viability on systems other than Linux. This is also why Docker was chosen, as it exists on these three operating systems.

The evaluation of the performance impact of our dockerised solution compared with running Firefox natively was carried out in these configurations:

<table>
    <tr>
        <th colspan="2" style="text-align: center;">Linux</th>
        <th colspan="2" style="text-align: center;">Windows</th>
        <th colspan="2" style="text-align: center;">macOS</th>
    </tr>
    <tr>
        <th>Machine</th>
        <td><a href="https://www.dell.com/support/manuals/en-uk/latitude-15-5520-laptop/5520_sp15_setupspecs/specifications-of-latitude-5520?guid=guid-7c9f07ce-626e-44ca-be3a-a1fb036413f9">Dell Latitude 5520 (2022)</a></td>
        <th>Machine</th>
        <td><a href="https://www.dell.com/support/manuals/en-uk/latitude-15-5520-laptop/5520_sp15_setupspecs/specifications-of-latitude-5520?guid=guid-7c9f07ce-626e-44ca-be3a-a1fb036413f9">Dell Latitude 5520 (2022)</a></td>
        <th>Machine</th>
        <td><a href="https://support.apple.com/en-gb/111869">Apple MacBook Pro (13-inch, 2022)</a></td>
    </tr>
    <tr>
        <th>CPU</th>
        <td>Intel Core i5-1145G7 @ 2.60 GHz</td>
        <th>CPU</th>
        <td>Intel Core i5-1145G7 @ 2.60 GHz</td>
        <th>CPU</th>
        <td>Apple M2</td>
    </tr>
    <tr>
        <th>RAM</th>
        <td>16 GiB</td>
        <th>RAM</th>
        <td>16 GiB</td>
        <th>RAM</th>
        <td>16 GiB</td>
    </tr>
    <tr>
        <th>GPU</th>
        <td>Intel® Iris® Xe Graphics</td>
        <th>GPU</th>
        <td>Intel® Iris® Xe Graphics</td>
        <th>GPU</th>
        <td>Apple M2</td>
    </tr>
    <tr>
        <th>Screen resolution</th>
        <td>1920x1080</td>
        <th>Screen resolution</th>
        <td>1920x1080</td>
        <th>Screen resolution</th>
        <td>2560x1600</td>
    </tr>
    <tr>
        <th>Host OS</th>
        <td>Ubuntu Desktop 22.04 LTS</td>
        <th>Host OS</th>
        <td>Windows 11 Pro 23H2</td>
        <th>Host OS</th>
        <td>macOS Sonoma 14.5</td>
    </tr>
    <tr>
        <th>Architecture</th>
        <td>x86-64</td>
        <th>Architecture</th>
        <td>x86-64</td>
        <th>Architecture</th>
        <td>arm64</td>
    </tr>
    <tr>
        <th>Native Firefox</th>
        <td>v125.0.3</td>
        <th>Native Firefox</th>
        <td>v125.0.3</td>
        <th>Native Firefox</th>
        <td>v125.0.3</td>
    </tr>
    <tr>
        <th>Docker image</th>
        <td>Ubuntu Server 22.04 LTS</td>
        <th>Docker image</th>
        <td>Ubuntu Server 22.04 LTS</td>
        <th>Docker image</th>
        <td>Ubuntu Server 22.04 LTS</td>
    </tr>
    <tr>
        <th>Docker image architecture</th>
        <td>x86-64</td>
        <th>Docker image architecture</th>
        <td>x86-64</td>
        <th>Docker image architecture</th>
        <td>arm64</td>
    </tr>
    <tr>
        <th>Containerised Firefox</th>
        <td>v125.0.3</td>
        <th>Containerised Firefox</th>
        <td>v125.0.3</td>
        <th>Containerised Firefox</th>
        <td>v125.0.3</td>
    </tr>
    <tr>
        <th>Docker Engine</th>
        <td>v26.1.4</td>
        <th rowspan="2"><a href="https://www.docker.com/products/docker-desktop/">Docker Desktop</a></th>
        <td rowspan="2">v4.30.0</td>
        <th rowspan="2"><a href="https://www.docker.com/products/docker-desktop/">Docker Desktop</a></th>
        <td rowspan="2">v4.30.0</td>
    </tr>
    <tr>
        <th>Docker Compose </th>
        <td>v2.27.1</td>
    </tr>
    <tr>
        <th>Host Wayland compositor</th>
        <td rowspan="2"><a href="https://mutter.gnome.org/">Mutter</a> v42.9</td>
        <th>Host Wayland compositor</th>
        <td rowspan="2"><a href="https://wayland.pages.freedesktop.org/weston/">Weston</a> (provided by WSLg) GitHub commit <code><a href="https://github.com/microsoft/weston-mirror/commit/f227edd681479ec3cb2290a25d84d2d3462aebfa">f227edd6</a></code>
        </td>
        <th>Host Wayland compositor</th>
        <td>N/A</td>
    </tr>
    <tr>
        <th>Host X server (X.Org/XWayland)</th>
        <th>Host X server (XWayland)</th>
        <th>Host X server (<a href="https://www.xquartz.org/">XQuartz</a>)</th>
        <td>v2.8.5</td>
    </tr>
    <tr>
        <th>Host PulseAudio server</th>
        <td>PulseAudio (on <a href="https://pipewire.org/">PipeWire</a> 0.3.48)</td>
        <th>Host <a href="https://www.freedesktop.org/wiki/Software/PulseAudio/">PulseAudio</a> server</th>
        <td>(provided by WSLg) GitHub commit <code><a href="https://github.com/microsoft/pulseaudio-mirror/commit/6f045ff0dca233a939a2aba815f84d177e294122">6f045ff0</a></code>
        </td>
        <th>Host <a href="https://www.freedesktop.org/wiki/Software/PulseAudio/">PulseAudio</a> server</th>
        <td>v17.0</td>
    </tr>
    <tr>
        <td colspan="2" rowspan="3"></td>
        <th><a href="https://learn.microsoft.com/en-gb/windows/wsl/about">WSL 2</a></th>
        <td>v2.2.4.0</td>
        <td colspan="2" rowspan="3"></td>
    </tr>
    <tr>
        <th><a href="https://github.com/microsoft/WSL2-Linux-Kernel">WSL 2 Linux Kernel</a> with camera driver support</th>
        <td>v5.15.153.1 - <a href="../../raw/main/1-testbed/3-firefox-containerised/Windows/linux-wsl-kernel-with-camera-drivers/vmlinux">Download</a></td>
    </tr>
    <tr>
        <th><a href="https://github.com/microsoft/wslg">WSLg</a></th>
        <td>v1.0.61</td>
    </tr>
</table>


## 2.2. Data organisation

Raw data are available in this folder.
