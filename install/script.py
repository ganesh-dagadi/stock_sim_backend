import sys
database_password = sys.argv[1]
import os

import psycopg2 as pg
import pandas as pd
try:
    conn = pg.connect(
        dbname="stocksim", password=database_password, user="postgres", host="localhost"
    )
    cur = conn.cursor()
    
    cur.execute(
        '''
            CREATE TABLE acc_transac(
                acc_transac_id SERIAL PRIMARY KEY,
                amount NUMERIC,
                on_date DATE DEFAULT CURRENT_DATE,
                at_time TIME WITH TIME ZONE DEFAULT CURRENT_TIME
            );

            CREATE TABLE accounts(
                acc_id SERIAL PRIMARY KEY,
                total_income NUMERIC DEFAULT 0,
                balance NUMERIC DEFAULT 0
            );

            CREATE TABLE holdings(
                holding_id SERIAL PRIMARY KEY,
                ticker varchar(20) NOT NULL,
                qty INTEGER,
                unit_price NUMERIC
            );

            CREATE TABLE stock_transac(
                stck_transac_id SERIAL PRIMARY KEY,
                trans_type varchar(5) NOT NULL,
                on_ticker varchar(20) NOT NULL,
                unit_price NUMERIC,
                qty INTEGER,
                profit NUMERIC, 
                on_date DATE DEFAULT CURRENT_DATE,
                on_time TIME WITH TIME ZONE DEFAULT CURRENT_TIME
            );

             CREATE TABLE acc_holding_transac(
                _id SERIAL PRIMARY KEY,
                acc_id INT NOT NULL
                REFERENCES accounts(acc_id)
                ON DELETE CASCADE,
                holding_id INT
                REFERENCES holdings(holding_id)
                ON DELETE CASCADE,
                stck_transac_id INT
                REFERENCES stock_transac(stck_transac_id)
                ON DELETE CASCADE,
                acc_transac_id INT  REFERENCES acc_transac(acc_transac_id)
                ON DELETE CASCADE
            );

            CREATE TABLE symbol_name(
                symbol varchar(200) PRIMARY KEY,
                stock_name TEXT NOT NULL
            );

            INSERT INTO accounts(balance) VALUES (0);
        '''
    )
    conn.commit()
    cur.close()
    conn.close()

    
    df = pd.read_csv('./install/Equity.csv')
    df2 = df[['Security Id' , 'Issuer Name']].copy()
    df2 = df2.rename(columns = {'Security Id' : 'stock_name' , 'Issuer Name' : 'symbol'})
    conn = pg.connect(
        dbname="stocksim", password=database_password, user="postgres", host="localhost"
    )
    cur = conn.cursor()
    for i in df2.index:
        name = df2["stock_name"][i]
        if(type(name) != str):
            continue
        name = name.upper()
        symbol = df2['symbol'][i] + '.BO'
        cur.execute("INSERT INTO symbol_name(symbol , stock_name) VALUES (%(symbol)s , %(name)s)", {'symbol':symbol , 'name' : name})
        conn.commit()
    cur.close()
    conn.close()
    os.remove('./install/Equity.csv')
    exit(code=0)
except Exception as e:
    print(e)
    exit(code=1)