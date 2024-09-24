# Preventing WebRTC IP Address Leaks

The WebRTC API enables real-time communication of text, video, and audio media streams through a web browser without requiring third-party extensions. However, it was not designed with privacy in mind. We conduct an experiment to analyse privacy leaks associated with WebRTC on Linux, macOS and Windows. Our findings show that despite recent updates to its specification and implementations, sensitive public IP addresses can still leak during audio/video communication, particularly in **large non-NAT corporate networks**, even when using a VPN, SOCKS or HTTP/S proxy. To address the observed leaks, we develop a simple, easily maintainable, cross-platform, open-source solution that confines the Mozilla Firefox web browser in a docker container.
Our tests show that our containerised solution is effective in all situations even with a compromised browser without restricting applications.

## Citation

If you find this work helpful and use it, please cite our paper.

> [!NOTE]  
> As soon as it is published, we will include the BibTeX reference and a DOI link in this README file.

## Table of contents

[1. Foreword - important note about the results](#1-foreword---important-note-about-the-results)  
[2. Overview](#2-overview)  
[3. Getting started](#3-getting-started)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[3.1. Fully reproduce the results](#31-fully-reproduce-the-results)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[3.2. Access only the containerised web browser solution](#32-access-only-the-containerised-web-browser-solution)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[3.3. Test WebRTC IP address leakage](#33-test-webrtc-ip-address-leakage)  
[Credits](#credits)


## 1. Foreword - important note about the results

The results were obtained in a configuration where the WebRTC client is located in a large **non-NAT network**, i.e. **public IPv4 and IPv6 addresses** are directly attached to its network interfaces (Wi-Fi/Ethernet).

Surprisingly, this configuration is not rare and can affect a large number of users: the [**eduroam** network](https://eduroam.org/) of two different universities has allocated us two public IPv4 and IPv6 addresses. These campuses are made up of approximately 1,500 people and 30,000 people respectively.

You can, of course, use the testbed with other configurations.

Also, regarding the WebRTC client on Ubuntu, the Firefox browser installed on the host machine is the **.deb version**, not the **snap version** [[1](#references)]. 

## 2. Overview

This Git repository is made up of three folders:
 - [`1-testbed`](1-testbed/README.md), containing the elements used to build the testbed;
 - [`2-evaluation`](2-evaluation/README.md), containing the results of the various evaluations described in the submission;
 - [`3-raw-data`](3-raw-data/README.md), containing the raw anonymised data (Wireshark traces and ICE candidates extracted from the SDP offers displayed in the browser console).


## 3. Getting started

There are three possible choices for getting started.  If the objective is:
 - to fully reproduce the results, please follow the section - *[3.1. Fully reproduce the results](#reproduce)*;
 - to access only the containerised web browser solution, please follow the section - *[3.2. Access only the containerised web browser solution](#containerised)*;
 - to quickly test the WebRTC leak, please follow the section - *[3.3 Quickly test WebRTC IP address leakage](#test)*.

Note: on Windows, to clone the repository correctly, make sure you enable long paths. To do this, Microsoft [[2](#references)] suggests running the following PowerShell command:

```powershell
New-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\FileSystem" -Name "LongPathsEnabled" -Value 1 -PropertyType DWORD -Force
```

### <a name="reproduce"></a>3.1. Fully reproduce the results
---

#### Required network configuration:
 - The WebRTC client must be located in a **non-NAT network**, i.e. **public IPv4 and IPv6 addresses** are directly attached to its network interfaces (Wi-Fi/Ethernet).
 - The WebRTC client must support **IPv4** and **IPv6**.
 - All servers and networks must support **IPv4** and **IPv6**.

Then, read in order the READMEs at the root of:
 - [`1-testbed`](1-testbed),
 - [`2-evaluation`](2-evaluation) and
 - [`3-raw-data`](3-raw-data).

### <a name="containerised"></a>3.2. Access only the containerised web browser solution
---

Go directly to the [`1-testbed/4-webrtc-client-setup/1-firefox-containerised`](1-testbed/4-webrtc-client-setup/1-firefox-containerised) folder.


### <a name="test"></a>3.3. Test WebRTC IP address leakage
---

1. Copy the entire [`1-testbed/3-web-page`](1-testbed/3-web-page) folder to your default `Downloads` folder<sup>[1](#footnote-1)</sup>.

<small><sup>[1](#3-testing-the-webrtc-ip-adress-leak)</sup>This non-mandatory step makes it easy to access the test web page in the containerised browser solution ([section 4 of the `1-testbed/README.md`](1-testbed/README.md#42-containerised-web-browser-solution)), as the `Downloads` folder on the host system (which can be Linux, Windows or macOS) is shared with the containers.</small>

***Linux/macOS***

```bash
cp -R ./preventing-webrtc-ip-address-leaks/1-testbed/3-web-page/ ~/Downloads
```

***Windows***

```powershell
Copy-Item -Path ".\preventing-webrtc-ip-address-leaks\1-testbed\3-web-page\" -Destination "$USERPROFILE\Downloads" -Recurse
```


2. Open the `index.html` page using the web browser you want to use by typing the following path in the address bar:

***Linux/macOS***

```bash
~/Downloads/3-web-page/index.html
```

***Windows***

```
file:///C:/Users/USERNAME/Downloads/3-web-page/index.html
```

3. Provide your STUN and TURN server adresses, click on the button **Gather ICE candidates** and see the addresses that have been gathered.

4. Restart the experiment by **turning ON** the switch **Give getUserMedia() permission**, click on the button **Gather ICE candidates** and see the new addresses that have been gathered.

More information about the JavaScript code used: read the [`1-testbed/3-web-page/README.md`](1-testbed/3-web-page/README.md) file.

## Credits

The web browser containerised solution were created thanks to the valuable previous works of:
* Jessie Frazelle \<jess@linux.com>: https://github.com/jessfraz/dockerfiles/tree/master/tor-browser, licensed under the [MIT License](https://opensource.org/license/mit), accessed on 24 May 2024.
* Guy Taylor \<thebigguy.co.uk@gmail.com>: https://github.com/TheBiggerGuy/docker-pulseaudio-example, licensed under the [Unlicense license](https://unlicense.org/), accessed on 24 May 2024.
* David Ricq \<davidricq87@orange.fr>: https://github.com/Inglebard/dockerfiles/tree/firefox, licensed under the [MIT License](https://opensource.org/license/mit), accessed on 24 May 2024.


## References

[[1](#1-foreword---important-note-about-the-results)] A. Wyman et al., *Install Firefox .deb package for Debian-based distributions* **In**: *Install Firefox on Linux*, Mozilla Support. Accessed: May 24, 2024. [Online]. Available: https://support.mozilla.org/en-US/kb/install-firefox-linux#w_install-firefox-deb-package-for-debian-based-distributions.  
[[2](#3-getting-started)] A. Ashcraft et al., *Enable Long Paths in Windows 10, Version 1607, and Later* **In**: *Maximum Path Length Limitation*, Microsoft Learn, Jul. 18, 2022. Accessed: May 30th, 2024. [Online]. Available: https://learn.microsoft.com/en-gb/windows/win32/fileio/maximum-file-path-limitation?tabs=powershell#enable-long-paths-in-windows-10-version-1607-and-later.
