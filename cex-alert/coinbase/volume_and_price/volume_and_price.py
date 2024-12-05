import requests

BIAN_API = "https://api.exchange.coinbase.com/products"

def get_all_product_volume():
    try:
        rep = requests.get(f'{BIAN_API}/volume-summary')
        rep.raise_for_status()    
    except requests.RequestException as e:
        print(f"Error sending faucet request: {e}")      

    spot_rep_js = rep.json()  
    print(spot_rep_js[100])
    print(spot_rep_js[101])
    print(spot_rep_js[102])
    print(spot_rep_js[221])

def get_single_product():
    try:
        rep = requests.get(f'{BIAN_API}/BTC-USDT')
        rep.raise_for_status()    
    except requests.RequestException as e:
        print(f"Error sending faucet request: {e}")     

    spot_rep_js = rep.json()   
    print(spot_rep_js)     

def get_trading_paires():
    try:
        rep = requests.get(BIAN_API)
        rep.raise_for_status()    
    except requests.RequestException as e:
        print(f"Error sending faucet request: {e}")      

    spot_rep_js = rep.json()  
    print(spot_rep_js[0])    

def get_product_trades():
    try:
        rep = requests.get(f'{BIAN_API}/BTC-USDT/trades?limit=1')
        rep.raise_for_status()    
    except requests.RequestException as e:
        print(f"Error sending faucet request: {e}")     

    spot_rep_js = rep.json()   
    print(spot_rep_js)        

def get_product_stats():
    try:
        rep = requests.get(f'{BIAN_API}/BTC-USDT/stats')
        rep.raise_for_status()    
    except requests.RequestException as e:
        print(f"Error sending faucet request: {e}")     

    spot_rep_js = rep.json()   
    print(spot_rep_js)           

def get_product_candles():
    try:
        rep = requests.get(f'{BIAN_API}//BTC-USDT/candles?granularity=60')
        rep.raise_for_status()    
    except requests.RequestException as e:
        print(f"Error sending faucet request: {e}")     

    spot_rep_js = rep.json()   
    print(spot_rep_js)      


if __name__ == "__main__":
    get_product()