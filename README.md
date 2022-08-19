<img 
    style="display: block; 
           margin-left: auto;
           margin-right: auto;
           width: 20%;"
    src="./banner_img.png" 
    alt="Our logo">
</img>
<h1 style="text-align: center;">Stock Sim</h1>

 Python based trading simulator to practice trading or test algorithms which perform algorithmic trading. 

 Get live prices and stock data of 4000+ tickers listed on the Bombay stock exchange to perform transactions on.


<br>

# Modules
 Stock sim windows client : <https://github.com/ganesh-dagadi/stock_sim_client>

 Stock sim backend module : <https://github.com/ganesh-dagadi/stock_sim_backend>

<hr>

# Backend Documentation

A python based backend which provides endpoint functions to perform database operations for Stock Sim Clients or trading algorithms. The backend uses postgresql as a database.

# Installation

## Prerequisities:

1. Python version 3.*
2. Postgresql 14 with a database called `stocksim` under `postgres` user

stock_sim_backend can be installed using `gdmm`. To install `gdmm` follow the instructions [here](https://github.com/ganesh-dagadi/gdmm). 

```
gdmm -c install -u ganesh-dagadi -r stock_sim_backend
```

to install locally, add `-l` flag

if you installed locally, navigate to the root of the directory.

if you installed globally, navigate to

 `C:\Users\<username\gdmm\modules\stock_sim_backend>`

create a `.env` file and write

```
    DATABASE_PASSWORD = your postgres user password
```

# Backend Setup
The backend requires a setup after you install it.

navigate to the root of the package and run 

```
gdmm -c setup
```
This will setup the package 

# API Endpoints

The following API endpoints can be used to interact with the backend.

The endpoints can be accessed as:

```
stock_sim_backend.endpoint_name(params)
```

## Stock info endpoints
The following endpoints can be used to get information on stocks.

1. **search_stocks(substr)**

    Fuzzy search endpoint that returns a list of stocks which match the `substr`

2. **get_live_price(ticker)**

    Gets the live price of a `ticker`. Ticker must be uppercase string

3. **get_historic_data(ticker , duration)**

    Returns a `pandas` series with historic prices of the given `dur` (duration)

    `ticker` must be uppercase `string`

    legal `dur` values: number of type `Integer` or string `'max'`  

## Transactions endpoints

The following endpoints can be used to perform transactions:

1. **add_amt_acc(amount)**

    Add the specified `amount` to the account
    `amount` must be `integer` or `float`

2. **buy_stock(ticker , qty)**

    Buy `ticker` of quantity `qty`.

    `ticker` must be uppercase `string` and qty `integer` 

3. **sell_stock(ticker , qty)**

    Sell `ticker` stock of `qty` quantity.

    `ticker` must be uppercase `string` and qty `integer`

## Account info endpoints

1. **get_one_holding(ticker)**

    Get data of a particular holding based on `ticker`

    `ticker` must be uppercase `string`.

2. **get_all_holdings()**

    Returns all the holdings of the current user

3. **get_all_transactions()**

    Returns all the transactions made.

    ```
    {
        acc_transac : list of all account transactions
        stck_transac : list of all stock transactions
    }
    ```

4. **get_total_holding_value()**

    Returns the total value of all holdings

5. **get_account_info()**

    Returns details on current account (balance, total amount added etc)



