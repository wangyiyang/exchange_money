# -*- coding: utf-8 -*-
import calls

# Constants
BUY_LIMIT_ORDER_TYPE_BUY = 0
BUY_LIMIT_ORDER_TYPE_SELL = 1

OPEN_ORDERS_TYPE_BUY = 0
OPEN_ORDERS_TYPE_SELL = 1

SELL_LIMIT_ORDER_TYPE_BUY = 0
SELL_LIMIT_ORDER_TYPE_SELL = 1

TRANSACTIONS_SORT_ASCENDING = 'asc'
TRANSACTIONS_SORT_DESCENDING = 'desc'

USER_TRANSACTIONS_SORT_ASCENDING = 'asc'
USER_TRANSACTIONS_SORT_DESCENDING = 'desc'

USER_TRANSACTIONS_TYPE_DEPOSIT = 0
USER_TRANSACTIONS_TYPE_WITHDRAWAL = 1
USER_TRANSACTIONS_TYPE_MARKET_TRADE = 2

WITHDRAWAL_REQUEST_TYPE_SEPA = 0
WITHDRAWAL_REQUEST_TYPE_BITCOIN = 1
WITHDRAWAL_REQUEST_TYPE_WIRE = 2
WITHDRAWAL_REQUEST_TYPE_BITSTAMP_CODE_1 = 3
WITHDRAWAL_REQUEST_TYPE_BITSTAMP_CODE_2 = 4
WITHDRAWAL_REQUEST_TYPE_MTGOX = 5

WITHDRAWAL_REQUEST_STATUS_OPEN = 0
WITHDRAWAL_REQUEST_STATUS_IN_PROCESS = 1
WITHDRAWAL_REQUEST_STATUS_FINISHED = 2
WITHDRAWAL_REQUEST_STATUS_CANCELLED = 3
WITHDRAWAL_REQUEST_STATUS_FAILED = 4


BITSTAMP_CLIENT_ID = ""
BITSTAMP_API_KEY = ""
BITSTAMP_API_SECRET = ""

# Wrapper functions
def account_balance(client_id=BITSTAMP_CLIENT_ID, api_key=BITSTAMP_API_KEY, api_secret=BITSTAMP_API_SECRET):
    return (
        calls.APIAccountBalanceCall(client_id, api_key, api_secret)
        .call()
    )


def bitcoin_deposit_address(client_id=BITSTAMP_CLIENT_ID, api_key=BITSTAMP_API_KEY, api_secret=BITSTAMP_API_SECRET):
    return (
        calls.APIBitcoinDepositAddressCall(client_id, api_key, api_secret)
        .call()
    )


def bitcoin_withdrawal(client_id, api_key, api_secret, amount, address):
    return (
        calls.APIBitcoinWithdrawalCall(client_id, api_key, api_secret)
        .call(amount=amount, address=address)
    )


def buy_limit_order(client_id=BITSTAMP_CLIENT_ID, api_key=BITSTAMP_API_KEY, api_secret=BITSTAMP_API_SECRET, amount=None, price=None):
    return (
        calls.APIBuyLimitOrderCall(client_id, api_key, api_secret)
        .call(amount=amount, price=price)
    )


def cancel_order(client_id, api_key, api_secret, order_id):
    return (
        calls.APICancelOrderCall(client_id, api_key, api_secret)
        .call(id=order_id)
    )


def check_bitstamp_code(client_id, api_key, api_secret, code):
    return (
        calls.APICheckBitstampCodeCall(client_id, api_key, api_secret)
        .call(code=code)
    )


def eur_usd_conversion_rate():
    return calls.APIEURUSDConversionRateCall().call()


def open_orders(client_id=BITSTAMP_CLIENT_ID, api_key=BITSTAMP_API_KEY, api_secret=BITSTAMP_API_SECRET):
    return (
        calls.APIOpenOrdersCall(client_id, api_key, api_secret)
        .call()
    )


def order_book(group=True):
    return calls.APIOrderBookCall().call(group='1' if group else '0')


def redeem_bitstamp_code(client_id, api_key, api_secret, code):
    return (
        calls.APIRedeemBitstampCodeCall(client_id, api_key, api_secret)
        .call(code=code)
    )


def ripple_deposit_address(client_id=BITSTAMP_CLIENT_ID, api_key=BITSTAMP_API_KEY, api_secret=BITSTAMP_API_SECRET):
    return (
        calls.APIRippleDepositAddressCall(client_id, api_key, api_secret)
        .call()
    )


def ripple_withdrawal(
        client_id, api_key, api_secret, amount, address, currency):
    return (
        calls.APIRippleWithdrawalCall(client_id, api_key, api_secret)
        .call()
    )


def sell_limit_order(client_id=BITSTAMP_CLIENT_ID, api_key=BITSTAMP_API_KEY, api_secret=BITSTAMP_API_SECRET, amount=None, price=None):
    return (
        calls.APISellLimitOrderCall(client_id, api_key, api_secret)
        .call(amount=amount, price=price)
    )


def ticker():
    return calls.APITickerCall().call()


def transactions(offset=0, limit=100, sort=TRANSACTIONS_SORT_DESCENDING):
    return calls.APITransactionsCall().call(
        offset=offset, limit=limit, sort=sort
    )


def unconfirmed_bitcoin_deposits(client_id=BITSTAMP_CLIENT_ID, api_key=BITSTAMP_API_KEY, api_secret=BITSTAMP_API_SECRET):
    return (
        calls.APIUnconfirmedBitcoinDepositsCall(client_id, api_key, api_secret)
        .call()
    )


def user_transactions(
        client_id, api_key, api_secret, offset=0, limit=100,
        sort=USER_TRANSACTIONS_SORT_DESCENDING):
    return (
        calls.APIUserTransactionsCall(client_id, api_key, api_secret)
        .call(offset=offset, limit=limit, sort=sort)
    )


def withdrawal_requests(client_id=BITSTAMP_CLIENT_ID, api_key=BITSTAMP_API_KEY, api_secret=BITSTAMP_API_SECRET):
    return (
        calls.APIWithdrawalRequestsCall(client_id, api_key, api_secret)
        .call()
    )


def get_bitstamp_market_amount_depth(bitcRes=None, ord_type=None, money=0):
    money = money
    try:
        results = order_book()
        results = results.get(ord_type)
        for ord in results:
            price = float(ord['price'])
            bitc = float(ord['amount'])
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


def get_bitstamp_market_value_depth(money=None):
    bitcRes = 0
    try:
        results = order_book()
        asks = results.get("asks")
        for ask in asks:
            price = float(ask['price'])
            bitc = float(ask['amount'])
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


def get_order_info(order_id):
    return (
        calls.APIUserOrderStatus(client_id=BITSTAMP_CLIENT_ID, api_key=BITSTAMP_API_KEY, api_secret=BITSTAMP_API_SECRET)
        .call(id=order_id)
    )
