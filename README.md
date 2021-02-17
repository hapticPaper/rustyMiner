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



![Monitor Output](https://raw.githubusercontent.com/hapticPaper/rustyMiner/main/images/screenshot.PNG?token=AAFFO73ZQB7X7B6APUVXK3DAFRQR4)