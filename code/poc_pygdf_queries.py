from pygdf.dataframe import DataFrame
import time
import pandas as pd
import logging

logging.basicConfig(filename='/home/ubuntu/pygdf/logs/poc_pygdf_queries.log', level=logging.INFO)

RATINGS = '/home/ubuntu/pygdf/input_files/ratings-1M.dat'


# RATINGS = '/home/ubuntu/pygdf/input_files/ratings-10M.dat'
# RATINGS = '/home/ubuntu/pygdf/input_files/ratings-20M.dat'
# RATINGS = '/home/ubuntu/pygdf/input_files/ratings-100M.dat'


def timing(f):
    def wrap(*args):
        time1 = time.time()
        ret = f(*args)
        time2 = time.time()
        diff_time = (time2 - time1) * 1000.0
        logging.info('=======================================================')
        logging.info(' %s tooks %s ms', f.__name__, diff_time)
        logging.info('=======================================================')
        return ret

    return wrap


@timing
def launch_query_1():
    logging.info('##########################')
    logging.info('launch_query_1')
    logging.info('##########################')
    result = df_ratings.query(
        'timestamp >= 788918400')


@timing
def launch_query_1B():
    logging.info('##########################')
    logging.info('launch_query_1B')
    logging.info('##########################')
    result = df_ratings.query(
        'timestamp >= 820454400')


@timing
def launch_query_2():
    logging.info('##########################')
    logging.info('launch_query_2')
    logging.info('##########################')
    result = df_ratings.query(
        'timestamp >= 788918400 or timestamp <= 852076799')


@timing
def launch_query_2B():
    logging.info('##########################')
    logging.info('launch_query_2B')
    logging.info('##########################')
    result = df_ratings.query(
        'timestamp >= 820454400 or timestamp <= 852076799')


@timing
def launch_query_3():
    logging.info('##########################')
    logging.info('launch_query_3')
    logging.info('##########################')
    result = df_ratings.query(
        '(timestamp >= 788918400 and timestamp <= 820454399) or  (timestamp >= 946684800 and timestamp <= 978307199)')


@timing
def launch_query_3B():
    logging.info('##########################')
    logging.info('launch_query_3B')
    logging.info('##########################')
    result = df_ratings.query(
        '(timestamp >= 820454400 and timestamp <= 852076799) or  (timestamp >= 978307200 and timestamp <= 1009843199)')


@timing
def launch_query_4():
    logging.info('##########################')
    logging.info('launch_query_4')
    logging.info('##########################')
    result = df_ratings.query(
        '(timestamp >= 788918400 and timestamp <= 820454399) or  (timestamp >= 946684800 and timestamp <= 978307199) or (timestamp >= 1104537600 and timestamp <= 1136073599)')


@timing
def launch_query_4B():
    logging.info('##########################')
    logging.info('launch_query_4B')
    logging.info('##########################')
    result = df_ratings.query(
        '(timestamp >= 820454400 and timestamp <= 852076799) or  (timestamp >= 978307200 and timestamp <= 1009843199) or (timestamp >= 1136073600 and timestamp <= 1167609599)')


@timing
def launch_query_5():
    logging.info('##########################')
    logging.info('launch_query_5')
    logging.info('##########################')
    result = df_ratings.query(
        '((timestamp >= 788918400 and timestamp <= 820454399) or  (timestamp >= 946684800 and timestamp <= 978307199) or (timestamp >= 1104537600 and timestamp <= 1136073599)) and (rating >=5)')


@timing
def launch_query_5B():
    logging.info('##########################')
    logging.info('launch_query_5B')
    logging.info('##########################')
    result = df_ratings.query(
        '((timestamp >= 820454400 and timestamp <= 852076799) or  (timestamp >= 978307200 and timestamp <= 1009843199) or (timestamp >= 1136073600 and timestamp <= 1167609599)) and (rating >=1)')


# =========
# LoadFiles
# =========
logging.info('loading data')
ratingHeader = ['user_id', 'movie_id', 'rating', 'timestamp']
ratings = pd.read_table(RATINGS, engine='python', sep='::', header=None, names=ratingHeader)
# ratings = pd.read_table(RATINGS, engine='python', sep=',', header=None, names=ratingHeader, skiprows=1)
df_ratings = DataFrame.from_pandas(ratings)

# ====================
# || LAUNCH QUERIES ||
# ====================
logging.info('launching queries')
launch_query_1()
launch_query_2()
launch_query_3()
launch_query_4()
launch_query_5()
launch_query_1B()
launch_query_2B()
launch_query_3B()
launch_query_4B()
launch_query_5B()

