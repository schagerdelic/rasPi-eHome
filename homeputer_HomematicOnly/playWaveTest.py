import os
import sys
import win32com.client
import pythoncom
import datetime
import time, wave
import pyaudio

filename = 'C:\\XBMC911\\scripts\\HomeControl\\resources\\esregnet.wav'
    chunk = 1024
    wf = wave.open(filename, 'rb')
    p = pyaudio.PyAudio()

    dev_cnt = p.get_device_count()

    if dev_cnt == 7:
    # open stream
        stream1 = p.open(format =
                        p.get_format_from_width(wf.getsampwidth()),
                        channels = wf.getnchannels(),
                        rate = wf.getframerate(),
                        output_device_index = 4,
                        output = True)

        stream2 = p.open(format =
                        p.get_format_from_width(wf.getsampwidth()),
                        channels = wf.getnchannels(),
                        rate = wf.getframerate(),
                        output_device_index = 5,
                        output = True)
        # read data
        data = wf.readframes(chunk)

        # play stream
        while data != '':
            stream1.write(data)
            stream2.write(data)
            data = wf.readframes(chunk)

        stream1.close()
        stream2.close()

    if dev_cnt == 5:
    # open stream
        stream1 = p.open(format =
                        p.get_format_from_width(wf.getsampwidth()),
                        channels = wf.getnchannels(),
                        rate = wf.getframerate(),
                        output_device_index = 3,
                        output = True)

        # read data
        data = wf.readframes(chunk)

        # play stream
        while data != '':
            stream1.write(data)
            data = wf.readframes(chunk)

        stream1.close()


    p.terminate()
