# -*- coding: cp1252 -*-
import os
import sys
import traceback

import time
#import win32com.client
#import pythoncom
import datetime
#import msvcrt
import subprocess

import ablaufRollos
import ablaufBewaesserung
import ablaufSonnenSchutz
import ablaufHeizung
import statusCheck

import fhzClient
import FHZHMInterface

#meine Klasse für XBMC Settings files
import xbmcSettings
import eHomeSettings
import inetCheck
import fhzClientCheck


# Control IDs
# 6000...Makros
# 7000...Views
# 8000...Rollos
# 9000...Lichter   

# Rollos: oben unten vertauscht: oben im FHZ heisst unten bei mir.

def debugWrite(cnt, s):
    try:
        fn = "C:\Users\eHome\Documents\homeputer\eHomeDebugLog.csv"
        fd = open(fn,"a")
        fd.write(str(datetime.datetime.today().date()))
        fd.write("\t")
        fd.write(str(datetime.datetime.now().time()))
        fd.write("\t")
        fd.write(str(cnt))
        fd.write("\t")
        fd.write(s)
        fd.write("\n")
        fd.close()
    except Exception, err:
        print('DebugLogFile konnte nicht geschrieben werden\n%s\n' % str(err))
        pass            

    

        
        
USE_XBMC = False

globalCnt = 0
bStartup = False
DELAY = 20


inetChk = inetCheck.inetCheck()
if not(inetChk.isConnectionAlive("www.schagerdelic.com/eHome/dyndns.php")):
    debugWrite(globalCnt,'CANNOT CONNECT TO SCHAGERDLEIC.COM')
    #debugWrite(globalCnt,'RESET ROUTER')
    #debugWrite(globalCnt, str(inetChk.resetRouter()))
                        
ablaufRollos = reload(sys.modules['ablaufRollos'])
autoRolloControl = ablaufRollos.AutoRollos()

ablaufBewaesserung = reload(sys.modules['ablaufBewaesserung'])
autoBewaesserungControl = ablaufBewaesserung.AutoBewaesserung()

ablaufSonnenSchutz = reload(sys.modules['ablaufSonnenSchutz'])
autoSonnenSchutzControl = ablaufSonnenSchutz.AutoSonnenSchutz()

ablaufSonnenSchutz = reload(sys.modules['ablaufHeizung'])
autoHeizungControl = ablaufSonnenSchutz.AutoHeizung()

statusCheck = reload(sys.modules['statusCheck'])
xbmcSettings = reload(sys.modules['xbmcSettings'])


aktHausStatus = statusCheck.HausStatus()
statusControl = statusCheck.StatusCheck()

fhzClientChk = fhzClientCheck.fhzClientCheck()

while 1:
        globalCnt = globalCnt + 1
        jetzt = datetime.datetime.now().time()

        
        try:

                try:
                    __settings__ = eHomeSettings.eHomeSettings("Q:\\eHome\\eHomeSettings.json")
                    ret = os.popen('copy Q:\\eHome\\eHomeSettings.json C:\\Users\\eHome\\Documents\\homeputer\\')
                except Exception, err:
                    print "Q:\eHome... NOT FOUND... using C:\\"
                    __settings__ = eHomeSettings.eHomeSettings("C:\\Users\\eHome\\Documents\\homeputer\\eHomeSettings.json")                        

                        
                online = __settings__.getSetting("online")

                debugWrite(globalCnt,'02')

                #Internetverbindungscheck
                if (globalCnt % 30 == 0): # 3 = 1min, 15 = 5min
                    if not(inetChk.isConnectionAlive("www.schagerdelic.com/eHome/dyndns.php")):
                        debugWrite(globalCnt,'CANNOT CONNECT TO SCHAGERDELIC')
                        #debugWrite(globalCnt, str(inetChk.resetRouter()))
               
                if online:
                        #persistFhz = win32com.client.Dispatch("homeputerStudio.ObjDataCom")
                        persistFhz = FHZHMInterface.FHZHMInterface()
                        #statusControl.initXBMC(persistFhz)
                else:
                        persistFhz = 0
                        break
                pass

                debugWrite(globalCnt,'03')
                

                #WATCHDOG SET
                #if globalCnt % 2 == 0: # 40sec
                #    persistFhz.RunMakro("WatchdogSet")
                #    if not(fhzClientChk.isClientAlive('C:\Users\eHome\AppData\Local\homeputer\spg\Msgfile.txt')):
                #        subprocess.Popen('shutdown /d u:99:99 /t 60 /r /f')
                    

                #if globalCnt % 30 == 0: # 10min
                #    persistFhz.SetObjValName("Anzeige",'Update : ' + str(jetzt)[0:8])

                debugWrite(globalCnt,'04')

        except Exception, err:
                debugWrite(globalCnt,'X1')
                print('Die COM Verbindung zu Homeputer konnte nicht hergestellt werden\nIst Homeputer gestartet?\n%s\n' % str(err))
                break   
                pass
        
                
                
        try:

                # Status Check  
                aktHausStatus.update(persistFhz)
                debugWrite(globalCnt,'05')
                
        except Exception, err:
                debugWrite(globalCnt,'X2')
                print('Die Sensorwerte konnten nicht gelesen werden.\nIst in der Homeputer SW die Ausführung gestartet.\n%s\n' % str(err))      
                pass

        try:
                statusControl.update(jetzt, aktHausStatus)
                debugWrite(globalCnt,'06')
        except Exception, err:
                debugWrite(globalCnt,'X3')
                print('ERROR3: %s\n' % str(err))        
                pass

        try:            
                # Automatische Rollos
                
                if (__settings__.getSetting("autorollos")):
                    autoRolloControl.initXBMC(persistFhz,__settings__)
                    autoRolloControl.update(datetime.datetime.now().time())
                #print 'autorollo OK'
                debugWrite(globalCnt,'07')

                
                # Automatischer Sonnenschutz
                if (__settings__.getSetting("autosonnenschutz")):
                    autoSonnenSchutzControl.initXBMC(persistFhz,__settings__)
                    autoSonnenSchutzControl.update(jetzt)
                #print 'sonnenschutz OK'
                debugWrite(globalCnt,'08')

                # Automatische Bewaesserung
                #if (__settings__.getSetting("autoWasserMorgens") or __settings__.getSetting("autoWasserAbends")):
                #    autoBewaesserungControl.initXBMC(persistFhz,__settings__)
                #    autoBewaesserungControl.update(jetzt, aktHausStatus)
                #print 'sonnenschutz OK'
                debugWrite(globalCnt,'09')

                # Automatische Heizung
                if (globalCnt % 3 == 0): # 3 = 1min, 15 = 5min
                    autoHeizungControl.initXBMC(persistFhz,__settings__)
                    autoHeizungControl.update(jetzt, aktHausStatus)


                debugWrite(globalCnt,'10')
        except Exception, err:
                debugWrite(globalCnt,'X4')
                print('ERROR4: %s\n' % str(err))        
                pass


        del persistFhz
        del __settings__
        debugWrite(globalCnt,'11')
                
        for i in range(1,DELAY):
            sys.stdout.flush()
            time.sleep(1)
            #ch = msvcrt.getch()

        debugWrite(globalCnt,'12')
        print "..."

