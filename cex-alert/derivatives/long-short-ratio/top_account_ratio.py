import argparse
from datetime import datetime

import requests

from common import *
from secret import *

logger = configure_logger('top-account-ratio.log')

def main(channel):
    alerts = []
    try:
        for symbol in symbols:
            rep_hour = requests.get(f"{BIAN_API}/futures/data/topLongShortAccountRatio?symbol={symbol}&period=1h&limit=1")
            rep_hour.raise_for_status()

            rep_hour_js = rep_hour.json()[0]
            long_short_ratio = float(rep_hour_js["longShortRatio"])
            if long_short_ratio > LONGRATIO or long_short_ratio < SHORTRATIO:
                alerts.append([rep_hour_js["symbol"], round(long_short_ratio, 2), round(float(rep_hour_js["longAccount"]), 2)])

    except requests.RequestException as e:
        logger.error(f"Error sending faucet request: {e}")
    
    if len(alerts)!= 0:
        content = f"One-Hour Top Account Ratio | {str(datetime.now())[5:19]}\n```\n"
        content += "Symbol     Ratio      Long Account\n"
        content += "------------------------------------\n"
        
        alerts.sort(key=lambda x:x[1], reverse=True)
        for symbol, ratio, longAccount in alerts:
            content += f"{symbol:<10} {ratio:>5} {longAccount:>10}\n"
        content += "```"
        
        sned_alerts_to_dc(logger, content, channel)            
        

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='volume')
    parser.add_argument('--channel', type=int, default=1)
    args = parser.parse_args()

    if args.channel == 0:
        main(test_channel)
    else:
        main(dc_channel)
