# -*- coding: utf-8 -*-
# models.py
from django.db import models
from decimal import *
from usd_cny.common.appconfig import BTC_PLATFORMS


class CurrencyType(models.Model):
    tag = models.CharField(max_length=255)

    def save(self, *args, **kwargs):
        self.tag = self.tag.upper()
        super(self.__class__, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "CurrencyType"
        verbose_name_plural = "CurrencyTypes"

    def __str__(self):
        return self.tag


class BTCPlatform(models.Model):
    name = models.CharField(max_length=255)
    currencyType = models.ManyToManyField(CurrencyType)

    class Meta:
        verbose_name = "Platform"
        verbose_name_plural = "Platform"

    def __str__(self):
        return self.name


class TransferOrder(models.Model):
    sendAmount = models.DecimalField(max_digits=9, decimal_places=2)
    sendOverAmount = models.DecimalField(max_digits=12, decimal_places=5)
    receiveAmount = models.DecimalField(max_digits=12, decimal_places=5)
    receiveOverAmount = models.DecimalField(max_digits=9, decimal_places=2)
    sendCurrency = models.ForeignKey(CurrencyType, related_name='FromCurrency')
    receiveCurrency = models.ForeignKey(CurrencyType)
    exchangeRate = models.DecimalField(max_digits=9, decimal_places=4)
    status = models.IntegerField(default=0, choices=((0, u"未处理"), (1, u"完成"), (2, u"中断")))

    class Meta:
        verbose_name = "TransferOrder"
        verbose_name_plural = "TransferOrders"



class TransferSubOrder(models.Model):
    sendAmount = models.DecimalField(max_digits=9, decimal_places=2)
    receiveAmount = models.DecimalField(max_digits=9, decimal_places=2)
    sendCurrency = models.ForeignKey(CurrencyType)
    receiveCurrency = models.ForeignKey(CurrencyType, related_name="ReceiveCurrency")
    btcoin_number = models.DecimalField(max_digits=12, decimal_places=5)
    orderID = models.ForeignKey(TransferOrder)
    status = models.IntegerField(default=0, choices=((0, u"未处理"), (1, u"完成"), (2, u"中断")))

    class Meta:
        verbose_name = "TransferSubOrder"
        verbose_name_plural = "TransferSubOrders"

    def __str__(self):
        return self.id


class BTCBalance(models.Model):
    currency = models.ForeignKey(CurrencyType)
    money = models.DecimalField(max_digits=15, decimal_places=5)
    btc = models.DecimalField(max_digits=15, decimal_places=5)

    def __str__(self):
        return self.currency.tag

    @staticmethod
    def get_all_platforms_balance():
        try:
            balances = [{platform: BTC_PLATFORMS[platform].get_balance()} for platform in BTC_PLATFORMS]
            currencys = [platform for platform in BTC_PLATFORMS]
            print balances
            for balance in balances:
                for currency in currencys:
                    if currency in balance:
                        BTCBalance.set_platform_balance(balance[currency], currency)
        except:
            pass

    @staticmethod
    def set_platform_balance(balance, currency):
        currency_id = CurrencyType.objects.get(tag=currency).id
        try:
            platform_balance = BTCBalance.objects.get(currency_id=currency_id)
            platform_balance.money = balance[currency]
            platform_balance.btc = balance['BTC']
            platform_balance.save()
        except:
            BTCBalance.objects.create(currency_id=currency_id, money=0, btc=0)

    @staticmethod
    def get_platform_balence(currency):
        currency_id = CurrencyType.objects.get(tag=currency).id
        obj, created = BTCBalance.objects.get_or_create(currency_id=currency_id, defaults={'money': 0, 'btc': 0})
        return {currency: {'btc': obj.btc, 'money': obj.money}}

    @staticmethod
    def get_all_platform_balance():
        result = [{currency: BTCBalance.get_platform_balence(currency)} for currency in BTC_PLATFORMS.keys()]
        print result
        return result
