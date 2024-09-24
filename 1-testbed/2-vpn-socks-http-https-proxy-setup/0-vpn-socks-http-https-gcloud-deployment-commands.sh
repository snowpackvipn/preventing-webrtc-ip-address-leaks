###################################
# Static IP addresses reservation #
###################################

# Create a static external IPv4 address for the future vpns-socks-http-https machine
gcloud compute addresses create vpns-socks-http-https-static-external-ipv4 --project=[yourproject-ID] --description=VPNs\ SOCKS\ static\ external\ IPv4\ address --network-tier=STANDARD --region=europe-west1
# Create a static external IPv6 address for the future vpns-socks-http-https machine
gcloud compute addresses create vpns-socks-http-https-static-external-ipv6 --project=[yourproject-ID] --description=VPNs\ SOCKS\ static\ external\ IPv6\ address --ip-version=IPV6 --region=europe-west1 --endpoint-type=VM --subnetwork=projects/[yourproject-ID]/regions/europe-west1/subnetworks/default-dualstack-subnet


#############################
# VPC network configuration #
#############################

# Create a VPC Network with subnet (europe-west1) https://cloud.google.com/compute/docs/regions-zones?hl=fr

gcloud compute networks create default-dualstack --project=[yourproject-ID] --description=Default\ IPv4\ \&\ IPv6 --subnet-mode=custom --mtu=1460 --bgp-routing-mode=regional

gcloud compute networks subnets create default-dualstack-subnet --project=[yourproject-ID] --range=10.132.0.0/20 --stack-type=IPV4_IPV6 --ipv6-access-type=EXTERNAL --network=default-dualstack --region=europe-west1


###############
# VM creation #
###############

# Create VM: vpns-socks-http-https
gcloud compute instances create vpns-socks-http-https-ubuntu-server --project=[yourproject-ID] --zone=europe-west1-d --machine-type=e2-medium --network-interface=address=198.51.100.1,external-ipv6-address=2001:db8::2,external-ipv6-prefix-length=96,network-tier=STANDARD,private-network-ip=192.168.1.91,subnet=default-dualstack-subnet --metadata=ssh-keys=[YOUR_SSH_KEY] [GOOGLE_USERNAME] --maintenance-policy=MIGRATE --provisioning-model=STANDARD --service-account=[SERVICE_ACCOUNT_ID]-compute@developer.gserviceaccount.com --scopes=https://www.googleapis.com/auth/devstorage.read_only,https://www.googleapis.com/auth/logging.write,https://www.googleapis.com/auth/monitoring.write,https://www.googleapis.com/auth/servicecontrol,https://www.googleapis.com/auth/service.management.readonly,https://www.googleapis.com/auth/trace.append --tags=vpns-socks-http-https,http-server,https-server --create-disk=auto-delete=yes,boot=yes,device-name=vpns-socks-http-https-ubuntu-server,image=projects/ubuntu-os-cloud/global/images/ubuntu-2204-jammy-v20230421,mode=rw,size=10,type=projects/[yourproject-ID]/zones/europe-west1-d/diskTypes/pd-balanced --no-shielded-secure-boot --shielded-vtpm --shielded-integrity-monitoring --labels=ec-src=vm_add-gcloud --reservation-affinity=any

#########################################
# Cloud NAT and Firewall configurations #
#########################################

# Allow SSH IPv4
gcloud compute --project=[yourproject-ID] firewall-rules create " default-dualstack-allow-ssh" --direction=INGRESS --priority=65534 --network=default-dualstack --action=ALLOW --rules=tcp:22 --source-ranges=0.0.0.0/0
# Allow SSH IPv6
gcloud compute --project=[yourproject-ID] firewall-rules create default-allow-ssh-v6 --direction=INGRESS --priority=65534 --network=default-dualstack --action=ALLOW --rules=tcp:22 --source-ranges=0::0/0


# Allow VPNs (OpenVPN UDP, WireGuard) IPv4 - Tag "vpns-socks-http-https"
gcloud compute --project=[yourproject-ID] firewall-rules create default-dualstack-openvpn-ipsec-wireguard --direction=INGRESS --priority=65534 --network=default-dualstack --action=ALLOW --rules=udp:1194,udp:2050 --source-ranges=0.0.0.0/0 --target-tags=vpns-socks-http-https
# Allow VPNs (OpenVPN UDP, WireGuard) IPv6 - Tag "vpns"
gcloud compute --project=[yourproject-ID] firewall-rules create default-dualstack-openvpn-ipsec-wireguard-v6 --direction=INGRESS --priority=65534 --network=default-dualstack --action=ALLOW --rules=udp:1194,udp:2050 --source-ranges=0::0/0 --target-tags=vpns-socks-http-https


# Allow SOCKS IPv4 - Tag "vpns-socks-http-https"
gcloud compute --project=[yourproject-ID] firewall-rules create default-dualstack-openvpn-ipsec-wireguard --direction=INGRESS --priority=65534 --network=default-dualstack --action=ALLOW --rules=tcp:1080 --source-ranges=0.0.0.0/0 --target-tags=vpns-socks-http-https
# Allow SOCKS IPv6 - Tag "vpns-socks-http-https"
gcloud compute --project=[yourproject-ID] firewall-rules create default-dualstack-openvpn-ipsec-wireguard-v6 --direction=INGRESS --priority=65534 --network=default-dualstack --action=ALLOW --rules=tcp:1080 --source-ranges=0::0/0 --target-tags=vpns-socks-http-https


# Allow HTTP-HTTPS proxy IPv4 - Tag "vpns-socks-http-https"
gcloud compute --project=[yourproject-ID] firewall-rules create default-dualstack-openvpn-ipsec-wireguard --direction=INGRESS --priority=65534 --network=default-dualstack --action=ALLOW --rules=udp:8081,tcp:8081 --source-ranges=0.0.0.0/0 --target-tags=vpns-socks-http-https
# Allow HTTP-HTTPS proxy IPv6 - Tag "vpns-socks-http-https"
gcloud compute --project=[yourproject-ID] firewall-rules create default-dualstack-openvpn-ipsec-wireguard-v6 --direction=INGRESS --priority=65534 --network=default-dualstack --action=ALLOW --rules=udp:8081,tcp:8081 --source-ranges=0::0/0 --target-tags=vpns-socks-http-https
