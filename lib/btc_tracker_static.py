import requests
import os
import time
import sys

from tabulate import tabulate
from ResponseUtility import ResponseUtility

# Public API URLs of supported exchanges
url_list = ['https://api.bitfinex.com/v1', 'https://api.kraken.com/0/public/Ticker', 'https://api.quadrigacx.com/v2/ticker',
     'https://api.taurusexchange.com/ticker', 'https://btc-e.com/api/3/ticker', 'https://www.bitstamp.net/api/v2/ticker', 
     'https://www.okcoin.com/api/v1/ticker.do', 'https://anxpro.com/api/2', 'https://api.hitbtc.com/api/1']

# Supported configuration parameters
available_exchanges = ['kraken', 'btc-e', 'bitstamp', 'okcoin', 'anxpro', 'hitbtc', 'bitfinex', 'taurus', 'quadrigacx']
available_currencies = ['usd', 'cad', 'eur', 'rub', 'gbp', 'aud', 'jpy']
avialiable_display_values = ['vwap', 'high', 'low', 'buy', 'sell']


# Returns URL for selected exchange_name and currency. 
# Returns -1 if exchange_name is invalid or if exchange doesn't support chosen currency.
def get_url(exchange_name, currency):

    if exchange_name == 'bitfinex' and currency == 'usd':
            return  url_list[0] + '/pubticker/BTCUSD'

    elif exchange_name == 'kraken':
        if currency == 'usd':
            return url_list[1] + '?pair=XBTUSD'
        elif currency == 'cad':
            return url_list[1] + '?pair=XBTCAD'
        elif (currency == 'eur'):
            return url_list[1] + '?pair=XBTEUR'
        elif (currency == 'gbp'):
            return url_list[1] + '?pair=XBTGBP'
        elif (currency == 'jpy'):
            return url_list[1] + '?pair=XBTJPY'
        else:
            return -1

    elif exchange_name == 'quadrigacx':
        if currency == 'usd':
            return url_list[2] + '?book=btc_usd'
        elif currency == 'cad':
            return url_list[2] + '?book=btc_cad'
        else:
            return -1

    elif exchange_name == 'taurus' and currency == 'cad':
        return url_list[3]

    elif exchange_name == 'btc-e':
        if currency == 'usd':
            return url_list[4] + '/btc_usd'
        if currency == 'eur':
            return url_list[4] + '/btc_eur'
        elif ((currency == 'rur') or (currency == 'rub')):
            return url_list[4] + '/btc_rur'
        else:
            return -1

    elif exchange_name == 'bitstamp':
        if (currency == 'usd'):
            return url_list[5] + '/btcusd/'
        elif (currency == 'eur'):
            return url_list[5] + '/btceur/'
        else:
            return -1

    elif exchange_name == 'okcoin' and currency == 'usd':
        return url_list[6] + '?symbol=btc_usd'

    elif exchange_name == 'anxpro':
        if currency == 'usd':
            return url_list[7] + '/BTCUSD/money/ticker'
        elif (currency == 'cad'):
            return url_list[7] + '/BTCCAD/money/ticker'
        elif (currency == 'eur'):
            return url_list[7] + '/BTCEUR/money/ticker'
        elif (currency == 'gbp'):
            return url_list[7] + '/BTCGBP/money/ticker'
        elif (currency == 'aud'):
            return url_list[7] + '/BTCAUD/money/ticker'
        elif (currency == 'jpy'):
            return url_list[7] + '/BTCJPY/money/ticker'
        else:
            return -1

    elif exchange_name == 'hitbtc':
        if currency == 'usd':
            return url_list[8] + '/public/BTCUSD/ticker'           
        elif (currency == 'eur'):
            return url_list[8] + '/public/BTCEUR/ticker'
        else:
            return -1

    else:
        return -1

# Displays prices
def display_prices(currency, request_url_list, exchange_list, display_values_list):

    price_table = [] 
    price_list=[]

    j = 0
    # Request public ticker data from exchanges, extract prices and construct a 2D list (each exchange has its own row)
    for url in request_url_list:
        response = requests.get(url).text
        price_list = ResponseUtility.select_exchange(response, exchange_list[j], display_values_list)
        price_table.append(price_list)
        j = j + 1

    display_values_list.insert(0, 'Exchanges')
    # Display prices
    print ("Currency: " + currency + "\n\n" + tabulate(price_table, headers=display_values_list))

# Reads from config. Constructs table. Makes http requests.
def main():
    

    # Get exchange names, currency and refresh rate from config. Check correctness.
    curr_dir = os.path.dirname(__file__)
    config = os.path.join(curr_dir, 'config_files/config')
    with open (config) as fp:
        for line in fp:
            if (line.startswith('exchanges:')):
                exchange_list = line[11:].strip().split(', ')
            elif (line.startswith('currency:')):
                currency = line[10:].strip()
            elif (line.startswith('data values:')):
                display_values_list = line[12:].strip().split(', ')

    for exchange in exchange_list:
        if exchange.lower() not in available_exchanges:
            sys.exit("Exchange \'" + exchange + "\' is not a supported exchange. Please check config for the list of avalable exchanges.")
    if currency not in available_currencies:
        sys.exit("Selected currency \'" + currency + "\' is not supported. Please check config for the list of available currencies.")

    for display_value in display_values_list:
        if display_value.lower() not in avialiable_display_values:
            sys.exit("Market data value \'" + display_value + "\' is not supported. Please check config for the list of available data values.")
            

    for value in display_values_list:
        if (value.lower() == 'vwap'):
            value = 'VWAP'
        else:
            value = value.capitalize()
       
    # Construct list of URLs for chosen exchanges and currency
    request_url_list = []
    for exchange in exchange_list[:]:
        request_url = get_url(exchange, currency)
        if (request_url == -1):
            exchange_list.remove(exchange)  # If exchange doesn't support chosen currency, remove from exchange_list
            continue
        request_url_list.append(request_url)


    display_prices(currency, request_url_list, exchange_list, display_values_list)

if __name__ == "__main__":
    main()
