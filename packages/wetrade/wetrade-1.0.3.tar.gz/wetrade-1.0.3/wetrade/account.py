import time
from wetrade.api import APIClient
from wetrade.utils import log_in_background

class Account:
  '''
  :param APIClient client: your :ref:`APIClient <api_client>`
  :param str account_key: (optional) manually specify your account key 
  '''
  def __init__(self, client:APIClient, account_key=''):
    self.client = client
    self.account_key = account_key if account_key else self.list_accounts()[0]['accountIdKey']

  def list_accounts(self):
    '''
    Provides details on all brokerage accounts connected to the active E-Trade user account
    '''
    response, status_code = self.client.request_account_list()
    try:
      accounts = response['AccountListResponse']['Accounts']['Account']
      return accounts
    except Exception as e:
      log_in_background(
        called_from = 'list_accounts',
        tags = ['user-message'], 
        message = time.strftime('%H:%M:%S', time.localtime()) + ': Error getting account list, retrying',
        e = e,
        account_key = self.account_key)
      return self.list_accounts()

  def check_balance(self):
    '''
    Returns the balance of your account
    '''
    response, status_code = self.client.request_account_balance(account_key=self.account_key)
    try:
      if 'accountBalance' in response['BalanceResponse']['Computed']:
        balance = response['BalanceResponse']['Computed']['accountBalance']
      else:
        balance = response['BalanceResponse']['Computed']['cashAvailableForInvestment']
      return balance
    except Exception as e:
      log_in_background(
        called_from = 'check_balance',
        tags = ['user-message'], 
        message = time.strftime('%H:%M:%S', time.localtime()) + ': Error getting account balance, retrying',
        e = e,
        account_key = self.account_key)
      return self.check_balance()

  def view_portfolio(self):
    '''
    Provides details for your account portfolio
    '''
    response, status_code = self.client.request_account_portfolio(account_key=self.account_key)
    try:
      portfolio = {} if status_code == 204 else response['PortfolioResponse']['AccountPortfolio']
      return portfolio
    except Exception as e:
      log_in_background(
        called_from = 'view_portfolio',
        tags = ['user-message'], 
        message = time.strftime('%H:%M:%S', time.localtime()) + ': Error getting portfolio, retrying',
        e = e,
        account_key = self.account_key)
      return self.view_portfolio()
    
  def get_order_history(self, start_date, end_date, marker=''):
    '''
    Provides details for all orders placed in account over specified time range
    '''
    response, status_code = self.client.request_account_orders(account_key=self.account_key, start_date=start_date, end_date=end_date, marker=marker)
    try:
      order_history = response['OrdersResponse']
      return order_history
    except Exception as e:
      log_in_background(
        called_from = 'get_order_history',
        tags = ['user-message'], 
        message = time.strftime('%H:%M:%S', time.localtime()) + ': Error getting account order history',
        e = e,
        account_key = self.account_key)
