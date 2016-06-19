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

import datetime
import httplib2
import os

from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools



argv = ''
__file__ = 'googleCal.py'



class GoogleCal:


  # Authenticate and construct service.

  heizungAUS_ID = '5oskoi2rcnklb0j8bk2evqp2rs@group.calendar.google.com'
  heizung_ID = 'ehfn31cohbi9lapr766u0qiqvo@group.calendar.google.com'
  service = None;

  def __init__(self):
    scope='https://www.googleapis.com/auth/calendar.readonly'
    client_secrets = 'client_secrets.json'
    flow = client.flow_from_clientsecrets(client_secrets,scope=scope)

    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'eHome_RasPi.json')


    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(client_secrets, scope)
        flow.user_agent = __file__ 
        credentials = tools.run_flow(flow, store, None)
    http = credentials.authorize(httplib2.Http())
    self.service = discovery.build('calendar', 'v3', http=http)


  def isEventAt(self, cal_id, eventTime):

    try:

      cal = self.service.calendarList().get(calendarId=cal_id).execute()
      
      #print calendar_AN['summary']
      t1 = eventTime;#datetime.datetime.now()
      t2 = t1 + datetime.timedelta(0,3)
      t1 = str(t1).replace(" ","T") + "+02:00"
      t2 = str(t2).replace(" ","T") + "+02:00"

      
      page_token = None
      eventList = self.service.events().list(calendarId=cal_id,timeMin=t1,timeMax=t2).execute()
      
    except client.AccessTokenRefreshError:
      print ('The credentials have been revoked or expired, please re-run'
        'the application to re-authorize.')


    return len(eventList['items']) > 0 


##myCal = GoogleCal()
##
##cal_id = 'ehfn31cohbi9lapr766u0qiqvo@group.calendar.google.com'
##start_date='2011-10-10T07:00:00.1234+02:00'
##end_date='2011-10-10T07:00:05.5687+02:00'
##
##print myCal.isEventAt(cal_id, datetime.datetime.now() - datetime.timedelta(hours = 3))


