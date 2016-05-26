# -*- coding: utf-8 -*-
import urllib2
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test
import redis
from usd_cny.apps.transfer.models import BTCBalance

RDB6 = redis.StrictRedis(host='localhost', port=6379, db=6)




def login_required(function=None,
                   redirect_field_name=REDIRECT_FIELD_NAME,
                   login_url=None, user_type=0):
    """
    Decorator for views that checks that the user is logged in, redirecting
    to the log-in page if necessary.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated(),
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def get_exchange_rate_yahoo(from_currency=None, to_currency=None):
    """
    从本地数据库获取汇率
    by wyy
    :param from_currency:被转换币种
    :param to_currency:到达币种
    :return:汇率
    """
    try:
        if RDB6.exists('{from_Currency},{to_Currency}'.format(from_Currency=from_currency, to_Currency=to_currency)):
            return float(
                RDB6.get('{from_Currency},{to_Currency}'.format(from_Currency=from_currency, to_Currency=to_currency)))
    except:
        return get_exchange_rate(from_currency, to_currency)


def get_exchange_rate(from_currency=None, to_currency=None):
    """
    从API获取汇率
    by wyy
    :param from_currency:被转换币种
    :param to_currency:到达币种
    :return:汇率
    """
    url = "https://openexchangerates.org/api/latest.json?app_id=f9265a7513c74c6bb3e2f7b2668d68ea&base=%s&symbols=%s" % (
        from_currency, to_currency)
    try:
        response = urllib2.urlopen(url, timeout=60).read()
        json_html = eval(response)
        return float(json_html.get("rates")[to_currency])
    except Exception, e:
        return 0


def judge_balance(from_currency=None, amount=None, to_currency=None, btcnum=None):
        """
        by wyy
        判断比特币平台的金额或比特币是否充足
        :param from_currency(str):转账币种
        :param amount(float): 需要金额
        :param to_currency(str: 到账币种
        :param btcnum(float): 需要比特币数量
        :return:bool
        """
        get_btc_balance_obj = BTCBalance()
        get_btc_balance_obj.get_all_platforms_balance()
        result_from = True
        result_to = True
        try:
            print from_currency, get_btc_balance_obj.get_platform_balence(from_currency)[from_currency]['money']
            print to_currency, get_btc_balance_obj.get_platform_balence(to_currency)[to_currency]['btc']
            result_from = True if float(get_btc_balance_obj.get_platform_balence(from_currency)[from_currency]['money']) >= float(
                amount) else False
            result_to = True if float(get_btc_balance_obj.get_platform_balence(to_currency)[to_currency]['btc']) >= float(
                btcnum) else False
        except:
            result_from = False
            result_to = False
            print "judge_balance from_currency: %s, to_currency: %s error!" % (from_currency, to_currency)
        result = True if result_from == result_to == True else False
        print "judge_balance: %s " % result
        return result