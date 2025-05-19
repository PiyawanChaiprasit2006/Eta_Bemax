import time

try:
    import board
    import busio
    from adafruit_pca9685 import PCA9685
    from adafruit_motor import servo
    IS_RPI = True
except (ImportError, NotImplementedError):
    print("Mock: Skipping hardware modules (non-RPi system)")
    board = None
    busio = None
    PCA9685 = None
    servo = None
    IS_RPI = False

# PCA9685 setup or mock
if IS_RPI:
    i2c = busio.I2C(board.SCL, board.SDA)
    pca = PCA9685(i2c)
    pca.frequency = 50
else:
    class MockChannel:
        def __init__(self): self.duty_cycle = 0
        def __setitem__(self, index, value): print(f"Mock: set servo[{index}] = {value}")
    class MockPCA:
        def __init__(self): self.channels = [MockChannel() for _ in range(16)]
    pca = MockPCA()

# Helper: Convert angle to duty cycle
def angle_to_duty(angle):
    min_us = 500
    max_us = 2500
    pulse_us = min_us + (angle / 180.0) * (max_us - min_us)
    return int(pulse_us * 65535 / (1000000 / 50))  # Assuming 50Hz

# Open servos to given angle
def open_all_servos(channels, target_angle=90, step=5, delay=0.02):
    for angle in range(0, target_angle + 1, step):
        for ch in channels:
            pca.channels[ch].duty_cycle = angle_to_duty(angle)
        time.sleep(delay)
    for ch in channels:
        pca.channels[ch].duty_cycle = 0

# Close servos back to 0
def close_all_servos(channels, start_angle=90, step=5, delay=0.02):
    for angle in range(start_angle, -1, -step):
        for ch in channels:
            pca.channels[ch].duty_cycle = angle_to_duty(angle)
        time.sleep(delay)
    for ch in channels:
        pca.channels[ch].duty_cycle = 0