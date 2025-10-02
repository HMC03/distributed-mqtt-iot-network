import os
import paho.mqtt.client as mqtt
from datetime import datetime

# --- MQTT Config ---
brokerIP = os.environ.get("MQTT_BROKER", "localhost")
brokerPort = 1883  # default MQTT port

# --- Log Config ---
log_file = "mqtt_messages.log"
max_lines = 500  # keep last N lines

def write_log(message):
    """Append message to log file and trim if too long."""
    with open(log_file, "a+") as f:
        f.write(message + "\n")
    # Trim file if it gets too big
    with open(log_file, "r") as f:
        lines = f.readlines()
    if len(lines) > max_lines:
        with open(log_file, "w") as f:
            f.writelines(lines[-max_lines:])  # keep only last N

# --- MQTT Callbacks ---
def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code == 0:
        print("Connected to broker")
        client.subscribe("#", qos=2)  # Subscribe to all topics at QoS 2
    else:
        print(f"Failed to connect, reason code: {reason_code}")

def on_message(client, userdata, msg):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {msg.topic}: {msg.payload.decode()}"
    print(log_entry)
    write_log(log_entry)

# --- Main ---
laptop2 = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
laptop2.on_connect = on_connect
laptop2.on_message = on_message

try:
    laptop2.connect(brokerIP, brokerPort, keepalive=60)
    laptop2.loop_forever()
except KeyboardInterrupt:
    print("\nDisconnected by user")
    laptop2.disconnect()