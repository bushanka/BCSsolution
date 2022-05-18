from django.shortcuts import render
from .models import TransactionsInfo
import requests
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
import json
from django.conf import settings


def send_transaction():

    MY_ADDRESS = 'BALZtbwGpa95fePEAE3HNYf7iPkSNbPkKf'
    PRIVATE = settings.PRIVATE_KEY

    END_POINT = 'https://bcschain.info/api/'

    AMOUNT_SEND = 1
    FEE = round(100000 / 10 ** 8, 8)

    rpc_connection = AuthServiceProxy("http://bcs_tester:iLoveBCS@45.32.232.25:3669/")

    try:
        r = requests.get(END_POINT + 'address/' + MY_ADDRESS)
        if r.status_code == 200:
            my_address_info = json.loads(r.text)
            balance = float(my_address_info['balance'])
        else:
            print(f'Connection error: {r.status_code}')
            return None
    except requests.exceptions.ConnectionError as error:
        print(f'Connection error: {error}')
        return None

    try:
        r = requests.get(END_POINT + 'address/' + MY_ADDRESS + '/utxo')
        if r.status_code == 200:
            utxo_data = json.loads(r.text)
            vout = utxo_data[0]['outputIndex']
            tx = utxo_data[0]['transactionId']
        else:
            print(f'Connection error: {r.status_code}')
            return None
    except requests.exceptions.ConnectionError as error:
        print(f'Connection error: {error}')
        return None

    balance_after_send_one = round(balance - AMOUNT_SEND - FEE, 8)

    try:
        new_address = rpc_connection.getnewaddress()
        create_transaction = rpc_connection.createrawtransaction([{'txid': tx, 'vout': vout}],
                                                                 {new_address: AMOUNT_SEND,
                                                                  MY_ADDRESS: balance_after_send_one})
        sign_transaction = rpc_connection.signrawtransactionwithkey(create_transaction, [PRIVATE])
        print(sign_transaction)
        try:
            send_trans = rpc_connection.sendrawtransaction(sign_transaction['hex'])
        except JSONRPCException as error:
            print(error)
            return None
    except TimeoutError:
        print(f'Failed to connect to rpc node: {TimeoutError}')
        return None

    return send_trans


def index(request):
    if request.method == 'POST':
        txid = send_transaction()
        if txid is not None:
            transaction = TransactionsInfo(Txid=txid)
            transaction.save()
        else:
            print('FAILED TO SEND TRANSACTION')  # TODO Create popup?
        # messages.info(request, 'Your transaction has been sent successfully!')

    tx_ids = TransactionsInfo.objects.all()
    all_txs_info = []
    for tx in tx_ids:
        txs_info = {
            'txid': tx.Txid,
            'description': tx.Description
        }
        all_txs_info.append(txs_info)

    context = {'all_tx_info': all_txs_info}

    return render(request, 'txApp/index.html', context)


def index_description(request, pk):
    tx = TransactionsInfo.objects.get(Txid=pk)
    txs_info = {
        'txid': tx.Txid,
        'description': tx.Description
    }
    context = {
        'info': txs_info
    }
    return render(request, 'txApp/index_description.html', context)
