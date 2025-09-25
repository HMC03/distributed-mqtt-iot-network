"""
Raspberry Pi B - LED Controller
Controls 3 LEDs based on light status and device status from other Raspberry Pi's
"""

import paho.mqtt.client as mqtt
from gpiozero import LED
import time

BROKER_HOST = "10.152.53.186" # Change to your broker's IP address'
BROKER_PORT = 1883 # Default port
timeoutSeconds = 60
CLIENT_ID = "RaspberryPiB"

# Topics
LIGHT_STATUS_TOPIC = "LightStatus"
STATUS_A_TOPIC = "Status/RaspberryPiA"
STATUS_C_TOPIC = "Status/RaspberryPiC"

# Change pins to match your setup
LED1_PIN = 21
LED2_PIN = 20
LED3_PIN = 16

class RaspberryPiB:
    def __init__(self):
        # Initialize LEDs
        self.led1 = LED(LED1_PIN)
        self.led2 = LED(LED2_PIN)
        self.led3 = LED(LED3_PIN)

        # Start LEDs off
        self.led1.off()
        self.led2.off()
        self.led3.off()

        # Status tracker
        self.piA_status = False
        self.piC_status = False
        self.last_light_status = None

        # MQTT Client Setup
        self.client = mqtt.Client(CLIENT_ID)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

    def on_connect(self, client, userdata, flags, rc):
        # Subscribe to topics
        client.subscribe(LIGHT_STATUS_TOPIC, qos=2)
        client.subscribe(STATUS_A_TOPIC, qos=2)
        client.subscribe(STATUS_C_TOPIC, qos=2)

    def on_message(self, client, userdata, msg):
        # Handle messages and control LEDs
        try :
            topic = msg.topic
            message = msg.payload.decode("utf-8") # Convert bytes to string

            print(f"Received message on topic {topic}: {message}")

            if topic == LIGHT_STATUS_TOPIC:
                self.handle_light_status(message)
            elif topic == STATUS_A_TOPIC:
                self.handle_status_a(message)
            elif topic == STATUS_C_TOPIC:
                self.handle_status_c(message)
        except Exception as e:
            print(f"Error handling message: {e}")

    def handle_light_status(self, status):
        # Handle LightStatus messages
        self.last_light_status = status

        if self.piC_status:
            if status == "TurnOn":
                self.led1.on()
                print("Light is on - LED1 on")
            elif status == "TurnOff":
                self.led1.off()
                print("Light is off - LED1 off")
        else:
            self.led1.off()
            print("LightStatus message received but C is offline - LED1 off")

    def handle_status_a(self, status):
        # Handle Raspberry Pi A messages
        if status == "online":
            self.piA_status = True
            self.led2.on()
            print("Raspberry Pi A is online - LED2 on")
        elif status == "offline":
            self.piA_status = False
            self.led2.off()
            print("Raspberry Pi A is offline - LED2 off")

    def handle_status_c(self, status):
        # Handle Raspberry Pi C messages
        if status == "online":
            self.piC_status = True
            self.led3.on()
            print("Raspberry Pi C is online - LED3 on")

            if self.last_light_status == "TurnOn" or self.last_light_status == "TurnOff":
                self.handle_light_status(self.last_light_status)
            else:
                self.led1.off()
                print("No LightStatus message available - LED1 off")
        elif status == "offline":
            self.piC_status = False
            self.led1.off()
            self.led3.off()
            print(self.last_light_status)
            print("Raspberry Pi C is offline - LED1 and LED3 off")

    def run(self):
        try:
            print("Starting Raspberry Pi B client...")
            self.client.connect(BROKER_HOST, BROKER_PORT, timeoutSeconds)

            print("Message ready to receives!")
            self.client.loop_forever()
        except KeyboardInterrupt:
            print("\nShutting down...")
        finally:
            self.led1.off()
            self.led2.off()
            self.led3.off()
            self.client.loop_stop()
            self.client.disconnect()

if __name__ == "__main__":
    rpiB = RaspberryPiB()
    rpiB.run()