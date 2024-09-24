# Evaluation

## Table of contents

[1. WebRTC IP address leakage evaluation](#1-webrtc-ip-address-leakage-evaluation)  
[2. Performance impact evaluation of the containerised solution](#2-performance-impact-evaluation-of-the-containerised-solution)  
[References](#references)


## 1. WebRTC IP address leakage evaluation

Please read the section ***IP address leakage evaluation*** of the submission.

The leak evaluation was carried out on **Linux Ubuntu 22.04 LTS**, **Microsoft Windows 11 23H2** and **macOS Sonoma 14.5**. Full details of the software and versions used in this evaluation are described in the table below:


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
        <td><a href="https://www.dell.com/support/manuals/en-uk/latitude-15-5540-laptop/latitude-5540-owners-manual/specifications-of-latitude-5540?guid=guid-7c9f07ce-626e-44ca-be3a-a1fb036413f9">Dell Latitude 5540 (2023)</a></td>
        <th>Machine</th>
        <td><a href="https://support.apple.com/en-gb/111869">Apple MacBook Pro (13-inch, 2022)</a></td>
    </tr>
    <tr>
        <th>CPU</th>
        <td>Intel Core i5-1145G7 @ 2.60 GHz</td>
        <th>CPU</th>
        <td>Intel Core i5-1335U @ 1.30 GHz</td>
        <th>CPU</th>
        <td>Apple M2</td>
    </tr>
    <tr>
        <th>RAM</th>
        <td>16 GiB</td>
        <th>RAM</th>
        <td>8 GiB</td>
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
        <th colspan="6" style="text-align: center;">Network configurations</th>
    </tr>
    <tr>
        <th>Ethernet IPv4 address</th>
        <td>203.0.113.20</td>
        <th>Ethernet IPv4 address</th>
        <td>203.0.113.20</td>
        <th>Ethernet IPv4 address</th>
        <td>203.0.113.20</td>
    </tr>
    <tr>
        <th>Ethernet temporary IPv6 address</th>
        <td>2001:db8::20</td>
        <th>Ethernet temporary IPv6 address</th>
        <td>2001:db8::20</td>
        <th>Ethernet temporary IPv6 address</th>
        <td>2001:db8::20</td>
    </tr>
    <tr>
        <th>Ethernet permanent IPv6 address</th>
        <td>2001:db8::21</td>
        <th>Ethernet permanent IPv6 address</th>
        <td>2001:db8::21</td>
        <th>Ethernet permanent IPv6 address</th>
        <td>2001:db8::21</td>
    </tr>
    <tr>
        <th>Wi-Fi IPv4 address</th>
        <td>203.0.113.30</td>
        <th>Wi-Fi IPv4 address</th>
        <td>203.0.113.30</td>
        <th>Wi-Fi IPv4 address</th>
        <td>203.0.113.30</td>
    </tr>
    <tr>
        <th>Wi-Fi temporary IPv6 address</th>
        <td>2001:db8::30</td>
        <th>Wi-Fi temporary IPv6 address</th>
        <td>2001:db8::30</td>
        <th>Wi-Fi temporary IPv6 address</th>
        <td>2001:db8::30</td>
    </tr>
    <tr>
        <th>Wi-Fi permanent IPv6 address</th>
        <td>2001:db8::31</td>
        <th>Wi-Fi permanent IPv6 address</th>
        <td>2001:db8::31</td>
        <th>Wi-Fi permanent IPv6 address</th>
        <td>2001:db8::31</td>
    </tr>
    <tr>
        <th colspan="6" style="text-align: center;">Natively installed browsers on the host client</th>
    </tr>
    <tr>
        <th>Mozilla Firefox</th>
        <td>v125.0.3</td>
        <th>Mozilla Firefox</th>
        <td>v125.0.3</td>
        <th>Mozilla Firefox</th>
        <td>v125.0.3</td>
    </tr>
    <tr>
        <th>Google Chrome</th>
        <td>v126.0.6478.126</td>
        <th>Google Chrome</th>
        <td>v126.0.6478.127</td>
        <th>Google Chrome</th>
        <td>v126.0.6478.127</td>
    </tr>
    <tr>
        <th>Microsoft Edge</th>
        <td>v126.0.2592.81</td>
        <th>Microsoft Edge</th>
        <td>v126.0.2592.81</td>
        <th>Microsoft Edge</th>
        <td>v126.0.2592.81</td>
    </tr>
    <tr>
        <th>Opera</th>
        <td>v111.0.5168.55</td>
        <th>Opera</th>
        <td>v111.0.5168.55</td>
        <th>Opera</th>
        <td>v111.0.5168.55</td>
    </tr>
    <tr>
        <th>Brave Browser</th>
        <td>v1.67.123</td>
        <th>Brave Browser</th>
        <td>v1.67.123</td>
        <th>Brave Browser</th>
        <td>v1.67.123</td>
    </tr>
    <tr>
        <td colspan="4"></td>
        <th>Safari</th>
        <td>v17.5</td>
    </tr>
    <tr>
        <th colspan="6" style="text-align: center;">VPN and SOCKS clients</th>
    </tr>
    <tr>
        <th>OpenVPN UDP client</th>
        <td>OpenVPN 2.5.9</td>
        <th>OpenVPN UDP client</th>
        <td>OpenVPN GUI v11.48.0.0</td>
        <th>OpenVPN UDP client</th>
        <td>Tunnelblick 4.0.1</td>
    </tr>
    <tr>
        <th>WireGuard client</th>
        <td>v1.0.20210914</td>
        <th>WireGuard client</th>
        <td>v0.5.3</td>
        <th>WireGuard client</th>
        <td>v1.0.16</td>
    </tr>
    <tr>
        <th>Mozilla Firefox built-in SOCKS client</th>
        <td>v125.0.3</td>
        <th>Mozilla Firefox built-in SOCKS client</th>
        <td>v125.0.3</td>
        <th>Mozilla Firefox built-in SOCKS client</th>
        <td>v125.0.3</td>
    </tr>
    <tr>
        <th>Mozilla Firefox built-in HTTP/S client</th>
        <td>v125.0.3</td>
        <th>Mozilla Firefox built-in HTTP/S client</th>
        <td>v125.0.3</td>
        <th>Mozilla Firefox built-in HTTP/S client</th>
        <td>v125.0.3</td>
    </tr>
    <tr>
        <th colspan="6" style="text-align: center;">Containerised Mozilla Firefox solution via docker</th>
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


The raw data are available in the following folder: [`preventing-webrtc-ip-address-leaks/3-raw-data/1-webrtc-leak-data`](../3-raw-data/README.md).


## 2. Performance impact evaluation of the containerised solution

We are also evaluating our containerised solution in terms of performance and comparing it to a native, non-containerised solution.

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

Please read the section ***Performance evaluation of the containerised solution*** of the submission.

The Python scripts used to calculate the confidence intervals and ratios and to plot the results can be found in this folder: [`2-performances`](2-performances).  

To plot the graphs, run this command inside the [`2-performances`](2-performances) folder:

```zsh
python3 ./graphs.py
```

The raw data are available in the following folder: [`preventing-webrtc-ip-address-leaks/3-raw-data/2-performance-data`](../README.md).


We use three open-source benchmark suites actively developed by the three main web browser engine developers:
- **Motionmark v1.3** [[1, 2](#references)], graphics benchmark, open governance [[3](#references)], jointly developed by the developers of Blink/V8 (Chromium & derivatives), Gecko/SpiderMonkey (Firefox) and WebKit/JavaScriptCore (Safari);
- **Speedometer v3.0** [[3, 4](#references)], web application responsiveness benchmark, open governance [[6](#references)], jointly developed by the developers of Blink/V8 (Chromium & derivatives), Gecko/SpiderMonkey (Firefox) and WebKit/JavaScriptCore (Safari);
- **JetStream2 v2.2** [[7](#references)], JavaScript/WebAssembly benchmark suite governed by Apple alone [[8](#references)], including benchmarks developed by Apple, Mozilla and Google. As this suite is managed by Apple: [Mozilla](https://github.com/mozilla/perf-automation/tree/master/benchmarks/JetStream2) and [Google](https://chromium.googlesource.com/external/github.com/WebKit/webkit/+/refs/heads/main/PerformanceTests/JetStream2/) retrieve the latest suite releases separately from Apple's main repository: https://github.com/WebKit/WebKit/tree/main/PerformanceTests/JetStream2 [Accessed: Feb. 26, 2024].

We use the [browserbench.org](https://browserbench.org/) website managed by Apple, which publicly hosts these three benchmark suites.


## References

[[1](#21-general-benchmarks)] S. Fraser, D. Jackson, and N. Ryosuke, *About MotionMark 1.3*, MotionMark. Accessed: Feb. 26, 2024. [Online]. Available: https://browserbench.org/MotionMark/about.html.  
[[2](#21-general-benchmarks)] S. Fraser et al., *MotionMark*. Jan. 10, 2024. Accessed: Feb. 26, 2024. [Online]. Available: https://github.com/WebKit/MotionMark.  
[[3](#21-general-benchmarks)] M. Maxfield, *MotionMark Moves to Open Governance*, WebKit. Accessed: Feb. 26, 2024. [Online]. Available: https://webkit.org/blog/14359/motionmark-moves-to-open-governance/.  
[[4](#21-general-benchmarks)] Speedometer developers, *About Speedometer 3.0*, Speedometer 3.0. Accessed: June 3, 2024. [Online]. Available: https://browserbench.org/Speedometer3.0/.  
[[5](#21-general-benchmarks)] Speedometer developers, *Speedometer*. The WebKit Open Source Project, Feb. 20, 2024. Accessed: Feb. 26, 2024. [Online]. Available: https://github.com/WebKit/Speedometer.  
[[6](#21-general-benchmarks)] N. Ryosuke and T. Kober, *Speedometer/Governance.md*, Speedometer/Governance.md at main · WebKit/Speedometer. Accessed: Feb. 26, 2024. [Online]. Available: https://github.com/WebKit/Speedometer/blob/main/Governance.md.  
[[7](#21-general-benchmarks)] JetStream 2 developers, *JetStream 2 In-Depth Analysis*, JetStream 2 In-Depth Analysis. Accessed: Feb. 26, 2024. [Online]. Available: https://browserbench.org/JetStream/in-depth.html.  
[[8](#21-general-benchmarks)] S. Barati and M. Saboff, *Introducing the JetStream 2 Benchmark Suite*, WebKit. Accessed: Feb. 26, 2024. [Online]. Available: https://webkit.org/blog/8685/introducing-the-jetstream-2-benchmark-suite/.  