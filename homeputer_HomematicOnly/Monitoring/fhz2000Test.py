import fhz2000Interface
import FHZHMInterface


fhzhm = reload(FHZHMInterface)
print "============"
fhzhm = FHZHMInterface.FHZHMInterface()

fhz2000Interface = reload(fhz2000Interface)
print "============"
fhz2000 = fhz2000Interface.fhz2000Interface()
#fhz2000.login()

#fhz2000.sendCmd("1114","","00+OFF");

#fhz2000.sendCmd("1114","","17+ON,+Last+value");
#ID':'1112','EXT':'1411','VAL':'23+Timer+on,+off
#fhz2000.sendCmd("1112","1411","23+Timer+on,+off"); # OK
fhzhm.RunMakro("LichtEssenAnTimer")

#fhz2000.LichtAus("1112")
#fhz2000.LichtAn("1112")

#fhz2000.RolloAuf("1211")
#fhz2000.RolloZu("1211")
#fhz2000.RolloZu("1211","1224") #(12=1, 24=32sec), 13=1sec

print "DONE"

#print ic.resetRouter()
