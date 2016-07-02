# exchange_rate.py
import urllib2

#https://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20yahoo.finance.xchange%20where%20pair%20in%20(%22{from_currency}{to_currency}%22)&format=json&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys

def get_exchange_rates(from_currency, to_currency):
    url = "https://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20yahoo.finance.xchange%20where%20pair%20in%20(%22{from_currency}{to_currency}%22)&format=json&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys".format(
        from_currency=from_currency, to_currency=to_currency)
    response = urllib2.urlopen(url, timeout=20).read()
    json_html = eval(response)
    return json_html["query"]["results"]["rate"]["Rate"]


if __name__ == '__main__':
    print(get_exchange_rates("USD", "CNY"))
