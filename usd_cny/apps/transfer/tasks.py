# -*- coding: utf-8 -*-
from usd_cny.apps.transfer.models import BTCBalance
from usd_cny.apps.transfer.objects import MBM
from celery import task

__author__ = 'wangyiyang'


@task
def run_BMB(order_id=None):
    """
    :rtype : 运行比特币平衡机运行比特币平衡机
    :param order_id:需要平衡的订单id
    :return:
    """
    _mbm = MBM(order_id=order_id)
    _mbm.run()

@task
def get_balances():
    get_btc_balance_obj = BTCBalance()
    get_btc_balance_obj.get_all_platforms_balance()
    return True