import telnetlib, mimetypes, time



class fhemInterface:

    #host = "192.168.0.96"
    host = "localhost"
    port = 7072


    def __init__(self):
        self.tn = telnetlib.Telnet(self.host,self.port,30)
        self.tn.write("\n\n\n")
        self.tn.read_until("fhem> ")

    def sendCmd(self,str):
        self.tn.write(str+"\n")
        return self.getReturnStr()
        

    def close(self):
        self.tn.close()

    def getReturnStr(self):
        ret = self.tn.read_until("fhem> ")
        ret.split('\n', 1)[0]
        return ret.splitlines()[0]
        


#main function
##if __name__ == "__main__":
##
##    fh = fhemInterface();
##    #fh.sendCmd("");
##
##    print "X" + fh.readCmd("get sensor_bad param temperature") + "Y";
##
##    print "X" +  fh.readCmd("get sensor_bad param humidity") + "Y";
##
##    print "X" + fh.sendCmd("set heizung_bad on") + "Y";
##    
##    print "X" + fh.readCmd("get heizung_bad param STATE") + "Y";
##
##
##    time.sleep(1);
##    fh.close();
