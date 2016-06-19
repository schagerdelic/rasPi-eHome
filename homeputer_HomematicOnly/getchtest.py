import msvcrt
import time

for i in range(1,10):
    ch = msvcrt.getch()
    print ord(ch)
    time.sleep(1)
    
