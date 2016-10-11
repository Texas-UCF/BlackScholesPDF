from scipy.misc import derivative
from BlackScholes import BlackScholesCallPrice
import numpy as np 
import pandas as pd 
from datetime import datetime 
from OptionsBase import OptionsDataFrame as odf
import datetime as dt 

def get_underlying(df):
	return list(set(df['underlying']))


def get_min_date(df):
	return min(df['date'])


def get_max_date(df):
	return max(df['date'])


def sample(ticker, df):
	copy_df = df[df['underlying'] == ticker]
	min_strike = min(copy_df['strike'])
	max_strike = max(copy_df['strike'])
	return np.linspace(min_strike, max_strike, 1000)


def get_mean(samples, function):
	return np.mean([function(s) for s in samples])


def get_std(samples, function):
	return np.std([function(s) for s in samples])


# decide where the 95% CI is 
# 4.721 is the k value for 95% confidence
def CI(ticker, df, function, confidence):
	samples = sample(ticker, df)
	mean = get_mean(samples, function)
	std = get_std(samples, function)
	k = (1 / np.sqrt(1 - confidence))
	return ((mean - k*std), (mean + k*std))	
	

def BS_probability(spot, sigma, tte):
	bs = BlackScholesCallPrice(spot, sigma, tte)
	return lambda x: derivative(bs, x, dx=0.1, n=2)


# if __name__ == '__main__':
	# df_interface = odf.OptionsDataFrame()
	# df = df_interface.fetch_data()
	# tickers = get_underlying(df)
	# min_date = get_min_date(df)
	# max_date = get_max_date(df)

	# for ticker in tickers:
	# 	samples = sample(ticker, df)
	# 	var = get_std(samples, function)
	# 	mean = get_mean(samples, function)
	# 	print (ticker, CI(mean, var, .95))


