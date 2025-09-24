import paho.mqtt.client as mqtt

brokerIP = "10.152.53.186"
brokerPort = 1883
timeoutSeconds = 60

# Create a client instance
raspiA = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

# Connect to broker with 
raspiA.connect(brokerIP, brokerPort, timeoutSeconds)

# Publish a message
raspiA.publish("test/topic", "Hello World")

# Disconnect when done
raspiA.disconnect()