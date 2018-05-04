import pickle
import time
import RPi.GPIO as GPIO
import MFRC522
import signal
import hashlib


# Capture SIGINT for cleanup when the script is aborted
def end_read(signal, frame):
    global continue_reading
    print("Ctrl+C captured, ending read.")
    continue_reading = False
    GPIO.cleanup()

# This read the File where the dictionary with pickle library
def getCodeBook():
    try:
        FILE = open("Codigos.json", "r")
        book = pickle.load(FILE)
        FILE.close()
    except:
        book
    return book

# This hash the sring parameter
def hashing(strUID):
    return hashlib.md5(strUID).hexdigest()

# This check if the hashed-UID is registered on the dictionary
def checkUID(book, hash_uid):
    if hash_uid in book:
        return True
    else:
        return False



code_book = getCodeBook()
choose = True
while choose != 0:
    choose = input("1.New user\n"
                   "2.List of users\n"
                   "3.Log\n"
                   "4.Delete user\n"
                   "0.Exit\n\n"
                   "Option: ")
    if choose == 1:
        # Hook the SIGINT
        signal.signal(signal.SIGINT, end_read)
        # Create an object of the class MFRC522
        MIFAREReader = MFRC522.MFRC522()
        # Welcome message
        print("Introduce tu tag")
        print("Press Ctrl-C to stop.")
        # This loop keeps checking for chips. If one is near it will get the UID and authenticate
        continue_reading = True
        while continue_reading:
            # Scan for cards
            (status, TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
            # If a card is found
            if status == MIFAREReader.MI_OK:
                print("Card detected")
                # Get the UID of the card
                (status, uid) = MIFAREReader.MFRC522_Anticoll()
                # If we have the UID, continue
                if status == MIFAREReader.MI_OK:
                    str_uid = ''.join(str(e) for e in str(uid))
                    hash_uid = hashing(str_uid)
                    if checkUID(code_book,hash_uid):
                        code_book[hash_uid] = {"name": raw_input("Name: "),
                                               "nextname": raw_input("Nextname: "),
                                               "mobile": raw_input("Mobile number: "),
                                               "mail": raw_input("Mail : ")}
                        print("Done")
                    else:
                        print("The tag already exists")
                    continue_reading = False
                    GPIO.cleanup()

    elif choose == 2:
        i = 0
        for none, y in code_book.items():
            print("\n")
            i = i + 1
            print("-> " + y)
        print("\n")
    elif choose == 3:
        pass
    elif choose == 4:
        pass
    elif choose == 0:
        print("\n\nFinished\n\n")
    else:
        print("\nPlease, choose a valid option\n")
