<snippet>
  <content>
# BTC Market Tracker
Real time Bitcoin market data tracker that runs in a terminal. Fully customizable.

![screenshot](http://i68.tinypic.com/8zk17t.png)

A static version is also available.

![screenshot](http://i68.tinypic.com/2mzfeoj.png)
## Getting Started
Python3 is required.

Just run `python3 btc_tracker.py` for real-time tracking or `python3 btc_tracker_static.py` for a single market data request.

OR

Use `btc.sh` for easier access to the script:

First, set correct path in btc.sh. Then:

````
$ set $PATH:(path to lib folder)
$ mv btc.sh /usr/local/bin
$ chmod 755 /usr/local/bin/btc.sh
````
Now `btc.sh` runs the script regardless of current working directory.

## Usage

To choose types of market data, currency and exchanges you want to display, make appropriate changes to `config` in `config_files` folder.

To exit btc_tracker.py press `[q]`.

## Supported exchanges

- [Bitfinex](https://www.bitfinex.com/): USD
- [Kraken](https://www.kraken.com/): USD, CAD, EUR, GBP, JPY
- [QuadrigaCX](https://www.quadrigacx.com/): USD, CAD
- [Taurus](https://www.taurusexchange.com/): CAD
- [BTC-E](https://btc-e.com/): USD, EUR, RUB
- [Bitstamp](https://www.bitstamp.net/): USD, EUR
- [OKCoin](https://www.okcoin.com/): USD
- [ANXPRO](https://anxpro.com/): USD, CAD, EUR, GBP, AUD, JPY
- [HitBTC](https://hitbtc.com/): USD, EUR

## Contributing
1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request.

## License

MIT License

Copyright (c) 2016 Maxim Mikhaylov

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
</snippet>
