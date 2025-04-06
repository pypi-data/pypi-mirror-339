import re
import pickle
import numpy as np
import pandas as pd
import os

FEATURE_STORE_DIR = "feature_store"

def load_feature_data(month):
    month_str = month.strftime("%Y-%m-%d")
    index_path = f"{FEATURE_STORE_DIR}/index_{month_str}.parquet"
    features_path = f"{FEATURE_STORE_DIR}/features_{month_str}.parquet"
    target_path = f"{FEATURE_STORE_DIR}/target_{month_str}.pkl"

    index = pd.read_parquet(index_path)
    
    if os.path.exists(features_path):
        features = pd.read_parquet(features_path)
    else:
        features = pd.DataFrame()

    with open(target_path, "rb") as f:
        target = pickle.load(f)

    return index, features, target

reg_index = ['item_id', 'shop_id', 'item_category', 'shop_type', 'lag_1', 'lag_3', 'lag_6', 'lag_12', 'lag_12']

clf_index = ['item_id', 'shop_id', 'item_category', 'shop_type', 'lag_1', 'lag_3', 'lag_6', 'lag_12', 'lag_12']

params ={'enable_categorical': True,
        'colsample_bytree': 0.9286474255634593,
        'eval_metric': 'rmse',
        'learning_rate': 0.0826010856865518,
        'max_bin': 1024, 'max_depth': 9,
        'min_child_weight': 1.5163752033499591, 
        'n_estimators': 550, 'nthread': 2, 
        'reg_lambda': 0.5020515121371055, 
        'subsample': 0.8090208851854477, 
        'tree_method': 'hist'}