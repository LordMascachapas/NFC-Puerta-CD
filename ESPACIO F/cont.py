#!/usr/bin/env python
# -*- coding: utf8 -*-

import RPi.GPIO as GPIO
import MFRC522
import signal
import time
import hashlib

continue_reading = True

# Capture SIGINT for cleanup when the script is aborted
def end_read(signal,frame):
    global continue_reading
    print "Ctrl+C captured, ending read."
    continue_reading = False
    GPIO.cleanup()

# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)

# Create an object of the class MFRC522
MIFAREReader = MFRC522.MFRC522()

# Welcome message
print "Lector activado. Las tarjetas de abono transportes funcionan,\npero el programa envía un aviso de error de autentificación ... no pasa nada :P"
print "Presiona Ctrl-C para detener."

n=0
Rec=0
Recoil=0
l=[]

# This loop keeps checking for chips. If one is near it will get the UID and authenticate
while continue_reading:
    
    # Scan for cards    
    (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

    # If a card is found
    if status == MIFAREReader.MI_OK:
        print "Card detected"
    
    # Get the UID of the card
    (status,uid) = MIFAREReader.MFRC522_Anticoll()

    # If we have the UID, continue
    if status == MIFAREReader.MI_OK:
            strN= ''.join(str(e) for e in str(uid))
            str1=hashlib.md5(strN)
            try:
                FILE=open(str1.hexdigest(),"r")
                nm=FILE.readline()
                FILE=open("Log","a")
                FILE.write("Peticion de acceso de "+str1.hexdigest()+"///"+nm+time.strftime(" a las %H:%M  del  %d/%m/%y <<CONCEDIDO>>\n"))
                FILE.close()
                print("\nok\n")
            except:
                print("Codigo no registrado")
                FILE=open("Log","a")
                FILE.write("Peticion de acceso de "+strN+time.strftime(" a las %H:%M  del  %d/%m/%y <<DENEGADO>>\n"))
                FILE.close()
                if n>0:
                      end=time.time()
                      Recoil=end-start
                      l=l+[Recoil]
                start=time.time()
                n=n+1
                Rec=Rec+Recoil
                if n==5:
                      if Rec<=30:
                          print("THE LA oSTia OF US\n...\n\n ")
                          FILE=open("Log","a")
                          FILE.write("Bloqueo activado a las "+time.strftime("%H:%M  del  %d/%m/%y\n"))
                          FILE.close()
                          time.sleep(30)
                          FILE=open("Log","a")
                          FILE.close()
                          n=0
                          Rec=0
                      else:
                          Rec=Rec-l[0]
                          l=l[1:]
                          n=n-1
            # This is the default key for authentication
            key = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]
        
            # Select the scanned tag
            MIFAREReader.MFRC522_SelectTag(uid)

            # Authenticate
            status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, 8, key, uid)

            # Check if authenticated
            if status == MIFAREReader.MI_OK:
                MIFAREReader.MFRC522_StopCrypto1()
            
            time.sleep(1) 