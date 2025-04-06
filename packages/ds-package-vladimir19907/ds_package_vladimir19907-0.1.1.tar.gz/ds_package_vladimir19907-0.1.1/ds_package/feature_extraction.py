import pandas as pd
import numpy as np
import re

test_str = 'pypi'

class FeatureExtractor:
    def __init__(
        self,
        target_col: str = "item_cnt_month",
        date_col: str = "date",
        lags: list = [1, 2, 3, 12],
        drop_cols: list = ['date'],
    ):
        self.target_col = target_col
        self.date_col = date_col
        self.lags = lags if lags else []
        self.drop_cols = drop_cols if drop_cols else []

    def extract(self, hist_df):
        forecast_date = hist_df[self.date_col].max() + pd.offsets.MonthBegin(1)
        base_df = self._create_full_grid(hist_df, forecast_date)
        
        features = [
                # self.mean_city_item_id(hist_df),
            # self.mean_item_category_item_id(hist_df),
            # self.mean_shop_id_item_id(hist_df),
            # self.mean_item_id(hist_df),
            # self._generate_cat_lags(hist_df),
            # self._generate_supcat_lags(hist_df),
            # self._generate_city_lags(hist_df),
            # self._generate_item_first_sale(hist_df),
            # self._generate_item_shop_first_sale(hist_df),
            # self._generate_shop_performance_index(hist_df),
            # self._generate_seasonality_ratio_by_item(hist_df), #пролагать
            # self._generate_sales_momentum_by_item(hist_df), #пролагать
            # self._generate_cov_by_item(hist_df), #пролагать
            # self._generate_sales_volatility_by_item_supcat(hist_df), #пролагать
            # self._generate_sales_volatility_by_city(hist_df),#пролагать
            # self._generate_sales_volatility_by_shop(hist_df),#пролагать
            # self._generate_sales_volatility_by_price_segment(hist_df),#пролагать
            # self._generate_sales_volatility_by_item(hist_df),#пролагать
            # self._generate_item_sales_timing_features(hist_df), 
            # self._generate_category_sales_timing_features(hist_df),
            # self._generate_category_sales_existence_features(hist_df),
            # self._generate_shop_sales_existence_features(hist_df),
            # self._generate_frequency_features(hist_df),
            # self._generate_sales_existence_features(hist_df),
            self._generate_lags(hist_df),
            self._generate_shop_type(hist_df),
            # self._generate_shop_city(hist_df),
            # self._generate_season(hist_df),
            # self._generate_holidays(hist_df),
            # self._generate_average_cnt_month(hist_df), #пролагать
            # self._generate_price_segment(hist_df),
            # self._generate_categorical_year(hist_df),
            self._generate_item_category(hist_df),
            # self._generate_cyclic_month_features(hist_df),
            # self._generate_sma(hist_df),#пролагать
            # # self._generate_holidays_prev_month(hist_df),
            # self._generate_category_sales(hist_df),#пролагать
            # # self._generate_shop_sales(hist_df),#пролагать
            # # self._generate_cat_cnt_prev_year(hist_df),
            # self._generate_category_price_segment(hist_df), 
            # self._generate_holiday_category_boost(hist_df),
            # # self._generate_category_seasonality(hist_df),
            # self._generate_last_month_sales_bin(hist_df),
            # self._generate_super_categories(hist_df),
            # # self._generate_holiday_supercategory_boost(hist_df),
            # self._generate_supercategory_sales(hist_df),
            # self._generate_supercategory_seasonality(hist_df),
            # self._generate_supercat_cnt_prev_year(hist_df),
            # self._generate_supercat_price_segment(hist_df),
            # self._generate_category_sales_features(hist_df),
            # self._generate_supcat_sales_features(hist_df),
            # self._generate_price_segment_sales_lags(hist_df),
            # self._generate_shop_type_sales_lags(hist_df),
            # self._generate_city_sales_lags(hist_df),
        ]

        for feature_df in features:
            base_df = base_df.merge(feature_df, on=[self.date_col, 'shop_id', 'item_id'], how='left')
        
        if self.date_col not in self.drop_cols:
            self.drop_cols.append(self.date_col)
        base_df.drop(columns=self.drop_cols, errors='ignore', inplace=True)
        
        for col in base_df.select_dtypes(include='object').columns:
            base_df[col] = base_df[col].astype('category')
            
        return base_df

  

    def mean_item_category_item_id(self, df):
        current_month = df[self.date_col].max() + pd.offsets.MonthBegin(1)
        item_category_df = self._generate_item_category(df)[['item_id', 'item_category']].drop_duplicates()
        grid = self._create_full_grid(df, current_month)
        grid = pd.merge(grid, item_category_df, on=['item_id'], how='left')
        
        group_cols = ['item_id', 'item_category']
        features = grid[['shop_id', 'item_id', 'item_category']].drop_duplicates()
        
        for lag in self.lags:
            lag_date = current_month - pd.offsets.MonthBegin(lag)
            
            lag_data = df[df[self.date_col].dt.to_period('M') == lag_date.to_period('M')]
            
            if not lag_data.empty:
                lag_data = pd.merge(lag_data, item_category_df, on='item_id', how='left')
                lag_features = lag_data.groupby(group_cols, observed=False)[self.target_col].mean().reset_index()
                lag_features.rename(columns={self.target_col: f'mean_item_category_item_id_lag_{lag}'}, inplace=True)
            else:
                lag_features = features[group_cols].drop_duplicates()
                lag_features[f'mean_item_category_item_id_lag_{lag}'] = 0
            
            features = pd.merge(features,lag_features,on=group_cols,how='left')
        
        features['date'] = current_month
        return features[['date', 'shop_id', 'item_id'] + [f'mean_item_category_item_id_lag_{lag}' for lag in self.lags]]


    def mean_shop_id_item_id(self, df):
        current_month = df[self.date_col].max() + pd.offsets.MonthBegin(1)
        grid = self._create_full_grid(df, current_month)
        
        group_cols = ['item_id', 'shop_id']
        features = grid[['shop_id', 'item_id']].drop_duplicates()
        
        for lag in self.lags:
            lag_date = current_month - pd.offsets.MonthBegin(lag)
            
            lag_data = df[df[self.date_col].dt.to_period('M') == lag_date.to_period('M')]
            
            if not lag_data.empty:
                lag_features = lag_data.groupby(group_cols, observed=False)[self.target_col].mean().reset_index()
                lag_features.rename(columns={self.target_col: f'mean_shop_id_item_id{lag}'}, inplace=True)
            else:
                lag_features = features[group_cols].drop_duplicates()
                lag_features[f'mean_shop_id_item_id{lag}'] = 0
            
            features = pd.merge(features,lag_features,on=group_cols,how='left')
        
        features['date'] = current_month
        return features[['date', 'shop_id', 'item_id'] + [f'mean_shop_id_item_id{lag}' for lag in self.lags]]

    def mean_city_item_id(self, df):
        current_month = df[self.date_col].max() + pd.offsets.MonthBegin(1)
        
        city_df = self._generate_shop_city(df)[['shop_id', 'city']]
        city_df = city_df.drop_duplicates(subset='shop_id', keep='first')
        
        grid = self._create_full_grid(df, current_month)
        grid = pd.merge(grid, city_df, on='shop_id', how='left')
        
        group_cols = ['item_id', 'city']
        features = grid[['shop_id', 'item_id', 'city']].drop_duplicates()
        
        for lag in self.lags:
            lag_date = current_month - pd.offsets.MonthBegin(lag)
            lag_period = lag_date.to_period('M')
            lag_data = df[df[self.date_col].dt.to_period('M') == lag_period]
            
            if not lag_data.empty:
                lag_data = pd.merge(lag_data, city_df, on='shop_id', how='left')
                
                lag_group = lag_data.groupby(group_cols, observed=True)[self.target_col].mean()
                lag_features = lag_group.reset_index(name=f'mean_city_item_id_lag_{lag}')
            else:
                lag_features = pd.DataFrame(columns=group_cols + [f'mean_city_item_id_lag_{lag}'])
                lag_features[f'mean_city_item_id_lag_{lag}'] = 0
            
            features = features.merge(lag_features, on=group_cols, how='left').fillna({f'mean_city_item_id_lag_{lag}': 0})
            
            features[f'mean_city_item_id_lag_{lag}'] = features[f'mean_city_item_id_lag_{lag}'].astype('float32')
        
        features['date'] = current_month
        return features[['date', 'shop_id', 'item_id'] + [f'mean_city_item_id_lag_{lag}' for lag in self.lags]]
    
    def mean_item_id(self, df):
        current_month = df[self.date_col].max() + pd.offsets.MonthBegin(1)
        grid = self._create_full_grid(df, current_month)
        
        group_cols = ['item_id']
        features = grid[['shop_id', 'item_id']].drop_duplicates()
        
        for lag in self.lags:
            lag_date = current_month - pd.offsets.MonthBegin(lag)
            
            lag_data = df[df[self.date_col].dt.to_period('M') == lag_date.to_period('M')]
            
            if not lag_data.empty:
                lag_features = lag_data.groupby(group_cols, observed=False)[self.target_col].mean().reset_index()
                lag_features.rename(columns={self.target_col: f'mean_item_id_lag_{lag}'}, inplace=True)
            else:
                lag_features = features[group_cols].drop_duplicates()
                lag_features[f'mean_item_id_lag_{lag}'] = 0
            
            features = pd.merge(features,lag_features,on=group_cols,how='left')
        
        features['date'] = current_month
        return features[['date', 'shop_id', 'item_id'] + [f'mean_item_id_lag_{lag}' for lag in self.lags]]

    def _generate_city_lags(self, df):
        current_month = df[self.date_col].max() + pd.offsets.MonthBegin(1)
        city_df = self._generate_shop_city(df)
        grid = self._create_full_grid(df, current_month)
        grid = pd.merge(grid, city_df, on=['shop_id', 'item_id'], how='left')
        
        group_cols = ['item_id', 'city']
        features = grid[['shop_id', 'item_id', 'city']].drop_duplicates()
        
        for lag in self.lags:
            lag_date = current_month - pd.offsets.MonthBegin(lag)
            
            lag_data = df[df[self.date_col].dt.to_period('M') == lag_date.to_period('M')]
            
            if not lag_data.empty:
                lag_data = pd.merge(lag_data, city_df, on=['shop_id', 'item_id'], how='left')
                lag_features = lag_data.groupby(group_cols, observed=False)[self.target_col].max().reset_index()
                lag_features.rename(columns={self.target_col: f'city_target_lag_{lag}'}, inplace=True)
            else:
                lag_features = features[group_cols].drop_duplicates()
                lag_features[f'city_target_lag_{lag}'] = 0
            
            features = pd.merge(features,lag_features,on=group_cols,how='left')
        
        features['date'] = current_month
        return features[['date', 'shop_id', 'item_id'] + [f'city_target_lag_{lag}' for lag in self.lags]]

    def _generate_supcat_lags(self, df):
        current_month = df[self.date_col].max() + pd.offsets.MonthBegin(1)
        city_df = self._generate_super_categories(df)
        grid = self._create_full_grid(df, current_month)
        grid = pd.merge(grid, city_df, on=['item_id','shop_id'], how='left')
        
        group_cols = ['item_id', 'super_category']
        features = grid[['shop_id', 'item_id', 'super_category']].drop_duplicates()
        
        for lag in self.lags:
            lag_date = current_month - pd.offsets.MonthBegin(lag)
            
            lag_data = df[df[self.date_col].dt.to_period('M') == lag_date.to_period('M')]
            
            if not lag_data.empty:
                lag_data = pd.merge(lag_data, city_df, on=['item_id','shop_id'], how='left')
                lag_features = lag_data.groupby(group_cols, observed=False)[self.target_col].max().reset_index()
                lag_features.rename(columns={self.target_col: f'supcat_target_lag_{lag}'}, inplace=True)
            else:
                lag_features = features[group_cols].drop_duplicates()
                lag_features[f'supcat_target_lag_{lag}'] = 0
            
            features = pd.merge(features,lag_features,on=group_cols,how='left')
        
        features['date'] = current_month
        return features[['date', 'shop_id', 'item_id'] + [f'supcat_target_lag_{lag}' for lag in self.lags]]

    def _generate_cat_lags(self, df):

        current_month = df[self.date_col].max() + pd.offsets.MonthBegin(1)
        cat_df = self._generate_item_category(df)
        grid = self._create_full_grid(df, current_month)
        grid = pd.merge(grid, cat_df, on=['item_id','shop_id'], how='left')
        
        group_cols = ['shop_id', 'item_category']
        features = grid[['shop_id','item_id', 'item_category']].drop_duplicates()
        
        for lag in self.lags:
            lag_date = current_month - pd.offsets.MonthBegin(lag)
            
            lag_data = df[df[self.date_col].dt.to_period('M') == lag_date.to_period('M')]
            
            if not lag_data.empty:
                lag_data = pd.merge(lag_data, cat_df, on=['item_id', 'shop_id'], how='left')
                lag_features = lag_data.groupby(group_cols, observed=False)[self.target_col].max().reset_index()
                lag_features.rename(columns={self.target_col: f'cat_target_lag_{lag}'}, inplace=True)
            else:
                lag_features = features[group_cols].drop_duplicates()
                lag_features[f'cat_target_lag_{lag}'] = 0
            
            features = pd.merge(features,lag_features,on=group_cols,how='left')
        
        features['date'] = current_month
        return features[['date', 'shop_id', 'item_id'] + [f'cat_target_lag_{lag}' for lag in self.lags]]

    def _generate_item_first_sale(self, hist_df):
        forecast_date = hist_df[self.date_col].max() + pd.offsets.MonthBegin(1)
        sales_data = hist_df[hist_df['item_cnt_month'] > 0]
        
        item_first_sale = sales_data.groupby('item_id')['date__month'].min().reset_index()
        item_first_sale.rename(columns={'date__month': 'item_first_sale'}, inplace=True)
        
        unique_items = hist_df[['item_id']].drop_duplicates()
        result = pd.merge(unique_items, item_first_sale, on='item_id', how='left')
        
        result['item_first_sale'] = result['item_first_sale'].fillna(99)
        grid = self._create_full_grid(hist_df, forecast_date)
        result = pd.merge(grid, result, on='item_id', how='left').drop_duplicates()
        return result[['date', 'shop_id','item_id', 'item_first_sale']]

    def _generate_item_shop_first_sale(self, hist_df):
        forecast_date = hist_df[self.date_col].max() + pd.offsets.MonthBegin(1)

        sales_data = hist_df[hist_df['item_cnt_month'] > 0]
        
        item_shop_first_sale = sales_data.groupby(['shop_id', 'item_id'])['date__month'].min().reset_index()
        item_shop_first_sale.rename(columns={'date__month': 'item_shop_first_sale'}, inplace=True)
        
        grid = self._create_full_grid(hist_df, forecast_date)
        result = pd.merge(grid, item_shop_first_sale, on=['shop_id', 'item_id'], how='left')
        
        result['item_shop_first_sale'] = result['item_shop_first_sale'].fillna(99)
        
        return result[['date', 'shop_id', 'item_id', 'item_shop_first_sale']]

    def _generate_shop_performance_index(self, hist_df, lookback_months=6):
        forecast_date = hist_df[self.date_col].max() + pd.offsets.MonthBegin(1)
        start_date = forecast_date - pd.DateOffset(months=lookback_months)
        
        recent_data = hist_df[(hist_df[self.date_col] >= start_date) & (hist_df[self.date_col] < forecast_date)]
        
        shop_item_sales = recent_data.groupby(['shop_id', 'item_id'])['item_cnt_month'].sum().reset_index()
        
        total_sales = shop_item_sales.groupby('shop_id')['item_cnt_month'].sum().reset_index()
        total_sales = total_sales.rename(columns={'item_cnt_month': 'total_sales'})
        
        num_items = shop_item_sales.groupby('shop_id')['item_id'].nunique().reset_index()
        num_items = num_items.rename(columns={'item_id': 'number_of_items'})
        
        avg_sales = shop_item_sales.groupby('shop_id')['item_cnt_month'].mean().reset_index()
        avg_sales = avg_sales.rename(columns={'item_cnt_month': 'avg_sales'})
        
        active_items = shop_item_sales.groupby('shop_id')['item_cnt_month'].apply(lambda s: (s > 0).sum()).reset_index()
        active_items = active_items.rename(columns={'item_cnt_month': 'active_items'})
        
        active_ratio = pd.merge(num_items, active_items, on='shop_id')
        active_ratio['active_ratio'] = active_ratio['active_items'] / active_ratio['number_of_items']
        active_ratio = active_ratio[['shop_id', 'active_ratio']]
        
        shop_perf = total_sales.merge(num_items, on='shop_id')
        shop_perf = shop_perf.merge(avg_sales, on='shop_id')
        shop_perf = shop_perf.merge(active_ratio, on='shop_id')
        
        grid = self._create_full_grid(hist_df, forecast_date)
        result = pd.merge(grid, shop_perf, on='shop_id', how='left')
        return result[['date', 'shop_id', 'item_id', 'active_ratio']]


    def _generate_seasonality_ratio_by_item(self, hist_df, lookback_months=12):
        forecast_date = hist_df[self.date_col].max() + pd.offsets.MonthBegin(1)
        same_month_last_year = forecast_date - pd.DateOffset(years=1)
        
        start_date = forecast_date - pd.DateOffset(months=lookback_months)
        rolling_data = hist_df[(hist_df[self.date_col] >= start_date) & (hist_df[self.date_col] < forecast_date)]
        
        rolling_mean = (rolling_data.groupby(['item_id', 'shop_id'])['item_cnt_month']
                        .mean().reset_index()
                        .rename(columns={'item_cnt_month': 'rolling_mean_12'}))
        
        same_month_sales = (hist_df[hist_df[self.date_col] == same_month_last_year]
                            [['item_id', 'shop_id','item_cnt_month']]
                            .drop_duplicates(subset=['item_id', 'shop_id'])
                            .rename(columns={'item_cnt_month': 'sales_last_year'}))
        
        season_df = pd.merge(same_month_sales, rolling_mean, on=['item_id', 'shop_id'], how='left')
        
        season_df['seasonality_ratio'] = season_df['sales_last_year'] / (season_df['rolling_mean_12'] + 1e-6)
        season_df['seasonality_ratio'] = season_df['seasonality_ratio']
        season_df['date'] = forecast_date
        return season_df[['date','item_id', 'shop_id', 'rolling_mean_12','seasonality_ratio']].fillna(0)

    def _generate_sales_momentum_by_item(self, hist_df):
        forecast_date = hist_df[self.date_col].max() + pd.offsets.MonthBegin(1)
        last_month = forecast_date - pd.offsets.MonthBegin(1)
        prev_month = forecast_date - pd.offsets.MonthBegin(2)
        
        sales_last = (hist_df[hist_df[self.date_col] == last_month].groupby(['item_id', 'shop_id'])['item_cnt_day'].sum().reset_index().rename(columns={'item_cnt_day': 'item_sales_last'}))
        sales_prev = (hist_df[hist_df[self.date_col] == prev_month].groupby(['item_id', 'shop_id'])['item_cnt_day'].sum().reset_index().rename(columns={'item_cnt_day': 'item_sales_prev'}))
        
        momentum_df = pd.merge(sales_last, sales_prev, on=['item_id', 'shop_id'], how='outer').fillna(0)
        momentum_df['momentum_abs'] = momentum_df['item_sales_last'] - momentum_df['item_sales_prev']
        momentum_df['momentum_pct'] = momentum_df.apply(lambda row: ((row['item_sales_last'] - row['item_sales_prev']) / row['item_sales_prev'] * 100)if row['item_sales_prev'] != 0 else 0, axis=1)
        grid = self._create_full_grid(hist_df, forecast_date)
        result = pd.merge(grid, momentum_df, on=['item_id', 'shop_id'], how='left').drop_duplicates()
        return result[['date','item_id', 'shop_id', 'momentum_abs', 'momentum_pct']]

    def _generate_cov_by_item(self, hist_df, lookback_months=6):
        forecast_date = hist_df[self.date_col].max() + pd.offsets.MonthBegin(1)
        start_date = forecast_date - pd.DateOffset(months=lookback_months)
        
        monthly_sales = hist_df.groupby(['shop_id','item_id', 'date'])['item_cnt_day'].sum().reset_index()
        monthly_sales = monthly_sales.rename(columns={'item_cnt_day': 'month_sum_sales_by_item'})
        
        stats_df = monthly_sales.groupby(['item_id', 'shop_id'])['month_sum_sales_by_item'].agg(['mean', 'std']).reset_index()
        stats_df['cov_sales'] = stats_df.apply(lambda row: row['std'] / row['mean'] if row['mean'] != 0 else 0, axis=1)
        grid = self._create_full_grid(hist_df, forecast_date)
        result = pd.merge(grid, stats_df, on=['item_id', 'shop_id'], how='left').drop_duplicates()
        return result[['date','item_id', 'shop_id', 'cov_sales']]

    def _generate_sales_volatility_by_item_supcat(self, hist_df, lookback_months=6):
        forecast_date = hist_df[self.date_col].max() + pd.offsets.MonthBegin(1)
        start_date = forecast_date - pd.DateOffset(months=lookback_months)
        
        cats_df = self._generate_super_categories(hist_df)[['item_id', 'super_category']].drop_duplicates(subset='item_id')
        
        grid = self._create_full_grid(hist_df, forecast_date)
        
        grid = pd.merge(grid, cats_df, on='item_id', how='left')
        
        recent_data = hist_df[(hist_df[self.date_col] >= start_date) & (hist_df[self.date_col] < forecast_date)]
        recent_data = pd.merge(recent_data, cats_df, on='item_id', how='left').drop_duplicates()
        
        volatility_df = (
            recent_data.groupby('super_category', observed=False)['item_cnt_month']
            .std().reset_index()
            .rename(columns={'item_cnt_month': 'sales_volatility_item_supcat'})
        )
        volatility_df['sales_volatility_item_supcat'] = volatility_df['sales_volatility_item_supcat'].fillna(0)
        result = pd.merge(grid, volatility_df, on='super_category', how='left')
        result = result.drop_duplicates(subset=['date', 'shop_id', 'item_id'])
        
        return result[['date','item_id', 'shop_id', 'sales_volatility_item_supcat']]


    def _generate_sales_volatility_by_city(self, hist_df, lookback_months=6):
        forecast_date = hist_df[self.date_col].max() + pd.offsets.MonthBegin(1)
        start_date = forecast_date - pd.DateOffset(months=lookback_months)
        
        shop_city_df = self._generate_shop_city(hist_df)[['shop_id', 'city']].drop_duplicates(subset='shop_id')
        
        recent_data = hist_df[(hist_df[self.date_col] >= start_date) & (hist_df[self.date_col] < forecast_date)]
        recent_data = pd.merge(recent_data, shop_city_df, on='shop_id', how='left')
        volatility_df = (recent_data.groupby('city', observed=False)['item_cnt_month']
                        .std()
                        .reset_index()
                        .rename(columns={'item_cnt_month': 'sales_volatility_item_city'}))
        volatility_df['sales_volatility_item_city'] = volatility_df['sales_volatility_item_city'].fillna(0)
        
        grid = self._create_full_grid(hist_df, forecast_date)
        grid = pd.merge(grid, shop_city_df, on='shop_id', how='left').drop_duplicates()
        result = pd.merge(grid, volatility_df, on='city', how='left')
        
        return result[['date', 'shop_id', 'item_id', 'sales_volatility_item_city']]


    def _generate_sales_volatility_by_price_segment(self, hist_df, lookback_months=6):
        forecast_date = hist_df[self.date_col].max() + pd.offsets.MonthBegin(1)
        start_date = forecast_date - pd.DateOffset(months=lookback_months)
        mapping_ps = self._generate_price_segment(hist_df)[['item_id', 'price_segment']].drop_duplicates(subset='item_id')
        
        recent_data = hist_df[(hist_df[self.date_col] >= start_date) & (hist_df[self.date_col] < forecast_date)]
        recent_data = recent_data.merge(mapping_ps, on='item_id', how='left')
        volatility_df = recent_data.groupby('price_segment', observed=False)['item_cnt_month'].std().reset_index()
        volatility_df = volatility_df.rename(columns={'item_cnt_month': 'sales_volatility_item_ps'})
        volatility_df['sales_volatility_item_ps'] = volatility_df['sales_volatility_item_ps'].fillna(0)
        
        grid = self._create_full_grid(hist_df, forecast_date)
        grid = pd.merge(grid, mapping_ps, on='item_id', how='left')
        result = pd.merge(grid, volatility_df, on='price_segment', how='left')
        
        result = result.drop_duplicates(subset=['date', 'shop_id', 'item_id'])
        
        return result[['date', 'shop_id', 'item_id', 'sales_volatility_item_ps']]


        forecast_date = hist_df[self.date_col].max() + pd.offsets.MonthBegin(1)
        start_date = forecast_date - pd.DateOffset(months=lookback_months)
        
        mapping_cat = self._generate_item_category(hist_df)[['item_id', 'item_category']].drop_duplicates(subset='item_id')
        
        recent_data = hist_df[(hist_df[self.date_col] >= start_date) & (hist_df[self.date_col] < forecast_date)]
        recent_data = recent_data.merge(mapping_cat, on='item_id', how='left')
        
        volatility_df = recent_data.groupby('item_category', observed=False)['item_cnt_month'].std().reset_index()
        volatility_df = volatility_df.rename(columns={'item_cnt_month': 'sales_volatility_item_cat'})
        volatility_df['sales_volatility_item_cat'] = volatility_df['sales_volatility_item_cat'].fillna(0)
        
        grid = self._create_full_grid(hist_df, forecast_date)
        
        grid = pd.merge(grid, mapping_cat, on='item_id', how='left')
        
        result = pd.merge(grid, volatility_df, on='item_category', how='left')
        result = result.drop_duplicates(subset=['date', 'shop_id', 'item_id'])
        
        return result[['date', 'shop_id', 'item_id', 'sales_volatility_item_cat']]


    def _generate_sales_volatility_by_shop(self, hist_df, lookback_months=6):
        forecast_date = hist_df[self.date_col].max() + pd.offsets.MonthBegin(1)
        grid = self._create_full_grid(hist_df, forecast_date)
        result = grid.copy()
        
        for lag in self.lags:
            end_date = forecast_date - pd.DateOffset(months=lag)
            start_date = end_date - pd.DateOffset(months=lookback_months)
            
            lag_data = hist_df[
                (hist_df[self.date_col] >= start_date) & 
                (hist_df[self.date_col] < end_date)
            ]
            
            volatility_df = lag_data.groupby('shop_id')['item_cnt_month'].std().reset_index()
            col_name = f"sales_volatility_shop_id_lag_{lag}"
            volatility_df = volatility_df.rename(columns={'item_cnt_month': col_name})
            volatility_df[col_name] = volatility_df[col_name].fillna(0)
            
            result = pd.merge(result, volatility_df, on='shop_id', how='left')
        
        volatility_cols = [f"sales_volatility_shop_id_lag_{lag}" for lag in self.lags]
        result[volatility_cols] = result[volatility_cols].fillna(0)
        
        return result


    def _generate_sales_volatility_by_item(self, hist_df, lookback_months=6):
        forecast_date = hist_df[self.date_col].max() + pd.offsets.MonthBegin(1)
        grid = self._create_full_grid(hist_df, forecast_date)
        result = grid.copy()
        
        for lag in self.lags:
            end_date = forecast_date - pd.DateOffset(months=lag)
            start_date = end_date - pd.DateOffset(months=lookback_months)
            
            lag_data = hist_df[
                (hist_df[self.date_col] >= start_date) & 
                (hist_df[self.date_col] < end_date)
            ]
            
            volatility_df = lag_data.groupby('item_id')['item_cnt_month'].std().reset_index()
            col_name = f"sales_volatility_item_id_lag_{lag}"
            volatility_df = volatility_df.rename(columns={'item_cnt_month': col_name})
            volatility_df[col_name] = volatility_df[col_name].fillna(0)
            
            result = pd.merge(result, volatility_df, on='item_id', how='left')
        
        volatility_cols = [f"sales_volatility_item_id_lag_{lag}" for lag in self.lags]
        result[volatility_cols] = result[volatility_cols].fillna(0)
        
        return result

    def _generate_category_sales_timing_features(self, hist_df, lookback_months=6):
        forecast_date = hist_df[self.date_col].max() + pd.offsets.MonthBegin(1)
        start_date = forecast_date - pd.DateOffset(months=lookback_months)
        
        recent_data = hist_df[(hist_df['date'] >= start_date) & (hist_df['date'] < forecast_date) & (hist_df['item_cnt_day'] > 0)]
        
        mapping_df = hist_df[['shop_id', 'item_id', 'item_category_id']].drop_duplicates(subset='item_id')
        last_sale = (recent_data.groupby(['shop_id', 'item_category_id'])['date']
                    .max()
                    .reset_index()
                    .rename(columns={'date': 'last_sale_date'}))

        active_months = (recent_data.assign(month=recent_data['date'].dt.to_period('M'))
                        .groupby(['shop_id', 'item_category_id'])['month']
                        .nunique()
                        .reset_index()
                        .rename(columns={'month': 'active_months_cat'}))
        
        grid = self._create_full_grid(hist_df, forecast_date)
        grid = grid.merge(mapping_df, on=['shop_id', 'item_id'], how='left')
        
        features = grid.merge(last_sale[['shop_id', 'item_category_id']], on=['shop_id', 'item_category_id'], how='left')
        features = features.merge(active_months, on=['shop_id', 'item_category_id'], how='left')
        
        fill_values = {
            'active_months_cat': 0
        }
        features = features.fillna(fill_values)
        
        return features[['date', 'shop_id', 'item_id', 'active_months_cat']]

    def _generate_item_sales_timing_features(self, hist_df, lookback_months=6):
        forecast_date = hist_df[self.date_col].max() + pd.offsets.MonthBegin(1)
        start_date = forecast_date - pd.DateOffset(months=lookback_months)
        
        recent_data = hist_df[(hist_df['date'] >= start_date) & (hist_df['date'] < forecast_date) & 
                            (hist_df['item_cnt_day'] > 0)]
        
        last_sale = (recent_data.groupby(['shop_id', 'item_id'])['date']
                    .max()
                    .reset_index()
                    .rename(columns={'date': 'last_sale_date'}))
        last_sale['months_since_last_sale_item'] = (
            (forecast_date.year - last_sale['last_sale_date'].dt.year) * 12 +
            (forecast_date.month - last_sale['last_sale_date'].dt.month)
        )
        
        active_months = (recent_data.copy()
                        .assign(month=recent_data['date'].dt.to_period('M'))
                        .groupby(['shop_id', 'item_id'])['month']
                        .nunique()
                        .reset_index()
                        .rename(columns={'month': 'active_months_item'}))
        
        grid = self._create_full_grid(hist_df, forecast_date)
        features = grid.merge(last_sale[['shop_id', 'item_id', 'months_since_last_sale_item']], 
                            on=['shop_id', 'item_id'], how='left')
        features = features.merge(active_months, on=['shop_id', 'item_id'], how='left')
        
        fill_values = {
            'months_since_last_sale_item': lookback_months + 1,
            'active_months_item': 0
        }
        features = features.fillna(fill_values)
        
        return features[['date', 'shop_id', 'item_id','months_since_last_sale_item', 'active_months_item']]

    def _generate_category_sales_existence_features(self, hist_df, lookback_months=6):
        forecast_date = hist_df[self.date_col].max() + pd.offsets.MonthBegin(1)
        start_date = forecast_date - pd.DateOffset(months=lookback_months)
        
        recent_data = hist_df[(hist_df['date'] >= start_date) & (hist_df['date'] < forecast_date) & 
                            (hist_df['item_cnt_day'] > 0)]
        
        last_month = forecast_date - pd.offsets.MonthBegin(1)
        last_month_sales = (
            recent_data[recent_data['date'] == last_month]
            .groupby('item_category_id')['item_cnt_day']
            .sum()
            .reset_index()
            .rename(columns={'item_cnt_day': 'had_sales_last_month_cat'})
        )
        last_month_sales['had_sales_last_month_cat'] = 1
        
        sales_months = (
            recent_data.groupby(['item_category_id', pd.Grouper(key='date', freq='ME')])['item_cnt_day']
            .sum().reset_index()
        )
        
        last_sale_date = (
            recent_data.groupby('item_category_id')['date']
            .max().reset_index().rename(columns={'date': 'last_sale_date'})
        )
        
        grid = self._create_full_grid(hist_df, forecast_date)
        mapping_df = hist_df[['shop_id', 'item_id', 'item_category_id']].drop_duplicates(subset='item_id')
        grid = grid.merge(mapping_df, on=['shop_id', 'item_id'], how='left')
        features = grid.merge(last_month_sales, on='item_category_id', how='left')
        
        fill_values = {
            'had_sales_last_month_cat': 0,
        }
        features = features.fillna(fill_values)
        
        return features[['date', 'shop_id', 'item_id', 'item_category_id', 'had_sales_last_month_cat']]


    def _generate_shop_sales_existence_features(self, hist_df, lookback_months=6):
        forecast_date = hist_df[self.date_col].max() + pd.offsets.MonthBegin(1)
        start_date = forecast_date - pd.DateOffset(months=lookback_months)
        
        recent_data = hist_df[(hist_df['date'] >= start_date) & 
                            (hist_df['date'] < forecast_date) & 
                            (hist_df['item_cnt_day'] > 0)]
        
        last_month = forecast_date - pd.offsets.MonthBegin(1)
        last_month_sales = (
            recent_data[recent_data['date'] == last_month]
            .groupby('shop_id')['item_cnt_day']
            .sum()
            .reset_index()
            .rename(columns={'item_cnt_day': 'had_sales_last_month_shop'})
        )
        last_month_sales['had_sales_last_month_shop'] = 1
        
        sales_months = (
            recent_data.groupby(['shop_id', pd.Grouper(key='date', freq='ME')])['item_cnt_day']
            .sum()
            .reset_index()
        )
        active_months = (
            sales_months.groupby('shop_id')['date']
            .nunique()
            .reset_index()
            .rename(columns={'date': 'active_months_count_shop'})
        )
        
        last_sale_date = (
            recent_data.groupby('shop_id')['date']
            .max()
            .reset_index()
            .rename(columns={'date': 'last_sale_date'})
        )

        
        grid = self._create_full_grid(hist_df, forecast_date)
        
        features = grid.merge(last_month_sales, on='shop_id', how='left')
        features = features.merge(active_months, on='shop_id', how='left')
        
        fill_values = {
            'had_sales_last_month_shop': 0,
            'active_months_count_shop': 0,
        }
        features = features.fillna(fill_values)
        
        return features[['date', 'shop_id', 'item_id', 'had_sales_last_month_shop', 'active_months_count_shop']]


    def _generate_sales_existence_features(self, hist_df, lookback_months=6):
        forecast_date = hist_df['date'].max() + pd.offsets.MonthBegin(1)
        start_date = forecast_date - pd.DateOffset(months=lookback_months)
        
        recent_data = hist_df[(hist_df['date'] >= start_date) & (hist_df['date'] < forecast_date) & (hist_df['item_cnt_day'] > 0)]
        
        last_month = forecast_date - pd.offsets.MonthBegin(1)
        last_month_sales = (
            recent_data[recent_data['date'] == last_month]
            .groupby('item_id')['item_cnt_day']
            .sum()
            .reset_index()
            .rename(columns={'item_cnt_day': 'had_sales_last_month'})
        )
        last_month_sales['had_sales_last_month'] = 1

        sales_months = (
            recent_data.groupby(['item_id', pd.Grouper(key='date', freq='ME')])['item_cnt_day']
            .sum()
            .reset_index()
        )
        active_months = (
            sales_months.groupby('item_id')['date']
            .nunique()
            .reset_index()
            .rename(columns={'date': 'active_months_count'})
        )
        
        last_sale_date = (
            recent_data.groupby('item_id')['date']
            .max()
            .reset_index()
            .rename(columns={'date': 'last_sale_date'})
        )
        last_sale_date['months_since_last_sale'] = (
            (forecast_date.year - last_sale_date['last_sale_date'].dt.year) * 12 +
            (forecast_date.month - last_sale_date['last_sale_date'].dt.month)
        )
        
        grid = self._create_full_grid(hist_df, forecast_date)
        
        features = grid.merge(last_month_sales, on='item_id', how='left')
        features = features.merge(active_months, on='item_id', how='left')
        features = features.merge(last_sale_date[['item_id', 'months_since_last_sale']], on='item_id', how='left')
        
        fill_values = {
            'had_sales_last_month': 0,
            'active_months_count': 0,
            'months_since_last_sale': lookback_months + 1
        }
        features = features.fillna(fill_values)
        
        return features[['date', 'shop_id', 'item_id', 
                        'had_sales_last_month', 
                        'active_months_count',
                        'months_since_last_sale']]

    def _generate_category_sales_features(self, hist_df):
        recent_data = hist_df
        item_to_cat = hist_df[['item_id', 'item_category_id']].drop_duplicates()
        forecast_date = recent_data[self.date_col].max() + pd.offsets.MonthBegin(1)
        last_month = forecast_date - pd.offsets.MonthBegin(1)
        
        last_month_cat_sales = (
            recent_data[(recent_data['date'] == last_month) & 
                (recent_data['item_cnt_day'] > 0)]
            .groupby('item_category_id')['item_cnt_day']
            .sum()
            .reset_index()
            .rename(columns={'item_cnt_day': 'cat_sales_last_month'})
        )
        last_month_cat_sales['had_cat_sales_last_month'] = 1

        active_months = (
            recent_data[recent_data['item_cnt_day'] > 0].groupby(['item_category_id', 'date'])['item_cnt_day']
            .sum()
            .groupby('item_category_id')
            .count()
            .reset_index()
            .rename(columns={'item_cnt_day': 'cat_active_months'})
        )
        
        grid=self._create_full_grid(hist_df, forecast_date)
        grid=grid.merge(item_to_cat, on='item_id', how='left')

        cat_sales_features = last_month_cat_sales.merge(active_months, on='item_category_id', how='outer')
        cat_sales_features.fillna({'cat_sales_last_month': 0, 'had_cat_sales_last_month': 0, 'cat_active_months': 0}, inplace=True)
        cat_sales_features = grid.merge(cat_sales_features, on='item_category_id', how='left')
        return cat_sales_features[['date', 'shop_id', 'item_id', 'cat_sales_last_month', 'had_cat_sales_last_month', 'cat_active_months']]

    def _generate_supcat_sales_features(self, hist_df):
        recent_data = hist_df
        supcat_data = self._generate_super_categories(hist_df)
        item_to_supcat = supcat_data[['item_id', 'super_category']].drop_duplicates()
        forecast_date = recent_data[self.date_col].max() + pd.offsets.MonthBegin(1)
        last_month = forecast_date - pd.offsets.MonthBegin(1)

        recent_data = recent_data.merge(item_to_supcat, on='item_id', how='left')
        last_month_cat_sales = (
            recent_data[(recent_data['date'] == last_month) & 
                (recent_data['item_cnt_day'] > 0)]
            .groupby('super_category', observed=False)['item_cnt_day']
            .sum()
            .reset_index()
            .rename(columns={'item_cnt_day': 'supcat_sales_last_month'})
        )
        last_month_cat_sales['had_supcat_sales_last_month'] = 1
        active_months = (
            recent_data[recent_data['item_cnt_day'] > 0].groupby(['super_category', 'date'], observed=False)['item_cnt_day']
            .sum()
            .groupby('super_category',observed=False)
            .count()
            .reset_index()
            .rename(columns={'item_cnt_day': 'supcat_active_months'})
        )
        
        grid=self._create_full_grid(hist_df, forecast_date)
        grid=grid.merge(item_to_supcat, on='item_id', how='left')

        cat_sales_features = last_month_cat_sales.merge(active_months, on='super_category', how='outer')
        cat_sales_features.fillna({'supcat_sales_last_month': 0, 'had_supcat_sales_last_month': 0, 'supcat_active_months': 0}, inplace=True)
        cat_sales_features = grid.merge(cat_sales_features, on='super_category', how='left')
        return cat_sales_features[['date', 'shop_id', 'item_id', 'supcat_sales_last_month', 'had_supcat_sales_last_month', 'supcat_active_months']]

    def _generate_lags(self, df):
        current_month = df[self.date_col].max() + pd.offsets.MonthBegin(1)
        group_cols = ['item_id', 'shop_id']
        
        features = pd.DataFrame(columns=group_cols)
        for lag in self.lags:
            lag_date = (current_month - pd.offsets.MonthBegin(lag))
            lag_data = df[df[self.date_col].dt.to_period('M') == lag_date.to_period('M')]
            
            if not lag_data.empty:
                lag_features = lag_data.groupby(group_cols)[self.target_col].max().reset_index()
                lag_features.rename(columns={self.target_col: f'lag_{lag}'}, inplace=True)
            else:
                unique_combinations = df[group_cols].drop_duplicates()
                lag_features = unique_combinations.copy()
                lag_features[f'lag_{lag}'] = 0

            if features.empty:
                features = lag_features
            else:
                features = features.merge(lag_features, on=group_cols, how='outer')

        features = features.fillna(0)
        features[self.date_col] = current_month

        return features

    def _generate_shop_type(self, df):
        current_month = df[self.date_col].max().to_period('M') + 1
        types = ['ТЦ', 'ТРК', 'ТРЦ', 'ТК', 'МТРЦ']
        shop_features = df[['shop_id', 'shop_name']].drop_duplicates().copy()
        shop_features['shop_type'] = shop_features['shop_name'].apply(
            lambda name: next(
                (t for t in types if re.search(r'\b' + re.escape(t) + r'\b', name, re.IGNORECASE)),
                'Other'
            )
        )
        shop_features['date'] = current_month.to_timestamp()
        
        unique_items = pd.DataFrame({'item_id': df['item_id'].unique()})
        
        shop_features['key'] = 1
        unique_items['key'] = 1
        shop_features = shop_features.merge(unique_items, on='key').drop('key', axis=1)
        
        return shop_features[['date', 'shop_id', 'item_id', 'shop_type']]

    def _generate_shop_city(self, df):
        current_month = df[self.date_col].max().to_period('M') + 1

        cities = ['москва', 'новосибирск', 'воронеж',
                'тюмень', 'уфа', 'новгород',
                'ростовнадону', 'самара', 'калуга', 'вологда',
                'курск', 'адыгея', 'красноярск', 'балашиха', 'казань',
                'томск', 'волга', 'спб', 'сургут', 'омск', 'сергиев',
                'ярославль', 'коломна']

        shop_features = df[['shop_id', 'shop_name']].drop_duplicates().copy()

        shop_features['city'] = 'Other'
        lower_names = shop_features['shop_name'].str.lower()

        for city in cities:
            shop_features.loc[lower_names.str.contains(city), 'city'] = city

        shop_features['date'] = current_month.to_timestamp()

        unique_items = pd.DataFrame({'item_id': df['item_id'].unique()})
        shop_features['key'] = 1
        unique_items['key'] = 1
        shop_features = shop_features.merge(unique_items, on='key').drop('key', axis=1)

        return shop_features[['date', 'shop_id', 'item_id', 'city']]

    def _generate_holidays(self, df):
        holidays_per_month = {
            1: 8, 2: 1, 3: 1,
            5: 2, 6: 1, 11: 1
        }
        
        current_month = df[self.date_col].max().to_period('M') + 1
        forecast_date = current_month.to_timestamp()
        month_number = current_month.month
        
        holidays = holidays_per_month.get(month_number, 0)
        
        unique_shop_items = df[['shop_id', 'item_id']].drop_duplicates()
        
        result = unique_shop_items.copy()
        result['date'] = forecast_date
        result['amt_holidays'] = holidays
        
        return result[['date', 'shop_id', 'item_id', 'amt_holidays']]

    def _generate_holidays_prev_month(self, df):
        holidays_per_month = {
            1: 8, 2: 1, 3: 1,
            5: 2, 6: 1, 11: 1
        }
        
        current_month = df[self.date_col].max().to_period('M') + 1
        forecast_date = current_month.to_timestamp()
        prev_month_number = current_month.month - 1
        
        holidays = holidays_per_month.get(prev_month_number, 0)
        
        unique_shop_items = df[['shop_id', 'item_id']].drop_duplicates()
        
        result = unique_shop_items.copy()
        result['date'] = forecast_date
        result['amt_holidays_prev'] = holidays
        
        return result[['date', 'shop_id', 'item_id', 'amt_holidays_prev']]

    def _generate_weekends(self, df):
        current_month = df[self.date_col].max().to_period('M') + 1
        forecast_date = current_month.to_timestamp()
        
        days_in_month = current_month.days_in_month
        month_dates = pd.date_range(start=forecast_date, periods=days_in_month, freq='D')
        
        weekends = sum(1 for d in month_dates if d.weekday() >= 5)
        
        unique_shop_items = df[['shop_id', 'item_id']].drop_duplicates()
        
        result = unique_shop_items.copy()
        result['date'] = forecast_date
        result['amt_weekends'] = weekends
        
        return result[['date', 'shop_id', 'item_id', 'amt_weekends']]
    
    def _generate_season(self, df):
        current_month = df[self.date_col].max().to_period('M') + 1
        forecast_date = current_month.to_timestamp()
        
        month = forecast_date.month
        season_name = (
            'winter' if month in [12, 1, 2] else
            'spring' if month in [3, 4, 5] else
            'summer' if month in [6, 7, 8] else
            'autumn'
        )
        
        season = (df[['shop_id', 'item_id']].drop_duplicates().assign(
                date=forecast_date,season=pd.Categorical(
                    [season_name] * len(df[['shop_id', 'item_id']].drop_duplicates()),
                    categories=['winter', 'spring', 'summer', 'autumn'],
                    ordered=False)))
        
        return season[['date', 'shop_id', 'item_id', 'season']]

    def _generate_average_cnt_month(self, df):
        current_month = df[self.date_col].max().to_period('M') + 1
        current_timestamp = current_month.to_timestamp()
        current_month_num = current_month.month

        avg = df.groupby(['date__month_of_year'])['item_cnt_month'].mean().reset_index()
        avg.rename(columns={'item_cnt_month': 'average_cnt_month'}, inplace=True)

        min_avg = avg['average_cnt_month'].min()
        max_avg = avg['average_cnt_month'].max()
        avg['average_cnt_month_norm'] = (avg['average_cnt_month'] - min_avg) / (max_avg - min_avg)

        avg = avg[avg['date__month_of_year'] == current_month_num].copy()
        avg['date'] = current_timestamp

        unique_items = pd.DataFrame({'item_id': df['item_id'].unique()})
        unique_shops = pd.DataFrame({'shop_id': df['shop_id'].unique()})
        unique_items['key'] = 1
        unique_shops['key'] = 1
        full_grid = unique_items.merge(unique_shops, on='key').drop('key', axis=1)
        full_grid['date'] = current_timestamp

        result = full_grid.merge(avg, on=['date'], how='left').fillna(0)
        
        return result[['date', 'shop_id', 'item_id', 'average_cnt_month_norm']]

    def _generate_category_price_segment(self, df):
        current_month = df[self.date_col].max().to_period('M') + 1
        forecast_date = current_month.to_timestamp()

        cat_prices = df.groupby(['shop_id', 'item_category_id'])['item_price'].mean().reset_index()
        
        non_zero_prices = cat_prices.loc[cat_prices['item_price'] > 0, 'item_price']
        price_q85 = non_zero_prices.quantile(0.85)
        price_q98 = non_zero_prices.quantile(0.98)

        bins = [0, price_q85, price_q98, np.inf]

        cat_prices['price_segment'] = pd.cut(
            cat_prices['item_price'], bins=bins,
            labels=['cheap', 'mid', 'expensive'],
            include_lowest=True
        )
        cat_prices['price_segment'] = pd.Categorical(
            cat_prices['price_segment'],
            categories=['cheap', 'mid', 'expensive'],
            ordered=True
        )
        cat_prices['date'] = forecast_date

        mapping = df[['shop_id', 'item_id', 'item_category_id']].drop_duplicates()
        mapping = mapping.merge(
            cat_prices[['shop_id', 'item_category_id', 'price_segment', 'date']],
            on=['shop_id', 'item_category_id'],
            how='left'
        )
        mapping = mapping.rename(columns={'price_segment': 'category_price_segment'})
        
        result = mapping[['date', 'shop_id', 'item_id', 'category_price_segment']]
        return result

    def _generate_supercat_price_segment(self, df):

        current_month = df[self.date_col].max().to_period('M') + 1
        forecast_date = current_month.to_timestamp()

        df_reduced = df[['item_id', 'shop_id', 'item_price', self.date_col]].copy()

        supcat_df = self._generate_super_categories(df)[['item_id', 'super_category']].drop_duplicates().copy()
        supcat_df['super_category'] = supcat_df['super_category'].astype('category')

        df_reduced = df_reduced.merge(supcat_df, on='item_id', how='left')

        supercat_prices = (df_reduced.groupby(['shop_id', 'super_category'], observed=False)['item_price']
            .mean().reset_index())

        del df_reduced

        non_zero_prices = supercat_prices.loc[supercat_prices['item_price'] > 0, 'item_price']
        price_q85 = non_zero_prices.quantile(0.85)
        price_q98 = non_zero_prices.quantile(0.98)
        bins = [0, price_q85, price_q98, np.inf]

        supercat_prices['price_segment'] = pd.cut(supercat_prices['item_price'], bins=bins,
            labels=['cheap', 'mid', 'expensive'], include_lowest=True)

        supercat_prices['price_segment'] = supercat_prices['price_segment'].astype('category')
        supercat_prices['date'] = forecast_date

        mapping = supcat_df.merge(df[['shop_id', 'item_id']].drop_duplicates(), on='item_id', how='left')
        mapping = mapping.merge(
            supercat_prices[['shop_id', 'super_category', 'price_segment', 'date']],
            on=['shop_id', 'super_category'], how='left'
        )
        mapping = mapping.rename(columns={'price_segment': 'supercat_price_segment'})

        result = mapping[['date', 'shop_id', 'item_id', 'supercat_price_segment']]
        return result

    def _generate_price_segment(self, df):
        current_month = df[self.date_col].max().to_period('M') + 1
        forecast_date = current_month.to_timestamp()

        item_prices = df.groupby(['shop_id', 'item_id'])['item_price'].mean().reset_index()
        non_zero_prices = item_prices.loc[item_prices['item_price'] > 0, 'item_price']

        price_q85 = non_zero_prices.quantile(0.85)
        price_q98 = non_zero_prices.quantile(0.98)

        bins = [0, price_q85, price_q98, np.inf]

        item_prices['price_segment'] = pd.cut(item_prices['item_price'], bins=bins,
            labels=['cheap', 'mid', 'expensive'], include_lowest=True)

        item_prices['price_segment'] = pd.Categorical(item_prices['price_segment'],
            categories=['cheap', 'mid', 'expensive'], ordered=True)

        item_prices['date'] = forecast_date

        result = item_prices[['date', 'shop_id', 'item_id', 'price_segment']]
        return result

    def _generate_categorical_month_of_year(self, df):
        current_month = df[self.date_col].max().to_period('M') + 1
        forecast_date = current_month.to_timestamp()

        unique_items = pd.DataFrame({'item_id': df['item_id'].unique()})
        unique_shops = pd.DataFrame({'shop_id': df['shop_id'].unique()})
        unique_items['key'] = 1
        unique_shops['key'] = 1
        full_grid = unique_items.merge(unique_shops, on='key').drop('key', axis=1)
        full_grid['date'] = forecast_date

        month_name = forecast_date.strftime('%B')
        month_categories = ['January', 'February', 'March', 'April', 'May', 'June',
                            'July', 'August', 'September', 'October', 'November', 'December']
        full_grid['cat_month_of_year'] = pd.Categorical(
            [month_name] * len(full_grid),
            categories=month_categories,
            ordered=True
        )
        
        return full_grid[['date', 'shop_id', 'item_id', 'cat_month_of_year']]

    def _generate_categorical_year(self, df):
        current_month = df[self.date_col].max().to_period('M') + 1
        forecast_date = current_month.to_timestamp()

        unique_items = pd.DataFrame({'item_id': df['item_id'].unique()})
        unique_shops = pd.DataFrame({'shop_id': df['shop_id'].unique()})
        unique_items['key'] = 1
        unique_shops['key'] = 1
        full_grid = unique_items.merge(unique_shops, on='key').drop('key', axis=1)
        full_grid['date'] = forecast_date

        year_str = str(forecast_date.year)
        full_grid['cat_year'] = pd.Categorical(
            [year_str] * len(full_grid),
            categories=[year_str],
            ordered=True
        )
        
        return full_grid[['date', 'shop_id', 'item_id', 'cat_year']]

    def _generate_item_category(self, df):
        current_month = df[self.date_col].max().to_period('M') + 1
        forecast_date = current_month.to_timestamp()

        unique_items = pd.DataFrame({'item_id': df['item_id'].unique()})
        unique_shops = pd.DataFrame({'shop_id': df['shop_id'].unique()})
        unique_items['key'] = 1
        unique_shops['key'] = 1
        full_grid = unique_items.merge(unique_shops, on='key').drop('key', axis=1)
        full_grid['date'] = forecast_date

        item_cat = df[['item_id', 'item_category_name']].drop_duplicates(subset=['item_id'])
        
        full_grid = full_grid.merge(item_cat, on='item_id', how='left')
        full_grid['item_category'] = full_grid['item_category_name'].astype('category')
        
        return full_grid[['date', 'shop_id', 'item_id', 'item_category']]

    def _generate_cyclic_month_features(self, df):
        current_month = df[self.date_col].max().to_period('M') + 1
        forecast_date = current_month.to_timestamp()

        unique_items = pd.DataFrame({'item_id': df['item_id'].unique()})
        unique_shops = pd.DataFrame({'shop_id': df['shop_id'].unique()})
        unique_items['key'] = 1
        unique_shops['key'] = 1
        full_grid = unique_items.merge(unique_shops, on='key').drop('key', axis=1)
        full_grid['date'] = forecast_date

        full_grid['date'] = pd.to_datetime(full_grid['date'])

        full_grid['month_sin'] = np.sin(2 * np.pi * full_grid['date'].dt.month / 12)
        full_grid['month_cos'] = np.cos(2 * np.pi * full_grid['date'].dt.month / 12)
        
        return full_grid[['date', 'shop_id', 'item_id', 'month_sin', 'month_cos']]

    def _generate_sma(self, hist_df, window=3):

        df_sorted = hist_df.sort_values(by='date').copy()
        grouped = df_sorted.groupby(['shop_id', 'item_id'])
        
        df_sorted['sma'] = (grouped['item_cnt_month'].rolling(window=window, min_periods=1)
            .mean().reset_index(level=[0,1], drop=True))
        
        forecast_date = df_sorted['date'].max() + pd.offsets.MonthBegin(1)
        latest_sma = df_sorted.groupby(['shop_id', 'item_id'])['sma'].last().reset_index()
        
        grid = self._create_full_grid(hist_df, forecast_date)
        grid = grid.merge(latest_sma, on=['shop_id', 'item_id'], how='left')
        
        return grid[['date', 'shop_id', 'item_id', 'sma']].fillna(0)

    def _generate_category_sales(self, hist_df):
        cat_sales = hist_df.groupby('item_category_id')['item_cnt_day']\
            .sum().reset_index(name='cat_total_sales')
        
        quantiles = np.linspace(0, 1, 4)
        bins = cat_sales['cat_total_sales'].quantile(quantiles).values
        bins = np.unique(bins)
        n_bins = len(bins) - 1
        
        if n_bins < 1:
            cat_sales['cat_sales_cat'] = 'low'
        else:
            if n_bins == 1:
                labels = ['low']
            elif n_bins == 2:
                labels = ['low', 'high']
            else:
                labels = ['low', 'mid', 'high'][:n_bins]
            cat_sales['cat_sales_cat'] = pd.cut(cat_sales['cat_total_sales'],
            bins=bins,labels=labels,include_lowest=True)
        
        forecast_date = hist_df[self.date_col].max() + pd.offsets.MonthBegin(1)
        
        grid = self._create_full_grid(hist_df, forecast_date)
        item_cat = hist_df[['item_id', 'item_category_id']].drop_duplicates()
        grid = grid.merge(item_cat, on='item_id', how='left')
        grid = grid.merge(cat_sales[['item_category_id', 'cat_sales_cat']],
                        on='item_category_id', how='left')
        grid['cat_sales_cat'] = grid['cat_sales_cat'].astype('category')
        
        return grid[['date', 'shop_id', 'item_id', 'cat_sales_cat']]

    def _generate_shop_sales(self, hist_df):
        shop_sales = hist_df.groupby('shop_id')['item_cnt_day'].sum().reset_index(name='total_sales')
        
        quantiles = np.linspace(0, 1, 4)
        bins = shop_sales['total_sales'].quantile(quantiles).values
        bins = np.unique(bins)
        n_bins = len(bins) - 1
        
        if n_bins < 1:
            shop_sales['shop_sales_cat'] = 'low'
        else:
            if n_bins == 1:
                labels = ['low']
            elif n_bins == 2:
                labels = ['low', 'high']
            else:
                labels = ['low', 'mid', 'high'][:n_bins]
            shop_sales['shop_sales_cat'] = pd.cut(
                shop_sales['total_sales'], 
                bins=bins, 
                labels=labels, 
                include_lowest=True
            )
        
        forecast_date = hist_df[self.date_col].max() + pd.offsets.MonthBegin(1)
        
        grid = self._create_full_grid(hist_df, forecast_date)
        grid = grid.merge(shop_sales[['shop_id', 'shop_sales_cat']], on='shop_id', how='left')
        grid['shop_sales_cat'] = grid['shop_sales_cat'].astype('category')
        
        return grid[['date', 'shop_id', 'item_id', 'shop_sales_cat']]
   
    def _generate_super_categories(self, hist_df):
        category_mapping = {
            'accessories': ['гарнитуры', 'аксессуары'],
            'consoles': ['консоли'],
            'films': ['кино'],
            'books': ['книги'],
            'music': ['музыка'],
            'gifts': ['подарки', 'билеты', 'служебные', 'карты'],
            'applications': ['программы'],
            'other': ['носители', 'элементы', 'доставка']
        }

        reverse_mapping = {}
        for super_cat, keywords in category_mapping.items():
            for keyword in keywords:
                reverse_mapping[keyword] = super_cat

        hist_df = hist_df.copy()
        hist_df['clean_category'] = (hist_df['item_category_name'].str.lower().fillna('other')
            .str.replace('[^а-яa-z]', '', regex=True))

        def map_category(name):
            for keyword, super_cat in reverse_mapping.items():
                if keyword in name:
                    return super_cat
            return 'other'

        hist_df['super_category'] = (hist_df['clean_category'].apply(map_category).astype('category'))
        forecast_date = hist_df[self.date_col].max() + pd.offsets.MonthBegin(1)
        grid = self._create_full_grid(hist_df, forecast_date)

        item_categories = (hist_df[['item_id', 'super_category']].drop_duplicates('item_id').set_index('item_id'))
        grid = grid.join(item_categories, on='item_id', how='left')
        grid['super_category'] = (grid['super_category'].fillna('other').astype('category'))

        return grid[['date', 'shop_id', 'item_id', 'super_category']]

    def _generate_cat_cnt_prev_year(self, hist_df):
        forecast_date = hist_df['date'].max() + pd.offsets.MonthBegin(1)
        
        prev_year_start = forecast_date - pd.DateOffset(years=1)
        prev_year_end = prev_year_start + pd.offsets.MonthBegin(1)
        
        prev_year_data = hist_df[(hist_df['date'] >= prev_year_start) & (hist_df['date'] < prev_year_end)]
        
        cat_cnt_prev_year = prev_year_data.groupby('item_category_id')['item_cnt_day'].sum().reset_index()
        cat_cnt_prev_year.rename(columns={'item_cnt_day': 'cat_cnt_prev_year'}, inplace=True)
        
        mapping = hist_df[['item_id', 'item_category_id']].drop_duplicates()
        
        cat_cnt_prev_with_item = mapping.merge(cat_cnt_prev_year, on='item_category_id', how='left')
        cat_cnt_prev_with_item['cat_cnt_prev_year'] = cat_cnt_prev_with_item['cat_cnt_prev_year'].fillna(0)
        
        grid = self._create_full_grid(hist_df, forecast_date)
        
        grid = grid.merge(cat_cnt_prev_with_item[['item_id', 'cat_cnt_prev_year']], on='item_id', how='left')
        grid['cat_cnt_prev_year'] = grid['cat_cnt_prev_year'].fillna(0)
        
        return grid[['date', 'shop_id', 'item_id', 'cat_cnt_prev_year']]

    def _generate_supercat_cnt_prev_year(self, hist_df):
        
        forecast_date = hist_df['date'].max() + pd.offsets.MonthBegin(1)
        prev_year_start = forecast_date - pd.DateOffset(years=1)
        prev_year_end = prev_year_start + pd.offsets.MonthBegin(1)
        
        supcat_mapping = (self._generate_super_categories(hist_df)
                        [['item_id', 'super_category']]
                        .drop_duplicates()
                        .set_index('item_id')['super_category']
                        .to_dict())
        
        hist = hist_df[['date', 'item_id', 'item_cnt_day']].copy()
        hist['super_category'] = hist['item_id'].map(supcat_mapping)
        
        prev_year_data = hist[(hist['date'] >= prev_year_start) & (hist['date'] < prev_year_end)]
        
        supercat_cnt = prev_year_data.groupby('super_category', observed=True)['item_cnt_day'].sum()
        
        grid = self._create_full_grid(hist_df, forecast_date)[['date', 'shop_id', 'item_id']]
        grid['super_category'] = grid['item_id'].map(supcat_mapping)
        grid['supercat_cnt_prev_year'] = grid['super_category'].map(supercat_cnt).fillna(0).astype('float32')
        
        return grid[['date', 'shop_id', 'item_id', 'supercat_cnt_prev_year']]


    def _generate_holiday_category_boost(self, hist_df):
        holiday_months = {2, 3, 11, 12}
        
        hist_df = hist_df.copy()
        hist_df['is_holiday_month'] = hist_df['date__month_of_year'].isin(holiday_months)

        holiday_stats = (hist_df.groupby(['item_category_id', 'is_holiday_month'])['item_cnt_day'].agg(['mean', 'count']).reset_index())
        
        holiday_mean = holiday_stats[holiday_stats['is_holiday_month'] == 1][['item_category_id', 'mean']]
        normal_mean = holiday_stats[holiday_stats['is_holiday_month'] == 0][['item_category_id', 'mean']]
        
        boost_df = pd.merge(
            holiday_mean.rename(columns={'mean': 'mean_holiday'}),
            normal_mean.rename(columns={'mean': 'mean_normal'}),
            on='item_category_id',
            how='outer'
        ).fillna(0)

        boost_df['holiday_boost'] = (
            (boost_df['mean_holiday'] - boost_df['mean_normal']) / 
            (boost_df['mean_normal'] + 1e-6)
        )

        forecast_date = hist_df['date'].max() + pd.offsets.MonthBegin(1)
        forecast_month = forecast_date.month
        grid = self._create_full_grid(hist_df, forecast_date)
        
        mapping = hist_df[['item_id', 'item_category_id']].drop_duplicates()
        grid = grid.merge(mapping, on='item_id', how='left')
        grid['is_holiday_month'] = (forecast_month in holiday_months)
        result = grid.merge(boost_df[['item_category_id', 'holiday_boost']], on='item_category_id',how='left').fillna(0)

        return result[['date', 'shop_id', 'item_id', 'holiday_boost']]

    def _generate_category_seasonality(self, hist_df):
        season_mapping = {
            12: 'winter', 1: 'winter', 2: 'winter',
            3: 'spring', 4: 'spring', 5: 'spring',
            6: 'summer', 7: 'summer', 8: 'summer',
            9: 'autumn', 10: 'autumn', 11: 'autumn'
        }
        
        hist_df = hist_df.copy()
        hist_df['season'] = hist_df['date__month_of_year'].map(season_mapping)

        seasonality = (hist_df.groupby(['item_category_id', 'season'])['item_cnt_day'].agg(['mean', 'std']).reset_index().rename(columns={
                'mean': 'cat_season_mean',
                'std': 'cat_season_std'}))

        forecast_date = hist_df['date'].max() + pd.offsets.MonthBegin(1)
        forecast_month = forecast_date.month
        current_season = season_mapping[forecast_month]

        seasonality = seasonality[seasonality['season'] == current_season]

        grid = self._create_full_grid(hist_df, forecast_date)
        mapping = hist_df[['item_id', 'item_category_id']].drop_duplicates()
        
        return (
            grid.merge(mapping, on='item_id', how='left')
            .merge(seasonality[['item_category_id', 'cat_season_mean', 'cat_season_std']], 
                    on='item_category_id', how='left')
            .fillna(0)
            [['date', 'shop_id', 'item_id', 'cat_season_mean', 'cat_season_std']]
        )

    def _generate_last_month_sales_bin(self, hist_df, n_bins=5):

        forecast_date = hist_df['date'].max() + pd.offsets.MonthBegin(1)
        last_month = forecast_date - pd.offsets.MonthBegin(1)

        last_month_sales = (
            hist_df[hist_df['date'] == last_month]
            .groupby('item_id')['item_cnt_day']
            .sum()
            .reset_index()
            .rename(columns={'item_cnt_day': 'last_month_sales'}))
        
        last_month_sales['last_month_sales_bin'] = pd.qcut(
            last_month_sales['last_month_sales'],
            q=n_bins,
            labels=False,
            duplicates='drop'
        )

        grid = self._create_full_grid(hist_df, forecast_date)
        
        result = grid.merge(last_month_sales[['item_id', 'last_month_sales_bin']],
            on='item_id', how='left').fillna(-1)

        return result[['date', 'shop_id', 'item_id', 'last_month_sales_bin']]

    def _generate_supercategory_sales(self, hist_df):

        supcat_df = self._generate_super_categories(hist_df)[['item_id', 'super_category']]
        
        item_sales = hist_df.groupby('item_id', observed=False)['item_cnt_day'].sum().reset_index()
        item_sales = item_sales.merge(supcat_df, on='item_id', how='left')
        
        cat_sales = item_sales.groupby('super_category', observed=False)['item_cnt_day'] \
            .sum().reset_index(name='supercat_total_sales')

        quantiles = np.linspace(0, 1, 4)
        bins = np.unique(cat_sales['supercat_total_sales'].quantile(quantiles).values)
        n_bins = len(bins) - 1

        if n_bins < 1:
            cat_sales['supercat_sales_cat'] = 'low'
        else:
            labels = ['low', 'mid', 'high'][:n_bins] if n_bins > 1 else ['low']
            cat_sales['supercat_sales_cat'] = pd.cut(
                cat_sales['supercat_total_sales'], bins=bins, labels=labels, include_lowest=True
            )

        forecast_date = hist_df[self.date_col].max() + pd.offsets.MonthBegin(1)
        grid = self._create_full_grid(hist_df, forecast_date)
        grid = grid.merge(supcat_df.drop_duplicates(), on='item_id', how='left')
        grid = grid.merge(cat_sales[['super_category', 'supercat_sales_cat']], 
                        on='super_category', how='left')
        
        grid['supercat_sales_cat'] = grid['supercat_sales_cat'].astype('category')

        return grid[['date', 'shop_id', 'item_id', 'supercat_sales_cat']]

    def _generate_supercategory_seasonality(self, hist_df):
        cols_needed = ['date', 'item_id', 'shop_id', 'item_category_name', 'date__month_of_year', 'item_cnt_day']
        hist_df = hist_df[cols_needed].copy()
        
        supcat_df = self._generate_super_categories(hist_df)[['item_id', 'super_category']].drop_duplicates()
        
        forecast_date = hist_df['date'].max() + pd.offsets.MonthBegin(1)
        current_season = self._get_season(forecast_date.month)
        
        supcat_df['super_category'] = supcat_df['super_category'].astype('category')
        hist_df['date__month_of_year'] = hist_df['date__month_of_year'].astype('int8')
        
        merged = hist_df.merge(
            supcat_df,
            on='item_id',
            how='left',
            validate='many_to_one'
        )
        
        merged['season'] = merged['date__month_of_year'].apply(
            lambda x: self._get_season(x)
        ).astype('category')
        
        filtered = merged[merged['season'] == current_season]
        
        season_stats = filtered.groupby(
            'super_category', 
            observed=True, 
            as_index=False
        ).agg(supercat_season_mean=('item_cnt_day', 'mean'))
        
        grid = self._create_full_grid(hist_df, forecast_date)
        grid = grid.merge(
            supcat_df,
            on='item_id',
            how='left',
            validate='many_to_one'
        )
        
        result = grid.merge(
            season_stats,
            on='super_category',
            how='left'
        )
        
        return result[['date', 'shop_id', 'item_id', 'supercat_season_mean']]

    @staticmethod
    def _get_season(month):
        return {
            12: 'winter', 1: 'winter', 2: 'winter',
            3: 'spring', 4: 'spring', 5: 'spring',
            6: 'summer', 7: 'summer', 8: 'summer',
            9: 'autumn', 10: 'autumn', 11: 'autumn'
        }[month]

    def _generate_holiday_supercategory_boost(self, hist_df):
        holiday_months = {2, 3, 11, 12}

        supcat_mapping = self._generate_super_categories(hist_df).set_index('item_id')['super_category']
        supcat_mapping = supcat_mapping.drop_duplicates()

        hist_df = hist_df.copy()
        hist_df['super_category'] = hist_df['item_id'].map(supcat_mapping)
        
        df_group = hist_df[['super_category', 'date__month_of_year', 'item_cnt_day']].copy()
        df_group['is_holiday_month'] = df_group['date__month_of_year'].isin(holiday_months)

        holiday_stats = (
            df_group.groupby(['super_category', 'is_holiday_month'], observed=False)['item_cnt_day']
            .agg(['mean', 'count'])
            .reset_index()
        )

        holiday_mean = holiday_stats.loc[holiday_stats['is_holiday_month'] == True, ['super_category', 'mean']]
        normal_mean  = holiday_stats.loc[holiday_stats['is_holiday_month'] == False, ['super_category', 'mean']]

        boost_df = pd.merge(
            holiday_mean.rename(columns={'mean': 'mean_holiday'}),
            normal_mean.rename(columns={'mean': 'mean_normal'}),
            on='super_category',
            how='outer'
        )

        boost_df[['mean_holiday', 'mean_normal']] = boost_df[['mean_holiday', 'mean_normal']].fillna(0)
        boost_df['supcat_holiday_boost'] = (
            (boost_df['mean_holiday'] - boost_df['mean_normal']) / (boost_df['mean_normal'] + 1e-6)
        )

        forecast_date = hist_df['date'].max() + pd.offsets.MonthBegin(1)
        forecast_month = forecast_date.month

        grid = self._create_full_grid(hist_df, forecast_date)
        
        grid['super_category'] = grid['item_id'].map(supcat_mapping)
        grid['super_category'] = grid['super_category'].astype(str).fillna('unknown')
        grid['is_holiday_month'] = forecast_month in holiday_months

        result = grid.merge(boost_df[['super_category', 'supcat_holiday_boost']], on='super_category', how='left')
        result['supcat_holiday_boost'] = result['supcat_holiday_boost'].fillna(0)

        lag_features = result.copy()

        for lag in self.lags:
            lag_month = forecast_date - pd.offsets.MonthBegin(lag)

            lag_data = hist_df[hist_df['date'] == lag_month].copy()
            lag_data['super_category'] = lag_data['item_id'].map(supcat_mapping)

            lag_stat = lag_data.groupby('super_category', observed=False)['item_cnt_day'].sum().reset_index()
            lag_stat.rename(columns={'item_cnt_day': f'supcat_holiday_boost_lag_{lag}'}, inplace=True)

            lag_features = lag_features.merge(lag_stat, on='super_category', how='left')

        lag_features.fillna(0, inplace=True)

        return lag_features[['date', 'shop_id', 'item_id', 'supcat_holiday_boost'] + 
                            [f'supcat_holiday_boost_lag_{lag}' for lag in self.lags]]

    def _generate_price_segment_sales_lags(self, hist_df):
        forecast_date = hist_df[self.date_col].max() + pd.offsets.MonthBegin(1)
        price_segment_df = self._generate_price_segment(hist_df)

        lag_features = price_segment_df.copy()

        for lag in self.lags:
            last_month = forecast_date - pd.offsets.MonthBegin(lag)

            last_month_sales = (
                hist_df[hist_df[self.date_col] == last_month]
                .groupby(['item_id', 'shop_id'])['item_cnt_day']
                .sum()
                .reset_index()
            )

            last_month_sales = last_month_sales.merge(price_segment_df, on=['item_id', 'shop_id'], how='left')

            segment_sales = (
                last_month_sales
                .groupby('price_segment', observed=False)['item_cnt_day']
                .sum()
                .reset_index()
                .rename(columns={'item_cnt_day': f'last_month_ps_sales_{lag}'})
            )

            lag_features = lag_features.merge(segment_sales, on='price_segment', how='left')

        return lag_features[['date', 'shop_id', 'item_id'] + [f'last_month_ps_sales_{lag}' for lag in self.lags]].fillna(0)

    def _generate_shop_type_sales_lags(self, hist_df):
        forecast_date = hist_df[self.date_col].max() + pd.offsets.MonthBegin(1)
        shop_type_df = self._generate_shop_type(hist_df)

        lag_features = shop_type_df.copy()

        for lag in self.lags:
            last_month = forecast_date - pd.offsets.MonthBegin(lag)

            last_month_sales = (
                hist_df[hist_df[self.date_col] == last_month]
                .groupby(['item_id', 'shop_id'])['item_cnt_day']
                .sum()
                .reset_index()
            )

            last_month_sales = last_month_sales.merge(shop_type_df, on=['item_id', 'shop_id'], how='left')

            segment_sales = (
                last_month_sales
                .groupby('shop_type', observed=False)['item_cnt_day']
                .sum()
                .reset_index()
                .rename(columns={'item_cnt_day': f'shop_type_sales_lag_{lag}'})
            )

            lag_features = lag_features.merge(segment_sales, on='shop_type', how='left')

        return lag_features[['date', 'shop_id', 'item_id'] + [f'shop_type_sales_lag_{lag}' for lag in self.lags]].fillna(0)


    def _generate_city_sales_lags(self, hist_df):
        forecast_date = hist_df[self.date_col].max() + pd.offsets.MonthBegin(1)
        city_df = self._generate_shop_city(hist_df)
        grid = self._create_full_grid(hist_df, forecast_date)

        lag_features = pd.DataFrame()
        
        for lag in self.lags:
            last_month = forecast_date - pd.offsets.MonthBegin(lag)

            last_month_sales = (
                hist_df[hist_df[self.date_col] == last_month]
                .groupby(['item_id', 'shop_id'])['item_cnt_day']
                .sum()
                .reset_index()
            )

            last_month_sales = last_month_sales.merge(city_df, on=['item_id', 'shop_id'], how='left')
            last_month_sales[f'city_sales_lag_{lag}'] = last_month_sales.groupby('city')['item_cnt_day'].transform('sum')
            last_month_sales = last_month_sales[['date', 'shop_id', 'item_id', f'city_sales_lag_{lag}']]

            if lag_features.empty:
                lag_features = last_month_sales
            else:
                lag_features = lag_features.merge(last_month_sales, on=['date', 'shop_id', 'item_id'], how='left')

        return lag_features.fillna(0)


    def _generate_frequency_features(self, hist_df):
        total_items = hist_df['item_id'].nunique()
        forecast_date = hist_df[self.date_col].max() + pd.offsets.MonthBegin(1)
        last_month = forecast_date - pd.offsets.MonthBegin(1)
        grid = self._create_full_grid(hist_df, forecast_date)

        city_df = self._generate_shop_city(hist_df)
        last_month_sales = hist_df[hist_df[self.date_col] == last_month].groupby(['item_id', 'shop_id'])['item_cnt_day'].sum().reset_index()
        last_month_sales = last_month_sales.merge(city_df, on=['item_id','shop_id'], how='left').drop_duplicates()

        city_counts = (
            last_month_sales[last_month_sales['item_cnt_day']>0].groupby('city')['item_id']
            .nunique()
            .reset_index()
            .rename(columns={'item_id': 'city_item_count'})
        )
        city_counts['city_frequency'] = city_counts['city_item_count'] / total_items
        
        result_city = last_month_sales.merge(city_counts[['city', 'city_frequency']], on='city', how='left')[['shop_id', 'item_id', 'date','city_frequency']]
        
        shop_type_df = self._generate_shop_type(hist_df)
        last_month_sales = hist_df[hist_df[self.date_col] == last_month].groupby(['item_id', 'shop_id'])['item_cnt_day'].sum().reset_index()
        last_month_sales = last_month_sales.merge(shop_type_df, on=['item_id','shop_id'], how='left').drop_duplicates()
        shop_type_counts = (
            last_month_sales[last_month_sales['item_cnt_day']>0].groupby('shop_type')['item_id']
            .nunique()
            .reset_index()
            .rename(columns={'item_id': 'shop_type_item_count'})
        )
        shop_type_counts['shop_type_frequency'] = shop_type_counts['shop_type_item_count'] / total_items
        result_shop_type = last_month_sales.merge(shop_type_counts[['shop_type', 'shop_type_frequency']], on='shop_type', how='left')[['shop_id', 'item_id', 'date','shop_type_frequency']]
        result = pd.merge(result_city, result_shop_type, on=['shop_id', 'item_id', 'date'], how='left')

        return result[['shop_id', 'item_id', 'date', 'shop_type_frequency', 'city_frequency']]

    def _create_full_grid(self, df, forecast_date):
        return pd.MultiIndex.from_product(
            [
                df['shop_id'].unique(),
                df['item_id'].unique(),
                [forecast_date]
            ],
            names=['shop_id', 'item_id', 'date']
        ).to_frame(index=False)