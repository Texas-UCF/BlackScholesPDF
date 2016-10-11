from __future__ import division 
from scipy import polyfit
import numpy as np 
import pandas as pd
from OptionsBase import OptionsDataFrame as odf
from BlackScholes import BlackScholesCallPrice
import datetime as dt 
import matplotlib.pyplot as plt
from UnderlyingProbability import BS_probability

options_df = odf.OptionsDataFrame().fetch_data()
options_df = options_df[pd.notnull(options_df['expdt'])]
options_df = options_df[pd.notnull(options_df['call_close'])]

# Returns a function sigma(x) that outputs volatility for any given strikesigma, pdf
def fit_pdf(ticker, date): 
	filter_df = options_df[options_df['underlying'] == ticker]
	filter_df = filter_df[filter_df['date'] == date]
	filter_df = filter_df[filter_df['expdt'] == min(filter_df['expdt'])]


	# filter_df = filter_df[(filter_df['expdt'] > date + dt.timedelta(days=min_bound)) &	(filter_df['expdt'] < date + dt.timedelta(days=max_bound))]
	call_close = [float(call_close) for call_close in filter_df['call_close']]
	strikes = list(filter_df['strike'])
	spots = list(filter_df['PX_LAST'])
	tte = [(delta / np.timedelta64(1, 'D')).astype(int) / 252 for delta in (filter_df['expdt'] - filter_df['date'])]
	vols = [newton_raphson_bs(spots[i], strikes[i], tte[i], call_close[i]) for i in range(len(call_close))]
	sigma = vol_polynomial(strikes, vols)
	bs = BlackScholesCallPrice(spots[0], sigma, tte[0])
	pdf = BS_probability(spots[0], sigma, tte[0])
	return sigma, bs, pdf 


# Gets the point value of volatility using the black-scholes formula
def newton_raphson_bs(spot, strike, tte, answer, initial_vol=0.3, step=.001, thresh=.01, max_iterations=5000):
	vol_func = lambda strike: initial_vol
	bs = BlackScholesCallPrice(spot, vol_func, tte)
	x = initial_vol
	y = bs(strike)
	count = 0 
	while abs(answer - y) > thresh and count < max_iterations:
		print x, y, answer 
		count += 1 
		x = (x+step) if y < answer else (x-step)
		vol_func = lambda strike: x 
		bs.set_vol_fun(vol_func)
		y = bs(strike)
	return x

# Fits a polynomial regression to the vol curve 
def vol_polynomial(strikes, implied_vols): 
	weights = polyfit(strikes, implied_vols, 4)
	p = np.poly1d(weights)
	return p 

def get_min_strike(ticker):
	return min(options_df[options_df['underlying'] == ticker]['strike'])

def get_max_strike(ticker):
	return max(options_df[options_df['underlying'] == ticker]['strike'])

if __name__ == '__main__':
	sigma, bs, pdf = fit_pdf('AMZN', min(options_df['date']))
	xp = np.linspace(get_min_strike('AMZN'), get_max_strike('AMZN'), 100)
	# plt.plot(xp, sigma(xp))
	# plt.plot(xp, bs(xp))
	plt.plot(xp, pdf(xp))

	plt.ylabel('p(x)')
	plt.xlabel('Strike')
	plt.title('AMZN Strike vs. p(x)')
	plt.show()