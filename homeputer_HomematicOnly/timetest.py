# -*- coding: cp1252 -*-
import sys
import datetime

if __name__ == '__main__':
    
    print 'Hallo Welt\n'
    mytime = '23:59'
    hour = mytime[0:2]
    minu = mytime[3:5]


    testtime = datetime.time(int(hour), int(minu))
    now = datetime.datetime.now().time()

    tToday = datetime.datetime.now().date().weekday()
    print tToday
    
    #print now
    #print testtime

    if now > testtime:
        print 'es ist spät'
    else:
        print 'zu früh'


        



#   1.
#      # using just time and not date ...
#   2.
#      import datetime
#   3.
#       
#   4.
#      lunch_start = datetime.time(11, 30)
#   5.
 #     lunch_end = datetime.time(12, 45)
#   6.
#      now = datetime.datetime.now().time()
 #  7.
#       
#   8.
#      # testing
#   9.
#      print lunch_start # 11:30:00
#  10.
#      print lunch_end # 12:45:00
 # 11.
#      print now # eg. 09:05:59.750000
#  12.
#       
#  13.
#      # you can compare type 'datetime.time' directly
#  14.
 #     if lunch_start < now < lunch_end:
 # 15.
#      print "Hey, it's lunch time! Mahlzeit!!"
#  16.
 ##     elif now < lunch_start:
#  17.
 #     print "Lunch is pretty soon!"
 # 18.
 #     else:
#  19.
###      print "Darn, missed lunch time!!"
