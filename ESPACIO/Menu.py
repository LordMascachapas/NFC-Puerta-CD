import time
from pirc522 import RFID
rdr = RFID()
import time
s=True
while s!=0:
    s=input("1.Nuevo usuario\n2.Lista de Usuarios\n3.Inspeccionar usuario\n4.Log\n0.Salir\n")
    if s==1:
        x=True
        while x:
            rdr.wait_for_tag()
            (error,tag_type)=rdr.request()
            if not error:
                print("Tag detected")
                (error, uid) = rdr.anticoll()
                if not error:
                    str1 = ''.join(str(e) for e in str(uid))
                    try:
                        open(str1)
                        print("El usuario ya existe\n\n")
                        x=False
                    except:
                        nm=raw_input("nombre?")
                        ocu=raw_input("ocupacion?")
                        FILE=open(str1,"w")
                        FILE.write(nm+"\n"+ocu+"\n\n"+time.strftime("Registrado a las %H:%M  del  %d/%m/%y"))
                        FILE.close()
                        FILE=open("Codigos","a")
                        FILE.write(str1+"  -->  "+nm+"\n")
                        FILE.close()
                        FILE=open("Log","a")
                        FILE.write(nm+time.strftime(" registrado a las %H:%M  del  %d/%m/%y")+" con el codigo "+str1+"\n")
                        FILE.close()
                        print("\nHECHO !!!\n")
                        x=False
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
        cod=raw_input("\nCodigo?")
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