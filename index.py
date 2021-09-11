import requests
from datetime import datetime
from twilio.rest import Client
import os

_URL_COINMARKETCAP = 'https://api.coinmarketcap.com/data-api/v3/cryptocurrency/detail/chart?id=2010&range=1D'
_URL_BINANCE = 'https://www.binance.com/es-LA/buy-sell-crypto?channel=card&fiat=PEN'
_PRICE_DESIRED = 5
_ACCOUNT_SID = os.environ['TWILIO_ACCOUNT_SID']
_AUTH_TOKEN = os.environ['TWILIO_AUTH_TOKEN']
_FROM_NUMBER = 'whatsapp:+14155238886'
_TO_NUMBER = os.environ['MY_NUMBER']

response = requests.get(_URL_COINMARKETCAP)

if response.status_code == 200:
    data = response.json()
    keys = list(data['data']['points'].keys())
    keys.sort(reverse=True)
    lastKey = keys[0]
    price = data['data']['points'][lastKey]['v'][0]
    price = round(price, 3)
    timestamp_to_date = datetime.fromtimestamp(int(lastKey))
    timestamp_to_date = timestamp_to_date.strftime('%Y-%m-%d %H:%M:%S')
    if price <= _PRICE_DESIRED:
        body = f'Price ADA is ${price}, buy now!\n{timestamp_to_date}\n{_URL_BINANCE}\nDanielgis'
        client = Client(_ACCOUNT_SID, _AUTH_TOKEN)
        message = client.messages.create(body=body, from_=_FROM_NUMBER, to=_TO_NUMBER)
        print(message.sid)
    else:
        print(f'Price ADA is ${price}, not buy!')
else:
    print(f'Error: {response.status_code}')






