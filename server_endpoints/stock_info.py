import yahoo_fin.stock_info as yf
import stock_sim_backend.database.main as db
import stock_sim_backend.middleware.validator as vd
import stock_sim_backend.error as err

def search_stocks(substr):  #Takes name of company and return its symbol with name
   try:
      substr = substr.upper()
      substr = '%%'+ substr + '%%'
      return db.queryGet("SELECT * FROM symbol_name WHERE name like '%s' "% (substr))
   except Exception as e:
      raise e

def get_live_price(ticker):
   try:
      vd.ticker_exists(ticker)
      return yf.get_live_price(ticker)
   except err.ValidationError as vdErr:
      raise vdErr

def get_historic_data(ticker , dur = 'max'):
   try:
      vd.ticker_exists(ticker)
      df = yf.get_data(ticker)
      df = df["close"]
      if((type(dur) == int and dur > len(df)) or (type(dur) != int and dur != 'max')):
         raise err.ValidationError("Invalid duration value")
      if(dur == 'max'):
         return df
      else:
         df = df.iloc[(len(df) - dur) : ]
         return df
   except err.ValidationError as vd_err:
      raise vd_err

   
