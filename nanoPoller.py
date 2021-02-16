import requests
import logging
import time, datetime
from nano import *

logging.basicConfig(level=logging.INFO, 
                    format='%(message)s')
                    
l = logging.getLogger("Nano Minder")

        
nano = nanoClient()
print("\n"*3)
skipper = 0
while True:
    try:
        nano.reportedHashrate()
        nano.accountData()
        if len(nano.reportDetail)>0 or skipper % 12 == 0:
            nano.report()
        else: 
            pass            
        skipper+=1
    
        print(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", end = "\r")
    except Exception as e:
        l.error(f"Uncaught Exception! - {e}\n\n")        
    time.sleep(15)