import os
import sys
#import win32com.client
#import pythoncom
import datetime

class AutoRollos:
    tNow = 0
    tLast = 0
    tToday = 0
    tWohnenAuf = 0
    tSchlafenAuf = 0
    tWohnenZu = 0
    tSchlafenZu = 0
    fhz = 0
    
    
    
    def __init__(self):
        self.tNow = datetime.datetime.now().time()
        self.tLast = datetime.datetime.now().time()
        self.tToday = datetime.datetime.now().date().weekday()
        self.tWohnenAuf = self.tNow
        self.tSchlafenAuf = self.tNow
        self.tSchlafenAufWE = self.tNow
        self.tWohnenZu = self.tNow
        self.autoLichtAn = False
        self.autoRollosSonnenstand = False
        self.tSchlafenZu = self.tNow
        self.midnight = datetime.time(0,0)
        
        self.fhz = 0
        
    
    def initXBMC(self, fhz, settings):
        self.fhz = fhz
        self.tWohnenZu  = self.setting2time(settings.getSetting("RollosWohnenRunter"))
        self.tSchlafenZu  = self.setting2time(settings.getSetting("RollosSchlafenRunter"))
        self.tWohnenAuf  = self.setting2time(settings.getSetting("RollosWohnenRauf"))
        self.tSchlafenAuf  = self.setting2time(settings.getSetting("RollosSchlafenRauf"))
        self.tSchlafenAufWE  = self.setting2time(settings.getSetting("RollosSchlafenRaufWE"))
        self.autoLichtAn = settings.getSetting("autoLichterAn")
        self.autoRollosSonnenstand = settings.getSetting("autorollossonnenstand")

    def initTest(self,fhz,t1,t2,t3,t4,t5):
        self.tWohnenAuf = t1
        self.tSchlafenAuf = t2
        self.tWohnenZu = t3
        self.tSchlafenZu = t4
	self.tSchlafenAufWE = t5
        self.fhz = fhz
        pass
    
    def update(self, time):
        self.tLast = self.tNow
        self.tNow = time
        self.tToday = datetime.datetime.now().date().weekday()

        print self.tNow

        #WOHNEN
        if (self.tLast <= self.tWohnenAuf < self.tNow) or ((self.tWohnenAuf == self.midnight) and (self.tLast > self.tNow)):
            print "AutoRollos - Wohnen - AUF"
            try:
                self.fhz.RunMakro("WohnenRollosAuf")
                print "FHZ RunMakro - OK"
            except:
                print "ablaufRollos.py - RunMakro FAILED"

        #WOHNEN runter
        else:
            if (self.tLast <= self.tWohnenZu < self.tNow) or ((self.tWohnenZu == self.midnight) and (self.tLast > self.tNow)):
                print "AutoRollos - Wohnen - ZU"
                try:
                    print self.fhz
                    self.fhz.RunMakro("WohnenRollosZu")
                    if (self.autoLichtAn):
                        self.fhz.RunMakro("LichtEssenAnTimer")
                except:
                    print "ablaufRollos.py - RunMakro FAILED"



        #SCHLAFEN
	# Wochenende
#	if (self.tToday == 5) or (self.tToday == 6):
#            if (self.tLast <= self.tSchlafenAufWE < self.tNow) or ((self.tSchlafenAufWE == self.midnight) and (self.tLast > self.tNow)):
#                print "AutoRollos - Schlafen - AUF"
#                try:
#                    self.fhz.RunMakro("RolloSchlafenAuf")
#                except:
#                    print "ablaufRollos.py - RunMakro FAILED"
#	else: # Wochentage
#            if (self.tLast <= self.tSchlafenAuf < self.tNow) or ((self.tSchlafenAuf == self.midnight) and (self.tLast > self.tNow)):
#                print "AutoRollos - Schlafen - AUF"
#                try:
#                    self.fhz.RunMakro("RolloSchlafenAuf")
#                except:
#                    print "ablaufRollos.py - RunMakro FAILED"

                
        if (self.tLast <= self.tSchlafenZu < self.tNow) or ((self.tSchlafenZu == self.midnight) and (self.tLast > self.tNow)):
            print "AutoRollos - Schlafen - ZU"
            try:
                self.fhz.RunMakro("RolloSchlafenZu")
            except:
                print "ablaufRollos.py - RunMakro FAILED"
            
        
        
        pass

    
  
    def setting2time(self, settingsStr):
        s = settingsStr.zfill(5)
        hour = int(s[0:2])
        minu  = int(s[3:5])
        t = datetime.time(hour, minu)
        return t
    
        
