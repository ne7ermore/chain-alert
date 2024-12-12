import requests

from secret_key import KEY

url = "https://api.coingecko.com/api/v3/simple/price?ids=celestia&vs_currencies=usd"

headers = {
    "accept": "application/json",
    "x-cg-demo-api-key": KEY
}

response = requests.get(url, headers=headers)

print(response.text)