# servo_control.py
import time
import board
import busio
from adafruit_pca9685 import PCA9685

# PCA9685 setup
i2c = busio.I2C(board.SCL, board.SDA)
pca = PCA9685(i2c)
pca.frequency = 50

def angle_to_duty(angle):
    min_us = 500
    max_us = 2500
    pulse_us = min_us + (angle / 180.0) * (max_us - min_us)
    return int(pulse_us * 65535 / (1000000 / pca.frequency))

def move_servo(channel, angle, duration=1):
    if 0 <= channel <= 15:
        pca.channels[channel].duty_cycle = angle_to_duty(angle)
        time.sleep(duration)
        pca.channels[channel].duty_cycle = 0  # Turn off pulse to avoid jitter
    else:
        raise ValueError("Channel must be between 0 and 15")
