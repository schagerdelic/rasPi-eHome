#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2014 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Simple command-line sample for the Calendar API.
Command-line application that retrieves the list of the user's calendars."""

import sys

from oauth2client import client
from oauth2client import gce
from googleapiclient import sample_tools
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import OAuth2WebServerFlow
import datetime

#flow = flow_from_clientsecrets('Google_Client_Secret_API Project-a0e468fd7ad1.json', scope='https://www.googleapis.com/auth/calendar', redirect_uri='http://example.com/auth_return')



#credentials = flow.

#credentials = gce.AppAssertionCredentials(scope='https://www.googleapis.com/auth/devstorage.read_write')
#http = credentials.authorize(httplib2.Http())

# List my public Google+ activities.
#result = service.activities().list(userId='me', collection='public').execute()
#tasks = result.get('items', [])
#for task in tasks:
#  print task['title']

argv = ''
__file__ = 'googleCal.py'



print __doc__
print __file__

class GoogleConnect:


  # Authenticate and construct service.

  heizungAUS_ID = '5oskoi2rcnklb0j8bk2evqp2rs@group.calendar.google.com'
  heizung_ID = 'ehfn31cohbi9lapr766u0qiqvo@group.calendar.google.com'


  def __init__(self):
    self.service, flags = sample_tools.init(
    argv, 'calendar', 'v3', __doc__, __file__,
    scope='https://www.googleapis.com/auth/calendar')

    scope='https://www.googleapis.com/auth/calendar'
    client_secrets = 'client_secrets.json'
    flow = client.flow_from_clientsecrets(client_secrets,
          scope=scope,
          message='ERROR')

#print service, flags


  def isEventAt(self, cal_id, eventTime):

    try:
##      page_token = None
##      while True:
##        calendar_list = service.calendarList().list(pageToken=page_token).execute()
##        for calendar_list_entry in calendar_list['items']:
##          print calendar_list_entry['id']
##        page_token = calendar_list.get('nextPageToken')
##
##        if not page_token:
##          break
##
##      calendar_AUS = service.calendarList().get(calendarId=heizungAUS_ID).execute()
##      calendar_AN = service.calendarList().get(calendarId=heizung_ID).execute()

      cal = self.service.calendarList().get(calendarId=cal_id).execute()
      
      #print calendar_AN['summary']
      t1 = eventTime;#datetime.datetime.now()
      t2 = t1 + datetime.timedelta(0,3)
      t1 = str(t1).replace(" ","T") + "+02:00"
      t2 = str(t2).replace(" ","T") + "+02:00"

      print t1
      print t2
      
      page_token = None
      eventList = self.service.events().list(calendarId=cal_id,timeMin=t1,timeMax=t2).execute()
      for eventList_Entry in eventList['items']:
        print eventList_Entry['start']
        print eventList_Entry['end']
          
        #page_token = calendar_list.get('nextPageToken')
      
    except client.AccessTokenRefreshError:
      print ('The credentials have been revoked or expired, please re-run'
        'the application to re-authorize.')

    print 'done'
    return eventList['items'].count > 0 


myCal = GoogleConnect()

cal_id = 'ehfn31cohbi9lapr766u0qiqvo@group.calendar.google.com'
start_date='2011-10-10T07:00:00.1234+02:00'
end_date='2011-10-10T07:00:05.5687+02:00'

print myCal.isEventAt(cal_id, datetime.datetime.now())


