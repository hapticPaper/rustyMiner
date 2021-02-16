from nano import *

nl = nanoClient()

nl.getPayments()

pmts = [*nl.payments.keys()]
pmts.sort()
lastTx = nl.payments[pmts[-1]]['tx']
print(lastTx)
nl.txInfo(lastTx)