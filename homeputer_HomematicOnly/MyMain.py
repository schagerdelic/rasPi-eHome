# -*- coding: cp1252 -*-
'''
Created on 21.06.2010

@author: SCHAGERL
'''
import sys
import win32com.client
import pythoncom

if __name__ == '__main__':
    pass
    sys.stdout.write('Hallo Welt\n')

    pythoncom.CoInitialize()
    fhz = win32com.client.Dispatch("homeputerStudio.ObjDataCom")
    #fhz = win32com.client.GetActiveObject("homeputerStudio.ObjDataCom")



    objCount = fhz.GetObjCnt()
    ret = fhz.SetObjValName("LichtTV", "aus")
    
    #val = fhz.GetObjVal("Wasser")

    for i in range(0,objCount+1):
        val = fhz.GetObjValIdx(i)
        sys.stdout.write(str(val[1]))
        sys.stdout.write(" - ")
        sys.stdout.write(str(val[2]))
        sys.stdout.write(" - ")
        sys.stdout.write(str(val[6]))
        sys.stdout.write(" - ")
        sys.stdout.write(str(val[7]))
        sys.stdout.write(" - ")
        sys.stdout.write(str(val[4]))
        sys.stdout.write("\n")
        
    #1..name
    #2..typ zb: EAGerät
    #3..Bezeichnung
    #4..Value
    #5..Mögliche Werte aus;an;
    #6..Art = 85?
    #7..hwTyp 1
    #8..objTyp 1

    
    val = fhz.GetObjVal('Anzeige')

    val = fhz.SetObjValName("Anzeige","hallo welt")

    sys.stdout.write(str(val))
    #sys.stdin.readline()
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
