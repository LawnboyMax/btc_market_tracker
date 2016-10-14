import time
# Methods that extract and format stats from exchange responses to API requests

class ResponseUtility:
    SIG_DIG = 2

    # Selects method specific to chosen exchange and passes on the response
    @staticmethod
    def select_exchange(response, exchange, display_values_list):

        ResponseUtility.exchange = exchange
        if exchange == 'bitfinex':
            return ResponseUtility().bitfinex_prices(response, display_values_list)
        elif exchange == 'kraken':
            return ResponseUtility().kraken_prices(response, display_values_list)
        elif exchange == 'quadrigacx':
            return ResponseUtility().quadriga_prices(response, display_values_list)
        elif exchange == 'taurus':
            return ResponseUtility().taurus_prices(response, display_values_list)
        elif exchange == 'btc-e':
            return ResponseUtility().btce_prices(response, display_values_list)
        elif exchange == 'bitstamp':
            return ResponseUtility().bitstamp_prices(response, display_values_list)
        elif exchange == 'okcoin':
            return ResponseUtility().okcoin_prices(response, display_values_list)
        elif exchange == 'anxpro':
            return ResponseUtility().anxpro_prices(response, display_values_list)
        elif exchange == 'hitbtc':
            return ResponseUtility().hitbtc_prices(response, display_values_list)

    # Rounds floats to SIG_DIG significant digits and return as str list. First element of list is exchange name.
    @staticmethod
    def round_prices(price_list):
        price_list_rounded = []
        price_list_rounded.append(ResponseUtility.exchange.capitalize()) # add exchange name for use with tabulate library
        for p in price_list:
            p = round(p, ResponseUtility.SIG_DIG)
            p = str(p)
            price_list_rounded.append(p)
        return price_list_rounded

    # Extract prices from Bitfinex response string
    @staticmethod
    def bitfinex_prices(response, display_values_list):
        # Start index is inclusive, end index is exclusive
        low_index_start = response.find('low') + 6
        low_index_end = low_index_start + response[low_index_start:].find('\",\"')
        high_index_start = response.find('high') + 7
        high_index_end = high_index_start + response[high_index_start:].find('\",\"')
        buy_index_start = response.find('ask') + 6
        buy_index_end = buy_index_start + response[buy_index_start:].find('\",\"')
        sell_index_start = response.find('bid') + 6
        sell_index_end = sell_index_start + response[sell_index_start:].find('\",\"')
        # Convert prices to float
        price_list = []
        if 'vwap' in display_values_list:
            price_list.append(0)
        if 'low' in display_values_list:
           price_list.append(float(response[low_index_start : low_index_end]))
        if 'high' in display_values_list:
            price_list.append(float(response[high_index_start : high_index_end]))
        if 'buy' in display_values_list:
           price_list.append(float(response[buy_index_start : buy_index_end]))
        if 'sell' in display_values_list:
            price_list.append(float(response[sell_index_start : sell_index_end]))
        price_list_rounded = ResponseUtility().round_prices(price_list) # Round prices
        price_list_rounded[1] = "N/A" # VWAP not available
        return price_list_rounded

    # Extract prices from Kraken response string
    @staticmethod
    def kraken_prices(response, display_values_list):
        # Start index is inclusive, end index is exclusive
        vwap = response.find('\"p\"')
        vwap_index_start = vwap + response[vwap:].find('\",\"') + 3
        vwap_index_end = vwap_index_start + response[vwap_index_start:].find('\"]')
        low = response.find('\"l\"')
        low_index_start = low + response[low:].find('\",\"') + 3
        low_index_end = low_index_start + response[low_index_start:].find('\"]')
        high = response.find('\"h\"')
        high_index_start = high + response[high:].find('\",\"') + 3
        high_index_end = high_index_start + response[high_index_start:].find('\"]')
        buy_index_start = response.find('\"a\"') + 6
        buy_index_end = buy_index_start + response[buy_index_start:].find('\",\"')
        sell_index_start = response.find('\"b\"') + 6
        sell_index_end = sell_index_start + response[sell_index_start:].find('\",\"')
        # Convert prices to float
        price_list = []
        if 'vwap' in display_values_list:
            price_list.append(float(response[vwap_index_start : vwap_index_end]))
        if 'low' in display_values_list:
           price_list.append(float(response[low_index_start : low_index_end]))
        if 'high' in display_values_list:
            price_list.append(float(response[high_index_start : high_index_end]))
        if 'buy' in display_values_list:
           price_list.append(float(response[buy_index_start : buy_index_end]))
        if 'sell' in display_values_list:
            price_list.append(float(response[sell_index_start : sell_index_end]))
        price_list_rounded = ResponseUtility().round_prices(price_list) # Round prices
        return price_list_rounded

    # Extract prices from Quadriga response string
    @staticmethod
    def quadriga_prices(response, display_values_list):
        # Start index is inclusive, end index is exclusive
        vwap_index_start = response.find('vwap') + 7
        vwap_index_end = vwap_index_start + response[vwap_index_start:].find('\",\"')
        low_index_start = response.find('low') + 6
        low_index_end = low_index_start + response[low_index_start:].find('\",\"')
        high_index_start = response.find('high') + 7
        high_index_end = high_index_start + response[high_index_start:].find('\",\"')
        buy_index_start = response.find('ask') + 6
        buy_index_end = buy_index_start + response[buy_index_start:].find('\",\"')
        sell_index_start = response.find('bid') + 6
        sell_index_end = sell_index_start + response[sell_index_start:].find('\"}')
        # Convert prices to float
        price_list = []
        if 'vwap' in display_values_list:
            price_list.append(float(response[vwap_index_start : vwap_index_end]))
        if 'low' in display_values_list:
           price_list.append(float(response[low_index_start : low_index_end]))
        if 'high' in display_values_list:
            price_list.append(float(response[high_index_start : high_index_end]))
        if 'buy' in display_values_list:
           price_list.append(float(response[buy_index_start : buy_index_end]))
        if 'sell' in display_values_list:
            price_list.append(float(response[sell_index_start : sell_index_end]))
        price_list_rounded = ResponseUtility().round_prices(price_list) # Round prices
        return price_list_rounded

    # Extract prices from Taurus response string
    @staticmethod
    def taurus_prices(response, display_values_list):
        # Start index is inclusive, end index is exclusive
        vwap_index_start = response.find('vwap') + 7
        vwap_index_end = vwap_index_start + response[vwap_index_start:].find('\",\"')
        low_index_start = response.find('low') + 6
        low_index_end = low_index_start + response[low_index_start:].find('\",\"')
        high_index_start = response.find('high') + 7
        high_index_end = high_index_start + response[high_index_start:].find('\",\"')
        buy_index_start = response.find('ask') + 6
        buy_index_end = buy_index_start + response[buy_index_start:].find('\",\"')
        sell_index_start = response.find('bid') + 6
        sell_index_end = sell_index_start + response[sell_index_start:].find('\",\"')
        # Convert prices to float
        price_list = []
        if 'vwap' in display_values_list:
            price_list.append(float(response[vwap_index_start : vwap_index_end]))
        if 'low' in display_values_list:
           price_list.append(float(response[low_index_start : low_index_end]))
        if 'high' in display_values_list:
            price_list.append(float(response[high_index_start : high_index_end]))
        if 'buy' in display_values_list:
           price_list.append(float(response[buy_index_start : buy_index_end]))
        if 'sell' in display_values_list:
            price_list.append(float(response[sell_index_start : sell_index_end]))
        price_list_rounded = ResponseUtility().round_prices(price_list) # Round prices
        return price_list_rounded

    # Extract prices from Taurus response string
    @staticmethod
    def btce_prices(response, display_values_list):
        # Start index is inclusive, end index is exclusive
        low_index_start = response.find('low') + 5
        low_index_end = low_index_start + response[low_index_start:].find(',\"')
        high_index_start = response.find('high') + 6
        high_index_end = high_index_start + response[high_index_start:].find(',\"')
        buy_index_start = response.find('buy') + 5
        buy_index_end = buy_index_start + response[buy_index_start:].find(',\"')
        sell_index_start = response.find('sell') + 6
        sell_index_end = sell_index_start + response[sell_index_start:].find(',\"')
        # Convert prices to float
        price_list = []
        if 'vwap' in display_values_list:
            price_list.append(0)
        if 'low' in display_values_list:
           price_list.append(float(response[low_index_start : low_index_end]))
        if 'high' in display_values_list:
            price_list.append(float(response[high_index_start : high_index_end]))
        if 'buy' in display_values_list:
           price_list.append(float(response[buy_index_start : buy_index_end]))
        if 'sell' in display_values_list:
            price_list.append(float(response[sell_index_start : sell_index_end]))
        price_list_rounded = ResponseUtility().round_prices(price_list) # Round prices
        price_list_rounded[1] = "N/A" # VWAP not available
        return price_list_rounded

     # Extract prices from Bitstamp response string
    @staticmethod
    def bitstamp_prices(response, display_values_list):
        # Start index is inclusive, end index is exclusive
        vwap_index_start = response.find('vwap') + 8
        vwap_index_end = vwap_index_start + response[vwap_index_start:].find('\", \"')
        low_index_start = response.find('low') + 7
        low_index_end = low_index_start + response[low_index_start:].find('\", \"')
        high_index_start = response.find('high') + 8
        high_index_end = high_index_start + response[high_index_start:].find('\", \"')
        buy_index_start = response.find('ask') + 7
        buy_index_end = buy_index_start + response[buy_index_start:].find('\", \"')
        sell_index_start = response.find('bid') + 7
        sell_index_end = sell_index_start + response[sell_index_start:].find('\", \"')
        # Convert prices to float
        price_list = []
        if 'vwap' in display_values_list:
            price_list.append(float(response[vwap_index_start : vwap_index_end]))
        if 'low' in display_values_list:
           price_list.append(float(response[low_index_start : low_index_end]))
        if 'high' in display_values_list:
            price_list.append(float(response[high_index_start : high_index_end]))
        if 'buy' in display_values_list:
           price_list.append(float(response[buy_index_start : buy_index_end]))
        if 'sell' in display_values_list:
            price_list.append(float(response[sell_index_start : sell_index_end]))
        price_list_rounded = ResponseUtility().round_prices(price_list) # Round prices
        return price_list_rounded

     # Extract prices from OKCoin response string
    @staticmethod
    def okcoin_prices(response, display_values_list):
        # Start index is inclusive, end index is exclusive
        low_index_start = response.find('low') + 6
        low_index_end = low_index_start + response[low_index_start:].find('\",\"')
        high_index_start = response.find('high') + 7
        high_index_end = high_index_start + response[high_index_start:].find('\",\"')
        buy_index_start = response.find('buy') + 6
        buy_index_end = buy_index_start + response[buy_index_start:].find('\",\"')
        sell_index_start = response.find('sell') + 7
        sell_index_end = sell_index_start + response[sell_index_start:].find('\",\"')
         # Convert prices to float
        price_list = []
        if 'vwap' in display_values_list:
            price_list.append(0)
        if 'low' in display_values_list:
           price_list.append(float(response[low_index_start : low_index_end]))
        if 'high' in display_values_list:
            price_list.append(float(response[high_index_start : high_index_end]))
        if 'buy' in display_values_list:
           price_list.append(float(response[buy_index_start : buy_index_end]))
        if 'sell' in display_values_list:
            price_list.append(float(response[sell_index_start : sell_index_end]))
        price_list_rounded = ResponseUtility().round_prices(price_list) # Round prices
        price_list_rounded[1] = "N/A" # VWAP not available
        return price_list_rounded

    # Extract prices from ANXPRO response string
    @staticmethod
    def anxpro_prices(response, display_values_list):
        # Start index is inclusive, end index is exclusive
        vwap = response.find('\"vwap\"')
        vwap_index_start = vwap + response[vwap:].find('\"value\":') + 10
        vwap_index_end = vwap_index_start + response[vwap_index_start:].find('\"')
        low = response.find('\"low\"')
        low_index_start = low + response[low:].find('\"value\":') + 10
        low_index_end = low_index_start + response[low_index_start:].find('\"')
        high = response.find('\"high\"')
        high_index_start = high + response[high:].find('\"value\":') + 10
        high_index_end = high_index_start + response[high_index_start:].find('\"')
        buy = response.find('\"buy\"')
        buy_index_start = buy + response[buy:].find('\"value\":') + 10
        buy_index_end = buy_index_start + response[buy_index_start:].find('\"')
        sell = response.find('\"sell\"')
        sell_index_start = sell + response[sell:].find('\"value\":') + 10
        sell_index_end = sell_index_start + response[sell_index_start:].find('\"')
        # Convert prices to float
        price_list = []
        if 'vwap' in display_values_list:
            price_list.append(float(response[vwap_index_start : vwap_index_end]))
        if 'low' in display_values_list:
           price_list.append(float(response[low_index_start : low_index_end]))
        if 'high' in display_values_list:
            price_list.append(float(response[high_index_start : high_index_end]))
        if 'buy' in display_values_list:
           price_list.append(float(response[buy_index_start : buy_index_end]))
        if 'sell' in display_values_list:
            price_list.append(float(response[sell_index_start : sell_index_end]))
        price_list_rounded = ResponseUtility().round_prices(price_list) # Round prices
        return price_list_rounded

        # Extract prices from HitBTC response string
    @staticmethod
    def hitbtc_prices(response, display_values_list):
        # Start index is inclusive, end index is exclusive
        low_index_start = response.find('low') + 6
        low_index_end = low_index_start + response[low_index_start:].find('\",\"')
        high_index_start = response.find('high') + 7
        high_index_end = high_index_start + response[high_index_start:].find('\",\"')
        buy_index_start = response.find('ask') + 6
        buy_index_end = buy_index_start + response[buy_index_start:].find('\",\"')
        sell_index_start = response.find('bid') + 6
        sell_index_end = sell_index_start + response[sell_index_start:].find('\",\"')
         # Convert prices to float
        price_list = []
        if 'vwap' in display_values_list:
            price_list.append(0)
        if 'low' in display_values_list:
           price_list.append(float(response[low_index_start : low_index_end]))
        if 'high' in display_values_list:
            price_list.append(float(response[high_index_start : high_index_end]))
        if 'buy' in display_values_list:
           price_list.append(float(response[buy_index_start : buy_index_end]))
        if 'sell' in display_values_list:
            price_list.append(float(response[sell_index_start : sell_index_end]))
        price_list_rounded = ResponseUtility().round_prices(price_list) # Round prices
        price_list_rounded[1] = "N/A" # VWAP not available
        return price_list_rounded
    
