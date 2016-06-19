# -*- coding: cp1252 -*-
import os
import sys
#import win32com.client
#import pythoncom
import datetime
import time, wave
#import pyaudio
#from bluetooth import *
from socket import * 
import subprocess
import jsonIO

GEFRIERFACH_LIMIT = -5.0

def isServerDead():
    adr = ('localhost',7777);
    sock = socket( AF_INET,SOCK_STREAM)               
    try:
        sock.connect(adr)
        sock.send('BYE')
        sock.close()
        ret = False
    except:
        ret = True
    return ret

def isMobileInRange(addr):
    pass
##    try: 
##        sock=BluetoothSocket( RFCOMM )
##        sock.connect((addr, 1))
##        sock.close()
##        del sock
##        return True
##    except IOError:
##        del sock
##        return False
##    
	
def playWAV(filename):

    chunk = 1024
##    wf = wave.open(filename, 'rb')
##    p = pyaudio.PyAudio()
##
##    dev_cnt = p.get_device_count()
##
##    if dev_cnt == 7:    #Bluetooth audio empfänger verbunden
##    # open stream
##        stream1 = p.open(format =
##                        p.get_format_from_width(wf.getsampwidth()),
##                        channels = wf.getnchannels(),
##                        rate = wf.getframerate(),
##                        output_device_index = 4,
##                        output = True)
##
##        stream2 = p.open(format =
##                        p.get_format_from_width(wf.getsampwidth()),
##                        channels = wf.getnchannels(),
##                        rate = wf.getframerate(),
##                        output_device_index = 5,
##                        output = True)
##        # read data
##        data = wf.readframes(chunk)
##
##        # play stream
##        while data != '':
##            stream1.write(data)
##            stream2.write(data)
##            data = wf.readframes(chunk)
##
##        stream1.close()
##        stream2.close()
##
##    if dev_cnt == 5:    #Bluetooth audio empfänger NICHT gefunden
##    # open stream
##        stream1 = p.open(format =
##                        p.get_format_from_width(wf.getsampwidth()),
##                        channels = wf.getnchannels(),
##                        rate = wf.getframerate(),
##                        output_device_index = 3,
##                        output = True)
##
##        # read data
##        data = wf.readframes(chunk)
##
##        # play stream
##        while data != '':
##            stream1.write(data)
##            data = wf.readframes(chunk)
##
##        stream1.close()
##
##
##    p.terminate()
#------ END OF playWAV

class HausStatus:
    
    def __init__(self):
	self.esRegnet = False 
    	self.gefrierfach = -99.9
    	self.wasserImBad = False
    	self.stromAn = True
    	self.letzterRegen = datetime.datetime.now()
    	self.anwesenheitGerhard = False
    	self.anwesenheitAndrea = False
    	self.logCounter = 0

        self.tempWohnen = -99 
        self.tempSchlafen = -99 
        self.tempBad = -99
        self.tempKinder = -99
        self.feuchteWohnen = -99
        self.feuchteSchlafen = -99
        self.feuchteBad = -99
        self.feuchteKinder = -99

        self.heizenWohnen = 0 
        self.heizenSchlafen = 0 
        self.heizenBad = 0
        self.heizenKinder = 0


        self.schalterUnreach = ""
 	self.schlafenUnreach = ""
        self.badUnreach = ""
        self.kinderUnreach = ""

        pass

    def init(self,gefrierStr, wasserImBadStr, esRegnetStr):
        if gefrierStr == (u'-99.999.999,0'):
            gefrierStr = "-99"            
        self.gefrierfach = float(gefrierStr.replace(",","."))
        self.wasserImBad = wasserImBadStr.lower() == "alarm"
        self.esRegnet = esRegnetStr.lower() == "an"
        self.stromAn = True
    	self.anwesenheitGerhard = False
    	self.anwesenheitAndrea = False
        self.logCounter = 0
        pass

    def copy(self):
    	tmp = HausStatus()
        tmp.gefrierfach = self.gefrierfach
        tmp.wasserImBad = self.wasserImBad
        tmp.esRegnet = self.esRegnet
        tmp.stromAn = self.stromAn
        tmp.letzterRegen = self.letzterRegen
    	tmp.anwesenheitGerhard = self.anwesenheitGerhard
    	tmp.anwesenheitAndrea = self.anwesenheitAndrea
        tmp.tempWohnen = self.tempWohnen 
        tmp.tempSchlafen = self.tempSchlafen 
        tmp.tempBad = self.tempBad
        tmp.tempKinder = self.tempKinder 
        tmp.feuchteWohnen = self.feuchteWohnen
        tmp.feuchteSchlafen = self.feuchteSchlafen
        tmp.feuchteBad = self.feuchteBad
        tmp.feuchteKinder = self.feuchteKinder

        return tmp
        pass

    def update(self,fhz):
        self.gefrierStr = '-99.9' #str(fhz.Get_FHEM("sensor_gefrierfach", "TEMPERATURE"))
        self.wasserImBadStr = fhz.GetObjVal("BadWasser")[2]
        self.esRegnetStr = fhz.GetObjVal("Regen")[2]
        self.raumTempStr = str(fhz.Get_FHEM("sensor_wohnen", "TEMPERATURE"))
        self.raumFeuchteStr = str(fhz.Get_FHEM("sensor_wohnen", "HUMIDITY"))
        self.aussenTempStr = fhz.GetObjVal("Aussentemperatur")[2]
        self.aussenFeuchteStr = fhz.GetObjVal("Aussenluftfeuchte")[2]
        self.windStr = fhz.GetObjVal("KS300_Wind")[2]
        self.regenATagStr = fhz.GetObjVal("KS300_RegenATag")[2]
        self.anzeigeStr = fhz.GetObjVal("Anzeige")[2]
        self.anzeigeSAStr = fhz.GetObjVal("AnzeigeSA")[2]
        self.anzeigeSUStr = fhz.GetObjVal("AnzeigeSU")[2]
        self.regenLTagStr = fhz.GetObjVal("RegenLetzterTag")[2]
        self.tempWohnen = float(fhz.Get_FHEM("sensor_wohnen", "TEMPERATURE"))
        self.tempSchlafen = float(fhz.Get_FHEM("sensor_schlafen", "TEMPERATURE"))
        self.tempBad = float(fhz.Get_FHEM("sensor_bad", "TEMPERATURE"))
        self.tempKinder = float(fhz.Get_FHEM("sensor_kinder", "TEMPERATURE"))
        self.feuchteWohnen = float(self.raumFeuchteStr.replace(',','.'))
        self.feuchteSchlafen = float(fhz.Get_FHEM("sensor_schlafen", "HUMIDITY"))
        self.feuchteBad = float(fhz.Get_FHEM("sensor_bad", "HUMIDITY"))
        self.feuchteKinder = float(fhz.Get_FHEM("sensor_kinder", "HUMIDITY"))
        self.schalterUnreach = fhz.Get_FHEM("heizung_bad", "UNREACH")
        self.schlafenUnreach = fhz.Get_FHEM("sensor_schlafen", "UNREACH")
        self.badUnreach = fhz.Get_FHEM("sensor_bad", "UNREACH")
        self.kinderUnreach = fhz.Get_FHEM("sensor_kinder", "UNREACH")


        if self.gefrierStr == (u'-99.999.999,0'):
            self.gefrierStr = "-99"            
        self.gefrierfach = float(self.gefrierStr.replace(",","."))
        self.wasserImBad = self.wasserImBadStr.lower() == "alarm"
        self.esRegnet = self.esRegnetStr.lower() == "an"
        self.stromAn = True
    	self.anwesenheitGerhard = False
       	self.anwesenheitAndrea = False
        #self.anwesenheitAndrea = isMobileInRange("00:23:D4:20:ED:8B");
        #self.anwesenheitGerhard = isMobileInRange("30:7C:30:51:5A:13");

        print "statusCheck"
        if self.logCounter == 0:
            self.logCounter = 30 # ca. alle 10 min
            try:
                print "HeizungswriteLogFile"
                
                if isServerDead():
                    #serverProc = subprocess.Popen('"C:\\Python27\\python.exe" "C:\\Users\\eHome\\Documents\\homeputer_HomematicOnly\\Monitoring\\myFHZServerMT.py"')
                    subprocess.Popen(["lxterminal", "-e", "python /home/pi/eHome/homeputer_HomematicOnly/Monitoring/myFHZServerMT.py"])
                    print('FHZServer neu gestartet')

                ###########
                ## LOGFILE
                #
                #self.writeLogFile("./../eHomeLog.csv")

                self.writeStatusJSON("/var/www/html/eHome/eHomeHeizungVals.json")


                
            except Exception, err:
                    print('LogFile konnte nicht geschrieben werden\n%s\n' % str(err))
                    pass            
        else:
            self.logCounter = self.logCounter - 1

        pass

    def writeLogFile(self,fn):
        fd = open(fn,"a")
        fd.write(str(datetime.datetime.today().date()))
        fd.write("\t")
        fd.write(str(datetime.datetime.now().time()))
        fd.write("\t")
        fd.write(self.anzeigeStr)
        fd.write("\t")
        fd.write(self.gefrierStr)
        fd.write("\t")
        fd.write(self.wasserImBadStr)
        fd.write("\t")
        fd.write(self.esRegnetStr)
        fd.write("\t")
        fd.write(self.raumTempStr)
        fd.write("\t")
        fd.write(self.raumFeuchteStr)
        fd.write("\t")
        fd.write(self.aussenTempStr)
        fd.write("\t")
        fd.write(self.aussenFeuchteStr)
        fd.write("\t")
        fd.write(self.windStr)
        fd.write("\t")
        fd.write(self.regenATagStr)
        fd.write("\t")
        fd.write(self.regenLTagStr)
        fd.write("\t")
        fd.write(self.anzeigeSAStr)
        fd.write("\t")
        fd.write(self.anzeigeSUStr)
        fd.write("\t")
        fd.write(str(self.tempWohnen).replace('.',','))
        fd.write("\t")
        fd.write(str(self.tempSchlafen).replace('.',','))
        fd.write("\t")
        fd.write(str(self.tempKinder).replace('.',','))
        fd.write("\t")
        fd.write(str(self.tempBad).replace('.',','))
        fd.write("\t")
        fd.write(str(self.feuchteWohnen).replace('.',','))
        fd.write("\t")
        fd.write(str(self.feuchteSchlafen).replace('.',','))
        fd.write("\t")
        fd.write(str(self.feuchteKinder).replace('.',','))
        fd.write("\t")
        fd.write(str(self.feuchteBad).replace('.',','))
        fd.write("\t")
        fd.write(str(self.heizenWohnen))
        fd.write("\t")
        fd.write(str(self.heizenSchlafen))
        fd.write("\t")
        fd.write(str(self.heizenKinder))
        fd.write("\t")
        fd.write(str(self.heizenBad))
        fd.write("\t")
        fd.write(str(self.schalterUnreach))
        fd.write("\t")
        fd.write(str(self.schlafenUnreach))
        fd.write("\t")
        fd.write(str(self.kinderUnreach))
        fd.write("\t")
        fd.write(str(self.badUnreach))
        fd.write("\n")
        fd.close()

    def writeStatusJSON(self,fn):

        jsonstate = dict()
        jsonstate['innentemp'] = '{0:.1f}'.format(self.tempWohnen)
        jsonstate['innenhumid'] = '{0:.0f}'.format(self.feuchteWohnen)
        jsonstate['aussentemp'] = self.aussenTempStr
        jsonstate['aussenhumid'] = self.aussenFeuchteStr 
        jsonstate['wind'] = self.windStr
        jsonstate['niederschlag'] = self.regenLTagStr
        jsonstate['gefrierfach'] = '{0:.1f}'.format(self.gefrierfach)
        jsonstate['waschmaschine'] = self.wasserImBadStr
        jsonstate['regen'] = self.esRegnetStr
        jsonstate['tempSchlafen'] = '{0:.1f}'.format(self.tempSchlafen) 
        jsonstate['tempBad'] = '{0:.1f}'.format(self.tempBad)
        jsonstate['tempKinder'] = '{0:.1f}'.format(self.tempKinder)
        jsonstate['feuchteSchlafen'] = '{0:.0f}'.format(self.feuchteSchlafen)
        jsonstate['feuchteBad'] = '{0:.0f}'.format(self.feuchteBad)
        jsonstate['feuchteKinder'] = '{0:.0f}'.format(self.feuchteKinder)
        fd = open(fn,"w")
        fd.write('[' + jsonIO.write(jsonstate) + ']')
        fd.close()


class StatusCheck:
    tNow = 0
    tLast = 0
    tToday = 0
    statusJetzt = None
    statusVorher = None
    fhz = 0
    
    
    
    def __init__(self):
        self.tNow = datetime.datetime.now().time()
        self.tLast = datetime.datetime.now().time()
        self.tToday = datetime.datetime.now().date().weekday()
        self.statusJetzt = HausStatus()
        self.statusVorher = HausStatus()
        self.fhz = 0
        
    def initXBMC(self, fhz):
        self.fhz = fhz
        pass

    def initTest(self,fhz):
        self.fhz = fhz
        pass

    def update(self, time, aktStatus):
        self.tLast = self.tNow
        self.tNow = time
        self.tToday = datetime.datetime.now()
        self.statusVorher = self.statusJetzt.copy()
        self.statusJetzt = aktStatus.copy()
        self.statusJetzt.letzterRegen = self.statusVorher.letzterRegen
        
        #Regen
        if (self.statusJetzt.esRegnet and not(self.statusVorher.esRegnet)):
	    # es hat angefangen zu regnen
	    #self.fhz.SetObjValName("Anzeige", "Es regnet")
            if (datetime.datetime.combine(self.tToday,self.tNow) - self.statusJetzt.letzterRegen) > datetime.timedelta(hours = 1):
                # es hat seit einer Stunde nicht geregnet und jetzt neu begonnen
                playWAV('C:\\XBMC911\\scripts\\HomeControl\\resources\\esregnet.wav')

        if (not(self.statusJetzt.esRegnet) and self.statusVorher.esRegnet):
                # es hat aufgehoert zu regner
                #self.fhz.SetObjValName("Anzeige", "Es hat aufgehoert zu regnen")
                self.statusJetzt.letzterRegen = datetime.datetime.combine(self.tToday,self.tNow)

	
        #Gefrierfach
	if (self.statusJetzt.gefrierfach > GEFRIERFACH_LIMIT):
	        playWAV('C:\\XBMC911\\scripts\\HomeControl\\resources\\meineisschmiltzt.wav')
                #self.fhz.SetObjValName("Anzeige", "ACHTUNG: Temperatur im Kellergefrierfach zu hoch")

	if (self.statusJetzt.gefrierfach > GEFRIERFACH_LIMIT and self.statusVorher.gefrierfach <= GEFRIERFACH_LIMIT):
		#dialog = homeControlWarning.homeControlWarning() #('WARNUNG', 'ACHTUNG: Die Temperatur im Gefrierfach ist zu hoch!','Bitte pruefen ob das Gefrierfach offen ist, Strom an ist etc.')
  		#ok = dialog.show()
  		#ui = xbmcgui.WindowDialog("homeControlWarning.xml", os.getcwd(), "default")
  		#ui.show()
	        pass
			 

        #Wasser Im Bad
	if (self.statusJetzt.wasserImBad):
	        playWAV('C:\\XBMC911\\scripts\\HomeControl\\resources\\wasserimbad.wav')
                #self.fhz.SetObjValName("Anzeige", "ACHTUNG: Wasser im Bad")
		print("WASSER IM BAD")
                    
            
        pass

     
