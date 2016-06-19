
try:
  from xml.etree import ElementTree
except ImportError:
  from elementtree import ElementTree
import gdata.calendar.data
import gdata.calendar.client
import gdata.calendar.service
import gdata.acl.data
import atom
import getopt
import sys
import string
import time



class GoogleCal:
  def __init__(self, email, password):
    self.cal_client = gdata.calendar.service.CalendarService()
    self.cal_client.ClientLogin(email, password, self.cal_client.source);

  def getEvents(self, cal_id = 'default', start_date='2012-01-01', end_date='2012-02-01'):
    """Retrieves events from the server which occur during the specified date
    range.  This uses the CalendarEventQuery class to generate the URL which is
    used to retrieve the feed.  For more information on valid query parameters,
    see: http://code.google.com/apis/calendar/reference.html#Parameters"""

    print cal_id
    query = gdata.calendar.service.CalendarEventQuery(cal_id,'private','full')
    query.start_min = start_date
    query.start_max = end_date
    #query.user = 'ehfn31cohbi9lapr766u0qiqvo@group.calendar.google.com'
    feed = self.cal_client.CalendarQuery(query)
    for i, an_event in zip(xrange(len(feed.entry)), feed.entry):
      print '\t%s. %s' % (i, an_event.title.text,)
      #print an_event.when  
      #for a_when in an_event.when:
      #  print '\t\tStart time: %s' % (a_when.startTime,)
      #  print '\t\tEnd time:   %s' % (a_when.endTime,)

    #print 'TEST'
    
    #print 'Cals'
    #feed = self.cal_client.GetAllCalendarsFeed()
    #cal_list = [x.title.text for x in feed.entry]
    #print cal_list
    #theID = feed.entry[cal_list.index('Heizung')].id.text
    #print theID


#user = 'ehfn31cohbi9lapr766u0qiqvo@group.calendar.google.com'
#user = 'ehfn31cohbi9lapr766u0qiqvo'

user = 'g.schagerl@gmail.com'
pw = 'gAnEmuGee'

myCal = GoogleCal(user, pw)

cal_id = 'ehfn31cohbi9lapr766u0qiqvo@group.calendar.google.com'
start_date='2011-10-10T07:00:00+02:00'
end_date='2011-10-10T07:00:10+02:00'

t1 = datetime.datetime.now()
t2 = t1 + datetime.timedelta(0,3)
print str(t1).replace(" ","T") + "+02:00"
print str(t2).replace(" ","T") + "+02:00"

myCal.getEvents(cal_id, start_date, end_date)


