import argparse

import requests

from common import *
from secret import *

import pandas as pd

logger = configure_logger('bian-volume-alert-crontab.log')

def four_hour(channel):
    try:
        rep_hour = requests.get(f'https://api.binance.com/api/v3/ticker?symbols={symbols}&type=MINI&windowSize=4h')
        rep_hour.raise_for_status()
        rep_day = requests.get(f'https://api.binance.com/api/v3/ticker?symbols={symbols}&type=MINI&windowSize=4d')          
        rep_day.raise_for_status()
    except requests.RequestException as e:
        logger.error(f"Error sending faucet request: {e}")

    alerts = []

    rep_hour_js = rep_hour.json()
    rep_day_js = rep_day.json()

    for token_hour, token_day in zip(rep_hour_js, rep_day_js):
        assert token_hour["symbol"] == token_day["symbol"]

        volume_1d = float(token_day["volume"])
        volume_1h = float(token_hour["volume"])
        avg_volume = (volume_1d-volume_1h)/23            

        if volume_1h >= avg_volume*RATIO:
            alerts.append([token_hour["symbol"], round(volume_1h/avg_volume, 1), float(token_hour["lastPrice"]), volume_1d])       

    if len(alerts) != 0:
        alerts.sort(key=lambda x: x[1], reverse=True)
        df = pd.DataFrame(alerts, columns=['Symbol', 'Times', 'Price', 'Volume'])
        content = f"Four-Hour Volume Info\n{df.to_string(index=False)}"
        sned_alerts_to_dc(logger, content, channel)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='volume')
    parser.add_argument('--channel', type=int, default=1)
    args = parser.parse_args()

    if args.channel == 0:
        four_hour(test_channel)
    else:
        four_hour(dc_channel)