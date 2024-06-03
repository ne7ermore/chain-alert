import argparse

import requests

from common import *
from secret import *


logger = configure_logger('bian-volume-alert-crontab.log')


def one_hour(channel):
    try:
        rep_hour = requests.get(f'{BIAN_API}/ticker?symbols={symbols}&type=MINI&windowSize=1h')
        rep_hour.raise_for_status()
        rep_day = requests.get(f'{BIAN_API}/ticker?symbols={symbols}&type=MINI&windowSize=1d')          
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
            alerts.append([token_hour["symbol"], token_hour["lastPrice"], volume_1d, round(volume_1h/avg_volume, 1)])       

    if len(alerts) != 0:
        content = "One-Hour Volume Info"

        for [symbol, lastPrice, volume_1d, times] in alerts:
            content += f"\nToken: {symbol}\nPrice:{lastPrice}\nVolume: {volume_1d}\nTimes: {times}\n--------------------------------------------\n"

        sned_alerts_to_dc(logger, content, channel)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='volume')
    parser.add_argument('--channel', type=int, default=1)
    args = parser.parse_args()

    if args.channel == 0:
        one_hour(test_channel)
    else:
        one_hour(dc_channel)
