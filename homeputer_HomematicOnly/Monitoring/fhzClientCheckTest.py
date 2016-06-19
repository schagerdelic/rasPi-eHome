import fhzClientCheck
import os
import subprocess

f = fhzClientCheck.fhzClientCheck()

if not(f.isClientAlive('C:\Users\eHome\AppData\Local\homeputer\spg\Msgfile.txt')):
    subprocess.Popen('shutdown')


