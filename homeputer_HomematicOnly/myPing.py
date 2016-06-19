import sys
import socket
import datetime
import time



while True:
    jetzt = datetime.datetime.now().time()
    print jetzt
    s = socket.socket()               
    adr = ('www.orf.at',80)                        
    try:
        ret = s.connect(adr)
        s.close()                                                                  
        print 'OK'
    except:
        print 'FAILED'
    
    time.sleep(5)
