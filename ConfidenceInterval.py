import numpy as np 
import pandas as pd 
from datetime import datetime 
from OptionsBase import OptionsDataFrame as odf
import datetime as dt 

def get_underlying(df):
	return list(set(df['underlying']))

def get_min_date(df):
	return min(list(set(df['date'])))

def get_max_date(df):
	return max(list(set(df['date'])))

def sample(ticker, df):
	copy_df = df
	copy_df = copy_df[copy_df['underlying'] == ticker]
	min_strike = min(list(set(copy_df['strike'])))
	max_strike = max(list(set(copy_df['strike'])))

	samples = np.linspace(min_strike, max_strike, 1000)
	return samples

def get_std(samples, function):
	points = []
	for sample in samples:
		points.append((sample, function(sample)))
	return np.std(points)

def get_mean(samples, function):
	points = []
	for sample in samples:
		points.append((sample, function(sample)))
	return np.mean(points)


# decide where the 95% CI is 
# 4.721 is the k value for 95% confidence
def CI(mean, std, confidence):
	k = (1 / np.sqrt(1 - confidence))
	return ((mean - k*std), (mean + k*std))	


def function(x):
	return x

if __name__ == '__main__':
	df_interface = odf.OptionsDataFrame()
	df = df_interface.fetch_data()
	tickers = get_underlying(df)
	min_date = get_min_date(df)
	max_date = get_max_date(df)

	for ticker in tickers:
		samples = sample(ticker, df)
		var = get_std(samples, function)
		mean = get_mean(samples, function)
		print (ticker, CI(mean,var))


