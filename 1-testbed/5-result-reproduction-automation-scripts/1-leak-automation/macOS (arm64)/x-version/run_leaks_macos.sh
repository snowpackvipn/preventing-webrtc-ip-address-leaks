#!/bin/sh

#############################################################
# Study 1 - Leaks in popular natively executed web browsers #
#############################################################
python ./main.py --host-platform macos --web-browser safari --study 1 &&
python ./main.py --host-platform macos --web-browser firefox --study 1 &&
python ./main.py --host-platform macos --web-browser chrome --study 1 &&
python ./main.py --host-platform macos --web-browser edge --study 1 &&
python ./main.py --host-platform macos --web-browser opera --study 1 &&
python ./main.py --host-platform macos --web-browser brave --study 1

####################################################################
# Study 2 - Leaks in different configurations of a vanilla Firefox #
####################################################################

Native execution of a vanilla Firefox in different configurations
python ./main.py --host-platform macos --web-browser firefox --study 2 &&
python ./main.py --host-platform macos --web-browser firefox --study 2 --proxy socks --ip 4 &&
python ./main.py --host-platform macos --web-browser firefox --study 2 --proxy socks --ip 6 &&

python ./main.py --host-platform macos --web-browser firefox --study 2 --proxy http-https --ip 4 &&
python ./main.py --host-platform macos --web-browser firefox --study 2 --proxy http-https --ip 6 &&

printf "%s " "Please connect to OpenVPN UDP in IPv4 then press enter to continue." &&
read ans &&
python ./main.py --host-platform macos --web-browser firefox --study 2 --proxy openvpn --ip 4 &&
printf "%s " "Please disconnect OpenVPN UDP IPv4 and connect to OpenVPN UDP in IPv6 then press enter to continue." &&
read ans &&
python ./main.py --host-platform macos --web-browser firefox --study 2 --proxy openvpn --ip 6 &&

printf "%s " "Please disconnect OpenVPN UDP IPv6 and connect to WireGuard in IPv4 then press enter to continue." &&
read ans &&
python ./main.py --host-platform macos --web-browser firefox --study 2 --proxy wireguard --ip 4 &&
printf "%s " "Please disconnect WireGuard IPv4 and connect to WireGuard in IPv6 then press enter to continue." &&
read ans &&
python ./main.py --host-platform macos --web-browser firefox --study 2 --proxy wireguard --ip 6 &&
printf "%s " "Please disconnect WireGuard IPv6 then press enter to continue." &&
read ans &&

# Containerised execution of a vanilla Firefox in different configurations
printf "%s " "Please start Docker Desktop." &&
read ans &&
python ./main.py --host-platform macos --web-browser firefox --study 2 --web-browser-containerised --container-window-manager x &&

python ./main.py --host-platform macos --web-browser firefox --study 2 --proxy socks --ip 4 --web-browser-containerised --container-window-manager x &&

python ./main.py --host-platform macos --web-browser firefox --study 2 --proxy http-https --ip 4 --web-browser-containerised --container-window-manager x &&

printf "%s " "Please connect to OpenVPN UDP in IPv4 then press enter to continue." &&
read ans &&
python ./main.py --host-platform macos --web-browser firefox --study 2 --proxy openvpn --ip 4 --web-browser-containerised --container-window-manager x &&
printf "%s " "Please disconnect OpenVPN UDP IPv4 and connect to WireGuard in IPv4 then press enter to continue." &&
read ans &&

python ./main.py --host-platform macos --web-browser firefox --study 2 --proxy wireguard --ip 4 --web-browser-containerised --container-window-manager x &&
printf "%s " "Please disconnect WireGuard IPv4 then press enter to continue." &&
read ans &&


########################################################################
# Study 3 - Leaks in different configurations of a compromised Firefox #
########################################################################

# Native execution of a compromised Firefox in different configurations
printf "%s " "Please close Docker Desktop." &&
read ans &&
python ./main.py --host-platform macos --web-browser firefox --study 3 &&
python ./main.py --host-platform macos --web-browser firefox --study 3 --proxy socks --ip 4 &&
python ./main.py --host-platform macos --web-browser firefox --study 3 --proxy socks --ip 6 &&

python ./main.py --host-platform macos --web-browser firefox --study 3 --proxy http-https --ip 4 &&
python ./main.py --host-platform macos --web-browser firefox --study 3 --proxy http-https --ip 6 &&

printf "%s " "Please connect to OpenVPN UDP in IPv4 then press enter to continue." &&
read ans &&
python ./main.py --host-platform macos --web-browser firefox --study 3 --proxy openvpn --ip 4 &&
printf "%s " "Please disconnect OpenVPN UDP IPv4 and connect to OpenVPN UDP in IPv6 then press enter to continue." &&
read ans &&
python ./main.py --host-platform macos --web-browser firefox --study 3 --proxy openvpn --ip 6 &&

printf "%s " "Please disconnect OpenVPN UDP IPv6 and connect to WireGuard in IPv4 then press enter to continue." &&
read ans &&
python ./main.py --host-platform macos --web-browser firefox --study 3 --proxy wireguard --ip 4 &&
printf "%s " "Please disconnect WireGuard IPv4 and connect to WireGuard in IPv6 then press enter to continue." &&
read ans &&
python ./main.py --host-platform macos --web-browser firefox --study 3 --proxy wireguard --ip 6 &&
printf "%s " "Please disconnect WireGuard IPv6 then press enter to continue." &&
read ans &&

# Containerised execution of a compromised Firefox in different configurations
printf "%s " "Please start Docker Desktop." &&
read ans &&
python ./main.py --host-platform macos --web-browser firefox --study 3 --web-browser-containerised --container-window-manager x &&

python ./main.py --host-platform macos --web-browser firefox --study 3 --proxy socks --ip 4 --web-browser-containerised --container-window-manager x &&

python ./main.py --host-platform macos --web-browser firefox --study 3 --proxy http-https --ip 4 --web-browser-containerised --container-window-manager x &&

printf "%s " "Please connect to OpenVPN UDP in IPv4 then press enter to continue." &&
read ans &&
python ./main.py --host-platform macos --web-browser firefox --study 3 --proxy openvpn --ip 4 --web-browser-containerised --container-window-manager x &&
printf "%s " "Please disconnect OpenVPN UDP IPv4 and connect to WireGuard in IPv4 then press enter to continue." &&
read ans &&
python ./main.py --host-platform macos --web-browser firefox --study 3 --proxy wireguard --ip 4 --web-browser-containerised --container-window-manager x &&
printf "%s " "Please disconnect WireGuard IPv4 then press enter to continue." &&
read ans &&
printf "%s " "Please close Docker Desktop." &&
read ans
