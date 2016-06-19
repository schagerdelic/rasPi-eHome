import httplib, urllib, mimetypes, time



class fhz2000Interface:

    hauscode = "23322332"
    

    def sendCmd(self,adr,ext,cmd):
#GET /fs20.cgi?pg=sys&fshc=23322332&fsadr=1112&fsext=&fscmd=00+OFF HTTP/1.1
#Host: 192.168.0.111
#Connection: keep-alive
#Authorization: Basic YWRtaW46
#Referer: http://192.168.0.111/fs20.cgi
        try:
            params = urllib.urlencode({"":""})
            headers = {"Connection": "keep-alive","Authorization": "Basic YWRtaW46","Referer":"http://192.168.0.111/fs20.cgi"}

            conn = httplib.HTTPConnection("192.168.0.111")
            conn.request("GET", "/fs20.cgi?pg=sys&fshc="+self.hauscode+"&fsadr="+adr+"&fsext="+ext+"&fscmd="+cmd, params, headers)
            response = conn.getresponse()
#            print response.status
            return True
        
        except Exception, err:
            return False
    
    def LichtAn(self,adr):
        self.sendCmd(adr,"","17+ON,+Last+value")

    def LichtAus(self,adr):
        self.sendCmd(adr,"","00+OFF")

    def RolloAuf(self,adr):         #OFF = Auf
        self.sendCmd(adr,"","00+OFF")

    def RolloAuf(self,adr,ext):     #OFF = Auf
        self.sendCmd(adr,ext,"22+Timer+off")

    def RolloZu(self,adr):         #ON = Zu
        self.sendCmd(adr,"","00+OFF")

    def RolloZu(self,adr,ext):     #ON = Zu
        self.sendCmd(adr,ext,"23+Timer+on,+off")
        
    def resetRouter(self): 
        try:
            params = urllib.urlencode({'page': 'login', 'lang_code': 'us', 'charset': 'iso-8859-1', 'logout': '2', 'login_password': '7fc132923bcfc14b4a21e8db16a5ed39'})
            headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}

            conn = httplib.HTTPConnection("192.168.0.1")
            conn.request("POST", "/password.cgi", params, headers)
            response = conn.getresponse()
            #print response.status
            time.sleep(1)

            boundary = '---------------------myBOUNDARY'
            content_type = 'multipart/form-data; boundary=' + boundary
            body = '\r\n'+boundary+'--\r\n'
            conn.putrequest('POST', "/system_restart.cgi")
            conn.putheader('content-type', content_type)
            conn.putheader('content-length', str(len(body)))
            conn.endheaders()
            conn.send(body)
            response = conn.getresponse()
            #print response.status
            time.sleep(1)

            conn.request("GET", "/reset_success.htm")
            response = conn.getresponse()
            #print response.status
            time.sleep(1)

            conn.request("GET", "/pre_reboot.htm")
            response = conn.getresponse()
            #print response.status
            time.sleep(2)

            conn.request("GET", "/reboot.htm")
            response = conn.getresponse()
            #print response.status
            conn.close()

            print("RESET ROUTER")
            time.sleep(100)

            return True
        
        except Exception, err:
            return False
        
