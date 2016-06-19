from socket import * 



adr = ('localhost',7777);
sock = socket( AF_INET,SOCK_STREAM)               
try:
    sock.connect(adr)
    sock.send('BYE')
    sock.close()
    ret = False
except:
    ret = True
