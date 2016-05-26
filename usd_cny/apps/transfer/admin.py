# admin.py
from django.contrib import admin
from usd_cny.apps.transfer.models import *
# Register your models here.


class BTCBalanceAdmin(admin.ModelAdmin):
    list_display = ('currency', 'money', 'btc')

class TransferOrderAdmin(admin.ModelAdmin):
    list_display = ('sendAmount','receiveAmount','sendCurrency','receiveCurrency','sendOverAmount','receiveOverAmount','exchangeRate','status')


admin.site.register(CurrencyType)
admin.site.register(TransferOrder,TransferOrderAdmin)
admin.site.register(BTCPlatform)
admin.site.register(BTCBalance,BTCBalanceAdmin)
