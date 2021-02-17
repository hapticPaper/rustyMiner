# rustyMiner

A REST script that will poll nanopool every 15 seconds, allowing it to report on:
- <B>Reported</b> Hashrate (Pool hashrate wasn't helpful)
- Current Balance, Estimated earnings since last payout, reward as a percentage of 0.1 ETH (standard payout)
- Hourly Earnings rate in USD
- Average Daily Earnings in ETH and USD
- Estimated time to payout (0.1 ETH)
- Estimated time to reach 1.0 ETH

Unless you want to monitor my mining, update the file to use your wallet address. 
The reporting frequency can also be modified by changing `SKIPPER` at the start of `nanoPoller.py`.
The main process is started by running `python nanoPoller.py`


![Monitor Output](https://github.com/hapticpaper/rustyMiner/blob/main/images/screenshot.PNG?raw=true)

Future Ideas:
- Making estimations more accurate by incorporating the actual transaction confirmation times. 
- Adding support for a persistent data layer (will most likely leverage docker)
- I did this to avoid wasting valuable GPU resources opening a web browser, but perhaps, a flask hosted dashboard. But probably not. 
- Miner specific data instead of wallet only
- Trello alerts based on varied criteria (like a miner hashrate dropping)
- Open to other requests. 


If this was helpful for you, consider donating some hashes: [0xc1817a207e1f7bdc3ace6283d071c93d190c330c](https://etherscan.io/address/0xc1817a207e1f7bdc3ace6283d071c93d190c330c)

If you really want to be helped, check out [nssm](https://nssm.cc/usage). Its a really easy to use tool that will let you turn any `.bat` or `.exe` into a window service... that can start when the computer does.. and restart if it fails. HiveOS and its fees can bit me. Windows FTW. 


My hashrate is achieved using the following on windows (highly tuned):
- 3 x 5700xt
- 2 x 5600xt
- 2 x 3070
- 1 x 3060ti
- 1 x 3090 

I would be more than happy to share all my tuning parameters, but that will cost *any* dontation to the ETH address above. Literally *ANY* donation will get you all the parameters I use for the cards above, and up to 2 hours of help tuning your hardware. (While supplies last - my time. Guaranteed for the first 25 requests.) If there is an overwhelming volume, I'll set something up to support everyone.
And since Im cool (and no one actually uses it), heres the [3090 Tuning](https://github.com/hapticPaper/rustyMiner/blob/main/config.txt).