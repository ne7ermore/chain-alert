import argparse
from datetime import datetime

import requests

from common import *

from rich.console import Console
from rich.table import Table

def main(args):
    duration = args.duration
    spot_rep_js_list = []
    for symbols in symbols_list:
        try:
            spot_rep = requests.get(f'{BIAN_API}/ticker?symbols={symbols}&windowSize={duration}')
            spot_rep.raise_for_status()
        except requests.RequestException as e:
            if args.logging:
                logger.error(f"Error sending faucet request: {e}")        
            else:
                print(f"Error sending faucet request: {e}")  
        spot_rep_js = spot_rep.json()
        spot_rep_js_list += spot_rep_js
    
    alerts = []
    for token in spot_rep_js_list:
        symbol = token["symbol"]
        priceChangePercent = token["priceChangePercent"]
        quoteVolume = token["quoteVolume"]
        price = float(token["lastPrice"])
        alerts.append([symbol, priceChangePercent, round(float(quoteVolume),2), price])

    if args.sort_type == "price":
        alerts.sort(key=lambda x:x[1], reverse=True)
        message = f"{duration}价格涨幅榜"
    else:
        alerts.sort(key=lambda x:x[2], reverse=True)
        message = f"{duration}现货交易量涨幅榜"

    alerts = alerts[:args.top]
    table = Table(title=f"{message}: {str(datetime.now())[5:19]}")
    table.add_column("币种")
    table.add_column("涨幅")
    table.add_column("现货交易量")
    table.add_column("期货交易量")

    for symbol, priceChangePercent, volume, price in alerts:
        try:
            rep = requests.get(f"{BIAN_FUTURE_API}/futures/data/takerlongshortRatio?symbol={symbol}&period=1h&limit=1")
            rep.raise_for_status()      
        except requests.RequestException as e:
            if args.logging:
                logger.error(f"Error sending faucet request: {e}")        
            else:
                print(f"Error sending faucet request: {e}")        

        if len(rep.json()):
            rep_js = rep.json()[0]        
            future_quoteVolume = (float(rep_js["buyVol"])+float(rep_js["sellVol"]))*price
            future_quoteVolume = round(float(future_quoteVolume),2)
        else:
            future_quoteVolume = 0.

        table.add_row(*[str(r) for r in [symbol.replace("USDT", ""), f"{priceChangePercent}%", '{:,}'.format(volume), '{:,}'.format(future_quoteVolume)]])
    
    Console().print(table)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='volume')
    parser.add_argument('--duration', type=str, default="1h")
    parser.add_argument('--sort_type', type=str, default="price")
    parser.add_argument('--logging', type=bool, default=False)
    parser.add_argument('--top', type=int, default=20)
    args = parser.parse_args()

    if args.logging:
        logger = configure_logger('price_and_volume.log')

    main(args)
