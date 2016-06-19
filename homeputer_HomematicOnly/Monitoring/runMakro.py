#import imp
#fhz = imp.load_source('module.name', '/home/pi/homeputer_HomematicOnly/Monitoring/FHZHMInterface.py')
import FHZHMInterface
import sys


fhz=FHZHMInterface.FHZHMInterface()
fhz.RunMakro(sys.argv[1])


