<small><i>This README is a copy of [section 4 - WebRTC client configurations](../README.md#4-webrtc-client-configurations) from the `1-testbed/README.md` file.</i></small>

## Table of contents

[4. WebRTC client configurations](#4-webrtc-client-configurations)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[4.1. Install web browsers on the host machine](#41-install-web-browsers-on-the-host-machine)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[4.2. Containerised web browser solution](#42-containerised-web-browser-solution)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[4.2.1. Linux](#421-linux-ubuntu)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[4.2.1.0. Prerequisites](#4210-prerequisites)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[4.2.1.1. Wayland version (Mutter)](#4211-wayland-version-mutter)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[4.2.1.2. X version (X.Org/XWayland)](#4212-x-version-xorgxwayland)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[4.2.2. Windows](#422-windows)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[4.2.2.0. Prerequisites](#4220-prerequisites)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[4.2.2.1. Wayland version (Weston)](#4221-wayland-version-weston)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[4.2.2.2. X version (XWayland)](#4222-x-version-xwayland)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[4.2.3. macOS](#423-macos)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[4.2.3.0. Prerequisites](#4230-prerequisites)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[4.2.3.1. X version (XQuartz)](#4231-x-version-xquartz)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[4.3. Compromised Firefox web browser](#43-compromised-firefox-web-browser)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[4.3.1. Threat model](#431-threat-model)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[4.3.2. Compromising tools](#432-compromising-tools)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[4.3.2.1. Compromised configuration used in our evaluation](#4321-compromised-configuration-used-in-our-evaluation)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[4.3.2.1.1. Host configuration](#43211-host-configuration)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[4.3.2.1.2. Containerised compromised web browser](#43212-containerised-compromised-web-browser)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[4.3.2.2. Other compromised configuration allowing the installation of extensions not signed by Mozilla [19]](#4322-other-compromised-configuration-allowing-the-installation-of-extensions-not-signed-by-mozilla-19)  
[References](#references)

## 4. WebRTC client configurations

#### Network configuration overview

<table>
    <tr>
        <th colspan="4">Physical interfaces <i>attaching directly - (non-NATed) - public IP addresses</i></th>
        <th colspan="4">Virtual interfaces</th>
    </tr>
    <tr>
        <th>Ethernet IPv4 address</th>
        <td>203.0.113.20</td>
        <th>Wi-Fi IPv4 address</th>
        <td>203.0.113.30</td>
        <th>OpenVPN IPv4 virtual private network </th>
        <td>10.7.0.0/24</td>
        <th>WireGuard IPv4 virtual private network </th>
        <td>10.8.0.0/24</td>
    </tr>
    <tr>
        <th>Ethernet temporary IPv6 address</th>
        <td>2001:db8::20</td>
        <th>Wi-Fi temporary IPv6 address</th>
        <td>2001:db8::30</td>
        <th>OpenVPN IPv6 virtual private network </th>
        <td>fddd:1194:1194:1194::/64</td>
        <th>WireGuard IPv6 virtual private network </th>
        <td>fd4c:61b4:9648::/64</td>
    </tr>
    <tr>
        <th >Ethernet permanent IPv6 address</th>
        <td>2001:db8::21</td>
        <th>Wi-Fi permanent IPv6 address</th>
        <td>2001:db8::31</td>
        <td colspan="4"></td>
    </tr>
</table>


### 4.1. Install web browsers on the host machine

The following web browsers have been evaluated. Install them on your computer:
- Mozilla Firefox v125.0.3: [Download](https://ftp.mozilla.org/pub/firefox/releases/125.0.3/)
- Google Chrome v126.0.6478.126 (Linux), v126.0.6478.127 (macOS & Windows): [Download](https://www.google.com/intl/en_GB/chrome/)
- Microsoft Edge v126.0.2592.81: [Download](https://www.microsoft.com/en-gb/edge/business/download?form=MA13FJ)
- Opera v111.0.5168.55: [Download](https://get.opera.com/pub/opera/desktop/111.0.5168.55/)
- Brave Browser v1.67.123: [Download](https://github.com/brave/brave-browser/releases/tag/v1.67.123)
- Safari (on macOS only) v17.5

### 4.2. Containerised web browser solution

#### 4.2.1. Linux (Ubuntu)

Latest tested configuration [links accessed on Mar. 05, 2024]:

<table>
    <tr>
        <th>Host OS</th>
        <td>Ubuntu Desktop 22.04 LTS</td>
    </tr>
    <tr>
        <th>Architecture</th>
        <td>x86-64</td>
    </tr>
    <tr>
        <th>Docker image</th>
        <td>Ubuntu Server 22.04 LTS</td>
    </tr>
    <tr>
        <th>Docker image architecture</th>
        <td>x86-64</td>
    </tr>
    <tr>
        <th>Containerised Firefox</th>
        <td>v125.0.3</td>
    </tr>
    <tr>
        <th>Docker Engine</th>
        <td>v26.1.4</td>
    </tr>
    <tr>
        <th>Docker Compose </th>
        <td>v2.27.1</td>
    </tr>
    <tr>
        <th>Host Wayland compositor</th>
        <td rowspan="2"><a href="https://mutter.gnome.org/">Mutter</a> v42.9</td>
    </tr>
    <tr>
        <th>Host X server (X.Org/XWayland)</th>
    </tr>
    <tr>
        <th>Host PulseAudio server</th>
        <td>PulseAudio (on <a href="https://pipewire.org/">PipeWire</a> 0.3.48)</td>
    </tr>
</table>

##### 4.2.1.0. Prerequisites

1. Having installed the **Docker Engine** and the **Docker Compose** plugin: https://docs.docker.com/engine/install/ubuntu/, [Accessed: Mar. 05, 2024].

2. Having done the **Linux post-installation steps** for Docker Engine: https://docs.docker.com/engine/install/linux-postinstall/, [Accessed: Mar. 05, 2024].

3. Create a folder which will contains the Firefox profiles shared with the container.

```bash
mkdir $HOME/Firefox_Docker_Profiles
```

4. Enable IPv6 support.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;4.1. Edit the docker daemon configuration file as follows:

```bash
sudo nano /etc/docker/daemon.json
```

```json
{
    "experimental": true,
    "ip6tables": true
}
```

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;4.2. Restart the docker daemon.

```bash
sudo systemctl restart docker
```

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;4.3. Enable IPV4 and IPv6 forwarding.

```bash
sudo nano /etc/sysctl.conf
```
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Make sure that these two lines exists or are uncommented and equal to 1.

```bash
net.ipv4.ip_forward=1
net.ipv6.conf.default.forwarding=1
net.ipv6.conf.all.forwarding=1
```

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Save the file.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;4.4. (required if you use the UFW firewall) If you have the UFW firewall, make sure that IPv4 and IPv6 forwarding is authorised.

```bash
sudo nano /etc/ufw/sysctl.conf
```

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Make sure that these two lines exists or are uncommented and equal to 1.

```bash
net/ipv4/ip_forward=1
net/ipv6/conf/default/forwarding=1
net/ipv6/conf/all/forwarding=1
```

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Save the file.

##### 4.2.1.1. Wayland version (Mutter)

###### Launch the container

Go to [`1-firefox-containerised/Linux (Ubuntu)/wayland-version`](1-firefox-containerised/Linux%20(Ubuntu)/wayland-version) and launch the docker image:

```bash
UID=$(id -u) GID=$(id -g) RENDER_GID=$(getent group render | cut -d: -f3) docker compose -f ./docker-compose-firefox-wayland-linux.yml up
```

###### Stop the container

Close the web browser or run this command:

```bash
UID=$(id -u) GID=$(id -g) RENDER_GID=$(getent group render | cut -d: -f3) docker compose -f ./docker-compose-firefox-wayland-linux.yml down
```

###### Update the containerised web browser

```bash
UID=$(id -u) GID=$(id -g) RENDER_GID=$(getent group render | cut -d: -f3) docker compose -f ./docker-compose-firefox-wayland-linux.yml down
UID=$(id -u) GID=$(id -g) RENDER_GID=$(getent group render | cut -d: -f3) docker compose -f ./docker-compose-firefox-wayland-linux.yml build --no-cache
```


##### 4.2.1.2. X version (X.Org/XWayland)

###### Prerequisite

Open a shell terminal and authorise the `docker` user to have an access to the X window display

```bash
xhost +local:docker
```

###### Launch the container

Go to [`1-firefox-containerised/Linux (Ubuntu)/x-version`](1-firefox-containerised/Linux%20(Ubuntu)/x-version) and launch the docker image:

```bash
UID=$(id -u) GID=$(id -g) RENDER_GID=$(getent group render | cut -d: -f3) docker compose -f ./docker-compose-firefox-x-linux.yml up
```

###### Stop the container

Close the web browser or run this command:

```bash
UID=$(id -u) GID=$(id -g) RENDER_GID=$(getent group render | cut -d: -f3) docker compose -f ./docker-compose-firefox-x-linux.yml down
```

###### Update the containerised web browser

```bash
UID=$(id -u) GID=$(id -g) RENDER_GID=$(getent group render | cut -d: -f3) docker compose -f ./docker-compose-firefox-x-linux.yml down
UID=$(id -u) GID=$(id -g) RENDER_GID=$(getent group render | cut -d: -f3) docker compose -f ./docker-compose-firefox-x-linux.yml build --no-cache
```

###### Remove docker access to the X window system

```bash
xhost -local:docker
```


##### Other options

Please look the appropriate *dockerfiles* and *dockercompose files* and their comments/documentation to change some options, such as the language, the linux architecture...

##### Linux issue

 - With Wayland, there is no minimise or maximise button for Firefox.

#### 4.2.2. Windows

Tested configuration [links accessed on Mar. 05, 2024]:

<table>
    <tr>
        <th>Host OS</th>
        <td>Windows 11 Pro 23H2</td>
    </tr>
    <tr>
        <th>Architecture</th>
        <td>x86-64</td>
    </tr>
    <tr>
        <th>Docker image</th>
        <td>Ubuntu Server 22.04 LTS</td>
    </tr>
    <tr>
        <th>Docker image architecture</th>
        <td>x86-64</td>
    </tr>
    <tr>
        <th>Containerised Firefox</th>
        <td>v125.0.3</td>
    </tr>
    <tr>
        <th><a href="https://www.docker.com/products/docker-desktop/">Docker Desktop</a></th>
        <td>v4.30.0</td>
    </tr>
    <tr>
        <th><a href="https://github.com/dorssel/usbipd-win">usbipd-win</a></th>
        <td>v.4.2.0 </td>
    </tr>
    <tr>
        <th><a href="https://learn.microsoft.com/en-gb/windows/wsl/about">WSL 2</a></th>
        <td>v2.2.4.0</td>
    </tr>
    <tr>
        <th><a href="https://github.com/microsoft/WSL2-Linux-Kernel">WSL 2 Linux Kernel</a> with camera driver support</th>
        <td>v5.15.153.1 - <a href="../../../../raw/refs/heads/main/1-testbed/4-webrtc-client-setup/1-firefox-containerised/Windows/linux-wsl-kernel-with-camera-drivers/vmlinux.zip?download=">Download</a> - More information in section <a href="#4220-prerequisites">4.2.2.0. Prerequisites</a></td>
    </tr>
    <tr>
        <th><a href="https://github.com/microsoft/wslg">WSLg</a></th>
        <td>v1.0.61</td>
    </tr>
    <tr>
        <th>Host Wayland compositor</th>
        <td rowspan="2"><a href="https://wayland.pages.freedesktop.org/weston/">Weston</a> (provided by WSLg) GitHub commit <code><a href="https://github.com/microsoft/weston-mirror/commit/f227edd681479ec3cb2290a25d84d2d3462aebfa">f227edd6</a></code>
        </td>
    </tr>
    <tr>
        <th>Host X server (XWayland)</th>
    </tr>
    <tr>
        <th>Host <a href="https://www.freedesktop.org/wiki/Software/PulseAudio/">PulseAudio</a> server</th>
        <td>(provided by WSLg) GitHub commit <code><a href="https://github.com/microsoft/pulseaudio-mirror/commit/6f045ff0dca233a939a2aba815f84d177e294122">6f045ff0</a></code>
        </td>
    </tr>
</table>


##### 4.2.2.0. Prerequisites

1. Install the Windows Subsystem for Linux 2 (WSL 2) via a PowerShell Terminal.

```powershell
wsl --install --no-distribution
```

2. Install Docker Desktop [[10](#references)] and USBIPD-WIN [[11, 12](#references)] to share the host integrated USB camera with the container. Your computer will restart.

```powershell
winget install --id Docker.DockerDesktop -e --source winget ;  winget install --id dorssel.usbipd-win -e --source winget ; shutdown /r -t 0
```

3. Compile the WSL Linux kernel with the USB camera drivers (~10GB RAM needed).

> :information_source: If you do not want to compile the WSL Linux kernel you can download this WSL Linux kernel build (v5.15.153.1) here: [`Download`](../../../../raw/refs/heads/main/1-testbed/4-webrtc-client-setup/1-firefox-containerised/Windows/linux-wsl-kernel-with-camera-drivers/vmlinux.zip?download=). Copy this file to `C:\Sources` and go directly to step [3.5](#35-stop-wsl).


&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;3.1. Install the Ubuntu distribution:

```powershell
wsl --install Ubuntu
```

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;3.2. Enter the Ubuntu distribution

```powershell
wsl --distribution Ubuntu
```

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;3.3. Get the current Linux WSL kernel version

```bash
uname -r
```

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;3.4. Compile the Linux WSL kernel with USB camera support.  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Please change the `VERSION` field with the one that correspond to your current Linux WSL kernel version.

```bash
######################
# Build WSL2 kernel with usb camera support
# menuconfig -> Device Drivers -> Multimedia support -> Filter media drivers
#            -> Device Drivers -> Multimedia support -> Media device types -> Cameras and video grabbers
#            -> Device Drivers -> Multimedia support -> Video4Linux options -> V4L2 sub-device userspace API
#            -> Device Drivers -> Multimedia support -> Media drivers -> Media USB Adapters -> USB Video Class (UVC)
#            -> Device Drivers -> Multimedia support -> Media drivers -> Media USB Adapters -> UVC input events device support
#            -> Device Drivers -> Multimedia support -> Media drivers -> Media USB Adapters -> GSPCA based webcams
######################
VERSION=5.15.153.1
sudo apt update && sudo apt upgrade -y && sudo apt install -y build-essential flex bison libgtk2.0-dev libelf-dev libncurses-dev autoconf libudev-dev libtool zip unzip v4l-utils libssl-dev python3-pip cmake git iputils-ping net-tools dwarves bc
sudo mkdir /usr/src
cd /usr/src
sudo git clone -b linux-msft-wsl-${VERSION} https://github.com/microsoft/WSL2-Linux-Kernel.git ${VERSION}-microsoft-standard && cd ${VERSION}-microsoft-standard
sudo cp /proc/config.gz config.gz
sudo gunzip config.gz
sudo mv config .config
sudo make menuconfig
sudo make -j$(nproc)
sudo make modules_install -j$(nproc)
sudo make install -j$(nproc)
sudo mkdir /mnt/c/Sources/
sudo cp -rf vmlinux /mnt/c/Sources/
exit
```

*Adaptation of the original works from AgileDevArt, https://agiledevart.github.io/wsl2_usb_camera.txt*, [Accessed: Mar. 05, 2024]

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<a name="35-stop-wsl"></a>3.5. Stop WSL

```powershell
wsl --shutdown
```

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;3.6. Go back to Windows and create a file named `.wslconfig` in your home directory (accessible via `%USERPROFILE%` in the address bar of the File explorer) that contains:

```config
[wsl2]
kernel=C:\\Sources\\vmlinux
```

More information in the video tutorial of AgileDevArt: https://www.youtube.com/watch?v=t_YnACEPmrM, [Accessed: Mar. 05, 2024].


4. <a name="step-4"></a>Open Docker Desktop, go to ***Settings > General*** and select ***Start Docker Desktop when you log in***.

5. Open an **administrator** Powershell, list your host USB devices and identify the camera one.

```powershell
usbipd list
```

6. Share and attach your host camera USB device to WSL. Now, your camera/microphone will no longer be accessible by your Windows host. Please change the `YOUR_DEVICE_BUS_ID` field with an appropriate bus id.

```powershell
usbipd bind --busid YOUR_DEVICE_BUS_ID

usbipd attach --wsl --busid YOUR_DEVICE_BUS_ID
```

7. Enter the `docker-desktop` WSL distribution and change the owner of `/dev/video0` to the firefox container user (of UID = `1000`).

```powershell
wsl --distribution docker-desktop
```

```bash
chown 1000:1000 /dev/video0

exit
```

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;You need to do that each time you attach a USB device to WSL via usbipd.

**Detach an USB device**

To detach the USB device, run the following command:

```powershell
usbipd detach --busid YOUR_DEVICE_BUS_ID
```

##### 4.2.2.1. Wayland version (Weston)

###### Launch the container

Go to [`1-firefox-containerised/Windows/wayland-version`](1-firefox-containerised/Windows/wayland-version) and launch the docker image:

```bash
docker compose -f ./docker-compose-firefox-wayland-windows.yml up
```

###### Stop the container

Close the web browser or run this command:

```bash
docker compose -f ./docker-compose-firefox-wayland-windows.yml down
```

###### Update the containerised web browser

```bash
docker compose -f ./docker-compose-firefox-wayland-windows.yml down
docker compose -f ./docker-compose-firefox-wayland-windows.yml build --no-cache
```


##### 4.2.2.2. X version (XWayland)

###### Launch the container

Go to [`1-firefox-containerised/Windows/x-version`](1-firefox-containerised/Windows/x-version) and launch the docker image:

```bash
docker compose -f ./docker-compose-firefox-x-windows.yml up
```

###### Stop the container

Close the web browser or run this command:

```bash
docker compose -f ./docker-compose-firefox-x-windows.yml down
```

###### Update the containerised web browser

```bash
docker compose -f ./docker-compose-firefox-x-windows.yml down
docker compose -f ./docker-compose-firefox-x-windows.yml build --no-cache
```

##### Other options

Please look the appropriate *dockerfiles* and *dockercompose files* and their comments/documentation to change some options, such as the language, the linux architecture...

##### Windows issues

 - IPv6 is not supported with Docker for Windows [[13](#references)].
 - With Wayland, there is currently no possibility to share the screen at all.
 - With Wayland, there is no minimise or maximise button for Firefox.
 - With Wayland, [`getUserMedia()`](https://developer.mozilla.org/en-US/docs/Web/API/MediaDevices/getUserMedia) pop-ups are not working properly due to a weston issue [[14](#references)]. Workaround: go to **Help > About Firefox**, type any key on the keyboard, close the window and navigate to the [`getUserMedia()`](https://developer.mozilla.org/en-US/docs/Web/API/MediaDevices/getUserMedia) ***Allow*** button thanks to the **Tab** and **Enter** keys of the keyboard.

#### 4.2.3. macOS

Tested configuration on an Apple MacBook Pro (13-inch, M2, 2022) [links accessed on Mar. 05, 2024]:

<table>
    <tr>
        <th>Host OS</th>
        <td>macOS Sonoma 14.5</td>
    </tr>
    <tr>
        <th>Architecture</th>
        <td>arm64</td>
    </tr>
    <tr>
        <th>Docker image</th>
        <td>Ubuntu Server 22.04 LTS</td>
    </tr>
    <tr>
        <th>Docker image architecture</th>
        <td>arm64</td>
    </tr>
    <tr>
        <th>Containerised Firefox</th>
        <td>v125.0.3</td>
    </tr>
    <tr>
        <th><a href="https://www.docker.com/products/docker-desktop/">Docker Desktop</a></th>
        <td>v4.30.0</td>
    </tr>
    <tr>
        <th>Host X server (<a href="https://www.xquartz.org/">XQuartz</a>)</th>
        <td>v2.8.5</td>
    </tr>
    <tr>
        <th>Host <a href="https://www.freedesktop.org/wiki/Software/PulseAudio/">PulseAudio</a> server</th>
        <td>v17.0</td>
    </tr>
</table>

##### 4.2.3.0. Prerequisites

1. Install Docker Desktop, follow the instructions: https://docs.docker.com/desktop/install/mac-install/, [Accessed: Mar. 05, 2024].
2. Open Docker Desktop, go to ***Settings > General*** and select ***Start Docker Desktop when you log in***.
3. Install the X server provided by XQuartz and the PulseAudio server.

```zsh
brew install --cask xquartz
brew install pulseaudio
```

4. Launch *XQuartz* > *Settings* > *Security tab* and select ***Allow connections from network clients***.
5. Open a zsh terminal and authorise the future container to have an access to the XQuartz window display. This step has to been done each time macOS is rebooted.

```zsh
xhost +localhost
```

6. (optional, seems to be unstable) Enable Indirect GLX (OpenGL Extension to XQuartz) rendering for the container [[15](#references)]. Open a zsh terminal and type the following command:

```zsh
defaults write org.macosforge.xquartz.X.Org enable_iglx -bool true
```

7. Enable Pulseaudio network access

```zsh
nano /opt/homebrew/opt/pulseaudio/etc/pulse/default.pa
```

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Uncomment these two lines and save:
```bash
# [...]

load-module module-esound-protocol-tcp
load-module module-native-protocol-tcp

# [...]
```

7. Start the pulseaudio service

```zsh
brew services start pulseaudio
```

##### 4.2.3.1. X version (XQuartz)

###### Launch the container

Go to [`1-firefox-containerised/macOS (arm64)/x-version`](1-firefox-containerised/macOS%20(arm64)/x-version) and launch the docker image:

```bash
UID=$(id -u) GID=$(id -g) docker compose -f ./docker-compose-firefox-x-macos.yml up
```

###### Stop the container

Close the web browser or run this command:

```bash
UID=$(id -u) GID=$(id -g) docker compose -f ./docker-compose-firefox-x-macos.yml down
```

###### Update the containerised web browser

```bash
UID=$(id -u) GID=$(id -g) docker compose -f ./docker-compose-firefox-x-macos.yml down
UID=$(id -u) GID=$(id -g) docker compose -f ./docker-compose-firefox-x-macos.yml build --no-cache
```

###### Remove docker access to the XQuartz window system

```zsh
xhost -localhost
```

##### Other options

Please look the appropriate *dockerfiles* and *dockercompose files* and their comments/documentation to change some options, such as the language, the linux architecture...

##### macOS issues

 - IPv6 is not supported with Docker for Mac [[13](#references)].
 - There is no official Wayland compositor on macOS.
 - The camera is not working because there is currently no possibility to share devices between the host and the container [[16, 17](#references)].
 - The screen sharing is not working.


### 4.3. Compromised Firefox web browser

#### 4.3.1. Threat model

The adversary is able to exploit any vulnerability in Firefox to force it to operate in the most unfavourable WebRTC mode, or even to modify the WebRTC implementation maliciously (e.g. mode 1 always used regardless of the user's consent). The adversary's capabilities are limited to compromise the browser. The WebRTC client is corrupted and is unaware of it.

Our compromised browser is forced to run only in a mode where WebRTC does not respect privacy: no mDNS protection, even if the user does not give his consent, and link-local/loop-back IP addresses can be candidates (cf. [ subsection 4.3.2.1](#4321-compromised-configuration-used-in-our-evaluation)).

A post on the Mozilla Russia forum [[19](#references)] gives a way of authorising the installation of extensions not signed by Mozilla. All that needs to be done is to create an executable script and have the user download it (cf. [subsection 4.3.2.2](#4322-other-compromised-configuration-allowing-the-installation-of-extensions-not-signed-by-mozilla-19)). This compromised Firefox browser version is not included in our evaluation.

#### 4.3.2. Compromising tools

<small><i>The bash scripts and paths presented in this subsection are only valid for Ubuntu. This has been tested with **Ubuntu 22.04 LTS** with the **.deb version** of Firefox [[18](#references)]. If you wish to compromise your Firefox web browser on **Windows** or **macOS**, the only Firefox configuration files to overwrite are ***config.js*** and **config-prefs.js**. Refer to this GitHub issue to find out where the paths to these configuration files can be found: https://github.com/xiaoxiaoflood/firefox-scripts/issues/8 [Accessed: Feb. 26, 2024].</i></small>

##### 4.3.2.1. Compromised configuration used in our evaluation

###### 4.3.2.1.1. Host configuration

The configuration used in our host system evaluation can be done by modifying/creating theses two files:

***config-prefs.js***

```javascript
pref("general.config.obscure_value", 0);
pref("general.config.filename", "config.js");
pref("general.config.sandbox_enabled", false);
```

***config.js***

```javascript
lockPref("media.peerconnection.ice.obfuscate_host_addresses", false);
lockPref("media.peerconnection.ice.proxy_only", false);
lockPref("media.peerconnection.ice.link_local", true);
lockPref("media.peerconnection.ice.loopback", true);
lockPref("media.peerconnection.ice.proxy_only_if_behind_proxy", false);
lockPref("media.peerconnection.ice.relay_only", false);
lockPref("media.peerconnection.ice.force_interface", true);
lockPref("media.peerconnection.ice.relay_only", false);
lockPref("media.peerconnection.use_document_iceservers", true);
lockPref("media.peerconnection.ice.default_address_only", false);
lockPref("media.peerconnection.ice.no_host", false);
lockPref("media.peerconnection.enabled", true);
lockPref("media.peerconnection.ice.tcp", true);
lockPref("media.peerconnection.identity.enabled", true);
lockPref("media.peerconnection.turn.disable", false);
lockPref("media.peerconnection.allow_old_setParameters", true);
```

To automatically achieve this configuration on Ubuntu, go to the [`2-compromising-firefox/1-compromising-firefox-evaluation-version`](2-compromising-firefox/1-compromising-firefox-evaluation-version) folder, open the [`index.html`](2-compromising-firefox/1-compromising-firefox-evaluation-version/index.html) page and follow the instructions on that page.


###### 4.3.2.1.2. Containerised compromised web browser

This compromising configuration is also included in the containerised version of the compromised Firefox web browser for all types of host OS (Linux, Windows, macOS).

To use them, simply use the *docker compose files* containing the word ***"compromised"***, e.g. for the ***Linux Wayland version***: 

```bash
UID=${UID} GID=${GID} docker compose -f ./docker-compose-compromised-firefox-wayland-linux.yml up
```

For more information on the Firefox containerised browser, please read [section 4.1 - Run the containerised web browser solution of the `1-testbed/README.md`](../README.md#42-containerised-web-browser-solution).


##### 4.3.2.2. Other compromised configuration allowing the installation of extensions not signed by Mozilla [[19](#references)]

This section is provided for information purposes only, to show that there are other ways of compromising the browser. For example by using the configuration provided by banbot [[19](#references)] which allows the installation of extensions not signed by Mozilla:

***config-prefs.js*** - Firefox v102+, author: banbot [[19](#references)]

```javascript
try {(jsval => {
	var dbg, gref, genv = func => {
		var sandbox = new Cu.Sandbox(g, {freshCompartment: true});
		Cc["@mozilla.org/jsdebugger;1"].createInstance(Ci.IJSDebugger).addClass(sandbox);
		(dbg = new sandbox.Debugger()).addDebuggee(g);
		gref = dbg.makeGlobalObjectReference(g);
		return (genv = func => func && gref.makeDebuggeeValue(func).environment)(func);
	}
	var g = Cu.getGlobalForObject(jsval), o = g.Object, {freeze} = o, disleg;

	var AC = "AppConstants", uac = `resource://gre/modules/${AC}.`;
	var lexp = () => lockPref("extensions.experiments.enabled", true);
	if (o.isFrozen(o)) { // Fx 102.0b7+
		lexp(); disleg = true;
		var env, def = g.ChromeUtils.defineModuleGetter;
		g.ChromeUtils.defineModuleGetter = (...args) => {
			try {
				genv();
				dbg.addDebuggee(globalThis);
				var e = dbg.getNewestFrame().older.environment;
				var obj = e.parent.type == "object" && e.parent.object;
				if (obj && obj.class.startsWith("N")) // JSM, NSVO
					obj.unsafeDereference().Object = {
						freeze: ac => (ac.MOZ_REQUIRE_SIGNING = false) || freeze(ac)
					};
				else env = e; // ESM, Lexy "var"(?)
			}
			catch(ex) {Cu.reportError(ex);}
			(g.ChromeUtils.defineModuleGetter = def)(...args);
		}
		ChromeUtils.import(uac + "jsm");
		// (?)
		env && env.setVariable(AC, gref.makeDebuggeeValue(freeze(o.assign(
			new o(), env.getVariable(AC).unsafeDereference(), {MOZ_REQUIRE_SIGNING: false}
		))));
	}
	else o.freeze = obj => {
		if (!Components.stack.caller.filename.startsWith(uac)) return freeze(obj);
		obj.MOZ_REQUIRE_SIGNING = false;

		if ((disleg = "MOZ_ALLOW_ADDON_SIDELOAD" in obj)) lexp();
		else
			obj.MOZ_ALLOW_LEGACY_EXTENSIONS = true,
			lockPref("extensions.legacy.enabled", true);

		return (o.freeze = freeze)(obj);
	}
	lockPref("xpinstall.signatures.required", false);
	lockPref("extensions.langpacks.signatures.required", false);

	var useDbg = true, xpii = "resource://gre/modules/addons/XPIInstall.jsm";
	if (Ci.nsINativeFileWatcherService) { // Fx < 100
		jsval = Cu.import(xpii, {});
		var shouldVerify = jsval.shouldVerifySignedState;
		if (shouldVerify.length == 1)
			useDbg = false,
			jsval.shouldVerifySignedState = addon => !addon.id && shouldVerify(addon);
	}
	if (useDbg) {
		jsval = g.ChromeUtils.import(xpii);

		var env = genv(jsval.XPIInstall.installTemporaryAddon);
		var ref = name => {try {return env.find(name).getVariable(name).unsafeDereference();} catch {}}
		jsval.XPIDatabase = (ref("lazy") || {}).XPIDatabase || ref("XPIDatabase");

		var proto = ref("Package").prototype;
		var verify = proto.verifySignedState;
		proto.verifySignedState = function(id) {
			return id ? {cert: null, signedState: undefined} : verify.apply(this, arguments);
		}
		dbg.removeAllDebuggees();
	}
	if (disleg) jsval.XPIDatabase.isDisabledLegacy = () => false;
})(
	"permitCPOWsInScope" in Cu ? Cu.import("resource://gre/modules/WebRequestCommon.jsm", {}) : Cu
);}
catch(ex) {Cu.reportError(ex);}
```

To compromise your Firefox web browser automatically on Ubuntu, go to the [`2-compromising-firefox/2-compromising-firefox-unsigned-extensions-version`](2-compromising-firefox/2-compromising-firefox-unsigned-extensions-version) folder, open the [`index.html`](2-compromising-firefox/2-compromising-firefox-unsigned-extensions-version/index.html) page and follow the instructions on that page. The page will ask you in this order:
1. to compromise Firefox using the a compromising script (located in the folder), then
2. to install an extension whose official purpose is to disable WebRTC and whose **hidden purpose** is to **leave WebRTC enabled** (and therefore vulnerable to the WebRTC IP address leakage).

## References

[[10](#4220-prerequisites)] Docker, *Install Docker Desktop on Windows*, Docker Docs. Accessed: Feb. 26, 2024. [Online]. Available: https://docs.docker.com/desktop/install/windows-install/.  
[[11](#4220-prerequisites)] F. van Dorsselaer et al, *usbipd-win*. Feb. 03, 2024. Accessed: Feb. 26, 2024. [Online]. Available: https://github.com/dorssel/usbipd-win.  
[[12](#4220-prerequisites)] C. Lowen et al., *Connect USB devices*, Microsoft Learn. Accessed: Feb. 26, 2024. [Online]. Available: https://learn.microsoft.com/en-us/windows/wsl/connect-usb.  
[[13](#windows-issues)] Docker, *Enable IPv6 support*, Docker Documentation. Accessed: Mar. 05, 2024. [Online]. Available: https://docs.docker.com/config/daemon/ipv6/.  
[[14](#windows-issues)] dindin, *Open Bug 1600584 - [Wayland] [Weston] Firefox 70, Drop-down list is not working in weston*, Bugzilla. Accessed: Mar. 05, 2024. [Online]. Available: https://bugzilla.mozilla.org/show_bug.cgi?id=1600584.  
[[15](#4230-prerequisites)] M. Kari, *Running an X Server with Indirect GLX Rendering on MacOS for containerized applications with GUIs*. Accessed: Mar. 04, 2024. [Online]. Available: https://mohamedkari.github.io/blog.mkari.de/posts/glx-on-mac/.  
[[16](#macos-issues)] M. Graff and J. Dubois, *MacOS USB device passthrough to a Docker container · rancher-sandbox/rancher-desktop · Discussion #3904*, GitHub. Accessed: Feb. 23, 2024. [Online]. Available: https://github.com/rancher-sandbox/rancher-desktop/discussions/3904.  
[[17](#macos-issues)] M. Weinold, *USB Passthrough on macOS · Open Issue \#511 · docker/roadmap*, GitHub. Accessed: Feb. 23, 2024. [Online]. Available: https://github.com/docker/roadmap/issues/511.  
[[18](#43-compromised-firefox-web-browser)] A. Wyman et al., *Install Firefox .deb package for Debian-based distributions* **In**: *Install Firefox on Linux*, Mozilla Support. Accessed: May 24, 2024. [Online]. Available: https://support.mozilla.org/en-US/kb/install-firefox-linux#w_install-firefox-deb-package-for-debian-based-distributions.  
[[19](#431-threat-model)] banbot, *Как отключить проверку цифровых подписей в дополнениях Firefox [How to disable digital signature verification in Firefox add-ons]*, Forum Mozilla Russia. Accessed: Feb. 26, 2024. [Online]. Available: https://forum.mozilla-russia.org/viewtopic.php?id=70326.