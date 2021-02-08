import requests
import logging
import time, datetime

logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(name)s\n%(message)s')
l = logging.getLogger("Nano Minder")

NANOAPI = 'https://api.nanopool.org/v1/'
WALLET = '0xc1817a207e1f7Bdc3ACe6283D071c93d190c330C'

class color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

class nanoClient():  
    def __init__(self, wallet=WALLET):
        self.wallet = wallet
        self.balance = 0
        self.reportedRate = 0
        self.globalHashrate = 0
        self.globalHashrate1h = 0
        self.globalHashrate3h = 0
        self.globalHashrate6h = 0
        self.globalHashrate12h = 0
        self.globalHashrate24h = 0
        self.workers = {}
        self.eth = 0

        self.reportDetail = """"""

    def getPrice(self):
        data = requests.get('https://api.nanopool.org/v1/eth/prices').json()
        self.eth = float(data['data']['price_usd'])


    def reportedHashrate(self):
        data = requests.get(f"{NANOAPI}eth/reportedhashrate/{self.wallet}")
        hr = float(data.json()['data'])
        self.thresholdCheck(self.reportedRate, hr, 0.09, 'Reported Hashrate')
        self.reportedRate=hr
        return hr

    def accountData(self):
        data = requests.get(f"{NANOAPI}eth/user/{self.wallet}")
        self.parseUserInfo(data.json())

    def thresholdCheck(self, prior, current, delta, label):
        if prior != 0:
            if current == prior:
                return 0
            d = (current - prior)/prior
            if abs(d) > delta:
                self.reportDetail += f"\t\t{label} changed by more than {delta:.1%}: {current-prior:0.6f} ({d:.2%})\n"
                return d
        else:
            return -1

    def parseUserInfo(self, data):
        
        self.reportDetail = """"""

        newVal = float(data['data']['hashrate'])
        self.thresholdCheck(self.globalHashrate, newVal, 0.15, 'Global Hashrate')
        self.globalHashrate=newVal

        newVal = float(data['data']['avgHashrate']['h1'])
        self.thresholdCheck(self.globalHashrate1h, newVal, 0.15, 'Global Hashrate')
        self.globalHashrate1h=newVal

        newVal = float(data['data']['avgHashrate']['h3'])
        self.thresholdCheck(self.globalHashrate3h, newVal, 0.07, 'Global Hashrate')
        self.globalHashrate3h=newVal

        newVal = float(data['data']['avgHashrate']['h6'])
        self.thresholdCheck(self.globalHashrate6h, newVal, 0.07, 'Global Hashrate')
        self.globalHashrate6h=newVal

        newVal = float(data['data']['avgHashrate']['h12'])
        self.thresholdCheck(self.globalHashrate12h, newVal, 0.07, 'Global Hashrate')
        self.globalHashrate12h=newVal

        newVal = float(data['data']['avgHashrate']['h24'])
        self.thresholdCheck(self.globalHashrate24h, newVal, 0.05, 'Global Hashrate')
        self.globalHashrate24h=newVal


        newVal = float(data['data']['balance'])
        self.thresholdCheck(self.balance, newVal, 0.001, f'{color.DARKCYAN}{color.BOLD}Cha-Ching!{color.END} Balance')
        self.balance=newVal

        for w in data['data']['workers']:
            if w['id'] in self.workers:
                    newVal = float(w['hashrate'])
                    self.thresholdCheck( self.workers[w['id']]['hashrate'], newVal, 0.08, f"{w['id']} hashrate")
                    self.workers[w['id']]['hashrate'] = newVal

                    newVal = int(w['lastshare'])
                    if self.workers[w['id']]['lastshare']!=newVal:                      
                        self.workers[w['id']]['lastshare'] = newVal
                        rating = int(w['rating'])
                        #self.reportDetail+=(f"{rating - self.workers[w['id']]['rating']} share(s) found by {w['id']}\n")  
                        self.reportDetail+=(f"\t\t{w['id']} lastshare updated..\n")
                        self.workers[w['id']]['rating'] = rating


            else:
                #create
                self.workers[w['id']]={'hashrate':float(w['hashrate']), 'lastshare':int(w['lastshare']), 'rating':int(w['rating'])}
                    

    def report(self):
        self.getPrice()
        l.info(f"""
    {self.reportDetail}
        Hashrate: {color.BOLD}{color.PURPLE}{self.reportedRate:.0f} mh/s{color.END} - Pool Hashrate {self.globalHashrate:.0f} mh/s\t3h:{self.globalHashrate3h:.0f} mh/s\t12h:{self.globalHashrate12h:.0f} mh/s
        Balance: {self.balance} x ${self.eth:.2f} = {color.BOLD}{color.GREEN}${self.eth*self.balance:.2f}{color.END} - {self.balance/0.1:.1%}
""")




        
nano = nanoClient(WALLET)
PRINT=True
while True:

    #try:
        nano.reportedHashrate()
        nano.accountData()
        if len(nano.reportDetail)>0 or PRINT:
            nano.report()
            PRINT=False
        else: 
            pass
        print(f"{datetime.datetime.now()}", end = "\r")
    # except Exception as e:
    #     l.error(f"Uncaught Exception! - {e}\n\n")        
        time.sleep(15)