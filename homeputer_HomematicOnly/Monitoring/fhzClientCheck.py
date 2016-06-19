import os


class fhzClientCheck:

    
    def isClientAlive(self, filename):
        try:
            f = file(filename, "r")
            last_line = f.readlines()[-1]
            f.close()
            if ('Client-Index 1 nicht bereit' in last_line):
                return False
            if ('Client automatisch abgemeldet' in last_line):
                return False
            
            return True
        
        except Exception, err:
            pass        


