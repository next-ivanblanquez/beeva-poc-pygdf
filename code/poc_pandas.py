import time
import pandas as pd
import logging

logging.basicConfig(filename='/home/ubuntu/pygdf/logs/poc_pandas.log', level=logging.INFO)

USERS = '/home/ubuntu/pygdf/input_files/users.dat'
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
	logging.info(' %s tooks %.2f ms', f.__name__, diff_time)
        logging.info('=======================================================')
        return ret

    return wrap


@timing
def launch_count():
    logging.info('##################')
    logging.info('launch_count')
    logging.info('##################')
    logging.info('Number of items in Data Frame is %s', len(ratings[ratings.axes[1].values[0]]))


@timing
def launch_max():
    logging.info('##################')
    logging.info('launch_max')
    logging.info('##################')
    # result = df.query('user_id==1')
    result = ratings
    for k in result.columns:
        logging.info('Max of %s is %s', k, result[k].max())


@timing
def launch_min():
    logging.info('##################')
    logging.info('launch_min')
    logging.info('##################')
    # result = df.query('user_id==1')
    result = ratings
    for k in result.columns:
        logging.info('Min of %s is %s', k, result[k].min())


@timing
def launch_mean():
    logging.info('##################')
    logging.info('launch_mean')
    logging.info('##################')
    # result = df.query('user_id==1')
    result = ratings
    for k in result.columns:
        logging.info('Mean of %s is %s', k, result[k].mean())


@timing
def launch_std():
    logging.info('################')
    logging.info('launch_std')
    logging.info('################')
    # result = df.query('user_id==1')
    result = ratings
    for k in result.columns:
        logging.info('STD of %s is %s', k, result[k].std())


@timing
def launch_query_best_movies():
    logging.info('##########################')
    logging.info('launch_query_best_movies')
    logging.info('##########################')
    # result = ratings.query('(user_id > 9 and user_id < 21)')
    result = ratings.query(
        '((timestamp >= 788918400 and timestamp <= 820454399) or  (timestamp >= 946684800 and timestamp <= 978307199) or (timestamp >= 1104537600 and timestamp <= 1136073599)) and (rating >=5)')
    # print(result[:10])


@timing
def launch_query_worst_movies():
    logging.info('##########################')
    logging.info('launch_query_worst_movies')
    logging.info('##########################')
    # result = ratings.query('(user_id > 9 and user_id < 21)')
    result = ratings.query(
        '((timestamp >= 788918400 and timestamp <= 820454399) or  (timestamp >= 946684800 and timestamp <= 978307199) or (timestamp >= 1104537600 and timestamp <= 1136073599)) and (rating <=1)')
    # print(result[:10])


@timing
def merge_ratings_users():
    # Merge tables users + ratings by user_id field
    merger_ratings_users = pd.merge(ratings, users)
    # print('# Merge tables users + ratings by user_id field \n%s', merger_ratings_users[:10])


@timing
def left_join_ratings_users():
    joined = ratings.join(users, how='left', lsuffix='_left', rsuffix='_right', sort=True)
    # print(joined[:10])


@timing
def inner_join_ratings_users():
    joined = ratings.join(users, how='inner', lsuffix='_left', rsuffix='_right', sort=True)
    # print(joined[:10])


@timing
def outer_join_ratings_users():
    joined = ratings.join(users, how='outer', lsuffix='_left', rsuffix='_right', sort=True)
    # print(joined[:10])


@timing
def right_join_ratings_users():
    joined = ratings.join(users, how='right', lsuffix='_left', rsuffix='_right', sort=True)
    # print(joined[:10])


# =========
# LoadFiles
# =========
logging.info('loading data')
ratingHeader = ['user_id', 'movie_id', 'rating', 'timestamp']
ratings = pd.read_table(RATINGS, engine='python', sep='::', header=None, names=ratingHeader)
# ratings = pd.read_table(RATINGS, engine='python', sep=',', header=None, names=ratingHeader, skiprows=1)

userHeader = ['user_id', 'age', 'ocupation', 'zip']
users = pd.read_table(USERS, engine='python', sep='::', header=None, names=userHeader)

# ====================
# || LAUNCH QUERIES ||
# ====================
logging.info('launching queries')
launch_count()
launch_max()
launch_min()
launch_mean()
launch_std()
launch_query_best_movies()
launch_query_worst_movies()
# merge_ratings_users()
left_join_ratings_users()
inner_join_ratings_users()
outer_join_ratings_users()
right_join_ratings_users()
