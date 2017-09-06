
# coding: utf-8

# # Mean
# 
# In this exercise will be compare *mean* function obtain the average value of each column in ratings, and compare time to process dataset between Pandas and PyGDF




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
def mean_pandas_1m():
    print('##################')
    print('mean_pandas_1m')
    for k in ratings_1m.columns:
        print('Mean of {} is {}'.format(k, ratings_1m[k].values.mean()))
    print('##################')





@timing
def mean_pandas_10m():
    print('##################')
    print('mean_pandas_10m')
    for k in ratings_10m.columns:
        print('Mean of {} is {}'.format(k, ratings_10m[k].values.mean()))
    print('##################')





@timing
def mean_pandas_20m():
    print('##################')
    print('mean_pandas_20m')
    for k in ratings_20m.columns:
        print('Mean of {} is {}'.format(k, ratings_20m[k].values.mean()))
    print('##################')





@timing
def mean_pygdf_1m():
    print('##################')
    print('mean_pygdf_1m')
    for k in df_ratings_1m.columns:
        print('Mean of {} is {}'.format(k, df_ratings_1m[k].mean()))
    print('##################')





@timing
def mean_pygdf_10m():
    print('##################')
    print('mean_pygdf_10m')
    for k in df_ratings_10m.columns:
        print('Mean of {} is {}'.format(k, df_ratings_10m[k].mean()))
    print('##################')





@timing
def mean_pygdf_20m():
    print('##################')
    print('mean_pygdf_20m')
    for k in df_ratings_20m.columns:
        print('Mean of {} is {}'.format(k, df_ratings_20m[k].mean()))
    print('##################')





def iteration_1():
    mean_pandas_1m()
    mean_pandas_10m()
    mean_pandas_20m()
    mean_pygdf_1m()
    mean_pygdf_10m()
    mean_pygdf_20m()





def iteration_2():
    mean_pandas_1m()
    mean_pandas_10m()
    mean_pandas_20m()
    mean_pygdf_1m()
    mean_pygdf_10m()
    mean_pygdf_20m()





iteration_1()





iteration_2()







