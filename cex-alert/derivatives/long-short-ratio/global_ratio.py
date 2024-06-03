import argparse

import requests

from common import *
from secret import *

import pandas as pd

logger = configure_logger('top-position-ratio.log')

def main(channel):
    alerts = []
    try:
        for symbol in symbols:
            rep_hour = requests.get(f"{BIAN_API}/futures/data/globalLongShortAccountRatio?symbol={symbol}&period=1h&limit=1")
            rep_hour.raise_for_status()

            rep_hour_js = rep_hour.json()[0]
            long_short_ratio = float(rep_hour_js["longShortRatio"])
            if long_short_ratio > RATIO:
                alerts.append([rep_hour_js["symbol"], round(long_short_ratio, 2), round(float(rep_hour_js["longAccount"]), 2)])

    except requests.RequestException as e:
        logger.error(f"Error sending faucet request: {e}")
    
    if len(alerts) != 0:
        alerts.sort(key=lambda x: x[1], reverse=True)
        df = pd.DataFrame(alerts, columns=['Symbol', 'Ratio', 'longAccount'])
        content = f"One-Hour Global Account Ratio\n{df.to_string(index=False)}"
        sned_alerts_to_dc(logger, content, channel)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='volume')
    parser.add_argument('--channel', type=int, default=1)
    args = parser.parse_args()

    if args.channel == 0:
        main(test_channel)
    else:
        main(dc_channel)
