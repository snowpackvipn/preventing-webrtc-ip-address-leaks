<small><i>This README is a copy of [section 2 - VPN, SOCKS and HTTP/HTTPS proxy deployment and configuration](../../1-testbed/README.md#2-vpn-socks-and-httphttps-proxy-deployment-and-configuration) from the `1-testbed/README.md` file.</i></small>

## Table of contents

[2. VPN, SOCKS and HTTP/HTTPS proxy deployment and configuration](#2-vpn-socks-and-httphttps-proxy-deployment-and-configuration)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[2.1. Configuration overview](#21-configuration-overview)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[2.2. Server and networks deployment](#22-server-and-networks-deployment)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[2.3. Installing the TShark network analyser](#23-installing-the-tshark-network-analyser)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[2.4. VPN servers configuration](#24-vpn-servers-configuration)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[2.4.1. Setting up the OpenVPN UDP VPN server](#241-setting-up-the-openvpn-udp-vpn-server)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[2.4.2. Setting up the WireGuard VPN server](#242-setting-up-the-wireguard-vpn-server)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[2.5. Proxy servers configuration](#25-proxy-servers-configuration)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[2.5.1. Setting up the Dante SOCKSv5 proxy server](#251-setting-up-the-dante-socksv5-proxy-server)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[2.5.2. Setting up the mitmproxy HTTP/HTTPS proxy server](#252-setting-up-the-mitmproxy-httphttps-proxy-server)  
[References](#references)

## 2. VPN, SOCKS and HTTP/HTTPS proxy deployment and configuration

### 2.1. Configuration overview

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

Each VPN (OpenVPN and WireGuard) provides one IPv4 (or IPv6) tunnel per client with IPv4 and IPv6 packet forwarding capabilities thanks to their IPv4 and IPv6 virtual networks. A virtual interface per VPN attaching a private IPv4 and IPv6 will therefore be offered to the VPN client.


### 2.2. Server and networks deployment

You can manually deploy a VM/VPS/machine to obtain the configuration described in the previous table.

In our case, we used the Google Cloud Platform to automatically generate the networks and VMs. The generation Google Cloud script is located there: [`0-vpn-socks-http-https-gcloud-deployment-commands.sh`](0-vpn-socks-http-https-gcloud-deployment-commands.sh). Please change the IP addresses in this file to those provided by Google, as well as the SSH key to connect to the machines using your own.

### 2.3. Installing the TShark network analyser

1. Enter the machine via SSH.

```bash
ssh username@198.51.100.1
```

2. Install tshark.

```bash
sudo apt update && sudo apt install tshark
```

### 2.4. VPN servers configuration

#### 2.4.1. Setting up the OpenVPN UDP VPN server

Please follow this online guide which contains a road warrior script [[7](#references)] automating the installation of the server: https://www.cyberciti.biz/faq/ubuntu-22-04-lts-set-up-openvpn-server-in-5-minutes/ [Accessed on May 24, 2024].

#### 2.4.2. Setting up the WireGuard VPN server

Please follow this online guide: https://www.digitalocean.com/community/tutorials/how-to-set-up-wireguard-on-ubuntu-22-04 [Accessed on May 24, 2024].

If you experience some problems with DNS, please read this blog post: https://www.procustodibus.com/blog/2022/03/wireguard-dns-config-for-systemd/ [Accessed on May 24, 2024].


### 2.5. Proxy servers configuration

#### 2.5.1. Setting up the Dante SOCKSv5 proxy server


1. Enter the *VPNs/SOCKS/HTTP/HTTPS proxies machine* via SSH.

```bash
ssh username@198.51.100.1
```

2. Install the Dante SOCKS server and tshark.

```bash
sudo apt update && sudo apt install dante-server tshark
```

3. Enable the Dante server.

```bash
sudo nano /etc/danted.conf
```

Edit the configuration file as follows:
```ini
#logging
logoutput: syslog
user.privileged: root
user.unprivileged: nobody

# listening network interface and protocols
internal.protocol: ipv4 ipv6
internal: wlan0

# proxying network interface and protocols
external.protocol: ipv4 ipv6
external: wlan0

# authentication methods
socksmethod: none
clientmethod: none

#allow connections from any ipv4 and ipv6 clients
client pass {
    from: 0/0 to: 0/0
}

socks pass {
    from: 0/0 to: 0/0
}
```

More information about the server configuration file: https://www.inet.no/dante/doc/latest/config/server.html (Accessed: May 24, 2024).

4. Enable the danted service, start it and check for the status:

```bash
sudo systemctl daemon-reload
sudo systemctl enable danted.service
sudo systemctl start danted.service
sudo systemctl status danted.service
```

5. Make sure that your firewall allows connections to port 1080.

```bash
sudo ufw allow 1080
```

If the service is active, you can close the SSH session. Otherwise, please look at the Dante project documentation [[8](#references)].


#### 2.5.2. Setting up the mitmproxy HTTP/HTTPS proxy server

1. Enter the machine via SSH.

```bash
ssh username@198.51.100.1
```

2. Install the mitmproxy HTTP/HTTPS proxy.

```bash
sudo apt update && sudo apt install mitmproxy
```

3. Create a mitmproxy systemd service.

```bash
sudo nano /etc/systemd/system/mitmdump.service 
```

Please change `username` with a non-root username.

```ini
[Unit]
Description=mitmdump service
After=network.target

[Service]
Type=simple
User=[username]
ExecStart=mitmdump --set block_global=false -p 8081 &>> /var/log/mitmdump.log
Restart=always
RestartSec=1

[Install]
WantedBy=multi-user.target
```


4. Enable the mitmproxy service, start it and check for the status:

```bash
sudo systemctl daemon-reload
sudo systemctl enable mitmdump.service
sudo systemctl start mitmdump.service
sudo systemctl status mitmdump.service
```

5. Make sure that your firewall allows connections to port 8081.

```bash
sudo ufw allow 8081
```

If the service is active, you can close the SSH session. Otherwise, please look at the mitmproxy project documentation [[9](#references)].


## References

[[7](#241-setting-up-the-openvpn-udp-vpn-server)] S. Lange et al, *openvpn-install*. Nov. 20, 2023. Accessed: May 24, 2024. [Online]. Available: https://github.com/angristan/openvpn-install.  
[[8](#251-setting-up-the-dante-socksv5-proxy-server)] Inferno Nettverk A/S, *Documentation*. Accessed: May 23, 2024. [Online]. Available: https://www.inet.no/dante/doc/.  
[[9](#252-setting-up-the-mitmproxy-httphttps-proxy-server)] mitmproxy team, *Introduction*, mitmproxy docs. Accessed: May 23, 2024. [Online]. Available: https://docs.mitmproxy.org/stable/.

