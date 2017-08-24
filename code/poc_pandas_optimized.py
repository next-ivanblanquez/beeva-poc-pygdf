import time
import pandas as pd
import logging

logging.basicConfig(filename='/home/ubuntu/pygdf/logs/poc_pandas_optimized.log', level=logging.INFO)

RATINGS = '/home/ubuntu/pygdf/input_files/ratings-1M.dat'
#RATINGS = '/home/ubuntu/pygdf/input_files/ratings-10M.dat'
#RATINGS = '/home/ubuntu/pygdf/input_files/ratings-20M.dat'
#RATINGS = '/home/ubuntu/pygdf/input_files/ratings-100M.dat'


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
def launch_max():
    logging.info('##################')
    logging.info('launch_max')
    logging.info('##################')
    result = ratings
    for k in result.columns:
        logging.info('Max of %s is %s', k, result[k].values.max())


@timing
def launch_min():
    logging.info('##################')
    logging.info('launch_min')
    logging.info('##################')
    result = ratings
    for k in result.columns:
        logging.info('Min of %s is %s', k, result[k].values.min())


@timing
def launch_mean():
    logging.info('##################')
    logging.info('launch_mean')
    logging.info('##################')
    result = ratings
    for k in result.columns:
        logging.info('Mean of %s is %s', k, result[k].values.mean())


@timing
def launch_std():
    logging.info('################')
    logging.info('launch_std')
    logging.info('################')
    result = ratings
    for k in result.columns:
        logging.info('STD of %s is %s', k, result[k].values.std())


# =========
# LoadFiles
# =========
logging.info('loading data')
ratingHeader = ['user_id', 'movie_id', 'rating', 'timestamp']
ratings = pd.read_table(RATINGS, engine='python', sep='::', header=None, names=ratingHeader)
# ratings = pd.read_table(RATINGS, engine='python', sep=',', header=None, names=ratingHeader, skiprows=1)


# ====================
# || LAUNCH QUERIES ||
# ====================
logging.info('launching queries')
launch_max()
launch_min()
launch_mean()
launch_std()
