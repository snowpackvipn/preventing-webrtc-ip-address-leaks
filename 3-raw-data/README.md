# Raw data

## Table of contents

[Note](#note)  
[1. Raw data on the WebRTC evaluation of IP address leaks](#1-raw-data-on-the-webrtc-evaluation-of-ip-address-leaks)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[1.1. Reminder about the network configuration](#11-reminder-about-the-network-configuration)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[1.2. Reminder about the client configurations](#12-reminder-about-the-client-configurations)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[1.3. Data organisation](#13-data-organisation)  
[2. Raw data on the performance evaluation of the containerised solution](#2-raw-data-on-the-performance-evaluation-of-the-containerised-solution)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[2.1. Reminder about the client configurations](#21-reminder-about-the-client-configurations)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[2.2. Data organisation](#22-data-organisation)  
[References](#references)

## Note

For privacy purposes, all public IP addresses have been anonymised using those reserved for documentation given in RFC 5737 for IPv4 [[1](#references)] and RFC 3849 for IPv6 [[2](#references)].

## 1. Raw data on the WebRTC evaluation of IP address leaks

### 1.1. Reminder about the network configuration

#### STUN/TURN machine

<table>
    <tr>
        <th>Public IPv4 address</th>
        <th>Public IPv6 address</th>
        <th>Private IPv4 address</th>
        <th>Operating System</th>
        <th>Architecture</th>
        <th>Service</th>
        <th>Version</th>
        <th>Listening port</th>
    </tr>
    <tr>
        <td rowspan="2">192.0.2.1</td>
        <td rowspan="2">2001:db8::1</td>
        <td rowspan="2">10.132.0.8</td>
        <td rowspan="2">Ubuntu Server 22.04 LTS</td>
        <td rowspan="2">arm64</td>
        <td>coturn</td>
        <td>4.5.2</td>
        <td>5349 (TLS)</td>
    </tr>
    <tr>
        <td>TShark</td>
        <td>4.2.5</td>
        <td>N/A</td>
    </tr>
</table>

#### VPN, SOCKS and HTTP/HTTPS proxy machines

<table>
    <tr>
        <th>Public IPv4 address</th>
        <th>Public IPv6 address</th>
        <th>Private IPv4 address</th>
        <th>Operating System</th>
        <th>Architecture</th>
        <th>Service</th>
        <th>Version</th>
        <th>Listening port</th>
        <th>Virtual private IPv4 network</th>
        <th>Virtual private IPv6 network</th>
    </tr>
    <tr>
        <td rowspan="5">198.51.100.1</td>
        <td rowspan="5">2001:db8::2</td>
        <td rowspan="5">192.168.1.91</td>
        <td rowspan="5">Ubuntu Server 24.04 LTS</td>
        <td rowspan="5">arm64</td>
        <td>OpenVPN UDP</td>
        <td>2.6.9</td>
        <td>1194</td>
        <td>10.7.0.0/24</td>
        <td>fddd:1194:1194:1194::/64</td>
    </tr>
    <tr>
        <td>WireGuard</td>
        <td>1.0.20210914</td>
        <td>2050</td>
        <td>10.8.0.0/24</td>
        <td>fd4c:61b4:9648::/64</td>
    </tr>
    <tr>
        <td>Dante SOCKS5 proxy</td>
        <td>1.4.3</td>
        <td>1080</td>
        <td colspan="2">N/A</td>
    </tr>
    <tr>
        <td>mitmproxy HTTP/HTTPS proxy</td>
        <td>8.1.1</td>
        <td>8081</td>
        <td colspan="2">N/A</td>
    </tr>
    <tr>
        <td>TShark</td>
        <td>4.2.5</td>
        <td colspan="3">N/A</td>
    </tr>
</table>

Each VPN (OpenVPN and WireGuard) provides one IPv4 tunnel per client with IPv4 and IPv6 packet forwarding capabilities thanks to their IPv4 and IPv6 virtual networks. A virtual interface per VPN attaching a private IPv4 and IPv6 will therefore be offered to the VPN client.


### 1.2. Reminder about the client configurations

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

### 1.3. Data organisation

In the [`1-webrtc-leak-data`](1-webrtc-leak-data/README.md) folder, the data are classified as follows:
 - **1 - Major web browser leaks**, corresponding to raw leak data on the various popular web browsers on the market.
 - **2 - MF diff confs leaks**, corresponding to raw data from the ***vanilla*** Firefox web browser in different configurations (with or without VPN, SOCKS, containerised or not...)
 - **3 - Compro MF diff confs leaks**: corresponding to raw data from the ***compromised*** Firefox web browser in different configurations (vanilla, with or without VPN, SOCKS, containerised or not...)

where

**MF** = **Mozilla Firefox**;  
**Compro** = **Compromised**;  
**diff confs** = **different configurations**.

Each configuration tested has two folders: `ClientData` and `STUN-TURN-ServersData`.

The data generated by the WebRTC clients is located in the `ClientData` folder. This is the final list of ICE candidates created by WebRTC clients (file `ice-candidates.txt`) and the traffic data captured by Wireshark for STUN/TURN requests and responses at the client interfaces. There is one file per mode (RFC 8828 [[3](#references)] & draft-uberti-ip-handling-ex-mdns-00 [[4](#references)]) tested (`[default|forced]-modeX-stun-turn.pacpng`) where `X` is the mode number, and if present, `UC` - *User consent*, `NUC` - *No user consent* (handled by [`getUserMedia()`](https://developer.mozilla.org/en-US/docs/Web/API/MediaDevices/getUserMedia) [[5](#references)]). 

The traffic data captured by Wireshark on the STUN/TURN server side (located at the same IPv4 and IPv6 addresses) is located in the `STUN-TURN-ServersData` folder. The naming rule is: `name-of-the-configuration-tested-mode-X.pcapng` and if present, `UC` - *User consent*, `NUC` - *No user consent* (handled by [`getUserMedia()`](https://developer.mozilla.org/en-US/docs/Web/API/MediaDevices/getUserMedia) [[5](#references)]).

If `UC` and `NUC` are not present then the consent is defined by the mode [[3, 4](#references)].

The list of interfaces present and the associated information on the client machine in the test state is present in the `ip-addr-interfaces-[host|docker-(default|forced)-modeX].txt` file. This file is either placed at the root of a set of tests if the machine configuration does not change for the set of tests, or placed specifically in the `ClientData` folder associated with a particular test.

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

Raw data are available in the following folder: [`2-performance-data`](2-performance-data).


## References

[[1](#note)] J. Arkko, M. Cotton, and L. Vegoda, *IPv4 Address Blocks Reserved for Documentation*, Internet Engineering Task Force, Request for Comments RFC 5737, Jan. 2010. doi: [10.17487/RFC5737](https://doi.org/10.17487/RFC5737).  
[[2](#note)] G. Huston, A. Lord, and P. F. Smith, *IPv6 Address Prefix Reserved for Documentation*, Internet Engineering Task Force, Request for Comments RFC 3849, Jul. 2004. doi: [10.17487/RFC3849](https://doi.org/10.17487/RFC3849).  
[[3](#1-raw-data-on-the-webrtc-evaluation-of-ip-address-leaks)] J. Uberti, *WebRTC IP Address Handling Requirements*, Internet Engineering Task Force, Request for Comments RFC 8828, Jan. 2021. doi: [10.17487/RFC8828](https://doi.org/10.17487/RFC8828).  
[[4](#1-raw-data-on-the-webrtc-evaluation-of-ip-address-leaks)] J. Uberti, J. D. Borst, Q. Wang, and Y. Fablet, *WebRTC IP Address Handling Extensions for Multicast DNS*, Internet Engineering Task Force, Internet Draft draft-uberti-ip-handling-ex-mdns-00, Nov. 2018. Accessed: Feb. 27, 2024. [Online]. Available: https://datatracker.ietf.org/doc/draft-uberti-ip-handling-ex-mdns-00.  
[[5](#1-raw-data-on-the-webrtc-evaluation-of-ip-address-leaks)] Mozilla, *MediaDevices: getUserMedia() method*, MDN Web Docs. Accessed: Feb. 22, 2024. [Online]. Available: https://developer.mozilla.org/en-US/docs/Web/API/MediaDevices/getUserMedia.  