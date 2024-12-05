import requests

BIAN_API = "https://api.exchange.coinbase.com"

def get_symbols():
    try:
        rep = requests.get(f'{BIAN_API}/currencies')
        rep.raise_for_status()    
    except requests.RequestException as e:
        print(f"Error sending faucet request: {e}")      

    spot_rep_js = rep.json()  
    print(spot_rep_js[0])
    print(spot_rep_js[1])
    print(spot_rep_js[2])
    print(spot_rep_js[3])
    print(spot_rep_js[4])
    symbols = []

if __name__ == "__main__":
    get_symbols()