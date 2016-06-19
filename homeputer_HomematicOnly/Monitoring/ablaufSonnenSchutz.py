import os
import sys
#import win32com.client
#import pythoncom
import datetime

class AutoSonnenSchutz:
    tNow = 0
    tLast = 0
    tWohnenAuf = 0
    tWohnenZu = 0
    fhz = 0
    
    
    
    def __init__(self):
        self.tNow = datetime.datetime.now().time()
        self.tLast = datetime.datetime.now().time()
        self.tWohnenAuf = self.tNow
        self.tWohnenZu = self.tNow
        self.midnight = datetime.time(0,0)
        
        self.fhz = 0
        
    
    def initXBMC(self, fhz, settings):
        self.fhz = fhz
        self.tWohnenZu  = self.setting2time(settings.getSetting("SonnenschutzRunter"))
        self.tWohnenAuf  = self.setting2time(settings.getSetting("SonnenschutzRauf"))
        pass

    def initTest(self,fhz,t1,t2,t3,t4):
        self.tWohnenAuf = t1
        self.tWohnenZu = t3
        self.fhz = fhz
        pass
    
    def update(self, time):
        self.tLast = self.tNow
        self.tNow = time
        
        if (self.tLast <= self.tWohnenAuf < self.tNow) or ((self.tWohnenAuf == self.midnight) and (self.tLast > self.tNow)):
            print "Automatischer Sonnenschutz - AUF"
            try:
                self.fhz.RunMakro("WohnenRollosAuf")
                print "FHZ RunMakro - OK"
            except:
                print "ablaufSonnenSchutz.py - RunMakro FAILED"
                

        if (self.tLast <= self.tWohnenZu < self.tNow) or ((self.tWohnenZu == self.midnight) and (self.tLast > self.tNow)):
            print "Automatischer Sonnenschutz - ZU"
            try:
                print self.fhz
                self.fhz.RunMakro("Sonnenschutz")
            except:
                print "ablaufSonnenSchutz.py - RunMakro FAILED"        
        
        pass

    
  
    def setting2time(self, settingsStr):
        s = settingsStr.zfill(5)
        hour = int(s[0:2])
        minu  = int(s[3:5])
        t = datetime.time(hour, minu)
        return t
    
        
