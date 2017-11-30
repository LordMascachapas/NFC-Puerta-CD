import time
from pirc522 import RFID
rdr = RFID()

while True:
  rdr.wait_for_tag()
  (error, tag_type) = rdr.request()
  if not error:
    print("Tag detected")
    (error, uid) = rdr.anticoll()
    if not error:
      print("UIDs: " + str(uid))
      try:
        open("caca")
        men=FILE.read()
        FILE.close()
      except:
        print("El usuario no existe\n")
      time.sleep(3)
rdr.cleanup()