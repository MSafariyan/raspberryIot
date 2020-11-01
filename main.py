import RPi.GPIO as GPIO
import time
relay_channel = 11
moisture_channel = 40
GPIO.setmode(GPIO.BOARD)
GPIO.setup(relay_channel, GPIO.OUT)
GPIO.setup(moisture_channel, GPIO.IN)
GPIO.output(relay_channel, GPIO.HIGH)


def pumpOn():
    GPIO.output(relay_channel, GPIO.LOW)
    print("pump is on.")

def pumpOff():
    GPIO.output(relay_channel, GPIO.HIGH)
    print("pump is off")

def Pump():
    pumpOff()
    if GPIO.input(moisture_channel):
        pumpOn()
        time.sleep(5)
        pumpOff()
    else:
        pumpOff()

Pump()

