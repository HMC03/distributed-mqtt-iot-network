# IOT_Projects_ECE592
Repository to contain the IOT group projects in class ECE 592 Internet of Things Applications &amp; Implementation

## HW2
Multi-device IoT network using MQTT. Three Raspberry Pis (or similar boards) and two WiFi-enabled devices communicate via a locally hosted MQTT broker. Raspberry Pi A reads a light sensor and potentiometer and publishes their values. Raspberry Pi C subscribes to these values to determine LED states, while Raspberry Pi B displays LED status and tracks the online/offline state of other devices. All devices coordinate in real time through MQTT topics with retained messages and last-will notifications. 