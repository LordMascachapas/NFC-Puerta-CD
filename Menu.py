import time
import RPi.GPIO as GPIO
import MFRC522
import signal
import hashlib


s=True
while s!=0:
    s=input("1.Nuevo usuario\n2.Lista de Usuarios\n3.Inspeccionar usuario\n4.Log\n0.Salir\n")
    if s==1:
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
        print("Introduce tu tag. Se aceptan abono transportes,\npero el programa enviara un aviso de error de autentificacion ... no pasa nada :P")
        print "Press Ctrl-C to stop."

        # This loop keeps checking for chips. If one is near it will get the UID and authenticate
        continue_reading = True
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
                            open(str1.hexdigest())
                            print("El usuario ya existe\n\n")
                        except:
                            nm=raw_input("nombre?:  ")
                            ocu=raw_input("ocupacion?:  ")
                            FILE=open(str1.hexdigest(),"w")
                            FILE.write(nm+"\n"+ocu+"\n\n"+time.strftime("Registrado a las %H:%M  del  %d/%m/%y"))
                            FILE.close()
                            FILE=open("Codigos","a")
                            FILE.write(str1.hexdigest()+"  -->  "+nm+"\n")
                            FILE.close()
                            FILE=open("Log","a")
                            FILE.write(nm+time.strftime(" registrado a las %H:%M  del  %d/%m/%y")+" con el codigo "+str1.hexdigest()+"\n")
                            FILE.close()
                            print("\nHECHO !!!\n")
                        continue_reading=False
                        key = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]
        
                        # Select the scanned tag
                        MIFAREReader.MFRC522_SelectTag(uid)

                        # Authenticate
                        status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, 8, key, uid)

                        # Check if authenticated
                        if status == MIFAREReader.MI_OK:
                            MIFAREReader.MFRC522_StopCrypto1()
                        GPIO.cleanup()
    if s==2:
        x=True
        try:
            open("Codigos")
        except:
            x=False
        if x:
            FILE=open("Codigos")
            men=FILE.read()
            print("\n"+men)
            FILE.close()
        else:
            print("No hay usuarios\n")
    elif s==3:
        cod=raw_input("\nCodigo?:  ")
        try:
            FILE=open(cod)
            men=FILE.read()
            print("\n"+men+"\n")
            FILE.close()
        except:
            print("El usuario no existe\n")
    elif s==4:
        try:
            FILE=open("Log")
            men=FILE.read()
            print("\n"+men+"\n")
        except:
            print("No hay actividad registrada\n")
    elif s==0: print("\n\nBYE\n\n")
    else: print ("\nbuff\n")