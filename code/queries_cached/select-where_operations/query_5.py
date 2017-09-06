
# coding: utf-8

# # Query 5
# 
# In this exercise will be compare *query* function to do select-where like query over ratings there are, and compare time to process dataset between Pandas and PyGDF




from pygdf.dataframe import DataFrame
import time
import pandas as pd
import logging
from IPython import display

RATINGS_1M = '/home/ubuntu/pygdf/input_files/ratings-1M.dat'
RATINGS_10M = '/home/ubuntu/pygdf/input_files/ratings-10M.dat'
RATINGS_20M = '/home/ubuntu/pygdf/input_files/ratings-20M.dat'

# ===========
# Load Files
# ===========
print('============')
print('loading data')
print('============')
ratingHeader = ['user_id', 'movie_id', 'rating', 'timestamp']

ratings_1m = pd.read_table(RATINGS_1M, engine='python', sep='::', header=None, names=ratingHeader)
df_ratings_1m = DataFrame.from_pandas(ratings_1m)

ratings_10m = pd.read_table(RATINGS_10M, engine='python', sep='::', header=None, names=ratingHeader)
df_ratings_10m = DataFrame.from_pandas(ratings_10m)

ratings_20m = pd.read_table(RATINGS_20M, engine='python', sep='::', header=None, names=ratingHeader)
df_ratings_20m = DataFrame.from_pandas(ratings_20m)
print('============')
print('data lodaded')
print('============')





def timing(f):
    def wrap(*args):
        time1 = time.time()
        ret = f(*args)
        time2 = time.time()
        diff_time = (time2 - time1) * 1000.0
        print('=======================================================')
        print('{} tooks {:.2f} ms'.format(f.__name__, diff_time))
        print('=======================================================')
        return ret

    return wrap





@timing
def query_pandas_1m():
    print('##########################')
    print('query_pandas_1m')
    result = ratings_1m.query('((timestamp >= 788918400 and timestamp <= 820454399) or  (timestamp >= 946684800 and timestamp <= 978307199) or (timestamp >= 1104537600 and timestamp <= 1136073599)) and (rating >=5)')
    print('##########################')
    





@timing
def query_pandas_1m_b():
    print('##########################')
    print('query_pandas_1m_b')
    result = ratings_1m.query('((timestamp >= 820454400 and timestamp <= 852076799) or  (timestamp >= 978307200 and timestamp <= 1009843199) or (timestamp >= 1136073600 and timestamp <= 1167609599)) and (rating >=1)')
    print('##########################')





@timing
def query_pandas_10m():
    print('##########################')
    print('query_pandas_10m')
    result = ratings_10m.query('((timestamp >= 788918400 and timestamp <= 820454399) or  (timestamp >= 946684800 and timestamp <= 978307199) or (timestamp >= 1104537600 and timestamp <= 1136073599)) and (rating >=5)')
    print('##########################')
    





@timing
def query_pandas_10m_b():
    print('##########################')
    print('query_pandas_10m_b')
    result = ratings_10m.query('((timestamp >= 820454400 and timestamp <= 852076799) or  (timestamp >= 978307200 and timestamp <= 1009843199) or (timestamp >= 1136073600 and timestamp <= 1167609599)) and (rating >=1)')
    print('##########################')





@timing
def query_pandas_20m():
    print('##########################')
    print('query_pandas_20m')
    result = ratings_20m.query('((timestamp >= 788918400 and timestamp <= 820454399) or  (timestamp >= 946684800 and timestamp <= 978307199) or (timestamp >= 1104537600 and timestamp <= 1136073599)) and (rating >=5)')
    print('##########################')





@timing
def query_pandas_20m_b():
    print('##########################')
    print('query_pandas_20m_b')
    result = ratings_20m.query('((timestamp >= 820454400 and timestamp <= 852076799) or  (timestamp >= 978307200 and timestamp <= 1009843199) or (timestamp >= 1136073600 and timestamp <= 1167609599)) and (rating >=1)')
    print('##########################')





@timing
def query_pygdf_1m():
    print('##########################')
    print('query_pygdf_1m')
    result = df_ratings_1m.query('((timestamp >= 788918400 and timestamp <= 820454399) or  (timestamp >= 946684800 and timestamp <= 978307199) or (timestamp >= 1104537600 and timestamp <= 1136073599)) and (rating >=5)')
    print('##########################')





@timing
def query_pygdf_1m_b():
    print('##########################')
    print('query_pygdf_1m_b')
    result = df_ratings_1m.query('((timestamp >= 820454400 and timestamp <= 852076799) or  (timestamp >= 978307200 and timestamp <= 1009843199) or (timestamp >= 1136073600 and timestamp <= 1167609599)) and (rating >=1)')
    print('##########################')





@timing
def query_pygdf_10m():
    print('##########################')
    print('query_pygdf_10m')
    result = df_ratings_10m.query('((timestamp >= 788918400 and timestamp <= 820454399) or  (timestamp >= 946684800 and timestamp <= 978307199) or (timestamp >= 1104537600 and timestamp <= 1136073599)) and (rating >=5)')
    print('##########################')





@timing
def query_pygdf_10m_b():
    print('##########################')
    print('query_pygdf_10m_b')
    result = df_ratings_10m.query('((timestamp >= 820454400 and timestamp <= 852076799) or  (timestamp >= 978307200 and timestamp <= 1009843199) or (timestamp >= 1136073600 and timestamp <= 1167609599)) and (rating >=1)')
    print('##########################')





@timing
def query_pygdf_20m():
    print('##########################')
    print('query_pygdf_20m')
    result = df_ratings_20m.query('((timestamp >= 788918400 and timestamp <= 820454399) or  (timestamp >= 946684800 and timestamp <= 978307199) or (timestamp >= 1104537600 and timestamp <= 1136073599)) and (rating >=5)')
    print('##########################')





@timing
def query_pygdf_20m_b():
    print('##########################')
    print('query_pygdf_20m_b')
    result = df_ratings_20m.query('((timestamp >= 820454400 and timestamp <= 852076799) or  (timestamp >= 978307200 and timestamp <= 1009843199) or (timestamp >= 1136073600 and timestamp <= 1167609599)) and (rating >=1)')
    print('##########################')





def iteration_1():
    query_pandas_1m()
    query_pandas_1m_b()
    query_pandas_10m()
    query_pandas_10m_b()
    query_pandas_20m()
    query_pandas_20m_b()
    query_pygdf_1m()
    query_pygdf_1m_b()
    query_pygdf_10m()
    query_pygdf_10m_b()
    query_pygdf_20m()
    query_pygdf_20m_b()





def iteration_2():
    query_pandas_1m()
    query_pandas_1m_b()
    query_pandas_10m()
    query_pandas_10m_b()
    query_pandas_20m()
    query_pandas_20m_b()
    query_pygdf_1m()
    query_pygdf_1m_b()
    query_pygdf_10m()
    query_pygdf_10m_b()
    query_pygdf_20m()
    query_pygdf_20m_b()





iteration_1()





iteration_2()







