# Homework 2
This homework introduces MQTT

## MQTT Network
* Laptop 1 (Broker)
* Laptop 2 (Subscriber)
* Raspi A (PUB & SUB)
* Raspi B (SUB)
* Raspi C (PUB & SUB)

## Laptop 1
**Setup**
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

## Raspi A
* Sample LDR & Potentiometer every 100ms
* Compare LDR & Pot. values with prev values every sample
* If diff in value reaches user defined threshold, it publishes those values to Laptop #1
* Uses topic “lightSensor” for LDR
* Users topic “threshold” for potentiometer
* Must subscribe to above topics in order to compare with previous value 
* Every time it publishes, use the retain flag so it can reconnect
* Include a lastwill message with retain flag, content “offline”, topic “Status/RaspberryPiA”
* With every connection to broker, send retain message to “Status/RaspberryPiA” with content “online”

## Raspi B
* Subscribe to “LightStatus”, "Status/RaspberryPiA ", and "Status/RaspberryPiC"
* Connected to LED1, LED2, LED3
* LED1 represents status of main LED (topic “LightStatus”) & default off
* LED2 represents status of Raspi A (topic “Status/RaspberryPiA”)
* LED 3 represents status of Raspi C (topic “Status/RasberryPiC”)

## Raspi C
* Connected to the broker and subscribed to “lightSensor” & “threshold”
* Compares lightsensor value to threshold value after it receives a value from either topic
* If lightSensor >= threshold, then “TurnOn” else “TurnOff (more light = turn off)
* Publish/subscribe result to topic “LightStatus” with retain flag if decision changes
* Lastwill message: retain flag, content “offline”, topic “Status/RasberryPiC”
* With every connection to broker, send content “online” to topic “Status/RasberryPiC”

## Laptop 2
* Subscribe to all topics
* Display messages sent by broker with timestamps
