from __future__ import division
import numpy as np
from scipy.stats import norm

class BlackScholesCallPrice(object):


  def __init__(self, spot_price, vol_fun, tenor, risk_free_rate=0.0173, dividend=0):
    self._spot_price = spot_price
    self._vol_fun = vol_fun
    self._risk_free_rate = risk_free_rate
    self._tenor = tenor
    self._dividend = dividend


  @property
  def spot_price(self):
    return self._spot_price


  @property
  def vol_fun(self):
    return self._vol_fun


  @property
  def risk_free_rate(self):
    return self._risk_free_rate


  @property
  def tenor(self):
    return self._tenor


  @property
  def dividend(self):
    return self._dividend

  
  def set_spot_price(self, spot):
    self._spot_price = spot 


  def set_vol_fun(self, vol):
    self._vol_fun = vol


  def set_risk_free_rate(self, r):
    self._risk_free_rate = r


  def set_tenor(self, tenor):
    self._tenor = tenor


  def set_dividend(self, dividend):
    self._dividend = dividend


  def __call__(self, strike):
    vol = self._vol_fun(strike) 
    t1 = np.log(self._spot_price/strike)
    t2 = (self._risk_free_rate + .5*vol**2)*self._tenor
    t3 = (self._risk_free_rate - .5*vol**2)*self._tenor
    t4 = vol * np.sqrt(self._tenor)

    d1 = (t1 + t2)/t4
    d2 = (t1 + t3)/t4

    discount = np.exp(-self._risk_free_rate * self._tenor)
    price = self._spot_price * norm.cdf(d1) - strike * discount * norm.cdf(d2)
    return price 
