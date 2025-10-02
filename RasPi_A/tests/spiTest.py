import spidev
import time

spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 1000000  # 1 MHz

def read_channel(channel):
    adc = spi.xfer2([6 | (channel >> 2), (channel & 3) << 6, 0])
    value = ((adc[1] & 15) << 8) | adc[2]
    return value

while True:
    ch0_val = read_channel(0)  # First analog input
    ch1_val = read_channel(1)  # Second analog input
    print(f"CH0: {ch0_val}, CH1: {ch1_val}")
    time.sleep(0.1)  # Sample every 100 ms
