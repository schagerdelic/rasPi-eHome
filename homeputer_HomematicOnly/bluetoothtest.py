from bluetooth import *
import time
import winsound

discovered_devices = discover_devices()

for address in discovered_devices:
   print lookup_name(address)
   print address


while True:

    bd_addr = "30:7C:30:51:5A:13" #Gerhard Blackberry
    #bd_addr = "00:23:D4:20:ED:8B" #Andrea HTC
    port = 1

    try: 
        sock=BluetoothSocket( RFCOMM )
        sock.connect((bd_addr, port))
        #sock.send("hello!!")
        sock.close()
        #winsound.Beep(1000,100)
        print "CONNECT"
    except IOError:
        print "NOT FOUND"
        winsound.Beep(100,100)

    del sock
    time.sleep(1)
    
