# #############################################################
# # Study 1 - Leaks in popular natively executed web browsers #
# #############################################################

cd host-native-version &&

# python .\main.py --host-platform windows --web-browser firefox --study 1 &&
# python .\main.py --host-platform windows --web-browser chrome --study 1 &&
# python .\main.py --host-platform windows --web-browser edge --study 1 &&
# python .\main.py --host-platform windows --web-browser opera --study 1 &&
# python .\main.py --host-platform windows --web-browser brave --study 1 &&

# ####################################################################
# # Study 2 - Leaks in different configurations of a vanilla Firefox #
# ####################################################################

# # Native execution of a vanilla Firefox in different configurations
# python .\main.py --host-platform windows --web-browser firefox --study 2 &&
# python .\main.py --host-platform windows --web-browser firefox --study 2 --proxy socks --ip 4 &&
# python .\main.py --host-platform windows --web-browser firefox --study 2 --proxy socks --ip 6 &&

# python .\main.py --host-platform windows --web-browser firefox --study 2 --proxy http-https --ip 4 &&
# python .\main.py --host-platform windows --web-browser firefox --study 2 --proxy http-https --ip 6 &&

# Write-Host "Please connect to OpenVPN UDP in IPv4 then press enter to continue." &&
# Read-Host &&
# python .\main.py --host-platform windows --web-browser firefox --study 2 --proxy openvpn --ip 4 &&
# Write-Host "Please disconnect OpenVPN UDP IPv4 and connect to OpenVPN UDP in IPv6 then press enter to continue." &&
# Read-Host &&
# python .\main.py --host-platform windows --web-browser firefox --study 2 --proxy openvpn --ip 6 &&

# Write-Host "Please disconnect OpenVPN UDP IPv6 and connect to WireGuard in IPv4 then press enter to continue." &&
# Read-Host &&
# python .\main.py --host-platform windows --web-browser firefox --study 2 --proxy wireguard --ip 4 &&
# Write-Host "Please disconnect WireGuard IPv4 and connect to WireGuard in IPv6 then press enter to continue." &&
# Read-Host &&
# python .\main.py --host-platform windows --web-browser firefox --study 2 --proxy wireguard --ip 6 &&
# Write-Host "Please disconnect WireGuard IPv6 then press enter to continue." &&
# Read-Host &&

cd ..\docker-wayland-version &&

# # Wayland Containerised execution of a vanilla Firefox in different configurations
# Write-Host "Please close Docker Desktop, do 'wsl --shutdown', start Docker Desktop, attach the camera 'usbipd attach --wsl --busid 2-6', do 'wsl --distribution docker-desktop' and 'chown 1000:1000 /dev/video0' and 'exit'" &&
# Read-Host &&
# python .\main.py --host-platform windows --web-browser firefox --study 2 --web-browser-containerised --container-window-manager wayland &&

# python .\main.py --host-platform windows --web-browser firefox --study 2 --proxy socks --ip 4 --web-browser-containerised --container-window-manager wayland &&

# python .\main.py --host-platform windows --web-browser firefox --study 2 --proxy http-https --ip 4 --web-browser-containerised --container-window-manager wayland &&

# Write-Host "Please connect to OpenVPN UDP in IPv4 then press enter to continue." &&
# Read-Host &&
# Write-Host "Please close Docker Desktop, do 'wsl --shutdown', start Docker Desktop, attach the camera 'usbipd attach --wsl --busid 2-6', do 'wsl --distribution docker-desktop' and 'chown 1000:1000 /dev/video0' and 'exit'" &&
# Read-Host &&
# python .\main.py --host-platform windows --web-browser firefox --study 2 --proxy openvpn --ip 4 --web-browser-containerised --container-window-manager wayland &&
# Write-Host "Please disconnect OpenVPN UDP IPv4 and connect to WireGuard in IPv4 then press enter to continue." &&
# Read-Host &&
# Write-Host "Please close Docker Desktop, do 'wsl --shutdown', start Docker Desktop" &&
# Read-Host &&
# python .\main.py --host-platform windows --web-browser firefox --study 2 --proxy wireguard --ip 4 --web-browser-containerised --container-window-manager wayland &&
# Write-Host "Please disconnect WireGuard IPv4 then press enter to continue." &&
# Read-Host &&

cd ..\docker-x-version &&

# X Containerised execution of a vanilla Firefox in different configurations
Write-Host "Please close Docker Desktop, do 'wsl --shutdown', start Docker Desktop, attach the camera 'usbipd attach --wsl --busid 2-6', do 'wsl --distribution docker-desktop' and 'chown 1000:1000 /dev/video0' and 'exit'" &&
Read-Host &&
python .\main.py --host-platform windows --web-browser firefox --study 2 --web-browser-containerised --container-window-manager x &&

python .\main.py --host-platform windows --web-browser firefox --study 2 --proxy socks --ip 4 --web-browser-containerised --container-window-manager x &&

python .\main.py --host-platform windows --web-browser firefox --study 2 --proxy http-https --ip 4 --web-browser-containerised --container-window-manager x &&

Write-Host "Please connect to OpenVPN UDP in IPv4 then press enter to continue." &&
Read-Host &&
Write-Host "Please close Docker Desktop, do 'wsl --shutdown', start Docker Desktop, attach the camera 'usbipd attach --wsl --busid 2-6', do 'wsl --distribution docker-desktop' and 'chown 1000:1000 /dev/video0' and 'exit'" &&
Read-Host &&
python .\main.py --host-platform windows --web-browser firefox --study 2 --proxy openvpn --ip 4 --web-browser-containerised --container-window-manager x &&

Write-Host "Please disconnect OpenVPN UDP IPv4 and connect to WireGuard in IPv4 then press enter to continue." &&
Read-Host &&
Write-Host "Please close Docker Desktop, do 'wsl --shutdown' and start Docker Desktop" &&
Read-Host &&
python .\main.py --host-platform windows --web-browser firefox --study 2 --proxy wireguard --ip 4 --web-browser-containerised --container-window-manager x &&
Write-Host "Please disconnect WireGuard IPv4 then press enter to continue." &&
Read-Host &&


########################################################################
# Study 3 - Leaks in different configurations of a compromised Firefox #
########################################################################

# Native execution of a compromised Firefox in different configurations
cd ..\host-native-version &&

python .\main.py --host-platform windows --web-browser firefox --study 3 &&
python .\main.py --host-platform windows --web-browser firefox --study 3 --proxy socks --ip 4 &&
python .\main.py --host-platform windows --web-browser firefox --study 3 --proxy socks --ip 6 &&

python .\main.py --host-platform windows --web-browser firefox --study 3 --proxy http-https --ip 4 &&
python .\main.py --host-platform windows --web-browser firefox --study 3 --proxy http-https --ip 6 &&

Write-Host "Please connect to OpenVPN UDP in IPv4 then press enter to continue." &&
Read-Host &&
python .\main.py --host-platform windows --web-browser firefox --study 3 --proxy openvpn --ip 4 &&
Write-Host "Please disconnect OpenVPN UDP IPv4 and connect to OpenVPN UDP in IPv6 then press enter to continue." &&
Read-Host &&
python .\main.py --host-platform windows --web-browser firefox --study 3 --proxy openvpn --ip 6 &&

Write-Host "Please disconnect OpenVPN UDP IPv6 and connect to WireGuard in IPv4 then press enter to continue." &&
Read-Host &&
python .\main.py --host-platform windows --web-browser firefox --study 3 --proxy wireguard --ip 4 &&
Write-Host "Please disconnect WireGuard IPv4 and connect to WireGuard in IPv6 then press enter to continue." &&
Read-Host &&
python .\main.py --host-platform windows --web-browser firefox --study 3 --proxy wireguard --ip 6 &&
Write-Host "Please disconnect WireGuard IPv6 then press enter to continue." &&
Read-Host &&

cd ..\docker-wayland-version &&

# Wayland Containerised execution of a compromised Firefox in different configurations
Write-Host "Please close Docker Desktop, do 'wsl --shutdown', start Docker Desktop, attach the camera 'usbipd attach --wsl --busid 2-6', do 'wsl --distribution docker-desktop' and 'chown 1000:1000 /dev/video0' and 'exit'" &&
Read-Host &&
python .\main.py --host-platform windows --web-browser firefox --study 3 --web-browser-containerised --container-window-manager wayland &&

python .\main.py --host-platform windows --web-browser firefox --study 3 --proxy socks --ip 4 --web-browser-containerised --container-window-manager wayland &&

python .\main.py --host-platform windows --web-browser firefox --study 3 --proxy http-https --ip 4 --web-browser-containerised --container-window-manager wayland &&

Write-Host "Please connect to OpenVPN UDP in IPv4 then press enter to continue." &&
Read-Host &&
Write-Host "Please close Docker Desktop, do 'wsl --shutdown', start Docker Desktop, attach the camera 'usbipd attach --wsl --busid 2-6', do 'wsl --distribution docker-desktop' and 'chown 1000:1000 /dev/video0' and 'exit'" &&
Read-Host &&
python .\main.py --host-platform windows --web-browser firefox --study 3 --proxy openvpn --ip 4 --web-browser-containerised --container-window-manager wayland &&
Write-Host "Please disconnect OpenVPN UDP IPv4 and connect to WireGuard in IPv4 then press enter to continue." &&
Read-Host &&
Write-Host "Please close Docker Desktop, do 'wsl --shutdown' and start Docker Desktop" &&
Read-Host &&
python .\main.py --host-platform windows --web-browser firefox --study 3 --proxy wireguard --ip 4 --web-browser-containerised --container-window-manager wayland &&
Write-Host "Please disconnect WireGuard IPv4 then press enter to continue." &&
Read-Host &&



cd ..\docker-x-version &&

# Containerised execution of a compromised Firefox in different configurations
Write-Host "Please close Docker Desktop, do 'wsl --shutdown', start Docker Desktop, attach the camera 'usbipd attach --wsl --busid 2-6', do 'wsl --distribution docker-desktop' and 'chown 1000:1000 /dev/video0' and 'exit'" &&
Read-Host &&
python .\main.py --host-platform windows --web-browser firefox --study 3 --web-browser-containerised --container-window-manager x &&

python .\main.py --host-platform windows --web-browser firefox --study 3 --proxy socks --ip 4 --web-browser-containerised --container-window-manager x &&

python .\main.py --host-platform windows --web-browser firefox --study 3 --proxy http-https --ip 4 --web-browser-containerised --container-window-manager x &&

Write-Host "Please connect to OpenVPN UDP in IPv4 then press enter to continue." &&
Read-Host &&
Write-Host "Please close Docker Desktop, do 'wsl --shutdown', start Docker Desktop, attach the camera 'usbipd attach --wsl --busid 2-6', do 'wsl --distribution docker-desktop' and 'chown 1000:1000 /dev/video0' and 'exit'" &&
Read-Host &&
python .\main.py --host-platform windows --web-browser firefox --study 3 --proxy openvpn --ip 4 --web-browser-containerised --container-window-manager x

Write-Host "Please disconnect OpenVPN UDP IPv4 and connect to WireGuard in IPv4 then press enter to continue." &&
Read-Host &&
Write-Host "Please close Docker Desktop, do 'wsl --shutdown' and start Docker Desktop" &&
Read-Host &&
python .\main.py --host-platform windows --web-browser firefox --study 3 --proxy wireguard --ip 4 --web-browser-containerised --container-window-manager x &&
Write-Host "Please disconnect WireGuard IPv4 then press enter to continue." &&
Read-Host
