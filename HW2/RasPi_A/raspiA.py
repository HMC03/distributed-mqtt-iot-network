import time
import spidev
import paho.mqtt.client as mqtt

# --- MQTT Setup ---
brokerIP = "10.152.53.186"
brokerPort = 1883
timeoutSeconds = 60

# Create MQTT client
raspiA = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

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
        value0 = read_channel(0)
        value1 = read_channel(1)

        # Publish to MQTT
        raspiA.publish("lightSensor", str(value0))
        raspiA.publish("threshold", str(value1))

        print(f"lightSensor: {value0}, threshold: {value1}")

        # Sample every 100ms
        time.sleep(0.1)

except KeyboardInterrupt:
    print("Stopping...")

finally:
    # Publish "offline" retained status before shutting down
    raspiA.publish("Status/RaspberryPiA", "offline", retain=True)
    raspiA.loop_stop()
    raspiA.disconnect()
    spi.close()
