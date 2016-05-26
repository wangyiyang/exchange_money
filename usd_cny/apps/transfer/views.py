# -*- coding: utf-8 -*-
from decimal import Decimal
import random

from django.shortcuts import render

# Create your views here.
from django.shortcuts import redirect
from django.contrib import messages
import json
import datetime
import logging
import base64
from usd_cny.apps.transfer.models import CurrencyType, TransferOrder, BTCBalance

logger = logging.getLogger(__name__)

# Third-Party Modules

from django.http import HttpResponseRedirect, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.utils import timezone
from django.contrib.auth.models import User
from usd_cny.common.util import login_required, get_exchange_rate_yahoo
from django.contrib import messages
from django.db import transaction
import traceback
from django.contrib.auth.hashers import check_password
from django.contrib import auth
import tasks


def index(request):
    return render(request, 'index.html')


@csrf_exempt
def login(request):
    # print request.POST
    if request.user.is_authenticated():
        auth.logout(request)
    msg = {"msg": ""}
    next = request.GET.get('next', 'transfer')
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = ''
        if not user:
            user = auth.authenticate(username=username, password=password)
        if user and user.is_active:
            auth.login(request, user)
            return HttpResponseRedirect(reverse(next))
        else:
            request.session["login_count"] = True
            msg = {
                "msg": u"The password or username entered \
                is incorrect. Please try again!"
            }
    return render_to_response('index.html', {
        'next': next,
        'err_msg': msg
    }, context_instance=RequestContext(request))


@login_required
def transfer(request):
    currencys=CurrencyType.objects.values_list('tag', flat=True).order_by('tag')
    return render_to_response('transfer.html', {
        'currencys': currencys,
        'error':request.GET.get('error','')
    }, context_instance=RequestContext(request))


@login_required
@csrf_exempt
def transfer_exchange(request):
    send_currency = request.POST.get('send_currency', 'CNY')
    revceive_currency = request.POST.get('receive_currency', 'USD')
    revceive_currency = 'CNY' if send_currency == revceive_currency else revceive_currency
    print send_currency,revceive_currency
    roe = float(get_exchange_rate_yahoo(send_currency, revceive_currency))
    return HttpResponse(json.dumps(
        {
            'revceive_amount': float(request.POST.get('send_amount', 100)) * roe,
            'revceive_currency':revceive_currency,
            "roe":roe
        }),
        content_type="application/json; charset=utf-8")


@login_required
def transfersubmit(request):
    print request.POST
    if TransferOrder.objects.filter(status=0):
         return HttpResponseRedirect('/transfer/?error=1')
    ts_order = TransferOrder()
    ts_order.sendAmount = float(request.POST.get('sendAmount', 100))
    ts_order.sendOverAmount = float(request.POST.get('sendAmount', 100))
    ts_order.receiveAmount = float(request.POST.get('receiveAmount', 100))
    ts_order.receiveOverAmount = 0
    ts_order.sendCurrency = CurrencyType.objects.get(tag=request.POST.get('sendCurrency', 'CNY'))
    ts_order.receiveCurrency = CurrencyType.objects.get(tag=request.POST.get('receiveCurrency', 'USD'))
    ts_order.exchangeRate = float(request.POST.get('roe', ''))
    ts_order.save()
    tasks.run_BMB.delay(ts_order.id)
    return HttpResponseRedirect(reverse(success))



@login_required
def success(request):
    return HttpResponse("Success")



@login_required
def get_all_platforms_balance(request):
    get_btc_balance_obj = BTCBalance()
    get_btc_balance_obj.get_all_platforms_balance()
    return HttpResponse("请到admin端查看")