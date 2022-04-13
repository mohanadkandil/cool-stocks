from .. import adapters

def retryTransaction(transaction):
    stocks = adapters.dbAdapter.sendRequest(payload={}, queryParams={ 'stock_id': transaction['stock_id'] }, method='get', url='stock/')
    if not stocks:
        # notify user stock if no longer available
        return
    transaction['transaction_success'] = True
    transaction['transaction_pending'] = False
    transaction['price_per_stock'] = stocks[0]['price']
    if transaction['upper_bound'] < stocks[0]['price'] or transaction['lower_bound'] > stocks[0]['price']:
        transaction['transaction_success'] = False
    updated_transaction = adapters.dbAdapter.sendRequest(payload={**transaction}, queryParams={}, method='put', url='transaction/')
    # ... notify user either transaction success/failure for second transaction attempt


def resetTimers():
    try:
        print('processing any pending transactions')
        transactions = adapters.dbAdapter.sendRequest(
            payload={},
            queryParams={'transaction_pending': True,
            'transaction_success': False},
            method='get',
            url='transaction/pending'
        )
        for transaction in transactions:
            retryTransaction(transaction)
        print(f'Done with processing pending transactions, {len(transactions)}')
    except Exception as err:    
        print('timers failed to reset ...', err)
