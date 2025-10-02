# Laptop 1

## Role in the System  
Acts as the **MQTT Broker** for the network. All Raspberry Pis and Laptop 2 connect here to publish and subscribe.  


## Setup
```bash
# install mosquitto
sudo apt update
sudo apt install mosquitto mosquitto-clients -y

# prevent auto-start
sudo systemctl disable mosquitto

# edit configuration
sudo nano /etc/mosquitto/mosquitto.conf

# Add the following lines:
listener 1883
allow_anonymous true

# restart mosquitto
sudo service mosquitto restart

# get LAN IP
hostname -I

# On Windows (PowerShell as Administrator):
# enable port forwarding
netsh interface portproxy add v4tov4 listenport=1883 listenaddress=0.0.0.0 connectport=1883 connectaddress=<LAN-IP>

# allow firewall rule
netsh advfirewall firewall add rule name="Mosquitto MQTT" dir=in action=allow protocol=TCP localport=1883

# confirm broker IP
ipconfig
# Look under Wireless LAN adapter Wi-Fi for the IPv4 Address (e.g., 10.152.6.37).
```

## Start Broker
```bash
sudo service mosquitto start
```

## Stop Broker
```bash
sudo service mosquitto stop
```