import requests

BIAN_API = "https://api.binance.com/api/v3"

def get_symbols():
    try:
        rep = requests.get(f'{BIAN_API}/exchangeInfo')
        rep.raise_for_status()    
    except requests.RequestException as e:
        print(f"Error sending faucet request: {e}")      

    spot_rep_js = rep.json()  
    symbols = []
    symbols_str = "%5B"
    count = 0
    for token in spot_rep_js["symbols"]:
        if "USDT" in token["symbol"] and token["status"] == "TRADING" and not token["symbol"].startwith("USDT"):
            symbol = token["symbol"]
            symbols.append(symbol)        
            symbols_str += f"%22{symbol}%22,"
            if count == 80:
                symbols_str = symbols_str[:-1] + "%5D"
                print(symbols_str)
                print()
                symbols_str = "%5B"
                count = 0
            count += 1

    symbols_str = symbols_str[:-1] + "%5D"
    print(symbols_str)            

if __name__ == "__main__":
    get_symbols()
