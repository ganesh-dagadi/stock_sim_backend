import stock_sim_backend.database.main as db

def remove_holdings_duplicated(holdings):
    output = []
    for i in holdings:
        notPresent = True
        for every in output:
            if(i['ticker'] == every['ticker']):
                notPresent = False
        
        if(notPresent):
            output.append(i)
        else:
            continue
    return output


def get_one_holding(ticker , acc_id = 1):
    try:
        holdings = db.queryGet(f'SELECT * FROM acc_holding_transac INNER JOIN holdings ON acc_holding_transac.holding_id = holdings.holding_id WHERE acc_id = {acc_id};')
        holdings = remove_holdings_duplicated(holdings)
        for i in holdings:
            i.pop('stck_transac_id')
            i.pop('acc_transac_id')
        for i in holdings:
            if(i['ticker'] == ticker):
                return i
        return None
    
    except Exception as e:
        raise e

def get_all_holdings(acc_id = 1):
    try:
        holdings = db.queryGet(f'SELECT * FROM acc_holding_transac INNER JOIN holdings ON acc_holding_transac.holding_id = holdings.holding_id WHERE acc_id = {acc_id};')
        holdings = remove_holdings_duplicated(holdings)
        for i in holdings:
            i.pop('stck_transac_id')
            i.pop('acc_transac_id')
        for i in holdings:
            symbol = i['ticker']
            name = db.queryGet(f"SELECT stock_name FROM symbol_name WHERE symbol = '{symbol}'")
            i['stock_name'] = name[0]['stock_name']
        return holdings
    except Exception as e:
        raise e

def get_all_transactions(acc_id = 1):
    try:
       stock_transactions =  db.queryGet(f'SELECT * FROM acc_holding_transac INNER JOIN stock_transac ON acc_holding_transac.stck_transac_id = stock_transac.stck_transac_id WHERE acc_id = {acc_id} ORDER BY stock_transac.on_date desc, stock_transac.on_time desc')
       acc_transactions = db.queryGet(f'SELECT * FROM acc_holding_transac INNER JOIN acc_transac ON acc_holding_transac.acc_transac_id = acc_transac.acc_transac_id WHERE acc_id = {acc_id} ORDER BY acc_transac.on_date desc, acc_transac.at_time desc')
       return {'stck_transac' : stock_transactions , 'acc_transac' : acc_transactions}
    except Exception as e:
        raise e

def get_total_holding_value(acc_id = 1):
    try:
        holdings = db.queryGet(f'SELECT * FROM acc_holding_transac INNER JOIN holdings ON acc_holding_transac.holding_id = holdings.holding_id WHERE acc_id = {acc_id};')
        holdings = remove_holdings_duplicated(holdings)
        for i in holdings:
            i.pop('stck_transac_id')
            i.pop('acc_transac_id')
        total = 0
        for i in holdings:
            total += i['unit_price'] * i['qty']
        return float(total)
    except Exception as e:
        raise e

def get_account_info(acc_id = 1):
    try:
        account = db.queryGet(f'SELECT * FROM accounts WHERE acc_id = {acc_id}')
        return account[0]
    except Exception as e:
        raise e
