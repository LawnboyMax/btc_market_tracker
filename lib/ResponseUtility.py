import time
import re

# Methods that extract and format stats from exchange responses to API requests
class ResponseUtility:
    SIG_DIG = 2

    # Selects method specific to chosen exchange and passes on the response
    @staticmethod
    def getInfo(response, exchange, watchlist):

        ResponseUtility.exchange = exchange
        price_list = []
        response = response.replace('\n', ' ').replace('\r', '') #remove linebreaks for easier regex matching

        for field in watchlist:
            matchnum = 1
            # accounts for aliases used by different exchanges
            if field == 'buy':
                field = '(ask|buy|\Wa|buy.+?value)'
                matchnum = 2
            elif field == 'sell':
                field = '(bid|sell|\Wb|sell.+?value)'
                matchnum = 2
            elif field == 'vwap':
                field = '(vwap|\Wp|vwap.+?value)'
                matchnum = 2
            elif field == 'low':
                field = '(low|\Wl|low.+?value)'
                matchnum = 2
            elif field == 'high':
                field = '(high|\Wh|high.+?value)'
                matchnum = 2

            ex = field + '\W\W\W??\W??(\d*\.?\d+)' # it is possible that there are 2-4 characters between field name and value
            regex = re.compile(ex, re.IGNORECASE)
            try:
                match = regex.search(response)
                price_list.append(float(match.group(matchnum)))
            except AttributeError:
                price_list.append(0) # field does not exits. Accounts for lack of WVAP in most cases

        price_list_rounded = ResponseUtility().roundPrices(price_list) # Round prices
        price_list_rounded = [x if (x != '0') else 'N/A' for x in price_list_rounded] # print N/A for field which is 0
        return price_list_rounded

    # Rounds floats to SIG_DIG significant digits and return as str list. First element of list is exchange name.
    @staticmethod
    def roundPrices(price_list):

        price_list_rounded = []
        price_list_rounded.append(ResponseUtility.exchange.capitalize()) # add exchange name for use with tabulate library
        for p in price_list:
            p = round(p, ResponseUtility.SIG_DIG)
            p = str(p)
            price_list_rounded.append(p)
        return price_list_rounded
