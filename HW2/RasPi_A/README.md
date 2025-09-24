# RasPi A

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

## SPI Setup
* Open the firmware config file
    ```
    sudo nano /boot/firmware/config.txt
    ```
* Scroll to the bottom and add this line:
    ```
    dtoverlay=spi0-1cs
    ```
* Reboot
    ```
    sudo reboot
    ```
* After reboot, check devices
    ```
    ls /dev/spi*
    ```
    You should now see:
    ```
    /dev/spidev0.0
    ```