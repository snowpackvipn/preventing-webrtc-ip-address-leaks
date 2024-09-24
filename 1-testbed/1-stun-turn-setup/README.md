<small><i>This README is a copy of [section 1 - STUN and TURN server deployment and configuration](../../1-testbed/README.md#1-stun-and-turn-server-deployment-and-configuration) from the `1-testbed/README.md` file.</i></small>

## Table of contents

[1. STUN and TURN server deployment and configuration](#1-stun-and-turn-server-deployment-and-configuration)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[1.1. Configuration overview](#11-configuration-overview)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[1.2. Server and networks deployment](#12-server-and-networks-deployment)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[1.3. STUN/TURN server configuration](#13-stunturn-server-configuration)  
[Reference](#reference)

## 1. STUN and TURN server deployment and configuration

### 1.1. Configuration overview

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


### 1.2. Server and networks deployment

You can manually deploy a VM/VPS/machine to obtain the configuration described in the previous table.

In our case, we used the Google Cloud Platform to automatically generate the networks and VMs. The generation Google Cloud script is located there: [`0-stun-turn-gcloud-deployment-commands.sh`](0-stun-turn-gcloud-deployment-commands.sh). Please change the IP addresses in this file to those provided by Google, as well as the SSH key to connect to the machines using your own.

### 1.3. STUN/TURN server configuration

1. Enter the *STUN/TURN machine* via SSH.

```bash
ssh username@192.0.2.1
```

2. Install coturn and tshark.

```bash
sudo apt update && sudo apt install coturn tshark
```

3. Enable the TURN server.

```bash
sudo nano /etc/default/coturn
```

Make sure that the TURN server is enabled:

```ini
# /etc/default/coturn
# ...

TURNSERVER_ENABLED=1
# ...
```

4. Configure the TURN server.

```bash
sudo mv /etc/turnserver.conf /etc/turnserver.conf.original

sudo nano /etc/turnserver.conf
```

Paste the following configuration, be careful to set the `TURN_USERNAME`, `TURN_PASSWORD` and `DOMAIN_NAME_OF_THE_TURN_SERVER_PROVIDER` fields:


```ini
# /etc/turnserver.conf

listening-port=3478
tls-listening-port=5349
# The "external-ip" value, if not empty, is returned in XOR-RELAYED-ADDRESS field. (doc du fichier de conf), puis : 
# MDN: For relay candidates, the related address and port are set to the mapped address selected by the TURN server. 
# rfc 8656 STUN https://www.rfc-editor.org/rfc/rfc8656.html
external-ip=192.0.2.1/10.132.0.8

fingerprint
lt-cred-mech

cli-password=[TO BE GENERATED WITH turnadmin -P -p <password>]

user=TURN_USERNAME:TURN_PASSWORD
total-quota=100
stale-nonce=600

proc-user=turnserver
proc-group=turnserver

realm=DOMAIN_NAME_OF_THE_TURN_SERVER_PROVIDER

cert=/usr/local/etc/turn_server_cert.pem
pkey=/usr/local/etc/turn_server_pkey.pem
```

5. Create a TLS certificate.

```bash
sudo openssl req -newkey rsa:4096 -x509 -sha256 -days 365 -nodes -out /usr/local/etc/turn_server_cert.pem -keyout /usr/local/etc/turn_server_pkey.pem

sudo chown turnserver:turnserver /usr/local/etc/turn_server_cert.pem
sudo chmod 644 /usr/local/etc/turn_server_cert.pem
sudo chown turnserver:turnserver /usr/local/etc/turn_server_pkey.pem
sudo chmod 600 /usr/local/etc/turn_server_pkey.pem
```

6. Create a coturn systemd service.

```bash
sudo nano /lib/systemd/system/coturn.service  
```

```ini
[Unit]
Description=coTURN STUN/TURN Server
Documentation=man:coturn(1) man:turnadmin(1) man:turnserver(1)
After=network.target

[Service]
User=root
Group=root
Type=notify
ExecStart=/usr/bin/turnserver -c /etc/turnserver.conf
Restart=on-failure
InaccessibleDirectories=/home
PrivateTmp=yes

[Install]
WantedBy=multi-user.target
```

7. Enable it, start it and check for the status:

```
sudo systemctl daemon-reload
sudo systemctl enable coturn.service
sudo systemctl start coturn.service
sudo systemctl status coturn.service
```

If the service is active, you can close the SSH session. Otherwise, please look at the coturn project documentation [[1](#references)].


## Reference

[[1](#test-bed)] coturn team, *Coturn TURN server*. 2014. Accessed: May 24, 2024. [Online]. Available: https://github.com/coturn/coturn.