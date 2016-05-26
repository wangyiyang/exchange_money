# coding=utf-8
# btcInterface.py

# -*- coding: utf-8 -*-

__author__ = 'KK'


"""
比特币平台接口
"""


class BTCInterface(object):

    def get_balance(self):
        """

        :return:{比特币数量，剩余金额}
        """

    def get_need_money_depth(self, bitcRes=None, ord_type=None):
        """

        :param bitcRes:比特币数量
        :param ord_type:交易类型
        :return:可能要 使用/获取 的金额
        """
        pass

    def get_btc_num_depth(self, money):
        """

        :param money:要使用的金额
        :return:可能获取的比特币
        """
        pass

    def get_order_info(self, order_id, order_type):
        """

        :return:订单信息
        """
        pass

    def tran_btc(self, num, ord_type):
        """

        :return:
        """

    def get_ticker(self):
        pass

    def get_market_depth(self):
        pass