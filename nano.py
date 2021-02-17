import requests
import logging
import datetime
import time

NANOAPI = 'https://api.nanopool.org/v1/'
EtherScanAPIKey='FWARZYTIH42F2ATIECV4VEDSDEGZVPWQ91'

PAYOUT = 0.1


logging.basicConfig(level=logging.INFO, 
                    format='%(message)s')
                    
l = logging.getLogger("Nano Client")

class color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    GREY = '\033[90m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

class nanoClient():  
    def __init__(self, wallet='0xc1817a207e1f7Bdc3ACe6283D071c93d190c330C'):
        self.WALLET = wallet
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
        self.payments = {}
        self.rewards = []
        self.shares = {}
        self.coins = False
        self.halfDing = False
        self.ding = False
        self.payoutReached = False
        self.firstRun = True
        self.pendingPayment = False
        self.transit = False
        self.ethSec = 0
        self.lastReward = time.time()
        


        self.reportDetail = """"""

    def requestData(self, url, params=None):
        try:
            response = requests.get(url, params=params)
            return response.json()
        except Exception as e:
            try:
                return {'Exception': e, 'response':response.content, 'code':response.status_code}
            except:
                return {'Exception': e}


    def getPayments(self):
        try:
            data = self.requestData(f'{NANOAPI}eth/payments/{self.WALLET}')
            pmts = data['data']
            for p in pmts:
                if p['date'] not in self.payments:
                    self.payments[p['date']] = {'amount': p['amount'], 'confirmed':p['confirmed'], 'tx':p['txHash']}
                if self.payments[p['date']]['confirmed'] != True:
                    if p['confirmed'] == True:
                        self.payments[p['date']]['confirmed'] = True
                        self.ding == True
                        self.transit = False
                    else:
                        self.transit = True
                        self.halfDing = True
                        
        except Exception as e:
            raise e

    def txInfo(self, tx):
        transactionData = self.requestData('https://api.etherscan.io/api', 
                        params={'module':'transaction',
                                'action':'getstatus',
                                'txhash':tx, 
                                'apikey':EtherScanAPIKey})
        l.warn(transactionData)     
        return                          


    def getPrice(self):
        try:
            data = self.requestData('https://api.nanopool.org/v1/eth/prices')
            self.eth = float(data['data']['price_usd'])
        except Exception as e:
            l.exception(f'Couldnt update ETH price. {e} - {data}')


    def reportedHashrate(self):
        data = requests.get(f"{NANOAPI}eth/reportedhashrate/{self.WALLET}")
        hr = float(data.json()['data'])
        self.thresholdCheck(self.reportedRate, hr, 0.02, f'{color.RED}Reported Hashrate{color.END}')
        self.reportedRate=hr
        return hr

    def accountData(self):
        data = requests.get(f"{NANOAPI}eth/user/{self.WALLET}")
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
        try:
            self.getPayments()                
            self.reportDetail = """"""

            newVal = float(data['data']['hashrate'])
            self.thresholdCheck(self.globalHashrate, newVal, 0.55, 'Global Hashrate')
            self.globalHashrate=newVal

            newVal = float(data['data']['avgHashrate']['h1'])
            self.thresholdCheck(self.globalHashrate1h, newVal, 0.55, 'Global Hashrate')
            self.globalHashrate1h=newVal

            newVal = float(data['data']['avgHashrate']['h3'])
            self.thresholdCheck(self.globalHashrate3h, newVal, 0.57, 'Global Hashrate')
            self.globalHashrate3h=newVal

            newVal = float(data['data']['avgHashrate']['h6'])
            self.thresholdCheck(self.globalHashrate6h, newVal, 0.17, 'Global Hashrate')
            self.globalHashrate6h=newVal

            newVal = float(data['data']['avgHashrate']['h12'])
            self.thresholdCheck(self.globalHashrate12h, newVal, 0.17, 'Global Hashrate')
            self.globalHashrate12h=newVal

            newVal = float(data['data']['avgHashrate']['h24'])
            self.thresholdCheck(self.globalHashrate24h, newVal, 0.15, 'Global Hashrate')
            self.globalHashrate24h=newVal


            newVal = float(data['data']['balance'])
            if self.thresholdCheck(self.balance, newVal, 0.001, f'{color.DARKCYAN}{color.BOLD}Cha-Ching!{color.END} Balance')>0:
                self.lastReward=time.time()
            self.balance=newVal
            self.ethSec
            if self.balance>=PAYOUT:
                self.payoutReached=True
                self.pendingPayment = time.time()
            else:
                self.pendingPayment = False
                self.payoutReached=True


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
        except Exception as e:
            raise Exception(f'Couldnt update nano data - {e}')

    def formatTime(self, seconds):
        if seconds > (259200):
            return f"~{int(seconds / 86400 )} days"
        return f"{int(seconds / 3600 )}:{int((seconds % 3600)/60):02d}"

    def report(self):
        self.getPrice()
        #l.info(f"{self.reportDetail}")

        flag = ''
        flag += f'💰{color.GREEN}{color.BOLD}...{color.END}' if self.pendingPayment else ''
        flag += f'💸💸 ({color.GREEN}{color.BOLD}Tx Pending{color.END})' if self.halfDing else ''
        flag += f'🤑🤑 ({color.GREEN}{color.BOLD}Received!{color.END})' if self.ding else ''
            
        pmts = [*self.payments.keys()]
        pmts.sort()
        lastPayment = pmts[-1]

        since = self.lastReward - lastPayment
        ethSec = self.balance / since
        usdSec = ethSec * self.eth
        oneETH = self.formatTime(1.0 / ethSec)

        unrewarded = (time.time() - self.lastReward)*ethSec
        
        
        div = f"{color.GREY}{color.BOLD}|{color.END}"

        if PAYOUT<self.balance:
            excess = self.balance-PAYOUT
            payout = f"{self.formatTime(excess / ethSec)} & {excess:.5f} ETH over"
        else: 
            if self.transit:
                payout = f"Payment in transit."  
            elif since<(60*3):
                prior = self.payments[pmts[-2]]['amount']
                span = lastPayment - pmts[-2]
                payout = f"Last: {prior:0.4f} ETH in {self.formatTime(span)} - ${(((prior/span)*3600*24) * self.eth):.2f}/day"
            else:
                payout = f"Payout in {color.BOLD}{color.YELLOW}{self.formatTime((PAYOUT - (self.balance+unrewarded))/ethSec)}{color.END} {div} {oneETH}/ETH"

        lastPayTime = self.formatTime(since)


        # {lastPayTime} = 
        rates = f'{div} ${usdSec * 3600 :.2f}/hr {div} {ethSec * 24* 3600:0.4f} ETH {color.RED}{color.BOLD}${usdSec * 3600 * 24 :.2f}{color.END}/day {div} {payout}'

        l.info(f"""{datetime.datetime.now().strftime('%m.%d %H:%M')} {div} {color.BOLD}{color.PURPLE}{self.reportedRate:.0f} Mh/s{color.END} {div} {self.balance:.4f} x ${self.eth:,.0f} = {color.BOLD}{color.GREEN}${self.eth*self.balance:>7.2f}{color.END} :{color.BLUE}{color.BOLD}{self.balance/0.1:>7.2%}{color.END} {rates} {flag}""")
        self.ding = False
        self.halfDing = False
        self.payoutReached = False
        self.firstRun=False


if __name__=='__main__':

    nc = nanoClient()
    nc.getPayments()