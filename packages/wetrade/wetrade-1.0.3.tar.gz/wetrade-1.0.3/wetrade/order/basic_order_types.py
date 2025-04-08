from wetrade.api import APIClient
from . import BaseOrder

class LimitOrder(BaseOrder):
  '''A limit order'''
  def __init__(self, client:APIClient, account_key, symbol, action, quantity, price, security_type='EQ'):
    self.order_type = 'LIMIT'
    BaseOrder.__init__(self, client, account_key, symbol, action, quantity, price, security_type)
    
class StopOrder(BaseOrder):
  '''A stop order'''
  def __init__(self, client:APIClient, account_key, symbol, action, quantity, price, security_type='EQ'):
    self.order_type = 'STOP'
    BaseOrder.__init__(self, client, account_key, symbol, action, quantity, price, security_type)
    
class MarketOrder(BaseOrder):
  '''A market order'''
  def __init__(self, client:APIClient, account_key, symbol, action, quantity, price=0.0, security_type='EQ'):
    self.order_type = 'MARKET'
    BaseOrder.__init__(self, client, account_key, symbol, action, quantity, price, security_type)
    
class StopLimitOrder(BaseOrder):
  '''A stop limit order'''
  def __init__(self, client:APIClient, account_key, symbol, action, quantity, price, security_type='EQ'):
    self.order_type = 'STOP_LIMIT'
    BaseOrder.__init__(self, client, account_key, symbol, action, quantity, price, security_type)