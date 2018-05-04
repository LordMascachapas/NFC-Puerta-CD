#!/usr/bin/env python
import RPi.GPIO as GPIO
import MFRC522
import signal
import time

sentinel = True
continue_reading = True

def end_read(signal,frame):
    global sentinel
    global continue_reading
    print "Ctrl+C captured, ending read."
    sentinel = False
    continue_reading = False
    GPIO.cleanup()

signal.signal(signal.SIGINT, end_read)
while sentinel:
    continue_reading = True
    abrir_puerta = False
    MIFAREReader = MFRC522.MFRC522()
    GPIO.output(7, True)
    while continue_reading:
        if abrir_puerta:
            print("Puerta Abierta")
            GPIO.output(7, False)
            time.sleep(2)
            GPIO.output(7, True)
            abrir_puerta = False
            continue_reading = False
        (detected,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
        (status,uid) = MIFAREReader.MFRC522_Anticoll()
        if detected == MIFAREReader.MI_OK:
            print("Card detected")
        if status == MIFAREReader.MI_OK:
            abrir_puerta = True