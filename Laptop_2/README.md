# Laptop 2

## Role in the System  
Acts as a monitoring client. Subscribes to all MQTT topics and logs/display messages with timestamps for debugging and verification.  

## Venv Setup
```bash
# install venv
sudo apt install python3-venv -y

# create venv
python3 -m venv .venv

# start venv
source .venv/bin/activate

# install dependencies
pip install -r requirements.txt
```
## Run Script
```bash
# source virtual environment
source .venv/bin/activate

# set broker ip environment variable
export MQTT_BROKER=<your-broker-ip>

# execute script
python3 laptop2.py
```