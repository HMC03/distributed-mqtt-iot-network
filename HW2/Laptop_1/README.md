## Laptop 1

## Setup
* Install MQTT mosquitto
    ```
    sudo apt update
    sudo apt install mosquitto mosquitto-clients -y
    ```
* Disable so it wont auto start
    ```
    sudo systemctl disable mosquitto
    ```
* Edit config
    ```
    sudo nano /etc/mosquitto/mosquitto.conf
    ```
* Add These Lines
    ```
    listener 1883
    allow_anonymous true
    ```
* Restart MQTT
    ```
    sudo service mosquitto restart
    ```
* Get LAN IP
    ```
    hostname -I
    ```
* Open Powershell as an Administrator
* Enable Port Forwarding
    ```
    netsh interface portproxy add v4tov4 listenport=1883 listenaddress=0.0.0.0 connectport=1883 connectaddress=`insert LAN IP`
    ```
* Firewall Bypass
    ```
    netsh advfirewall firewall add rule name="Mosquitto MQTT" dir=in action=allow protocol=TCP localport=1883
    ```
* Get Broker IP
    ```
    ipconfig
    ```
    Look for: Wireless LAN adapter Wi-Fi: IPv4 Address. . . . . . . . . . . : 10.152.6.37

## Start Broker
* start mosquitto service
    ```
    sudo service mosquitto start
    ```
* open powershell
* share broker ip
    ```
    ipconfig
    ```

## Stop Broker
```
sudo service mosquitto stop
```