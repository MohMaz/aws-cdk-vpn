sudo apt update
sudo apt-get remove docker docker-engine docker.io containerd runc

sudo apt-get install -y \
    ca-certificates \
    curl \
    gnupg \
    lsb-release

curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io

sudo groupadd docker
sudo usermod -aG docker $USER


# openvpn --genkey --secret ta.key
# wget https://github.com/OpenVPN/easy-rsa/releases/download/v3.0.8/EasyRSA-3.0.8.tgz

docker run --rm -it \
  --name=openvpn-client \
  --cap-add=NET_ADMIN \
  --device=/dev/net/tun \
  --env KILL_SWITCH=off \
  --volume ${PWD}/openvpn-config/:/data/vpn \
  ghcr.io/wfg/openvpn-client  