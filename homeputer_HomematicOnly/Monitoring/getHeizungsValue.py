import sys
import jsonIO

f = open("/var/www/eHome/eHomeHeizungVals.json","r")
str = f.read()
f.close()

obj = jsonIO.read(str[1:-1])
print obj[sys.argv[1]]



