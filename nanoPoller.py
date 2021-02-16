import requests
import logging
import time, datetime
from nano import *

logging.basicConfig(level=logging.INFO, 
                    format='%(message)s')
                    
l = logging.getLogger("Nano Minder")
DEBUG=True
        
def runner(nano, skip=3):
    skipper = 0
    nano.reportedHashrate()
    nano.accountData()
    if len(nano.reportDetail)>0 or skipper % (skip*4) == 0:
        nano.report()
    else: 
        pass            
    skipper+=1

    print(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", end = "\r")

nano = nanoClient()
print("\n"*3)
p = None
b = None
while True and p==None and b==None:
    if DEBUG:
        runner(nano, skip=0.25)
    else:
        try:
            runner(nano)
        except Exception as e:
            l.error(f"Uncaught Exception! - {e}\n\n")      
    
    time.sleep(15)