import time
from pirc522 import RFID
rdr = RFID()

n=0
Rec=0
Recoil=0
l=[]
while True:
  rdr.wait_for_tag()
  (error, tag_type) = rdr.request()
  if not error:
    print("Tag detected")
    (error, uid) = rdr.anticoll()
    if not error:
      print("UID: " + str(uid))
      str1= ''.join(str(e) for e in str(uid))
      try:
          FILE=open(str1,"r")
          nm=FILE.readline()
          FILE=open(str1,"a")
          FILE.write("Peticion de acceso "+time.strftime(" a las %H:%M  del  %d/%m/%y <<CONCEDIDO>>\n"))
          FILE.close()
          FILE=open("Log","a")
          FILE.write("Peticion de acceso de "+str1+"///"+nm+time.strftime(" a las %H:%M  del  %d/%m/%y <<CONCEDIDO>>\n"))
          FILE.close()
          print("\nok\n")
      except:
          print("Codigo no registrado")
          FILE=open("Log","a")
          FILE.write("Peticion de acceso de "+str1+time.strftime(" a las %H:%M  del  %d/%m/%y <<DENEGADO>>\n"))
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
                  FILE.write("Bloqueo desactivado a las "+time.strftime("%H:%M  del  %d/%m/%y\n"))
                  FILE.close()
                  n=0
                  Rec=0
              else:
                  Rec=Rec-l[0]
                  l=l[1:]
                  n=n-1
      time.sleep(1)
rdr.cleanup()