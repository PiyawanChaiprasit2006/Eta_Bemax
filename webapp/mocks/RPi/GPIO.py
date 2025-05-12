# mocks/RPi/GPIO.py

# Mock GPIO functions for non-Raspberry Pi environments
BCM = "BCM"
OUT = "OUT"
LOW = 0
HIGH = 1

def setwarnings(flag):
    print(f"Mock: GPIO setwarnings({flag})")

def setmode(mode):
    print(f"Mock: GPIO setmode({mode})")

def setup(pin, mode):
    print(f"Mock: GPIO setup(pin={pin}, mode={mode})")

def output(pin, state):
    print(f"Mock: GPIO output(pin={pin}, state={state})")

def cleanup():
    print("Mock: GPIO cleanup()")

class MockPWM:
    def __init__(self, pin, frequency):
        print(f"Mock: PWM initialized on pin {pin} with frequency {frequency} Hz")
    def start(self, duty_cycle):
        print(f"Mock: PWM start with duty cycle {duty_cycle}%")
    def ChangeDutyCycle(self, duty_cycle):
        print(f"Mock: PWM ChangeDutyCycle to {duty_cycle}%")
    def stop(self):
        print("Mock: PWM stopped")

def PWM(pin, frequency):
    return MockPWM(pin, frequency)