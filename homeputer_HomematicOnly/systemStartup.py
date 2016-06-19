import os
import subprocess
import time

import RPi.GPIO as GPIO
from time import sleep

# Needs to be BCM. GPIO.BOARD lets you address GPIO ports by periperal
# connector pin number, and the LED GPIO isn't on the connector
GPIO.setmode(GPIO.BCM)

# 3 pin von oben aussen = GND, 4 pin von oben aussen ist GPIO14
#GPIO.setup(14,GPIO.IN,pull_up_down = GPIO.PUD_UP)
#if GPIO.input(14) == 0:
os.chdir("/home/pi/eHome/homeputer_HomematicOnly/Monitoring/")
subprocess.Popen(["lxterminal", "-e", "sudo python /home/pi/eHome/homeputer_HomematicOnly/Monitoring/monitoring_RasPi.py"])
#else:
#    print "PIN 3 und 4 (oben, aussen) nicht verbunden. Ausfuehrung abgebrochen"
#    ret = raw_input("press any key...")


#PROP_BELOW_NORMAL = 0x00004000
#PRIO_IDLE = 0x00000040

#time.sleep(60)
#p1 = subprocess.Popen('"C:\\Program Files\\homeputer Standard\\homeputerStandard.exe"')
#time.sleep(10)
#p6 = subprocess.Popen('"C:\\windows\\explorer.exe" "Q:\\"')
#time.sleep(100)
#p3 = subprocess.Popen('"C:\\Python27\\python.exe" "C:\\Users\\eHome\\Documents\\homeputer_HomematicOnly\\Monitoring\\monitoring_HomeMaticOnly.py"')
#time.sleep(10)
#p5 = subprocess.Popen('"C:\Program Files\Safari\Safari.exe" "http://192.168.0.100/eHome/"')





#p2 = subprocess.Popen('"C:\\Python24\\python.exe" "C:\\Users\\eHome\\Documents\\homeputer\\myFHZServer.py"')
#time.sleep(5)
#p5 = subprocess.Popen('"C:\Users\eHome\AppData\Local\Google\Chrome\Application\chrome.exe" "http://fhz:fhz@192.168.0.100/eHome/"')
#p4 = subprocess.Popen('"C:\\Users\\eHome\\Documents\\homeputer\\bewegungsMeldung\\facedetect32.exe" "-1" "200" "80" "60" "40" "60000" "3" "0" "0"')
#time.sleep(5)
#p5 = subprocess.Popen('"C:\\XBMC911\\XBMC.exe" "-p"', creationflags = PRIO_IDLE)

