# -*- coding: cp1252 -*-
'''
Created on 21.06.2010

@author: SCHAGERL
'''
from socket import *
import select
import os
import sys
import win32com.client
import time

BUFSIZ = 4096
HOST = ''
PORT = 7777
ADDR = (HOST,PORT)



class myFHZServer:
    def __init__(s):
        s.__fhz = win32com.client.Dispatch("homeputerStudio.ObjDataCom")
        s.__serv = socket( AF_INET,SOCK_STREAM)
        s.__serv.setblocking(0)
        s.__serv.settimeout(5.0)
        s.__serv.bind((ADDR))
        s.__cli = None
        s.__imlistening  = 0
        s.__improcessing = 0
        s.__timeOut = 5 #sec
        s.__run()
  
    def __run(s):
        s.__imlistening = 1
        while s.__imlistening:
            while s.__cli == None:
                s.__listen()
            s.__improcessing = 1
            while s.__improcessing:
                s.__procCmd()
                
            s.__cli.close()
        s.__serv.close()
  
    def __listen(s):
          s.__serv.listen(5)
          print '...listening'
          try:
              cli,addr = s.__serv.accept()
              s.__cli = cli
              print '...connected: ', addr
          except:
              print '...timeout'
              s.__cli = None
  
    def __procCmd(s):
          cmd = s.__recv(BUFSIZ)
          #cmd = s.__cli.readline()
          if not cmd: return
          #print cmd
          s.__servCmd(cmd)
          #if s.__improcessing:
          #    proc = os.popen(cmd)
          #    outp = proc.read()
          #    if outp:
          #        s.__cli.send(outp)
          #    else   :
          #        s.__cli.send('good')

  
    def __servCmd(s,cmd):
         cmd = cmd.strip()
         if cmd == 'BYE':
            s.__cli.send('OK\n')
            s.__improcessing = 0

         elif cmd == 'GET_OBJ_COUNT':
            s.__cli.send('OK0')
            objCount = s.__fhz.GetObjCnt()
            s.__cli.send(str(objCount))

   
         elif cmd == 'GET_OBJ_TYPE':
            s.__cli.send('OK1')
            cmd = s.__cli.recv(BUFSIZ)
            val = s.__fhz.GetObjValIdx(int(cmd)) #Abfangen wenn kein Integer
            objType = str(val[2])
            if (objType == ""):
                objType = "XXX"

            s.__cli.send(objType)
            #print cmd
            #print objType

            
         elif cmd == 'GET_OBJ_NAME':
            s.__cli.send('OK1')
            cmd = s.__recv(BUFSIZ)
            val = s.__fhz.GetObjValIdx(int(cmd))
            objName = str(val[1])
            if (objName == ""):
                objName = "XXX"

            s.__cli.send(objName)
            #print cmd
            #print objName


         elif cmd == 'GET_OBJ_VAL':
            s.__cli.send('OK1')
            cmd = s.__cli.recv(BUFSIZ)
            val = s.__fhz.GetObjValIdx(int(cmd))
            objVal = str(val[4])
            if (objVal == ""):
                objVal = "XXX"

            s.__cli.send(objVal)
            #print cmd
            #print objVal

            
         elif cmd == 'SET_OBJ_VAL':
            s.__cli.send('OK2')
            objName = s.__cli.recv(BUFSIZ)
            s.__cli.send('OK1')
            cmd = s.__cli.recv(BUFSIZ)
            val = s.__fhz.SetObjValName(objName, cmd)
            s.__cli.send('OK0')
            #print objName
            #print cmd
            

         elif cmd == 'RUN_MAKRO':
            s.__cli.send('OK1')
            cmd = s.__cli.recv(BUFSIZ)
            val = s.__fhz.RunMakro(cmd)
            s.__cli.send('OK0')

         else:
            s.__cli.send('NOTOK')

    def __kill(s):
         s.__improcessing = 0
         s.__imlistening = 0

    def __recv(s,bufferSize):
        ready = select.select([s.__serv], [], [], s.__timeOut)
        if ready[0]:
            data = s.__cli.recv(bufferSize)
            
if __name__ == '__main__':
    pass
    sys.stdout.write('FHZ Server started...\n')
    sys.stdout.flush()

    serv = myFHZServer()
    
