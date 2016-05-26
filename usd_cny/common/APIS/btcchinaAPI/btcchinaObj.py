# coding=utf-8
# btcchinaObj.py
from decimal import Decimal
import time
import urllib2
from usd_cny.common.APIS.btcInterface import BTCInterface
from usd_cny.common.APIS.btcchinaAPI import btcchina

access_key = ""
secret_key = ""
bc = btcchina.BTCChina(access_key, secret_key)


class BTCChina(BTCInterface):
    def __init__(self, currency="cny"):
        self.currency = currency

    def get_balance(self):
        """

        :return:{比特币数量，剩余金额}
        """
        bc = btcchina.BTCChina(access_key, secret_key)
        result = bc.get_account_info()
        btc_amount = result['balance']['btc']['amount']
        money_amount = result['balance'][self.currency]['amount']
        return {
            "BTC": btc_amount,
            self.currency.upper(): money_amount
        }

    def get_need_money_depth(self, bitcRes=None, ord_type=None):
        """

        :param bitcRes:比特币数量
        :param ord_type:交易类型
        :return:可能要 使用/获取 的金额
        """
        bc = btcchina.BTCChina(access_key, secret_key)
        bc.get_market_depth2(limit=100)
        bitcRes = Decimal(round(bitcRes, 2))
        if ord_type == "asks":
            ord_type = "ask"
        elif ord_type == "bids":
            ord_type = "bid"
        money = 0
        try:
            results = bc.get_market_depth2(limit=100)
            results = results.get('market_depth')
            results = results.get(ord_type[:3])
            for ord in results:
                price = Decimal(ord['price'])
                bitc = Decimal(ord['amount'])
                if bitcRes <= 0:
                    break
                if bitc <= bitcRes:
                    money += price * bitc
                    bitcRes -= bitc
                else:
                    money += bitcRes * price
                    break
        except:
            print u"get_btcchina_market_amount_depth error!"
        return money

    def get_btc_num_depth(self, money):
        """

        :param money:要使用的金额
        :return:可能获取的比特币
        """
        bc = btcchina.BTCChina(access_key, secret_key)
        money = Decimal(round(money, 2))
        bitcRes = 0
        try:
            results = bc.get_market_depth2(limit=100)
            asks = results.get('market_depth').get('ask')
            for ask in asks:
                price = Decimal(ask['price'])
                bitc = Decimal(ask['amount'])
                if money <= 0:
                    break
                if price * bitc <= money:
                    money -= price * bitc
                    bitcRes += bitc
                else:
                    bitcRes += money / price
                    break
        except:
            print u"get_btcchina_market_value_depth error!"

        return bitcRes

    def get_order_info(self, order_id, order_type=None):
        """

        :return:订单信息
        """
        time.sleep(5)
        result = {}
        oc = btcchina.BTCChina(access_key, secret_key)
        try:
            result = oc.get_orders(order_id)
            print result
        except:
            result['order']['amount_original'] = 0.0
            result['order']['avg_price'] = 0.0
        return {
            "money": Decimal(float(result['order']['amount_original']) * float(result['order']['avg_price'])),
            "btc": Decimal(result['order']['amount_original']),
            # 'status': get_order_info(order_id)['status']
        }

    def tran_btc(self, num, ord_type):
        """

        :return:
        """
        oc = btcchina.BTCChina(access_key, secret_key)
        if ord_type == "buy":
            result = oc.buy(amount=num)
        else:
            result = oc.sell(amount=num)
        return result

    def get_ticker(self):
        url = "https://data.btcchina.com/data/ticker?market=btccny"
        response = urllib2.urlopen(url, timeout=60).read()
        return eval(response)

    def get_suit_btc(self, price, order_type):
        bc = btcchina.BTCChina(access_key, secret_key)
        results = bc.get_market_depth2(limit=1000)
        if order_type == "asks":
            order_type = "ask"
        elif order_type == "bids":
            order_type = "bid"
        results = results.get('market_depth')
        results = results.get(order_type[:3])
        btcnum = 0
        for result in results:
            _price = float(result['price'])
            bitc = float(result['amount'])
            if order_type == "ask":
                if float(_price) <= float(price):
                    btcnum += float(bitc)
            else:
                if float(_price) >= float(price):
                    btcnum += float(bitc)
        return btcnum

    def get_market_depth(self):
        bc = btcchina.BTCChina(access_key, secret_key)
        results = bc.get_market_depth2(limit=1000)
        return results.get('market_depth')