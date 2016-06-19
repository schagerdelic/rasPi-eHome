#import win32com.client
#import xmlrpclib
from time import time                                         
from time import sleep                                        
import sys                                                    
import datetime
import fhz2000Interface
  
def setting2time(settingsStr):
        s = settingsStr.zfill(5)
        hour = int(s[0:2])
        minu  = int(s[3:5])
        t = datetime.time(hour, minu)
        return t
    
                                        
class FHZHMInterface:

   
    HM_Devices = {'sensor_schlafen'     : {'type':'sensor','HM_ID':'IEQ0022938'},  # ...Sensor_1
                  'sensor_bad'          : {'type':'sensor','HM_ID':'IEQ0022877'},  # ...Sensor_2
                  'sensor_kinder'       : {'type':'sensor','HM_ID':'IEQ0023308'},  # ...Sensor_3
                  'heizungsschalter'    : {'type':'schalter','HM_ID':'IEQ0040432'}, # ...Schalter_1
                  'sensor_wohnen'       : {'type':'sensor','HM_ID':'JEQ0122099'},  # ...Sensor_4
                  'sensor_gefrierfach'  : {'type':'sensor','HM_ID':'JEQ0490343'},  # ...Sensor_5
                  }


    HM_FHZDevNames = ['Temperatur_Schlafen', 'Feuchte_Schlafen', 'Temperatur_Bad','Feuchte_Bad', 'Temperatur_Kinder','Feuchte_Kinder', 'Temperatur_Wohnen','Feuchte_Wohnen','Temperatur_Gefrierfach']
    HM_FHZ_Converter = [['sensor_schlafen','TEMPERATURE'],['sensor_schlafen','HUMIDITY'],['sensor_bad','TEMPERATURE'],['sensor_bad','HUMIDITY'],['sensor_kinder','TEMPERATURE'],['sensor_kinder','HUMIDITY'],['sensor_wohnen','TEMPERATURE'],['sensor_wohnen','HUMIDITY'],['sensor_gefrierfach','TEMPERATURE']]

    # IF..... InterfaceType: FHZ|HM|CMD
    # ID......Adress/DeviceName
    # EXT.....extended/Channel
    # VAL.....Value/Command
    # CMD.....Makro Kommandos, Namen der Befehle die aufgerufen werden sollen
    HM_FHZ_Makros = {'LichtEssenAn':    {'IF':'FHZ','ID':'1112','EXT':'','VAL':'17+ON,+Last+value'},
                     'LichtEssenAus':   {'IF':'FHZ','ID':'1112','EXT':'','VAL':'00+OFF'},
                     'LichtWohnenAn':   {'IF':'FHZ','ID':'1113','EXT':'','VAL':'17+ON,+Last+value'},
                     'LichtWohnenAus':  {'IF':'FHZ','ID':'1113','EXT':'','VAL':'00+OFF'},
                     'LichtTVAn':       {'IF':'FHZ','ID':'1114','EXT':'','VAL':'17+ON,+Last+value'},
                     'LichtTVAus':      {'IF':'FHZ','ID':'1114','EXT':'','VAL':'00+OFF'},
                     'LichtSchlafenAn': {'IF':'FHZ','ID':'1311','EXT':'','VAL':'17+ON,+Last+value'},
                     'LichtSchlafenAus':{'IF':'FHZ','ID':'1311','EXT':'','VAL':'00+OFF'},
                     'RolloKuecheAuf':  {'IF':'FHZ','ID':'1211','EXT':'','VAL':'00+OFF'},
                     'RolloKuecheZu':   {'IF':'FHZ','ID':'1211','EXT':'','VAL':'17+ON,+Last+value'},
                     'RolloAusgangAuf': {'IF':'FHZ','ID':'1212','EXT':'','VAL':'00+OFF'},
                     'RolloAusgangZu':  {'IF':'FHZ','ID':'1212','EXT':'','VAL':'17+ON,+Last+value'},
                     'RolloEssenAuf':   {'IF':'FHZ','ID':'1213','EXT':'','VAL':'00+OFF'},
                     'RolloEssenZu':    {'IF':'FHZ','ID':'1213','EXT':'','VAL':'17+ON,+Last+value'},
                     'RolloArbeitAuf':  {'IF':'FHZ','ID':'1214','EXT':'','VAL':'00+OFF'},
                     'RolloArbeitZu':   {'IF':'FHZ','ID':'1214','EXT':'','VAL':'17+ON,+Last+value'},
                     'RolloSchlafenAuf':{'IF':'FHZ','ID':'1412','EXT':'','VAL':'00+OFF'},
                     'RolloSchlafenZu': {'IF':'FHZ','ID':'1412','EXT':'','VAL':'17+ON,+Last+value'},
                     'SonnensegelEinfahren':{'IF':'FHZ','ID':'2111','EXT':'','VAL':'00+OFF'},
                     'SonnensegelAusfahren':{'IF':'FHZ','ID':'2111','EXT':'','VAL':'17+ON,+Last+value'},
                     'WohnenRollosAuf':     {'IF':'FHZ','ID':'1244','EXT':'','VAL':'00+OFF'},
                     'WohnenRollosZu':      {'IF':'FHZ','ID':'1244','EXT':'','VAL':'17+ON,+Last+value'},
                     'LichtEssenAnTimer':   {'IF':'FHZ','ID':'1112','EXT':'4134','VAL':'23+Timer+on,+off'},
                     'WohnenLichterAus':    {'IF':'MAKRO','CMD':['LichtEssenAus','LichtWohnenAus','LichtTVAus']},
                     'WohnenLichterAn':     {'IF':'MAKRO','CMD':['LichtEssenAn','LichtWohnenAn','LichtTVAn']},
                     'WohnenGutenAbend':    {'IF':'MAKRO','CMD':['WohnenRollosZu','WohnenLichterAn']},
                     'WohnenGuteNacht':     {'IF':'MAKRO','CMD':['WohnenRollosZu','WohnenLichterAus']},
                     'SchlafenGutenAbend':  {'IF':'MAKRO','CMD':['RolloSchlafenZu','LichtSchlafenAn']},
                     'SchlafenGuteNacht':   {'IF':'MAKRO','CMD':['RolloSchlafenZu','LichtSchlafenAus']},
                     'Sonnenschutz':        {'IF':'MAKRO','CMD':['RolloKuecheZu','RolloEssenZu','RolloArbeitZu']},
                     }

    
    def __init__(self):                                     
        # self.fhz = win32com.client.Dispatch("homeputerStudio.ObjDataCom")
        self.fhz = fhz2000Interface.fhz2000Interface();
        #HM WIN SERVICEself.hmProxy = xmlrpclib.ServerProxy("http://localhost:2001/")

    def GetObjCnt(self):
        # return self.fhz.GetObjCnt()
        return 0;
    
    def GetObjValIdx(self,idx):
        return tuple(['-99', '-99', '-99', '-99'])
        '''   
        tmp1 = self.fhz.GetObjValIdx(idx)
        if (tmp1[1] == 'RaumTemperatur'):
            tmp1 = list(tmp1)
            tmp2 = tmp1;
            tmp2[4] = str(float(tmp1[4].replace(',','.')) - 0.6).replace('.',',').encode('utf8')
            return tuple(tmp2)            
        elif (tmp1[1] == 'Raumluftfeuchtigkeit'):
            tmp1 = list(tmp1)
            tmp2 = tmp1;
            tmp2[4] = str(float(tmp1[4].replace(',','.')) + 7).replace('.',',').encode('utf8')
            return tuple(tmp2)            
        else:    
            return tmp1
        '''

    def GetObjVal(self,objName):
        return tuple(["-99", "-99", "-99", "-99"])
        '''
        tmp1 = self.fhz.GetObjVal(objName)
        if (objName == 'RaumTemperatur'):
            tmp1 = list(tmp1)
            tmp2 = tmp1;
            tmp2[2] = str(float(tmp1[2].replace(',','.')) - 0.6).replace('.',',').encode('utf8')
            return tuple(tmp2)
        elif (objName == 'Raumluftfeuchtigkeit'):
            tmp1 = list(tmp1)
            tmp2 = tmp1;
            tmp2[2] = str(float(tmp1[2].replace(',','.')) + 7).replace('.',',').encode('utf8')
            return tuple(tmp2)            
        else:
            return tmp1


    def RunMakro(self,makroName):
        print('RUNMAKRO: '+makroName)
        return "OK" # self.fhz.RunMakro(makroName)

    def SetObjValName(self,objName, objVal):
        print('SETOBJVALNAME: '+objName+', VAL: '+objVal)
        return self.fhz.SetObjValName(objName,objVal)
    '''    
    def RunMakro(self,makroName):
        try:
            makro = self.HM_FHZ_Makros[makroName]
            if (makro['IF'] == 'FHZ'):
                # FHZ Interface
                self.fhz.sendCmd(makro['ID'],makro['EXT'],makro['VAL'])
                print('RUNMAKRO FHZ: ' + makroName)
            elif (makro['IF'] == 'HM'):
                # HomeMatic Interface
                self.SetObjVal_HM(makro['ID'],makro['EXT'],makro['VAL'])
                print('RUNMAKRO HomeMatic: ' + makroName)
            else:
                # len = len(makro['CMD'])
                for m in makro['CMD']:
                    self.RunMakro(m)
                print ('RUNMAKRO MAKRO: ' + makroName)
                    
                
            return "OK" # self.fhz.RunMakro(makroName)
        except:
            print "ERROR: RUNMAKRO failed: " + makroName
            return "NOK"

        
    def GetObjVal_HM(self,deviceName,valType):
        if ((valType.upper() == 'TEMPERATURE') or (valType.upper() == 'HUMIDITY')):
                chID = ':1'
        else:
                chID = ':0'

        #print self.HM_Devices[deviceName]+chID
        #print valType.upper()        
        #HM WIN SERVICEtmp = self.hmProxy.getValue(self.HM_Devices[deviceName]['HM_ID']+chID,valType.upper())
        tmp = -99
        return tmp
    
    def SetObjVal_HM(self, deviceName, chID, value):
        #print self.HM_Devices[deviceName]['HM_ID']+':'+str(chID)
        #HM WIN SERVICEself.hmProxy.setValue(self.HM_Devices[deviceName]['HM_ID']+':'+str(chID),'STATE',value)
        pass

 
