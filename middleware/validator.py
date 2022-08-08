import stock_sim_backend.database.main as db
import stock_sim_backend.error as err

def ticker_exists(ticker):
    try:
        data = db.queryGet("SELECT * FROM symbol_name WHERE symbol = '%s'" % (ticker))
        if(len(data) == 0):
            raise err.ValidationError("Ticker does not exist")
        return 
    except err.ValidationError as v_err:
        raise v_err
    except Exception as e:
        raise Exception("Internal error")

def acc_balance_sufficient(req_amount , acc_id):
    try:
        acc_info = db.queryGet(f'SELECT * FROM accounts WHERE acc_id = {acc_id}')[0]
        if(acc_info['balance'] < req_amount):
            raise err.BalanceError("Balance is insufficient")
        else:
            return
    except err.BalanceError as bal_e:
        raise bal_e
    except Exception as e:
        raise e

def can_sell(ticker , holdings , qty):
    try:
        foundHolding = {}
        HoldingExists = False
        for i in holdings:
            if(ticker == i['ticker']):
                foundHolding = i
                HoldingExists = True
        if(not HoldingExists):
            raise err.HoldingError('You dont have any stocks of that company')
        if(foundHolding['qty'] < qty):
            raise err.HoldingError('You dont have enough stocks to sell')
        return
    except err.HoldingError as hold_err:
        raise hold_err
    except Exception as e:
        raise e

    
