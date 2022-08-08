import stock_sim_backend.database.main as db
import stock_sim_backend.middleware.validator as vd
import stock_sim_backend.server_endpoints.stock_info as si


def add_amt_acc(amount , acc_id = 3): #Only one account in V1
    try:
        # Check if account exists Done in V2
        db.querySet('''
             UPDATE accounts SET balance = balance + {amount} , total_income = total_income + {amount} WHERE acc_id = {acc_id};
             WITH rows AS(INSERT INTO acc_transac(amount) VALUES(%s) RETURNING acc_transac_id)
             INSERT INTO acc_holding_transac(acc_transac_id , acc_id) SELECT acc_transac_id , {acc_id} FROM rows 
        '''.format(amount = amount,
                   acc_id = acc_id
        ) , values=[amount])
        return f"{amount} added to account"
    except Exception as e:
        raise e

def buy_stock(ticker , qty , acc_id = 3):
    try:
        #Check if account exists in V2
        vd.ticker_exists(ticker)
        unit_price = si.get_live_price(ticker)
        total = unit_price * qty
        #Check if balance exists
        vd.acc_balance_sufficient(total , acc_id)
        #Get all holdings of current account
        holdings = db.queryGet(f'SELECT * FROM acc_holding_transac INNER JOIN holdings ON acc_holding_transac.holding_id = holdings.holding_id WHERE acc_holding_transac.acc_id = {acc_id} AND acc_holding_transac.holding_id IS NOT NULL ')
        holdingExists = False
        foundTicker = {}
        for i in holdings:
            if(ticker == i['ticker']):
                holdingExists = True
                foundTicker = i

        if(holdingExists):
           hold_qty = foundTicker['qty']
           hold_price = foundTicker['unit_price']
           holding_id = foundTicker['holding_id']
           hold_total = hold_qty * hold_price
           avg_unit_price = (float(hold_total) + total) / (hold_qty + qty)
           db.querySet(
            '''
            UPDATE accounts SET balance = balance - {total} WHERE acc_id = {acc_id};
            WITH row1 AS (
                    INSERT INTO stock_transac(trans_type , on_ticker , unit_price , qty) VALUES ('BUY' , %(ticker)s, %(unit_price)s , %(qty)s ) RETURNING stck_transac_id
                )
                INSERT INTO acc_holding_transac(stck_transac_id, holding_id , acc_id)
                SELECT  stck_transac_id , {holding_id} , {acc_id}
                FROM row1;
             UPDATE holdings SET unit_price = {avg_unit_price}, qty = {total_qty} WHERE holding_id = {holding_id}
                '''.format(
                    total = total,
                    acc_id = acc_id,
                    avg_unit_price = avg_unit_price,
                    total_qty = qty + hold_qty,
                    holding_id = holding_id
                    ),
                    values={'ticker' : ticker ,'unit_price' : unit_price , 'qty' : qty}
           )
           
           return "Stocks brought"
        else:
            #Fresh buy
            db.querySet(
                '''
                UPDATE accounts SET balance = balance - {total} WHERE acc_id = {acc_id};
                WITH row1 AS (
                    INSERT INTO stock_transac(trans_type , on_ticker , unit_price , qty) VALUES ('BUY' , %(ticker)s, %(unit_price)s , %(qty)s ) RETURNING stck_transac_id
                ), row2 AS (
                    INSERT INTO holdings(ticker , qty , unit_price) VALUES (%(ticker)s , %(qty)s , %(unit_price)s) RETURNING holding_id
                )
                INSERT INTO acc_holding_transac(holding_id , stck_transac_id , acc_id)
                SELECT holding_id , stck_transac_id , {acc_id}
                FROM row1 CROSS JOIN row2;
                '''.format(
                    total = total,
                    acc_id = acc_id
                    ),
                    values={'ticker' : ticker ,'unit_price' : unit_price , 'qty' : qty }
            )
            return 'Stocks brought'
    except Exception as e:
        raise e

def sell_stock(ticker , qty , acc_id = 3):
    try:
        vd.ticker_exists(ticker)
        holdings = db.queryGet(f'SELECT * FROM acc_holding_transac INNER JOIN holdings ON acc_holding_transac.holding_id = holdings.holding_id WHERE acc_holding_transac.acc_id = {acc_id} AND acc_holding_transac.holding_id IS NOT NULL ')
        vd.can_sell(ticker , holdings , qty)
        curr_price = si.get_live_price(ticker)
        onHolding = {}
        for i in holdings:
            if(ticker == i['ticker']):
                onHolding = i
        profit_loss = (curr_price - float(onHolding['unit_price'])) * qty
        holding_id = onHolding['holding_id']

        db.querySet('''
            WITH stck_row AS(INSERT INTO stock_transac(trans_type , on_ticker , unit_price , qty , profit) VALUES ('SELL', %(ticker)s , %(curr_price)s , %(qty)s , %(profit)s ) RETURNING stck_transac_id)
            INSERT INTO acc_holding_transac(stck_transac_id , holding_id , acc_id)
            SELECT stck_transac_id , {holding_id} , {acc_id} 
            FROM stck_row;
            UPDATE holdings SET qty = {remaining_qty} WHERE holding_id = {holding_id};
            UPDATE accounts SET balance = balance + {total_transac_val} WHERE acc_id = {acc_id};

        '''.format(
            holding_id = holding_id,
            acc_id = acc_id,
            remaining_qty = float(onHolding['qty']) - qty,
            total_transac_val = curr_price * qty
        ),
        values = {'ticker': ticker , 'curr_price' : curr_price , 'qty' : qty , 'profit' : profit_loss }
        ) 

        return "Stocks sold"

    except Exception as e:
        raise e

