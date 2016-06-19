import jsonIO #.jsonIOReader
import os
import types



class eHomeSettings:
    

    def __init__(self):
        self.d = []
        pass

    def __init__(self, path):
        f = os.open(path,os.O_RDONLY)
        str = os.read(f,9999)
        os.close(f)
        self.d = jsonIO.read(str)
        pass

    def save(self, path):
        pass

    def getSetting(self, str):
        tmp = self.d[str]
        if isinstance(tmp,types.StringTypes):
            return tmp.replace(',','.')
        else:
            return tmp
        

    def putSetting(self, str):
        pass



