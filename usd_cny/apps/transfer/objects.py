# -*- coding: utf-8 -*-
from copy import copy
import time
from decimal import Decimal
from usd_cny.apps.transfer.models import TransferOrder, TransferSubOrder, BTCBalance
from usd_cny.common.appconfig import BTC_PLATFORMS
from usd_cny.common.util import judge_balance, get_exchange_rate_yahoo

__author__ = 'wangyiyang'

"""比特币平衡机类，主要封装了比特币交易的主要方法"""

INTEREST_RATE = 0.01



def get_suit_amount(from_currency, to_currency):
    amount = 0
    try:
        roe = float(get_exchange_rate_yahoo(from_currency, to_currency))
        from_depth = sorted(
            BTC_PLATFORMS[from_currency].get_market_depth()['asks' if from_currency != 'CNY' else "ask"],
            key=lambda x: float(x['price']))
        to_depth = sorted(BTC_PLATFORMS[to_currency].get_market_depth()['bids' if to_currency != 'CNY' else "bid"],
                          key=lambda x: float(x['price']), reverse=True)
        for from_item in from_depth:
            bitcRes = float(from_item['amount'])
            money = 0
            count = 0
            for to_item in to_depth:
                price = float(to_item['price'])
                bitc = float(to_item['amount'])

                if float(to_item['amount']) <= 0 or bitcRes<=0:
                    to_item['amount'] = 0
                    break
                if bitc <= bitcRes:
                    money += float(price) * float(bitc)
                    bitcRes -= float(bitc)
                else:
                    money += float(bitcRes) * float(price)
                    to_item['amount'] = float(to_item['amount']) - float(bitcRes)
                    bitcRes = 0
                    break

                count += 1
            if float(from_item['price'] * from_item['amount']) * roe * (1 + INTEREST_RATE) <= float(money):
                amount += bitcRes
                print "买入金额加利润换算:{from_money},单价{from_price}卖出金额:{to_money}，单价：{to_price},比特币数量：{amount}".format(
                    to_price=float(money) / float(from_item['amount']), from_price=float(from_item['price']) * roe,
                    from_money=float(from_item['price'] * from_item['amount']) * roe * (1 + INTEREST_RATE),
                    to_money=float(money), amount=bitcRes)
    finally:
        return amount


def choose_btc_buy_platforms_depth(currency, amount):
    """
    by wyy
    :param currency(str):币种
    :param amount(float): 需要兑换的金额
    :return:比特币数量
    """
    return BTC_PLATFORMS[currency].get_btc_num_depth(amount)


def get_market_amount_depth(currency, bitcRes, ord_type):
    """
    by wyy
    :param currency: (string)币种
    :param bitcRes: (float)比特币数量
    :param ord_type: (string asks & bids)order类型
    :return:(float)需要货币的金额
    """
    return BTC_PLATFORMS[currency].get_need_money_depth(bitcRes, ord_type)


def tran_btc_money(currency, num, ord_type):
    """
    by wyy
    :param currency(str):交易币种
    :param num(float):交易比特币数量
    :param ord_type:交易类型（sell/buy）
    :return:currency_account_change_money 交易 使用/获得 的金额
    """
    print "交易货币:", currency
    btc_obj = BTC_PLATFORMS[currency]
    btc_order = btc_obj.tran_btc(num, ord_type)
    if not btc_order:
        order_info = {"btc": 0, "money": 0}
    else:
        order_info = btc_obj.get_order_info(btc_order, order_type=ord_type)
    return float(order_info['money']), float(order_info['btc'])


def tran_btc(num, mbm_ord, btctran, ord_type):
    """
    by wyy
    :param num(float):交易比特币的数量
    :param mbm_ord(object):主订单对象
    :param mbm_subord(object):子订单对象
    :param btctran(object):切片订单对象
    :param ord_type(str):交易类型
    :return:
    """
    if ord_type == 'buy':
        currency = btctran.currency_type.tag
    else:
        currency = btctran.sell_currency_type.tag
    currency_account_change_money, currency_account_change_btc = tran_btc_money(currency, num, ord_type)
    print("交易到的金额{currency_account_change_money}".format(
        currency_account_change_money=currency_account_change_money))
    if abs(currency_account_change_money):
        if ord_type == 'buy':
            order = TransferOrder.objects.get(id=mbm_ord)
            order.sendOverAmount = Decimal(order.sendOverAmount) - Decimal(currency_account_change_money)
            order.save()
            btctran.amount_confirmed = currency_account_change_money
            btctran.status = 1
        else:
            order = TransferOrder.objects.get(id=mbm_ord)
            order.receiveOverAmount = Decimal(order.receiveOverAmount) + Decimal(currency_account_change_money)
            order.save()
    elif ord_type == 'sell':
        btctran.save()
    return currency_account_change_btc


def init():
    TransferOrder.objects.filter(status=1).update(status=2)


class MBM(object):
    NEED_TRAN_BTC_COUNT = 5
    MBM_LIMIT_UNIT = 0.1
    BTC_TRAN_BIT_TIME = 10

    def __init__(self, order_id=None):
        self.order = None
        self.order_id = order_id

    def get_order(self):
        if self.order_id:
            self.order = TransferOrder.objects.get(id=self.order_id)
        else:
            orders = TransferOrder.objects.filter(status=0)
            if len(orders):
                self.order = orders[0]
        return self.order

    def run(self):
        self.get_order()
        print self.order_id
        #
        # if float(self.order.sendOverAmount) < buy_money or float(
        #                 self.order.receiveAmount - self.order.receiveOverAmount) < sell_money:
        #     print "金额不足买卖"
        #     print float(self.order.sendOverAmount) < buy_money
        #     print float(self.order.receiveAmount - self.order.receiveOverAmount) < sell_money
        #     self.order.status = 1
        #     self.order.save()
        #     return
        # else:
        tan_amount = 0.0
        while True:
            tan_btc_num = get_suit_amount(self.order.sendCurrency.tag, self.order.receiveCurrency.tag)/2
            print tan_btc_num
            if tan_btc_num:
                buy_money = get_market_amount_depth(self.order.sendCurrency.tag, tan_btc_num, "asks")
                sell_money = get_market_amount_depth(self.order.receiveCurrency.tag, tan_btc_num, "bids")
                print "buy_money: ", buy_money
                print "sell_money: ", sell_money
                print "To come up with surplus money"
                order = TransferOrder.objects.get(id=self.order.id)
                if buy_money > order.sendOverAmount:
                    tan_btc_num = choose_btc_buy_platforms_depth(self.order.sendCurrency.tag,
                                                                 order.sendOverAmount)
                    tan_amount = copy(order.sendOverAmount)
                    order.save()
                if buy_money <= order.sendOverAmount:
                    tan_btc_num = self.MBM_LIMIT_UNIT
                    tan_amount = buy_money
                    order.save()
                if not buy_money or not sell_money or not judge_balance(from_currency=self.order.sendCurrency.tag,
                                                                    amount=tan_amount,
                                                                    to_currency=self.order.receiveCurrency.tag,
                                                                    btcnum=round(tan_btc_num,2)):
                    orderae = TransferOrder.objects.get(id=self.order_id)
                    orderae.status = 2
                    orderae.save()
                    print "Platform amount not enough"
                    return
                # try:
                btctran = TransferSubOrder()
                btctran.amount = tan_amount
                btctran.btcoin_number = tan_btc_num
                btctran.orderID_id = self.order.id
                btctran.currency_type = order.sendCurrency
                btctran.sell_currency_type = order.receiveCurrency
                if tan_btc_num < 0.1:
                    print u"买卖数量过小"
                    orderce = TransferOrder.objects.get(id=self.order_id)
                    orderce.status = 1
                    orderce.save()
                    break
                print("buy or sell btc:{num}".format(num=tan_btc_num))
                btctran.btcoin_number = tran_btc(num=round(btctran.btcoin_number, 2), mbm_ord=order.id,
                                                 btctran=btctran, ord_type='buy')
                if btctran.status == 1:
                    tran_btc(num=btctran.btcoin_number, mbm_ord=order.id, btctran=btctran,
                                 ord_type='sell')
                # except:
                #     print u"BtcTransaction create Object ERROR！"
                # finally:
                get_btc_balance_obj = BTCBalance()
                get_btc_balance_obj.get_all_platforms_balance()
                print "sleep order"
            time.sleep(self.BTC_TRAN_BIT_TIME)
