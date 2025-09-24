# Laptop 2

## Venv Setup
* install venv
    ```
    sudo apt install python3-venv -y
    ```
* create venv
    ```
    python3 -m venv .venv
    ```
* start venv
    ```
    source .venv/bin/activate
    ```
* install dependencies
    ```
    pip install -r requirements.txt
    ```

## Run Script
* source virtual environment
    ```
    source .venv/bin/activate
    ```
* set broker ip environment variable
    ```
    export MQTT_BROKER=<your-broker-ip>
    ```
* execute script
    ```
    python3 laptop2.py
    ```