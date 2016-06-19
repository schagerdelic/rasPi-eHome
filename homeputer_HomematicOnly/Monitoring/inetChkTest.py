import inetCheck

inetCheck = reload(inetCheck)
print "============"
ic = inetCheck.inetCheck()
print ic.isConnectionAlive("www.schagerdelic.com","/eHome/dyndns.php")

#print ic.resetRouter()
