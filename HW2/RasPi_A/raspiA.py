import os
import time
import spidev
import paho.mqtt.client as mqtt

# MQTT Variables
brokerIP = os.environ.get("MQTT_BROKER", "localhost")
brokerPort = 1883
timeoutSeconds = 60

# Minimum change in sensor value required to publish it
minDiff = 30

# Store last received values
last_values = {
    "lightSensor": 0,
    "threshold": 0
}

# Subscribe to the same topics we publish to
def on_connect(client, userdata, flags, reason_code, properties):
    print("Connected to broker")
    
    client.subscribe("lightSensor")
    client.subscribe("threshold")

# Save the last values on topic
def on_message(client, userdata, msg):
    topic = msg.topic
    payload = int(msg.payload.decode())
    if topic in last_values:
        last_values[topic] = payload

# Create MQTT client
raspiA = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
raspiA.on_connect = on_connect
raspiA.on_message = on_message

# Last Will (retained "offline")
raspiA.will_set("Status/RaspberryPiA", payload="offline", retain=True)

# Connect to broker
raspiA.connect(brokerIP, brokerPort, timeoutSeconds)

# Publish "online" status (retained)
raspiA.publish("Status/RaspberryPiA", "online", retain=True)

# Start loop in background so MQTT stays alive
raspiA.loop_start()

# --- SPI Setup (MCP3208) ---
spi = spidev.SpiDev()
spi.open(0, 0)            # Bus 0, Device 0 (CE0)
spi.max_speed_hz = 1000000

def read_channel(channel):
    """Read MCP3208 channel (0-7)."""
    if not 0 <= channel <= 7:
        raise ValueError("MCP3208 channel must be 0-7")
    adc = spi.xfer2([6 | (channel >> 2), (channel & 3) << 6, 0])
    value = ((adc[1] & 15) << 8) | adc[2]
    return value

# --- Main Loop ---
try:
    while True:
        # Read from channel 0 and 1
        lightSensor = read_channel(0)
        threshold = read_channel(1)

        # Update lightSensor Value
        if(abs(last_values["lightSensor"] - lightSensor) > minDiff):
            raspiA.publish("lightSensor", str(lightSensor), retain=True)
            print("lightSensor: ", lightSensor)

        # Update threshold Value
        if(abs(last_values["threshold"] - threshold) > minDiff):
            raspiA.publish("threshold", str(threshold), retain=True)
            print("threshold: ", threshold)

        # Sample every 100ms
        time.sleep(0.1)

finally:
    # Publish "offline" retained status before shutting down
    raspiA.publish("Status/RaspberryPiA", "offline", retain=True)
    raspiA.loop_stop()
    raspiA.disconnect()
    spi.close()
