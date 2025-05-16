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

def open_servo(channel, target_angle=90, step=5, delay=0.02):
    for angle in range(0, target_angle + 1, step):
        pca.channels[channel].duty_cycle = angle_to_duty(angle)
        time.sleep(delay)
    pca.channels[channel].duty_cycle = 0

def close_servo(channel, start_angle=90, step=5, delay=0.02):
    for angle in range(start_angle, -1, -step):
        pca.channels[channel].duty_cycle = angle_to_duty(angle)
        time.sleep(delay)
    pca.channels[channel].duty_cycle = 0
 