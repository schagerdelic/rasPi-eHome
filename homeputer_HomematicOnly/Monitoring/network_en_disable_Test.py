import time
import subprocess

p1 = subprocess.Popen('netsh interface set interface name=LAN admin=DISABLED')
time.sleep(5)
p2 = subprocess.Popen('netsh interface set interface name=LAN admin=ENABLED')
time.sleep(10)
p3 = subprocess.Popen('"C:\\windows\\explorer.exe" "Q:\\"')
