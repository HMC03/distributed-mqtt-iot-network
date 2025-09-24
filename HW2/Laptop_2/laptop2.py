import os
import paho.mqtt.client as mqtt
from datetime import datetime

BROKER = os.environ.get("MQTT_BROKER", "localhost")
brokerPort = 1883            # default MQTT port

# Handle connection
def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code == 0:
        print("Connected to broker")
        # Subscribe to all topics
        client.subscribe("#")
    else:
        print(f"Failed to connect, reason code: {reason_code}")

# Handle incoming messages
def on_message(client, userdata, msg):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {msg.topic}: {msg.payload.decode()}")

# Create MQTT client
laptop2 = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
laptop2.on_connect = on_connect
laptop2.on_message = on_message

# Connect and loop forever
try:
    laptop2.connect(BROKER, brokerPort, keepalive=60)
    laptop2.loop_forever()
except KeyboardInterrupt:
    print("\nDisconnected by user")
    laptop2.disconnect()
