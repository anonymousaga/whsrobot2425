import tcs34725
from machine import I2C, Pin
i2c = I2C(1, freq=400000, scl=Pin(3), sda=Pin(2))
print('Scanning i2c bus...')
devices = i2c.scan()
print('I2C devices found:', [hex(device) for device in devices])
sensor = tcs34725.TCS34725(i2c)
sensor.integration_time(2.4)  # Set integration time to 2.4 ms
sensor.gain(4)  # Set gain to 4x
print(sensor.sensor_id())  # Print sensor ID to verify connection
import time
sensor.active(True)
#time.sleep_ms(500)

count=0
while True:
    x=sensor.read()
    print(x)
    #if x > 6500:
    #    print("Light intensity is high", x)
    #    count +=1
