import FHZHMInterface

fhz=FHZHMInterface.FHZHMInterface()

##print ("wohnen:")
##print fhz.GetObjVal_HM("sensor_wohnen","HUMIDITY")
##print ("schlafen:")
##print fhz.GetObjVal_HM("sensor_schlafen","TEMPERATURE")
##print ("wohnen:")
##print fhz.GetObjVal_HM("sensor_wohnen","TEMPERATURE")
##print ("kinder:")
##print fhz.GetObjVal_HM("sensor_kinder","TEMPERATURE")
##print ("bad:")
##print fhz.GetObjVal_HM("sensor_bad","TEMPERATURE")

#fhz.RunMakro("Sonnenschutz")
#print ("Sonnenschutz")

#fhz.RunMakro("WohnenRollosZu")
#print ("WohnenRollosZu")


fhz.RunMakro("HeizungWohnenAus")
fhz.RunMakro("HeizungSchlafenAus")
fhz.RunMakro("HeizungBadAus")
fhz.RunMakro("HeizungKinderAus")
