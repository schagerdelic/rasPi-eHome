# -*- coding: cp1252 -*-
'''
Created on 21.06.2010

@author: SCHAGERL
'''
from socket import *
import os
import sys
import win32com.client
import time
import FHZHMInterface

BUFSIZ = 4096
HOST = ''
PORT = 7777
ADDR = (HOST,PORT)



class myFHZServer:
    def __init__(s):
        #s.__fhz = win32com.client.Dispatch("homeputerStudio.ObjDataCom")
        s.__fhz = FHZHMInterface.FHZHMInterface()
        s.__serv = socket( AF_INET,SOCK_STREAM)
        s.__serv.bind((ADDR))
        s.__serv.settimeout(None)
        s.__cli = None
        s.__imlistening  = 0
        s.__improcessing = 0
        s.__fhzObjCount = 0
        s.__hmObjCount = 0
        s.__HMInterface = FHZHMInterface.FHZHMInterface()
        s.__run()

  
    def __run(s):
        s.__imlistening = 1
        while s.__imlistening:
            s.__listen()
            s.__improcessing = 1
            while s.__improcessing:
                s.__procCmd()
                
            s.__cli.close()
        s.__serv.close()
  
    def __listen(s):
          s.__serv.listen(5)
          print '...listening'
          cli,addr = s.__serv.accept()
          s.__cli = cli
          print '...connected: ', addr
  
    def __procCmd(s):
          cmd = s.__cli.recv(BUFSIZ)
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
            s.__fhzObjCount = s.__fhz.GetObjCnt()
            s.__hmObjCount = len(s.__HMInterface.HM_FHZDevNames)
            objCount = s.__fhzObjCount + s.__hmObjCount
            s.__cli.send(str(objCount))
            # print '...GET_OBJ_COUNT: ', str(objCount)

   
         elif cmd == 'GET_OBJ_TYPE':
            s.__cli.send('OK1')
            cmd = s.__cli.recv(BUFSIZ)
            objType = "XXX"
            if  (int(cmd) < s.__fhzObjCount):
                val = s.__fhz.GetObjValIdx(int(cmd)) #Abfangen wenn kein Integer
                objType = str(val[2])
            else:
                hmIdx = int(cmd) - s.__fhzObjCount
                objType = s.__HMInterface.HM_Devices[s.__HMInterface.HM_FHZ_Converter[hmIdx][0]]['type']
                
            if (objType == ""):
                objType = "XXX"

            s.__cli.send(objType)
            #print cmd
            #print objType

            
         elif cmd == 'GET_OBJ_NAME':
            s.__cli.send('OK1')
            cmd = s.__cli.recv(BUFSIZ)
            if  (int(cmd) < s.__fhzObjCount):
                val = s.__fhz.GetObjValIdx(int(cmd))
                objName = str(val[1])
            else:
                hmIdx = int(cmd) - s.__fhzObjCount
                objName = s.__HMInterface.HM_FHZDevNames[hmIdx]
                # print '...GET_OBJ_NAME: ', objName
                

            if (objName == ""):
                objName = "XXX"

            s.__cli.send(objName)
            #print cmd
            #print objName


         elif cmd == 'GET_OBJ_VAL':
            s.__cli.send('OK1')
            cmd = s.__cli.recv(BUFSIZ)
            if  (int(cmd) < s.__fhzObjCount):
                val = s.__fhz.GetObjValIdx(int(cmd))
                objVal = str(val[4])
            else:
                hmIdx = int(cmd) - s.__fhzObjCount
                objVal = str(s.__HMInterface.GetObjVal_HM(s.__HMInterface.HM_FHZ_Converter[hmIdx][0],s.__HMInterface.HM_FHZ_Converter[hmIdx][1])).replace('.',',')


            if (objVal == ""):
                objVal = "XXX"

            s.__cli.send(objVal)
            # print cmd
            # print objVal

            
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


if __name__ == '__main__':
    pass
    sys.stdout.write('FHZ Server started...\n')
    sys.stdout.flush()

    serv = myFHZServer()
    
    
    #fhz = win32com.client.Dispatch("homeputerStudio.ObjDataCom")
    objCount = 0
    #objCount = fhz.GetObjCnt()
    #ret = fhz.SetObjValName("RolloKueche", "oben")
    
    #val = fhz.GetObjVal("Wasser")
    
    for i in range(1,objCount):
        val = fhz.GetObjValIdx(i)
        sys.stdout.write(str(val[1]))
        sys.stdout.write(" - ")
        sys.stdout.write(str(val[2]))
        sys.stdout.write(" - ")
        sys.stdout.write(str(val[6]))
        sys.stdout.write(" - ")
        sys.stdout.write(str(val[7]))
        sys.stdout.write(" - ")
        sys.stdout.write(str(val[8]))
        sys.stdout.write("\n")
        
    #1..name
    #2..typ zb: EAGeraet,Zeichen,TempSensor,ASensor,Rollade,Knopf
    #3..Bezeichnung
    #4..Value
    #5..Mögliche Werte aus;an;
    #6..Art = 85?
    #7..hwTyp 1
    #8..objTyp 1


    
    sys.stdin.readline()

    serv.kill()
    del serv
    sys.stdout.write('DONE\n')

    #ret = fhz.RunMakro("AlleLichterAus")    
   
    
'''
    Dim fhz As FHZ1x00.ObjDataCom
    Dim varVal As String

    Set fhz = CreateObject("FHZ1x00.ObjDataCom")
    
    i = fhz.GetObjCnt
    
    'varVal = "an"
    ret = fhz.GetObjVal("LichtTV ", varVal)
    ret = fhz.GetObjVal("Temp", varVal)
    ret = fhz.GetObjVal("Wasser", varVal)
    
    ret = fhz.SetObjValName("LichtEssen", "an")
    
    ret = fhz.RunMakro("AlleLichterAus")
'''    
