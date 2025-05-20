'''
import time
from adafruit_pca9685 import PCA9685
from board import SCL, SDA
import busio

# Set up I2C and PCA9685
i2c = busio.I2C(SCL, SDA)
pca = PCA9685(i2c)
pca.frequency = 50  # SG90 uses 50 Hz

# Convert angle (0–180°) to 16-bit PWM duty cycle
def angle_to_duty(angle):
    min_us = 500    # pulse for 0°
    max_us = 2500   # pulse for 180°
    pulse_us = min_us + (angle / 180.0) * (max_us - min_us)
    duty = int(pulse_us * 65535 / (1000000 / pca.frequency))
    return duty

# Move all servos to a specified angle
def move_all_servos(angle):
    duty = angle_to_duty(angle)
    for ch in range(4):  # channels 0 through 3
        pca.channels[ch].duty_cycle = duty

# Move 0° → 90°
move_all_servos(0)
time.sleep(1)
move_all_servos(90)
time.sleep(1)
move_all_servos(0)

'''

import time
from adafruit_pca9685 import PCA9685
from board import SCL, SDA
import busio

# Set up I2C and PCA9685
i2c = busio.I2C(SCL, SDA)
pca = PCA9685(i2c)
pca.frequency = 50  # 50Hz for SG90 servos

# Function to convert angle to 16-bit duty cycle
def angle_to_duty(angle):
    min_us = 500    # 0° = 500 microseconds
    max_us = 2500   # 180° = 2500 microseconds
    pulse_us = min_us + (angle / 180.0) * (max_us - min_us)
    duty = int(pulse_us * 65535 / (1000000 / pca.frequency))
    return duty

# Function to convert angle to 16-bit duty cycle
def angle_to_duty(angle):
    min_us = 500    # 0° = 500 microseconds
    max_us = 2500   # 180° = 2500 microseconds
    pulse_us = min_us + (angle / 180.0) * (max_us - min_us)
    duty = int(pulse_us * 65535 / (1000000 / pca.frequency))
    return duty

# Move servos on channels 0 to 3
for channel in range(4):
    pca.channels[channel].duty_cycle = angle_to_duty(0)  # Start at 0°
time.sleep(1)

for channel in range(4):
    pca.channels[channel].duty_cycle = angle_to_duty(90)  # Move to 90°

time.sleep(10)

for channel in range(4):
    pca.channels[channel].duty_cycle = angle_to_duty(0)  # Return to 0°


time.sleep(5)

for channel in range(4):
    pca.channels[channel].duty_cycle = angle_to_duty(0)  # Return to 0°
