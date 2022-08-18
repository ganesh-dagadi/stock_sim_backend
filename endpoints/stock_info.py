import yahoo_fin.stock_info as yf
from ..database import main as db
from ..middleware import validator as vd
from ..error import *

def search_stocks(substr):  #Takes name of company and return its symbol with name
   try:
      substr = substr.upper()
      substr = '%%'+ substr + '%%'
      return db.queryGet("SELECT * FROM symbol_name WHERE stock_name like '%s' "% (substr))
   except Exception as e:
      raise e

def get_live_price(ticker):
   try:
      vd.ticker_exists(ticker)
      return yf.get_live_price(ticker)
   except ValidationError as vdErr:
      raise vdErr

def get_historic_data(ticker , dur = 'max'):
   try:
      vd.ticker_exists(ticker)
      df = yf.get_data(ticker)
      df = df["close"]
      if((type(dur) == int and dur > len(df)) or (type(dur) != int and dur != 'max')):
         raise ValidationError("Invalid duration value")
      if(dur == 'max'):
         return df
      else:
         df = df.iloc[(len(df) - dur) : ]
         return df
   except ValidationError as vd_err:
      raise vd_err

   
