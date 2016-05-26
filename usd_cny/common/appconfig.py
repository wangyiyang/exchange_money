# -*- coding: utf-8 -*-
from usd_cny.common.APIS.bitstampAPI.bitstamObj import Bitstam
from usd_cny.common.APIS.btcchinaAPI.btcchinaObj import BTCChina

__author__ = 'wangyiyang'


BTC_PLATFORMS = {"USD": Bitstam(currency="usd"), "CNY": BTCChina(currency="cny")}



