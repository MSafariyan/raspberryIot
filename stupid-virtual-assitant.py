#!/usr/bin/env python3
from vosk import Model, KaldiRecognizer
import pyaudio
import json
import RPi.GPIO as GPIO

relay_channel = 11
moisture_channel = 40
status = ["آب وصل شد", "رله خاموش است", "آب قطع شد.", "منتظر دستور"]
result = []
subs = []
model = Model("model")
rec = KaldiRecognizer(model, 16000)

p = pyaudio.PyAudio()
stream = p.open(
	format=pyaudio.paInt16, 
	channels=1, 
	rate=16000, 
	input=True
)
stream.start_stream()

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


while True:
    data = stream.read(1024, exception_on_overflow = False)
    if len(data) == 0:
        break
    if rec.AcceptWaveform(data):
        result = rec.FinalResult()
        jres = json.loads(result)
        s = jres["text"]
        print(status[3]) if s == "" else print(s)
        if "آب" and "وصل" in s:
            pumpOn()
        elif "آب" and "قطع" in s:
            pumpOff()
        elif "رله" and "روشن" in s:
            pumpOn()
        elif "رله" and "خاموش" in s:
            pumpOff()
