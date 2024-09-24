###################################
# Static IP addresses reservation #
###################################

# Create a static external IPv4 address for the future STUN TURN server
gcloud compute addresses create stun-turn-static-external-ipv4 --project=[yourproject-ID] --description=STUN\ TURN\ static\ external\ IPv4\ address --network-tier=STANDARD --region=europe-west1
# Create a static external IPv6 address for the future STUN TURN server
gcloud compute addresses create stun-turn-static-external-ipv6 --project=[yourproject-ID] --description=STUN\ TURN\ static\ external\ IPv6\ address. --ip-version=IPV6 --region=europe-west1 --endpoint-type=VM --subnetwork=projects/[yourproject-ID]/regions/europe-west1/subnetworks/default-dualstack-subnet

# Create a static internal IPv4 address for the future STUN-TURN server
gcloud compute addresses create stun-turn-static-internal-ipv4 --project=[yourproject-ID] --description=STUN\ TURN\ static\ internal\ IPv4 --network-tier=STANDARD --region=europe-west1


#############################
# VPC network configuration #
#############################

# Create a VPC Network with subnet (europe-west1) https://cloud.google.com/compute/docs/regions-zones?hl=fr

gcloud compute networks create default-dualstack --project=[yourproject-ID] --description=Default\ IPv4\ \&\ IPv6 --subnet-mode=custom --mtu=1460 --bgp-routing-mode=regional

gcloud compute networks subnets create default-dualstack-subnet --project=[yourproject-ID] --range=10.132.0.0/20 --stack-type=IPV4_IPV6 --ipv6-access-type=EXTERNAL --network=default-dualstack --region=europe-west1


###############
# VM creation #
###############

# Create VM: STUN-TURN
gcloud compute instances create stun-turn-ubuntu-server --project=[yourproject-ID] --zone=europe-west1-d --machine-type=e2-medium --network-interface=address=192.0.2.1,external-ipv6-address=2001:db8::1,external-ipv6-prefix-length=96,network-tier=STANDARD,private-network-ip=10.132.0.8,subnet=default-dualstack-subnet --metadata=ssh-keys=[YOUR_SSH_KEY] [GOOGLE_USERNAME] --maintenance-policy=MIGRATE --provisioning-model=STANDARD --service-account=[SERVICE_ACCOUNT_ID]-compute@developer.gserviceaccount.com --scopes=https://www.googleapis.com/auth/devstorage.read_only,https://www.googleapis.com/auth/logging.write,https://www.googleapis.com/auth/monitoring.write,https://www.googleapis.com/auth/servicecontrol,https://www.googleapis.com/auth/service.management.readonly,https://www.googleapis.com/auth/trace.append --tags=stun-turn-server --create-disk=auto-delete=yes,boot=yes,device-name=stun-turn-ubuntu-server,image=projects/ubuntu-os-cloud/global/images/ubuntu-2204-jammy-v20230421,mode=rw,size=10,type=projects/[yourproject-ID]/zones/europe-west1-d/diskTypes/pd-balanced --no-shielded-secure-boot --shielded-vtpm --shielded-integrity-monitoring --labels=ec-src=vm_add-gcloud --reservation-affinity=any


#########################################
# Cloud NAT and Firewall configurations #
#########################################

# Allow SSH IPv4
gcloud compute --project=[yourproject-ID] firewall-rules create " default-dualstack-allow-ssh" --direction=INGRESS --priority=65534 --network=default-dualstack --action=ALLOW --rules=tcp:22 --source-ranges=0.0.0.0/0
# Allow SSH IPv6
gcloud compute --project=[yourproject-ID] firewall-rules create default-allow-ssh-v6 --direction=INGRESS --priority=65534 --network=default-dualstack --action=ALLOW --rules=tcp:22 --source-ranges=0::0/0


# Allow STUN-TURN IPv4 - Tag "stun-turn-server"
gcloud compute --project=[yourproject-ID] firewall-rules create default-dualstack-allow-stun-turn --direction=INGRESS --priority=65534 --network=default-dualstack --action=ALLOW --rules=tcp:3478,tcp:5349,udp:3478 --source-ranges=0.0.0.0/0 --target-tags=stun-turn-server
# Allow STUN-TURN IPv4 - Tag "stun-turn-server"
gcloud compute --project=[yourproject-ID] firewall-rules create default-dualstack-stun-turn-v6 --direction=INGRESS --priority=65534 --network=default-dualstack --action=ALLOW --rules=tcp:3478,tcp:5349,udp:3478,udp:5349 --source-ranges=0::0/0 --target-tags=stun-turn-server