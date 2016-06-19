import os
import sys
#import win32com.client
#import pythoncom
import datetime

class AutoBewaesserung:
    
    def __init__(self):
        self.tNow = datetime.datetime.now().time()
        self.tLast = datetime.datetime.now().time()
        self.tToday = datetime.datetime.now().date().weekday()
        self.tMorgen = self.tNow
        self.morgenDauer = 5
        self.tAbend = self.tNow
        self.abendDauer = 5
        self.autoMorgen = False
        self.autoAbend = False
        self.niederSchlagsLimit = 99
        self.fhz = 0
        
    
    def initXBMC(self, fhz, settings):
        self.fhz = fhz
        self.tToday = datetime.datetime.now().date().weekday()
        self.tMorgen = self.setting2time(settings.getSetting("WasserMorgensUhrzeit"))
        self.morgenDauer = float(settings.getSetting("WasserMorgensDauer"))
        self.tAbend = self.setting2time(settings.getSetting("WasserAbendsUhrzeit"))
        self.abendDauer = float(settings.getSetting("WasserAbendsDauer"))
        self.autoMorgen = settings.getSetting("autoWasserMorgens")
        self.autoAbend = settings.getSetting("autoWasserAbends")
        self.niederSchlagsLimit = float(settings.getSetting("RegenLimit"))

    
    def update(self, time, aktStatus):
        self.tLast = self.tNow
        self.tNow = time
        self.tToday = datetime.datetime.now().date().weekday()
        try:
            self.niederSchlagL = float(aktStatus.regenLTagStr.replace(",","."))
        except:
            self.niederSchlagL = 0.0

        try:    
            self.niederSchlagA = float(aktStatus.regenATagStr.replace(",","."))
        except:
            self.niederSchlagA = 0.0
            
        self.esRegnet = aktStatus.esRegnet

        
        #MORGENS
        if ((self.autoMorgen) and (self.niederSchlagL < self.niederSchlagsLimit) and (self.tLast <= self.tMorgen < self.tNow)):
            try:
                print "Bewaesserung - AN"
                if (self.morgenDauer == 5):
                    self.fhz.RunMakro("Bewaesserung05min")
                elif (self.morgenDauer == 15):
                    self.fhz.RunMakro("Bewaesserung15min")
                elif (self.morgenDauer == 30):
                    self.fhz.RunMakro("Bewaesserung30min")
                print "FHZ RunMakro - OK"
            except:
                print "ablaufBewaesserung.py - RunMakro FAILED"


        #MORGENS
        if ((self.autoAbend) and (self.niederSchlagA < self.niederSchlagsLimit) and (self.tLast <= self.tAbend < self.tNow)):
            try:
                print "Bewaesserung - AN"
                if (self.abendDauer == 5):
                    self.fhz.RunMakro("Bewaesserung05min")
                elif (self.abendDauer == 15):
                    self.fhz.RunMakro("Bewaesserung15min")
                elif (self.abendDauer == 30):
                    self.fhz.RunMakro("Bewaesserung30min")
                print "FHZ RunMakro - OK"
            except:
                print "ablaufBewaesserung.py - RunMakro FAILED"

        pass

    
  
    def setting2time(self, settingsStr):
        s = settingsStr.zfill(5)
        hour = int(s[0:2])
        minu  = int(s[3:5])
        t = datetime.time(hour, minu)
        return t
    
        
