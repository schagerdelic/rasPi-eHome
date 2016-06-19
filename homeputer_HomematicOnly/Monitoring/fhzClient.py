from socket import *                                          
from time import time                                         
from time import sleep                                        
import sys                                                    
BUFSIZE = 4096                                                
                                                              
class fhzClient:                                                
    def __init__(s,host):                                     
        s.__HOST = host                                       
        s.__PORT = 7777                                      
        s.__ADDR = (s.__HOST,s.__PORT)                        
        s.__sock = None                                       
                                                              
    def makeConnection(s):                                    
        s.__sock = socket( AF_INET,SOCK_STREAM)               
        s.__sock.connect(s.__ADDR)                            
                                                              
    def sendCmd(s, cmd):                                      
        s.__sock.send(cmd)                                    
                                                              
    def getResults(s):                                        
        data = s.__sock.recv(BUFSIZE)                         
        return data                                            

    def GetObjVal(s,objName):
	s.sendCmd("GET_OBJ_VAL\n")
	ret = s.getResults()
	print ret
	if ret == "OK1":
            s.sendCmd(objName)
            ret = s.getResults()
            return ret
        else:
            return -1
        pass

    def RunMakro(s,makroName):
	s.sendCmd("RUN_MAKRO")
	ret = s.getResults()
	if ret == "OK1":
            s.sendCmd(makroName)
            ret = s.getResults()
            if ret == "OK0":
                return 0
            else:
                return -1
        else:
            return -1
        pass

    def SetObjValName(s,objName, objVal):
        s.sendCmd("SET_OBJ_VAL")
        ret = s.getResults()
	if ret == "OK2":
            s.sendCmd(objName)
            ret = s.getResults()
            if ret == "OK1":
                s.sendCmd(objVal)
                ret = s.getResults()
                if ret == "OK0":
                    return 0
                else:
                    return -1
            else:
                return -1
        else:
            return -1
        pass
    
    def Close(s):
	s.sendCmd("BYE")
	ret = s.getResults()
        s.__sock.close()
        return ret
    
if __name__ == '__main__':                                    

    conn = fhzClient('localhost')
    #conn = CmdLine('schagerlib.dyndns.org')                               
    conn.makeConnection()
    #print conn.SetObjValName("Anzeige","Hallo Welt")
    cmd = raw_input('--> ')
    print conn.RunMakro(cmd)
    print conn.Close()
    
    print 'DONE'
    del conn
