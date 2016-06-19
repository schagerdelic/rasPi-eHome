import os
import subprocess
import time
import ctypes

PROP_BELOW_NORMAL = 0x00004000
PRIO_IDLE = 0x00000040
p6 = subprocess.Popen('"C:\\windows\\explorer.exe" "Q:\\"')
print '1'
time.sleep(10)
print '2'

killCmd = "taskkill /IM Qweb"

print killCmd

p7 = subprocess.Popen(killCmd)
