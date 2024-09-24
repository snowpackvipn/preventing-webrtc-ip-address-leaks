<small><i>This README is a copy of [section 5 - Automated reproduction of results](../README.md#5-automated-reproduction-of-results) from the `1-testbed/README.md` file.</i></small>

## Table of contents

[5. Automated reproduction of results](#5-automated-reproduction-of-results)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[5.1. Automated reproduction of IP address leak results](#51-automated-reproduction-of-ip-address-leak-results)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[5.1.1. Linux](#511-linux)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[5.1.1.0. Prerequisites](#5110-prerequisites)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[5.1.1.1. Wayland version (Mutter)](#5111-wayland-version-mutter)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[5.1.1.2. X version (X.Org/XWayland)](#5112-x-version-xorgxwayland)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[5.1.2. Windows](#512-windows)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[5.1.3. macOS](#513-macos)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[5.2. Automated reproduction of performance results](#52-automated-reproduction-of-performance-results)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[5.2.1. Linux](#521-linux)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[5.2.1.1. Wayland version (Mutter)](#5211-wayland-version-mutter)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[5.2.1.2. X version (X.Org/XWayland)](#5212-x-version-xorgxwayland)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[5.2.2. Windows](#522-windows)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[5.2.3. macOS](#523-macos)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[5.3. Analysing the results](#53-analysing-the-results)  


## 5. Automated reproduction of results

### 5.1. Automated reproduction of IP address leak results

#### 5.1.1. Linux

##### 5.1.1.0. Prerequisites

- Ensure that IPv6 is enabled on interfaces connected to the Internet.
- Ensure that you have set up an SSH public/private key connection with the coturn server.
- [TShark](https://tshark.dev/): to capture IP packets locally on the WebRTC client machine.
- [Python](https://www.python.org/) 3.10+: to automate experiments.
- [Selenium WebDriver](https://www.selenium.dev/documentation/webdriver/) 4.22 and its [Python bindings](https://selenium-python.readthedocs.io/): for web browser automation.
- [Paramiko](https://www.paramiko.org/): SSH python client used to launch remote TShark captures on the STUN-TURN server.

Install these tools by running the following commands in a shell and **allow non-root users to capture packets**:

```bash
sudo add-apt-repository ppa:wireshark-dev/stable
sudo apt update
sudo apt install tshark python3 python3-pip
pip install --upgrade pip
pip install paramiko selenium
```

Configure the addresses and credentials of your coturn server and VPN, SOCKS, HTTP-HTTPS proxies by running the following script:

```bash
./server_credential_and_address_configuration.py
```

##### 5.1.1.1. Wayland version (Mutter)

1. Run the experiments (duration: ~1h30 to 3 hours).

Go to [`1-leaks-automation/Linux (Ubuntu)/wayland-version/`](1-leaks-automation/Linux%20(Ubuntu)/wayland-version/) and run the experiments:

```bash
./run_leaks_linux_wayland.sh
```

2. Collect the results.

The Wireshark traces and ICE candidates extracted from SDP offers are available in the following folder: `~/Downloads/1-webrtc-leak-data/`.

##### 5.1.1.2. X version (X.Org/XWayland)

1. Run the experiments (duration: ~1h30 to 3 hours).

Go to [`1-leaks-automation/Linux (Ubuntu)/x-version/`](1-leaks-automation/Linux%20(Ubuntu)/x-version/) and run the experiments:

```bash
./run_leaks_linux_x.sh
```

2. Collect the results.

The Wireshark traces and ICE candidates extracted from SDP offers are available in the following folder: `~/Downloads/1-webrtc-leak-data/`.

#### 5.1.2. Windows

##### Prerequisites

- Ensure that IPv6 is enabled on interfaces connected to the Internet.
- Ensure that you have set up an SSH public/private key connection with the coturn server.
- Download and install [Wireshark](https://www.wireshark.org/download.html) to capture IP packets locally on the WebRTC client machine.
- Download and install [Python](https://www.python.org/downloads/windows/) 3.10+ to automate experiments.
- Install [Selenium WebDriver](https://www.selenium.dev/documentation/webdriver/) 4.22, its [Python bindings](https://selenium-python.readthedocs.io/) for web browser automation and the [Paramiko](https://www.paramiko.org/) SSH python client used to launch remote TShark captures on the STUN-TURN server:

```powershell
python -m pip install --upgrade pip
python -m pip install paramiko selenium
```

Configure the addresses and credentials of your coturn server and VPN, SOCKS, HTTP-HTTPS proxies by running the following script:

```powershell
python .\server_credential_and_address_configuration.py
```


1. Disable Docker Desktop's Resource Saver mode: https://docs.docker.com/desktop/use-desktop/resource-saver/, [Accessed: July 02, 2024].

2. Open an **administrator** Powershell, list your host USB devices and identify the camera one.

```powershell
usbipd list
```

3. Share and attach your host camera USB device to WSL. Now, your camera/microphone will no longer be accessible by your Windows host. Please change the `YOUR_DEVICE_BUS_ID` field with an appropriate bus id.

```powershell
usbipd bind --busid YOUR_DEVICE_BUS_ID

usbipd attach --wsl --busid YOUR_DEVICE_BUS_ID
```

4. Enter the `docker-desktop` WSL distribution and change the owner of `/dev/video0` to the firefox container user (of UID = `1000`).

```powershell
wsl --distribution docker-desktop
```

```bash
chown 1000:1000 /dev/video0

exit
```

5. Run the experiments (duration: ~3 to 4 hours).

Go to [`1-leaks-automation/Windows/`](1-leaks-automation/Windows/) and run the experiments:

```powershell
.\run_leaks_windows.ps1
```

6. Collect the results.

The Wireshark traces and ICE candidates extracted from SDP offers are available in the following folder: `~\Downloads\1-webrtc-leak-data\`.

#### 5.1.3. macOS

##### Prerequisites

- Ensure that IPv6 is enabled on interfaces connected to the Internet.
- Ensure that you have set up an SSH public/private key connection with the coturn server.
- Download and install [Wireshark](https://www.wireshark.org/download.html) to capture IP packets locally on the WebRTC client machine.
- Download and install [Python](https://www.python.org/downloads/macos/) 3.10+ to automate experiments.
- Create a Python virtual environment, activate it, install [Selenium WebDriver](https://www.selenium.dev/documentation/webdriver/) 4.22, its [Python bindings](https://selenium-python.readthedocs.io/) for web browser automation and the [Paramiko](https://www.paramiko.org/) SSH python client used to launch remote TShark captures on the STUN-TURN server:

```zsh
python -m venv /pathandnameofvirtualenv

source pathandnameofvirtualenv/bin/activate

pip install --upgrade pip
pip install paramiko selenium
```

Configure the addresses and credentials of your coturn server and VPN, SOCKS, HTTP-HTTPS proxies by running the following script:

```zsh
python ./server_credential_and_address_configuration.py
```

1. Launch *XQuartz* > *Settings* > *Security tab* and select ***Allow connections from network clients***.
2. Open a zsh terminal and authorise the future container to have an access to the XQuartz window display. This step has to been done each time macOS is rebooted.

```zsh
xhost +localhost
```

3. (optional, seems to be unstable) Enable Indirect GLX (OpenGL Extension to XQuartz) rendering for the container [[15](#references)]. Open a zsh terminal and type the following command:

```zsh
defaults write org.macosforge.xquartz.X.Org enable_iglx -bool true
```

4. Run the experiments (duration: ~1 to 2 hours).

Go to [`1-leaks-automation/macOS (arm64)/`](1-leaks-automation/macOS%20(arm64)/) and run the experiments. You may need to grant macOS authorisations related to the automation of *System Events*, web browsers, or access to the camera/microphone:

```zsh
./run_leaks_macos.sh
```

5. Collect the results.

The Wireshark traces and ICE candidates extracted from SDP offers are available in the following folder: `~/Downloads/1-webrtc-leak-data/`.

### 5.2. Automated reproduction of performance results

#### 5.2.1. Linux

##### 5.2.1.1. Wayland version (Mutter)

1. Run the experiments (duration: ~15h); user actions are required during script execution.

Go to [`2-benchmark-execution-automation/Linux (Ubuntu)/`](2-benchmark-execution-automation/Linux%20(Ubuntu)/) and run the experiments:

```bash
./run_benchmarks_linux_wayland.sh
```

2. Collect the results.

The JSON data are available in the following folder: `~/Downloads/2-performance-data/`.

##### 5.2.1.2. X version (X.Org/XWayland)

1. Run the experiments (duration: ~15h); user actions are required during script execution.

Go to [`2-benchmark-execution-automation/Linux (Ubuntu)/`](2-benchmark-execution-automation/Linux%20(Ubuntu)/) and run the experiments:

```bash
./run_benchmarks_linux_x.sh
```

2. Collect the results.

The JSON data are available in the following folder: `~/Downloads/2-performance-data/`.

#### 5.2.2. Windows

1. Disable Docker Desktop's Resource Saver mode: https://docs.docker.com/desktop/use-desktop/resource-saver/, [Accessed: July 02, 2024].

2. Open an **administrator** Powershell, list your host USB devices and identify the camera one.

```powershell
usbipd list
```

3. Share and attach your host camera USB device to WSL. Now, your camera/microphone will no longer be accessible by your Windows host. Please change the `YOUR_DEVICE_BUS_ID` field with an appropriate bus id.

```powershell
usbipd bind --busid YOUR_DEVICE_BUS_ID

usbipd attach --wsl --busid YOUR_DEVICE_BUS_ID
```

4. Enter the `docker-desktop` WSL distribution and change the owner of `/dev/video0` to the firefox container user (of UID = `1000`).

```powershell
wsl --distribution docker-desktop
```

```bash
chown 1000:1000 /dev/video0

exit
```

5. Run the experiments (duration: ~30h).

Go to [`2-benchmark-execution-automation/Windows/`](2-benchmark-execution-automation/Windows/) and run the experiments:

```powershell
.\run_benchmarks_windows.ps1
```

6. Collect the results.

The JSON data are available in the following folder: `~\Downloads\2-performance-data\`.

#### 5.2.3. macOS

1. Launch *XQuartz* > *Settings* > *Security tab* and select ***Allow connections from network clients***.
2. Open a zsh terminal and authorise the future container to have an access to the XQuartz window display. This step has to been done each time macOS is rebooted.

```zsh
xhost +localhost
```

3. (optional, seems to be unstable) Enable Indirect GLX (OpenGL Extension to XQuartz) rendering for the container [[15](#references)]. Open a zsh terminal and type the following command:

```zsh
defaults write org.macosforge.xquartz.X.Org enable_iglx -bool true
```

4. Run the experiments (duration: ~15h).

Go to [`2-benchmark-execution-automation/macOS (arm64)/`](2-benchmark-execution-automation/macOS%20(arm64)/) and run the experiments:

```zsh
./run_benchmarks_macos.sh
```

5. Collect the results.

The JSON data are available in the following folder: `~/Downloads/2-performance-data/`.


### 5.3. Analysing the results

1. Copy the folders `~\Downloads\1-webrtc-leak-data\` and `~/Downloads/2-performance-data/` at the root of the `3-raw-data` folder of this Git repository.
2. Continue by leaving the `1-testbed` folder, then read the [README](../../2-evaluation/README.md) in the `2-evaluation` folder at the root of this Git repository to analyse the results you have just produced.