import os
import time
import paho.mqtt.client as mqtt

# MQTT Variables
brokerIP = os.environ.get("MQTT_BROKER", "localhost")
brokerPort = 1883
timeoutSeconds = 5

# Store last received values
last_values = {
    "lightSensor": 0,
    "threshold": 0,
    "LightStatus": None
}

# Subscribe to the same topics we publish to
def on_connect(client, userdata, flags, reason_code, properties):
    print("Connected to broker")

    # Publish "online" status (retained)
    raspiC.publish("Status/RaspberryPiC", "online", qos=2, retain=True)
    
    # Subscribe to topics
    client.subscribe("lightSensor", qos=2)
    client.subscribe("threshold", qos=2)
    client.subscribe("LightStatus", qos=2)

# Save the last values on topic
def on_message(client, userdata, msg):
    topic = msg.topic
    payload = msg.payload.decode()
    
    # Save appropriately
    if topic in ["lightSensor", "threshold"]:
        payload = int(payload)
        last_values[topic] = payload

    # Compare
    comparison = last_values["lightSensor"] < last_values["threshold"]
    if(comparison):
        if(last_values["LightStatus"] != "TurnOn"):
            raspiC.publish("LightStatus", "TurnOn", qos=2, retain=True)
            last_values["LightStatus"] = "TurnOn"
            print("TurnOn")
    else:
        if(last_values["LightStatus"] != "TurnOff"):
            raspiC.publish("LightStatus", "TurnOff", qos=2, retain=True)
            last_values["LightStatus"] = "TurnOff"
            print("TurnOff")

# Create MQTT client
raspiC = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
raspiC.on_connect = on_connect
raspiC.on_message = on_message

# Last Will (retained "offline")
raspiC.will_set("Status/RaspberryPiC", payload="offline", qos=2, retain=True)

# Connect and start background loop
raspiC.connect(brokerIP, brokerPort, timeoutSeconds)
raspiC.loop_start()

# Connect and loop forever
try:
    while True:
        time.sleep(0.1)
finally:
    # Publish "offline" retained status before shutting down
    raspiC.publish("Status/RaspberryPiC", "offline", qos=2, retain=True)
    raspiC.loop_stop()
    raspiC.disconnect()