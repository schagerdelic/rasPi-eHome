# -*- coding: cp1252 -*-
import os
import sys
import datetime
import time, wave
import statusCheck
import FHZHMInterface


##try:
##  from xml.etree import ElementTree
##except ImportError:
##  from elementtree import ElementTree
##import gdata.calendar.data
##import gdata.calendar.client
##import gdata.calendar.service
##import gdata.acl.data
##import atom
import getopt
import string
import GoogleCal


class AutoHeizung:
    tNow = 0
    tLast = 0
    tToday = 0
    statusJetzt = None
    statusVorher = None
    fhz = 0
    
    HYST = 0.2
    user =  'g.schagerl@gmail.com'
 
    
    def __init__(self):
        self.tNow = datetime.datetime.now().time()
        self.tLast = datetime.datetime.now().time()
        self.tToday = datetime.datetime.now().date().weekday()
        self.statusJetzt = statusCheck.HausStatus()
        self.statusVorher = statusCheck.HausStatus()
        self.fhz = 0
        #self.cal_client = gdata.calendar.service.CalendarService()
        #self.cal_client.ClientLogin(self.user, self.pw, self.cal_client.source);
        self.googleCal = GoogleCal.GoogleCal()

    def initXBMC(self, fhz, settings):
        self.fhz = fhz
        self.heizungAN = settings.getSetting("HeizungAn")
        self.heizungsModus = settings.getSetting("HeizungsModus")
        self.tempDMDWohnen = float(settings.getSetting("TempWohnen"))
        self.tempDMDSchlafen = float(settings.getSetting("TempSchlafen"))
        self.tempDMDBad = float(settings.getSetting("TempBad"))
        self.tempDMDKinder = float(settings.getSetting("TempKinder"))
        self.tempNachtAbsenkung = float(settings.getSetting("Nachtabsenkung"))
        self.tNacht  = FHZHMInterface.setting2time(settings.getSetting("HeizungZeitNacht"))
        self.tTag  = FHZHMInterface.setting2time(settings.getSetting("HeizungZeitTag"))        
        pass


    def getUhrzeitModus(self):
        modus = 'tag'
        if (self.tTag < self.tNacht):
            if (self.tTag < self.tNow < self.tNacht):
                modus = 'tag'
            else:
                modus = 'nacht'
                
        if (self.tNacht < self.tTag):
            if (self.tNacht < self.tNow < self.tTag):
                modus = 'nacht'
            else:
                modus = 'tag'

        return modus


    def getKalenderModus(self):
        modus = 'nacht'

        if self.googleCal.isEventAt(GoogleCal.GoogleCal.heizung_ID, datetime.datetime.now()):
            modus = 'tag'
        if self.googleCal.isEventAt(GoogleCal.GoogleCal.heizungAUS_ID, datetime.datetime.now()):
            modus = 'nacht'
        #print modus
        return modus

    
    def update(self, time, aktStatus):
        self.tLast = self.tNow
        self.tNow = time
        self.tToday = datetime.datetime.now()
        self.statusVorher = self.statusJetzt.copy()
        self.statusJetzt = aktStatus#.copy()

        if (self.heizungAN == False):
            try:
                self.fhz.RunMakro('HeizungWohnenAn')
                self.fhz.RunMakro('HeizungSchlafenAn')
                self.fhz.RunMakro('HeizungBadAn')
                self.fhz.RunMakro('HeizungKinderAn')

                #self.statusJetzt.schalterUnreach = False
                #print('Schalter OK')
                return

            except Exception, err:
                #print('Schalter UNREACH')
                #self.statusJetzt.schalterUnreach = True
                return    
        
        modus = 'tag'
        # welcher Regelmodus ist aktiv?
        if (self.heizungsModus == 'Tag'):
            modus = 'tag'

        if (self.heizungsModus == 'Nacht'):
            modus = 'nacht'

        if (self.heizungsModus == 'Uhrzeit'):
            modus = self.getUhrzeitModus()
        
        if (self.heizungsModus == 'Kalender'):
            modus = self.getKalenderModus()

        if (self.heizungsModus == 'An'):
            modus = 'an'
            self.tempDMDWohnen   = 99
            self.tempDMDSchlafen = 99
            self.tempDMDBad      = 99
            self.tempDMDKinder   = 99

        #print "MODUS:"+modus


        if (modus == 'nacht'):
            self.tempDMDWohnen   = self.tempDMDWohnen   - self.tempNachtAbsenkung
            self.tempDMDSchlafen = self.tempDMDSchlafen - self.tempNachtAbsenkung
            self.tempDMDBad      = self.tempDMDBad      - self.tempNachtAbsenkung
            self.tempDMDKinder   = self.tempDMDKinder   - self.tempNachtAbsenkung

        
        try:
            # ACHTUNG: heizungsschalter  True heisst HEIZUNG AUS
            if (self.statusJetzt.tempWohnen < self.tempDMDWohnen):
                self.fhz.RunMakro('HeizungWohnenAn')
                self.statusJetzt.heizenWohnen = 1 
            else:
                self.fhz.RunMakro('HeizungWohnenAus')
                self.statusJetzt.heizenWohnen = 0 
                
            if (self.statusJetzt.tempSchlafen < self.tempDMDSchlafen):
                self.fhz.RunMakro('HeizungSchlafenAn')
                self.statusJetzt.heizenSchlafen = 1 
            else:
                self.fhz.RunMakro('HeizungSchlafenAus')
                self.statusJetzt.heizenSchlafen = 0 

            if (self.statusJetzt.tempBad < self.tempDMDBad):
                self.fhz.RunMakro('HeizungBadAn')
                self.statusJetzt.heizenBad = 1
            else:
                self.fhz.RunMakro('HeizungBadAus')
                self.statusJetzt.heizenBad = 0

            if (self.statusJetzt.tempKinder < self.tempDMDKinder):
                self.fhz.RunMakro('HeizungKinderAn')
                self.statusJetzt.heizenKinder = 1
            else:
                self.fhz.RunMakro('HeizungKinderAus')
                self.statusJetzt.heizenKinder = 0
            #self.statusJetzt.schalterUnreach = False
            #print('Schalter OK')

        except Exception, err:
            #print('Schalter UNREACH')
            #self.statusJetzt.schalterUnreach = True
            pass

        pass

     
