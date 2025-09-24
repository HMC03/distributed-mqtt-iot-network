import paho.mqtt.client as mqtt

brokerIP = "10.152.53.186"
brokerPort = 1883
timeoutSeconds = 60

# Create a client instance
raspiA = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

# Set Last Will message (sent if client disconnects unexpectedly)
# Retained so others always see the last status
raspiA.will_set("Status/RaspberryPiA", payload="offline", retain=True)

# Connect to broker
raspiA.connect(brokerIP, brokerPort, timeoutSeconds)

# As soon as connected, publish "online" as a retained message
raspiA.publish("Status/RaspberryPiA", "online", retain=True)

# Example: also publish Hello World as a retained message
raspiA.publish("test/topic", "Hello World", retain=True)

# Disconnect cleanly
raspiA.disconnect()
