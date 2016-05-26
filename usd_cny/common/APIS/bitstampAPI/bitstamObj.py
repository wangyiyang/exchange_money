# -*- coding: utf-8 -*-
from decimal import Decimal
from usd_cny.common.APIS.bitstampAPI.api import account_balance, \
    buy_limit_order, sell_limit_order, ticker, get_order_info, order_book
from usd_cny.common.APIS.btcInterface import BTCInterface

__author__ = 'wangyiyang'


class Bitstam(BTCInterface):

    def __init__(self, currency="usd"):
        self.currency = currency
        # print "调用 Bitstam API"

    def get_balance(self):
        """

        :return:{比特币数量，剩余金额}
        """
        result = account_balance()
        return {
            "BTC": result["btc"],
            self.currency.upper(): result[self.currency]
        }

    def get_need_money_depth(self, bitcRes=None, ord_type=None):
        """

        :param bitcRes:比特币数量
        :param ord_type:交易类型
        :return:可能要 使用/获取 的金额
        """
        bitcRes = Decimal(round(bitcRes,2))
        money = 0
        try:
            results = order_book()
            results = results.get(ord_type)
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
            print u"get_bitstamp_market_amount_depth error!"
        return money

    def get_btc_num_depth(self, money):
        """

        :param money:要使用的金额
        :return:可能获取的比特币
        """
        money = Decimal(round(money,2))
        bitcRes = 0
        try:
            results = order_book()
            asks = results.get("asks")
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
            print u"get_bitstamp_market_value_depth error!"

        return bitcRes

    def get_order_info(self, order_id, order_type):
        """

        :return:订单信息
        """
        amount = Decimal(0.0)
        money = Decimal(0.0)
        try:
            result = get_order_info(order_id)
        except:
            print u"获取订单信息失败"
        else:
            for ord in result['transactions']:
                amount += Decimal(ord['btc'])
                money += Decimal(ord['usd'])
        return {
            "money": money,
            "btc": amount,
            'status': get_order_info(order_id)['status']
        }

    def tran_btc(self, num, ord_type):
        """

        :return:
        """
        if ord_type == "buy":
            result = buy_limit_order(amount=num, price=ticker()['ask'])
        else:
            result = sell_limit_order(amount=num, price=ticker()['bid'])
        return result['id']

    def get_market_depth(self):
        return order_book()

