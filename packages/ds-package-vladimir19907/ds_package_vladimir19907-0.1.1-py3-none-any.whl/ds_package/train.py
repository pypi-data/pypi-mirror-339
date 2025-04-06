import neptune
from utils import load_feature_data, reg_index, clf_index, params
import os
import re
import pickle
import numpy as np
import pandas as pd
import xgboost as xgb
from tqdm import tqdm
from sklearn.metrics import accuracy_score
from sklearn.metrics import root_mean_squared_error
from feature_extraction import FeatureExtractor
from validation import CV

FEATURE_STORE_DIR = "feature_store"

os.makedirs(FEATURE_STORE_DIR, exist_ok=True)

df = pd.read_csv('sales_train_complete.csv')
df['item_cnt_month'] = df.groupby(['date__month', 'shop_id', 'item_id'])['item_cnt_day'].transform('sum')

run = neptune.init_run(
    project="uladzimir.pakhomau/production-ds",
    api_token="eyJhcGlfYWRkcmVzcyI6Imh0dHBzOi8vYXBwLm5lcHR1bmUuYWkiLCJhcGlfdXJsIjoiaHR0cHM6Ly9hcHAubmVwdHVuZS5haSIsImFwaV9rZXkiOiI0M2IxZWM0ZC02MjNhLTQyMTEtYjhiNi0zN2M0N2RlOGYzOGYifQ==",
)

fe = FeatureExtractor(
    target_col="item_cnt_month",
    date_col="date",
    lags=[1, 2, 3, 6, 12],
    drop_cols=['date__year', 'date__month', 
     'date', 'date__day', 'item_price', 'date__month_of_year',
       'date__week', 'date__day_of_month', 'date__day_of_week',
       'date__week_of_year', 'item_name', 'item_cnt_day',
       'shop_name', 'item_category_name', 'item_category_id'
        ]
)

cv = CV(df=df, date_col="date", min_train_size=12, val_size=1, test_size=1, skip_months=1)

splits = cv.split()

#Feature extraction
feature_store = {}
for month in tqdm(cv.months[1:], desc="Processing months"):
    hist_df = cv.get_hist_df(month)
    if not hist_df.empty:
        features = fe.extract(hist_df)
        index, target = cv.get_target_df(month, fe.target_col, fe.drop_cols)
        for dt in [index, features]:
            for col in dt.select_dtypes(include=['object']).columns:
                dt[col] = dt[col].astype('category')
        feature_store[month] = (index, features, target)
        run['feature_store_size'].append([len(index), len(features), len(target)])

for month, (index, features, target) in tqdm(feature_store.items(), desc="Staging data"):
    month_str = month.strftime("%Y-%m-%d")
    index.to_parquet(f"{FEATURE_STORE_DIR}/index_{month_str}.parquet")
    features.to_parquet(f"{FEATURE_STORE_DIR}/features_{month_str}.parquet")
    with open(f"{FEATURE_STORE_DIR}/target_{month_str}.pkl", "wb") as f:
        pickle.dump(target, f)

use_stored_data = True

#CV
train_months, val_months, test_months = cv.split()

while len(val_months) >= cv.val_size:
    print("==========================================")
    print(f"Train months: {[m.strftime('%m') for m in train_months]}")
    print(f"Validation months: {[m.strftime('%m') for m in val_months[:cv.val_size]]}")

    index_data, y_train_data = [], []
    for m in train_months:
        if use_stored_data:
            index, features, target = load_feature_data(m)
        else:
            index, features, target = feature_store.get(m)
        if index is not None and features is not None and target is not None:
            month_data = index.merge(features, on=['shop_id', 'item_id'],
                                     suffixes=('', '_drop'), how='right')
            index_data.append(month_data)
            y_train_data.append(target)
    if not index_data:
        break

    index_df = pd.concat(index_data, ignore_index=True)
    y_train = list(pd.concat(y_train_data, ignore_index=True))
    X_train = index_df[[col for col in index_df.columns if not col.endswith('_drop')]]
    for col in X_train.select_dtypes(include=['object']).columns:
        X_train[col] = X_train[col].astype('category')

    y_train_flag = (np.array(y_train) > 0).astype(int)
    
    clf = xgb.XGBClassifier(learning_rate=0.15, n_estimators=70, max_depth=6, enable_categorical=True, gamma=1, early_stopping_rounds = 2)
    clf.fit(X_train, y_train_flag, eval_set=[(X_train, y_train_flag)], verbose = False)

    mask = np.array(y_train) > 0
    if mask.sum() > 0:
        reg = xgb.XGBRegressor(**params)
        reg.fit(X_train[mask], np.array(y_train)[mask], eval_set = [(X_train[mask], np.array(y_train)[mask])], verbose = False)
    else:
        reg = None

    sale_prob_train_raw = clf.predict_proba(X_train)[:, 1]
    # sale_prob_train_bina = (sale_prob_train_raw >= 0.5).astype(int)
    sale_prob_train_binary = sale_prob_train_raw

    # clf_train_preds_list.append(sale_prob_train_binary)
    # clf_train_acc = accuracy_score(y_train_flag, sale_prob_train_bina)
    # clf_train_acc_list.append(clf_train_acc)
    
    if reg is not None:
        reg_pred_train = reg.predict(X_train)
    else:
        reg_pred_train = np.zeros_like(sale_prob_train_binary)
    # reg_train_preds_list.append(reg_pred_train)
    
    final_train_preds = sale_prob_train_binary * reg_pred_train
    final_train_preds = final_train_preds.clip(max=82, min=0)
    # final_train_preds_list.append(final_train_preds)
    
    train_rmse = root_mean_squared_error(y_train, final_train_preds)
    # train_rmse_list.append(train_rmse)
    
    for i in range(cv.val_size):
        m = val_months[i]
        index_data_val, y_val_data = [], []
        if use_stored_data:
            index, features, target = load_feature_data(m)
        else:
            index, features, target = feature_store.get(m)
        if index is not None and features is not None and target is not None:
            month_data_val = index.merge(features, on=['shop_id', 'item_id'],
                                         suffixes=('', '_drop'), how='right')
            index_data_val.append(month_data_val)
            y_val_data.append(target)
        if index_data_val:
            index_df_val = pd.concat(index_data_val, ignore_index=True)
            y_val = list(pd.concat(y_val_data, ignore_index=True))
            X_val = index_df_val[[col for col in index_df_val.columns if not col.endswith('_drop')]]
            for col in X_val.select_dtypes(include=['object']).columns:
                X_val[col] = X_val[col].astype('category')
            
            sale_prob_val_raw = clf.predict_proba(X_val)[:, 1]
            sale_prob_val_bin = (sale_prob_val_raw >= 0.5).astype(int)
            sale_prob_val_binary = sale_prob_val_raw
            # clf_val_preds_list.append(sale_prob_val_bin)
            y_val_flag = (np.array(y_val) > 0).astype(int)
            clf_val_acc = accuracy_score(y_val_flag, sale_prob_val_bin)
            # clf_val_acc_list.append(clf_val_acc)
            
            if reg is not None:
                reg_pred_val = reg.predict(X_val)
            else:
                reg_pred_val = np.zeros_like(sale_prob_val_binary)
            # reg_val_preds_list.append(reg_pred_val)
            
            final_val_preds = sale_prob_val_binary * reg_pred_val
            final_val_preds = final_val_preds.clip(max=82, min=0)
            # final_val_preds_list.append(final_val_preds)
            
            rmse_val = root_mean_squared_error(y_val, final_val_preds)
            # val_rmse_list.append(rmse_val)
            
            print(f"Validation month {m.strftime('%Y-%m')}: RMSE = {rmse_val:.4f}|{train_rmse:.4f}, CLF ACC = {clf_val_acc:.4f}")
            run['rmse_val'].append(rmse_val)
            run['train_rmse'].append(train_rmse)
            run['clf_val_acc'].append(clf_val_acc)


    train_months = train_months.union(val_months[:cv.val_size])
    val_months = val_months[cv.val_size:]


#Test
train_months = cv.months[cv.skip_months:].difference(test_months)
index_data, y_train_data = [], []
for m in train_months:
    if use_stored_data:
        index, features, target = load_feature_data(m)
    else:
        index, features, target = feature_store.get(m)
    if index is not None and features is not None and target is not None:
        month_data = index.merge(features, on=['shop_id', 'item_id'],
                                 suffixes=('', '_drop'), how='right')
        index_data.append(month_data)
        y_train_data.append(target)
if index_data:
    index_df = pd.concat(index_data, ignore_index=True)
    y_train = list(pd.concat(y_train_data, ignore_index=True))
    X_train = index_df[[col for col in index_df.columns if not col.endswith('_drop')]]
    for col in X_train.select_dtypes(include=['object']).columns:
        X_train[col] = X_train[col].astype('category')
    y_train_flag = (np.array(y_train) > 0).astype(int)
    clf = xgb.XGBClassifier(learning_rate=0.15 , n_estimators=70, max_depth=10, enable_categorical=True, gamma=0.25, early_stopping_rounds = 2)
    clf.fit(X_train, y_train_flag, eval_set=[(X_train, y_train_flag)], verbose=False)

    mask = np.array(y_train) > 0
    if mask.sum() > 0:
        reg = xgb.XGBRegressor(**params)
        reg.fit(X_train, np.array(y_train), eval_set=[(X_train, np.array(y_train))], verbose=False)


if not test_months.empty:
    print("\n==========================================")
    print(f"Train months: {[m.strftime('%m') for m in train_months]}")
    print(f"Test months: {[m.strftime('%m') for m in test_months]}\n")

    for m in test_months:
        index_data_test, y_test_data = [], []
        if use_stored_data:
            index, features, target = load_feature_data(m)
        else:
            index, features, target = feature_store.get(m)
        if index is not None and features is not None and target is not None:
            month_data_test = index.merge(features, on=['shop_id', 'item_id'],
                                          suffixes=('', '_drop'), how='right')
            index_data_test.append(month_data_test)
            y_test_data.append(target)
        if index_data_test:
            index_df_test = pd.concat(index_data_test, ignore_index=True)
            y_test = list(pd.concat(y_test_data, ignore_index=True))
            X_test = index_df_test[[col for col in index_df_test.columns if not col.endswith('_drop')]]
            for col in X_test.select_dtypes(include=['object']).columns:
                X_test[col] = X_test[col].astype('category')
            
            sale_prob_test_raw = clf.predict_proba(X_test)[:, 1]
            sale_prob_test_bin = (sale_prob_test_raw >= 0.5).astype(int)
            sale_prob_test_binary = sale_prob_test_raw
            
            # clf_test_preds_list.append(sale_prob_test_binary)
            y_test_flag = (np.array(y_test) > 0).astype(int)
            clf_test_acc = accuracy_score(y_test_flag, sale_prob_test_bin)
            # clf_test_acc_list.append(clf_test_acc)
            
            if reg is not None:
                reg_pred_test = reg.predict(X_test)
            else:
                reg_pred_test = np.zeros_like(sale_prob_test_binary)
            # reg_test_preds_list.append(reg_pred_test)
            
            final_test_preds = sale_prob_test_binary * reg_pred_test
            # final_test_preds_list.append(final_test_preds)
            
            rmse_test = root_mean_squared_error(y_test, final_test_preds)
            # test_rmse_list.append(rmse_test)
            
            print(f"Test month {m.strftime('%Y-%m')}: RMSE = {rmse_test:.4f}, CLF ACC = {clf_test_acc:.4f}")
            run['rmse_test'].append(rmse_test)
            run['clf_test_acc'].append(clf_test_acc)


# params = {"learning_rate": 0.001, "optimizer": "Adam"}
# run["parameters"] = params

# for epoch in range(10):
#     run["train/loss"].append(0.9 ** epoch)

# run["eval/f1_score"] = 0.66

run.stop()