import psutil
import datetime as dt
import json 
import logging
from nano import *

l = logging.getLogger("Phoenix Runner")

try:    
    with open('./config.txt', 'r') as cfg:
        CONFIG = json.loads(cfg.read())
        WALLET = CONFIG['wallet']
except Exception as e:
    l.critical(f"Couldnt open config file.\n{e}")


nc = nanoClient()




if 'PhoenixMiner.exe' in [p.name() for p in psutil.process_iter(attrs=None, ad_value=None)]:
    print(f"Phoenix still running - {dt.datetime.now().strftime('%c')}")