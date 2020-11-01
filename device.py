import time
import RPi.GPIO as GPIO

class my_Device:
    def  __init__(self,pin,IO):
        GPIO.setmode(GPIO.BOARD)
        self.pin = pin
        self.IO = IO
        if IO == "in":
            IO = GPIO.IN
        elif IO == "out":
            IO = GPIO.OUT
        GPIO.setup(self.pin, IO)
    def __str__(self):
        return f"running device on channel {self.pin}"
    def toggle(self,status):
        if status == 1:
            status = GPIO.LOW
        else:
            status = GPIO.HIGH
        GPIO.output(self.pin,status)

    def state(self):
        return "on" if not GPIO.input(self.pin) else "off"
