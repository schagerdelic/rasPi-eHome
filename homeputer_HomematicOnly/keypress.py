import sys
import time
import msvcrt

for i in range(1,10):
    time.sleep(1)
    #ch = msvcrt.getch()
    if msvcrt.kbhit():
	print ord(msvcrt.getch())

