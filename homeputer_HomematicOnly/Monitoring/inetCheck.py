import httplib, urllib, mimetypes, time



class inetCheck:

    def isConnectionAlive(self,url, resource = ""):
        try:
            conn = httplib.HTTPConnection(url)
            conn.request("GET", resource )
            response = conn.getresponse()
            #print response.status
            conn.close()
            return True
        except Exception, err:
            return False
        
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
        
