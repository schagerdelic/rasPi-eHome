import xmlrpclib


thermostat_1 = 'IEQ0022938' #...schlafen
thermostat_2 = 'IEQ0022877' #...bad
thermostat_3 = 'IEQ0023308' #...kinder

schalter_1  = 'IEQ0040432'


proxy = xmlrpclib.ServerProxy("http://localhost:2001/")

#print str(proxy.system.listMethods())
#devices = proxy.listDevices()
#print devices

#print devices[54]['ADDRESS']
#print len(devices)

#print str(proxy.system.methodSignature('init'))
#print proxy.getValue(thermostat_1+':0','UNREACH')
#print proxy.getValue(thermostat_1+':0','LOWBAT')

#print proxy.getValue(thermostat_1+':1','TEMPERATURE')
#print proxy.getValue(thermostat_1+':1','HUMIDITY')

print 'SENSOR 1'
print proxy.getParamset(thermostat_1+':0','VALUES')
print proxy.getParamset(thermostat_1+':1','VALUES')

print 'SENSOR 2'
print proxy.getParamset(thermostat_2+':0','VALUES')
print proxy.getParamset(thermostat_2+':1','VALUES')

print 'SENSOR 3'
print proxy.getParamset(thermostat_3+':0','VALUES')
print proxy.getParamset(thermostat_3+':1','VALUES')

#print proxy.getParamset(schalter_1+':0','VALUES')
#print proxy.getParamset(schalter_1+':1','VALUES')
#print proxy.getParamset(schalter_1+':2','VALUES')
#print proxy.getParamset(schalter_1+':3','VALUES')
#print proxy.getParamset(schalter_1+':4','VALUES')

print 'SCHALTER'
state_temp = proxy.getValue(schalter_1+':1','STATE')
print proxy.setValue(schalter_1+':1','STATE',not(state_temp))

print proxy.getValue(schalter_1+':0','UNREACH',False)

print "DONE"
del proxy
