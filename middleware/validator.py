from ..database import main as db
from ..error import *  
def ticker_exists(ticker):
    try:
        data = db.queryGet("SELECT * FROM symbol_name WHERE symbol = '%s'" % (ticker))
        if(len(data) == 0):
            raise ValidationError("Ticker does not exist")
        return 
    except ValidationError as v_err:
        raise v_err
    except Exception as e:
        raise Exception("Internal error")

def acc_balance_sufficient(req_amount , acc_id):
    try:
        acc_info = db.queryGet(f'SELECT * FROM accounts WHERE acc_id = {acc_id}')[0]
        if(acc_info['balance'] < req_amount):
            raise BalanceError("Balance is insufficient")
        else:
            return
    except BalanceError as bal_e:
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
            raise HoldingError('You dont have any stocks of that company')
        if(foundHolding['qty'] < qty):
            raise HoldingError('You dont have enough stocks to sell')
        return
    except HoldingError as hold_err:
        raise hold_err
    except Exception as e:
        raise e

    
