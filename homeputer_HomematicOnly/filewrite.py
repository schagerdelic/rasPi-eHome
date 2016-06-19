import datetime
import os

fn = "C:\pytest.csv"


jetzt = datetime.datetime.now().time()

fd = open(fn,"a")
fd.write(jetzt.isoformat())
fd.close()

