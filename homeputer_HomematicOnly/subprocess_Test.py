#import subprocess
#serverProc = subprocess.Popen('ls',shell=True, stdout = subprocess.)

#import subprocess
import shlex
import os
#process = subprocess.Popen(" /home/pi/homeputer_HomematicOnly/print_loop.py", stdout=subprocess.PIPE)

#process = os.popen("/home/pi/homeputer_HomematicOnly/print_loop.py")

os.system("x-terminal-emulator -e python /home/pi/homeputer_HomematicOnly/Monitoring/myFHZServerMT.py")

#process = subprocess.Popen("x-terminal-emulator -e", stdout=subprocess.PIPE);
#process.wait()
