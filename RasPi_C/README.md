# RasPi C

## Role in the System  
Acts as a decision node. Compares sensor values from RasPi A against the threshold and publishes LED control commands.  
- Subscribes to `lightSensor` and `threshold`.  
- Publishes to `LightStatus` with retained messages.  
- Includes online/offline status via last-will notifications.  

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
python3 raspiC.py
```