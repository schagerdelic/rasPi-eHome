import sys

eHomeSettings = reload(sys.modules['eHomeSettings'])

__settings__ = eHomeSettings.eHomeSettings("Q:\\eHome\\eHomeSettings.json")
__settings__.getSetting("online")

__settings__.getSetting("TempKinder")
s  = __settings__.getSetting("TempKinder")
print s
    
