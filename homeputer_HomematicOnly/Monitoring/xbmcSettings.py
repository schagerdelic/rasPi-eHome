import xml.dom.minidom


class xbmcSettings:

    xbmcset= dict()


    def getText(self,nodelist):
        rc = []
        for node in nodelist:
            if node.nodeType == node.TEXT_NODE:
                rc.append(node.data)
        return ''.join(rc)

    def handleSettings(self,settings):
        sets = settings.getElementsByTagName("setting")
        for s in sets:
            id = s.getAttribute("id")
            value = s.getAttribute("value")
            self.xbmcset[id] = value

    def getSetting(self,id):
        if self.xbmcset[id] == 'true':
            return True
        elif self.xbmcset[id] == 'false':
            return False
        else:
            return self.xbmcset[id]
            
 
    def load(self,filename):
        dom = xml.dom.minidom.parse(filename)
        self.handleSettings(dom)

    def __init__(self,filename):
        self.load(filename)

        
#myset = xbmcSettings("C:\\XBMC911\\userdata\\script_data\\HomeControl\\settings.xml")
#myset.load("C:\\XBMC911\\userdata\\script_data\\HomeControl\\settings.xml")

#print myset.getSetting("RollosSchlafenRauf")

