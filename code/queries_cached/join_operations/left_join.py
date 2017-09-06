
# coding: utf-8

# # Left Join
# 
# In this exercise will be compare *join* function to do left join between ratings and users, and compare time to process dataset between Pandas and PyGDF




from pygdf.dataframe import DataFrame
import time
import pandas as pd
import logging
from IPython import display


USERS = '/home/ubuntu/pygdf/input_files/users.dat'
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

userHeader = ['user_id', 'age', 'ocupation', 'zip']

users = pd.read_table(USERS, engine='python', sep='::', header=None, names=userHeader)
df_users = DataFrame.from_pandas(users)
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
def left_join_pandas_1m():
    print('##########################')
    print('left_join_pandas_1m')
    joined = ratings_1m.join(users, how='left', lsuffix='_left', rsuffix='_right', sort=True)
    print('##########################')
    





@timing
def left_join_pandas_10m():
    print('##########################')
    print('left_join_pandas_10m')
    joined = ratings_10m.join(users, how='left', lsuffix='_left', rsuffix='_right', sort=True)
    print('##########################')





@timing
def left_join_pandas_20m():
    print('##########################')
    print('left_join_pandas_20m')
    joined = ratings_20m.join(users, how='left', lsuffix='_left', rsuffix='_right', sort=True)
    print('##########################')





@timing
def left_join_pygdf_1m():
    print('##########################')
    print('left_join_pygdf_1m')
    joined = df_ratings_1m.join(df_users, how='left', lsuffix='_left', rsuffix='_right', sort=True)
    print('##########################')





@timing
def left_join_pygdf_10m():
    print('##########################')
    print('left_join_pygdf_10m')
    joined = df_ratings_10m.join(df_users, how='left', lsuffix='_left', rsuffix='_right', sort=True)
    print('##########################')





@timing
def left_join_pygdf_20m():
    print('##########################')
    print('left_join_pygdf_20m')
    joined = df_ratings_20m.join(df_users, how='left', lsuffix='_left', rsuffix='_right', sort=True)
    print('##########################')





def iteration_1():
    left_join_pandas_1m()
    left_join_pandas_10m()
    left_join_pandas_20m()
    left_join_pygdf_1m()
    left_join_pygdf_10m()
    left_join_pygdf_20m()





def iteration_2():
    left_join_pandas_1m()
    left_join_pandas_10m()
    left_join_pandas_20m()
    left_join_pygdf_1m()
    left_join_pygdf_10m()
    left_join_pygdf_20m()





iteration_1()





iteration_2()







