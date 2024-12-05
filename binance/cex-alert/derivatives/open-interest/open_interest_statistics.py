import argparse
from datetime import datetime

import requests

from common import *
from secret import *

logger = configure_logger('open-interest-statistics.log')

def main(channel):
    alerts = []
    try:
        for symbol in symbols:
            rep_hour = requests.get(f"{BIAN_API}/futures/data/openInterestHist?symbol={symbol}&period=1h&limit=25")
            rep_hour.raise_for_status()

            rep_hour_js = rep_hour.json()

            open_interest_now = float(rep_hour_js[0]["sumOpenInterest"])
            open_interest_sum = sum([float(rep_hour["sumOpenInterest"]) for rep_hour in rep_hour_js[1:]])
            open_interest_rato = round((open_interest_now*24)/open_interest_sum, 2)
            if open_interest_rato > LONGRATIO or open_interest_rato < SHORTRATIO:
                alerts.append([rep_hour_js[0]["symbol"], open_interest_rato, round(float(rep_hour_js[0]["sumOpenInterest"]),2), round(float(rep_hour_js[0]["sumOpenInterestValue"]),2)])

    except requests.RequestException as e:
        logger.error(f"Error sending faucet request: {e}")

    if len(alerts)!= 0:
        content = f"One-Hour Open Interest Info | {str(datetime.now())[5:16]}\n```\n"
        content += "Symbol     Times      OpenInterest      OpenInterestValue\n"
        content += "------------------------------------------------------------\n"
        
        alerts.sort(key=lambda x:x[1], reverse=True)
        for symbol, ratio, open_interest, open_interest_value in alerts:
            content += f"{symbol:<10} {ratio:>} {'{:,}'.format(open_interest):>18}  {'{:,}'.format(open_interest_value):>18}\n"
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
