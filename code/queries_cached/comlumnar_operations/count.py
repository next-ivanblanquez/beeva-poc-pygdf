
# coding: utf-8

# # Count
# 
# In this exercise will be compare *count* function to count number of ratings there are, and compare time to process dataset between Pandas and PyGDF




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
def count_pandas_1m():
    print('##################')
    print('count_pandas_1m')
    print('Number of items in Data Frame is {}'.format(len(ratings_1m[ratings_1m.axes[1].values[0]])))
    print('##################')





@timing
def count_pandas_10m():
    print('##################')
    print('count_pandas_10m')
    print('Number of items in Data Frame is {}'.format(len(ratings_10m[ratings_10m.axes[1].values[0]])))
    print('##################')





@timing
def count_pandas_20m():
    print('##################')
    print('count_pandas_20m')
    print('Number of items in Data Frame is {}'.format(len(ratings_20m[ratings_20m.axes[1].values[0]])))
    print('##################')





@timing
def count_pygdf_1m():
    print('##################')
    print('count_pygdf_1m')
    print('Number of items in Data Frame is {}'.format(len(df_ratings_1m[df_ratings_1m.columns[0]])))
    print('##################')





@timing
def count_pygdf_10m():
    print('##################')
    print('count_pygdf_10m')
    print('Number of items in Data Frame is {}'.format(len(df_ratings_10m[df_ratings_10m.columns[0]])))
    print('##################')





@timing
def count_pygdf_20m():
    print('##################')
    print('count_pygdf_20m')
    print('Number of items in Data Frame is {}'.format(len(df_ratings_20m[df_ratings_20m.columns[0]])))
    print('##################')





def iteration_1():
    count_pandas_1m()
    count_pandas_10m()
    count_pandas_20m()
    count_pygdf_1m()
    count_pygdf_10m()
    count_pygdf_20m()





def iteration_2():
    count_pandas_1m()
    count_pandas_10m()
    count_pandas_20m()
    count_pygdf_1m()
    count_pygdf_10m()
    count_pygdf_20m()





iteration_1()





iteration_2()

