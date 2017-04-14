import requests
import curses
import os
import time
import sys

from ResponseUtility import ResponseUtility

# Coordinates used by curses to display prices
curses_yx = []

# Extract list from field
def getList(fieldname, line):
    
    offset = len(fieldname) + len(': ')
    return line[offset:].strip().split(', ')

# Get exchange names, currency and refresh rate from config. Check correctness.
def readConfig():

    curr_dir = os.path.dirname(__file__)
    config = os.path.join(curr_dir, 'config_files/config')
    with open (config) as fp:
        for line in fp:
            if (line.startswith('exchanges')):
                global exchange_list
                exchange_list = getList('exchanges', line)     # Write exchanges to a list
            elif (line.startswith('currency')):
                global currency_list
                currency_list = getList('currency', line)     # Write to currency list
            elif (line.startswith('watchlist')):                 
                global watchlist
                watchlist = getList('watchlist', line)     # Write to watchlist
            elif (line.startswith('refresh rate')):                 
                global refresh_rate_list
                refresh_rate_list = getList('refresh rate', line)   # Write to refresh rate list

# loads list of supported configuration parameters from field
def loadAvailParam(field):

    curr_dir = os.path.dirname(__file__)
    param = os.path.join(curr_dir, 'dict/avail_param')
    l = []
    with open(param) as f:
        for line in f:
           if (line.startswith(field)):
               l = getList(field, line)
    return l

# Check if chosen exchanges/currency/watchlist_items are supported. Check for typos
def checkConfig():

    # Check if specified exchanges are supported
    available_exchanges = loadAvailParam('exchange')
    for exchange in exchange_list:
        if exchange.lower() not in available_exchanges:
            sys.exit("Exchange \'" + exchange + "\' is not a supported exchange. Please check config for the list of avalable exchanges.")
    
    # Check if specified currency is supported and only one is entered
    if len(currency_list) != 1:
        sys.exit("Currency field contains more than one value.")
    available_currencies = loadAvailParam('currency')
    global currency
    currency = ''.join(currency_list)
    if currency not in available_currencies:
        sys.exit("Selected currency \'" + currency + "\' is not supported. Please check config for the list of available currencies.")

    # Check if specified watchitems are supported
    available_watchitems = loadAvailParam('watchlist')
    for display_value in watchlist:
        if display_value.lower() not in available_watchitems:
            sys.exit("Market data value \'" + display_value + "\' is not supported. Please check config for the list of available data values.")

    # Check if specified refresh rate is suppoted and only one is entered
    if len(refresh_rate_list) != 1:
        sys.exit("Refresh rate field contains more than one value.")
    global refresh_rate
    try:
            refresh_rate = int(''.join(refresh_rate_list))
    except ValueError:
        sys.exit("Entered refresh rate is not a number. Please check config.")
    if refresh_rate <= 0:
        sys.exit("Refresh rate should be a positive number.")

# Creates a table using ncurses library and populates it
def createTable(screen):

    # Display currency at the top of the table
    screen.addstr(0, 0, "Currency: " + currency.upper())

    # Place column names
    screen.addstr(2, 0, "Exchange", curses.A_STANDOUT)
    k = 0
    for value in watchlist:
        if (value.lower() == 'vwap'):
            header = 'VWAP'
        else:
            header = value.capitalize()
        screen.addstr(2, (15 + 10 * k), header, curses.A_STANDOUT)
        k = k + 1
       
    # Construct list of URLs for chosen exchanges and currency
    global request_url_list
    request_url_list = []
    for exchange in exchange_list[:]:
        request_url = getUrl(exchange, currency)
        if (request_url == 1):
            exchange_list.remove(exchange)  # If exchange doesn't support chosen currency, remove from exchange_list
            continue
        request_url_list.append(request_url)

    # Populate curses_yx
    col_num = len(exchange_list)
    row_num = len(watchlist)
    for c in range(0, col_num):
        curses_yx.append([(4 + c * 2), 0])  # Leave more space between exchange name and first price in a row
        curses_yx.append([(4 + c * 2), 15])
        for r in range(0, row_num - 1):
            curses_yx.append([(4 + c * 2), (r * 10 + 25)])

# Returns URL for selected exchange_name and currency. 
# Returns -1 if exchange_name is invalid or if exchange doesn't support chosen currency.
def getUrl(exchange_name, currency):

    url_dict = loadUrl()
    path_dict = loadPath()
    try:
        return url_dict[exchange_name] + path_dict[exchange_name,currency]
    except (KeyError, NameError):
        return 1

# Loads dictionary of URL addresses for supported exchanges APIs
def loadUrl():
    curr_dir = os.path.dirname(__file__)
    urls = os.path.join(curr_dir, 'dict/url')
    d = {}
    with open(urls) as f:
        for line in f:
           (key, val) = line.split()
           d[key] = val
    return d

# Loads dictionary of filepaths to BTC ticker in exchanges APIs
def loadPath():
    curr_dir = os.path.dirname(__file__)
    path = os.path.join(curr_dir, 'dict/url_path')
    d = {}
    with open(path) as f:
        for line in f:
           (key_str, val) = line.split()
           key = eval(key_str)
           d[key] = val
    return d

# Infinite loop. Displays prices and updates them every (refresh_rate) # of seconds
def displayPrices(screen, refresh_rate, request_url_list, exchange_list, watchlist):

    try:
        while True:
            j = 0
            # Reinitialize lists used for printing the retrieved prices
            price_table = [] 
            price_list=[]
            # Request public ticker data from exchanges, extract prices and construct a 2D list (each exchange has its own row)
            for url in request_url_list:
                response = requests.get(url).text
                price_list = ResponseUtility.getInfo(response, exchange_list[j], watchlist)
                price_table.append(price_list)
                j = j + 1
            j = 0

            # Display prices
            for  ticker_stats in price_table:
                for price in ticker_stats:
                    y = curses_yx[j][0]
                    x = curses_yx[j][1]
                    screen.addstr(y, x, price)
                    screen.refresh()
                    j = j + 1

            # Exit the program if 'q' is pressed
            for num in range(0, refresh_rate*20): # Each iteration of the loop is 50ms. refresh_rates * 50 * 20 = refresh_rate in ms
                curses.napms(50)
                if screen.getch() == ord('q'):
                    sys.exit()

    except KeyboardInterrupt:
        pass

# Reads from config. Constructs table. Makes http requests.
def main(screen):

    screen.nodelay(1)
    readConfig()
    checkConfig()
    createTable(screen)        
    # Infinite loop. Displays prices and updates them every (refresh_rate) # of seconds
    displayPrices(screen, refresh_rate, request_url_list, exchange_list, watchlist)

if __name__ == "__main__":
    curses.wrapper(main)
