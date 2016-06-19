import httplib, urllib, mimetypes, time

def post_multipart(host, selector, fields, files):
    """
    Post fields and files to an http host as multipart/form-data.
    fields is a sequence of (name, value) elements for regular form fields.
    files is a sequence of (name, filename, value) elements for data to be uploaded as files
    Return the server's response page.
    """
    content_type, body = encode_multipart_formdata(fields, files)
    h = httplib.HTTP(host)
    h.putrequest('POST', selector)
    h.putheader('content-type', content_type)
    h.putheader('content-length', str(len(body)))
    h.endheaders()
    h.send(body)
    errcode, errmsg, headers = h.getreply()
    return h.file.read()

def encode_multipart_formdata(fields, files):
    """
    fields is a sequence of (name, value) elements for regular form fields.
    files is a sequence of (name, filename, value) elements for data to be uploaded as files
    Return (content_type, body) ready for httplib.HTTP instance
    """
    BOUNDARY = '----------ThIs_Is_tHe_bouNdaRY_$'
    CRLF = '\r\n'
    L = []
    for (key, value) in fields:
        L.append('--' + BOUNDARY)
        L.append('Content-Disposition: form-data; name="%s"' % key)
        L.append('')
        L.append(value)
    for (key, filename, value) in files:
        L.append('--' + BOUNDARY)
        L.append('Content-Disposition: form-data; name="%s"; filename="%s"' % (key, filename))
        L.append('Content-Type: %s' % get_content_type(filename))
        L.append('')
        L.append(value)
    L.append('--' + BOUNDARY + '--')
    L.append('')
    body = CRLF.join(L)
    content_type = 'multipart/form-data; boundary=%s' % BOUNDARY
    return content_type, body

def get_content_type(filename):
    return mimetypes.guess_type(filename)[0] or 'application/octet-stream'



params = urllib.urlencode({'page': 'login', 'lang_code': 'us', 'charset': 'iso-8859-1', 'logout': '2', 'login_password': '7fc132923bcfc14b4a21e8db16a5ed39'})
headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}

conn = httplib.HTTPConnection("192.168.0.1")
conn.request("POST", "/password.cgi", params, headers)

response = conn.getresponse()
print "11\n"
print response.status, response.reason
data = response.read()
print "12\n" + data

time.sleep(1)

#Content-Type: multipart/form-data; boundary=----WebKitFormBoundaryt44VDeC7nRtT3f1T
#------WebKitFormBoundaryt44VDeC7nRtT3f1T--
#------WebKitFormBoundary2AAeGjLDN66fWOy1--

#params = urllib.urlencode('Restart Router')
#headers = {"Content-type": "multipart"}
#conn.request("POST", "/system_restart.cgi")
boundary = '---------------------myBOUNDARY'
content_type = 'multipart/form-data; boundary=' + boundary
body = '\r\n'+boundary+'--\r\n'
conn.putrequest('POST', "/system_restart.cgi")
conn.putheader('content-type', content_type)
conn.putheader('content-length', str(len(body)))
conn.endheaders()
conn.send(body)
#errcode, errmsg, headers = h.getreply()
#conn.file.read()

response = conn.getresponse()
print "21\n"
print response.status, response.reason
data = response.read()
print "22\n" + data

time.sleep(1)
conn.request("GET", "/reset_success.htm")

response = conn.getresponse()
print "31\n"
print response.status, response.reason
data = response.read()
print "32\n" + data

time.sleep(1)
conn.request("GET", "/pre_reboot.htm")

response = conn.getresponse()
print "41\n"
print response.status, response.reason
data = response.read()
print "42\n" + data


time.sleep(2)
conn.request("GET", "/reboot.htm")

response = conn.getresponse()
print "51\n"
print response.status, response.reason
data = response.read()
print "52\n" + data




conn.close()
