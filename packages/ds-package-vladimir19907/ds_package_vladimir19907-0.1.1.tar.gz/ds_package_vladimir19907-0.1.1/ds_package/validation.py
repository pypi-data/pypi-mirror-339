import pandas as pd

class CV:
    """
    Provides an expanding window split for monthly time series data.
    The last 'test_size' months are always used as the final test set.
    """
    def __init__(self, df, date_col='date', min_train_size=3, val_size=1, test_size=1, skip_months=12):
        self.df = df.copy()
        self.date_col = date_col
        self.min_train_size = min_train_size
        self.val_size = val_size
        self.test_size = test_size
        self.skip_months = skip_months

        if self.date_col not in self.df.columns:
            raise ValueError(f"DataFrame must contain '{self.date_col}' column")
    
        self.df[self.date_col] = pd.to_datetime(self.df[self.date_col]).dt.normalize()
        self.months = pd.date_range(start=self.df[self.date_col].min(), end=self.df[self.date_col].max(), freq='MS')
        if len(self.months) < self.min_train_size + self.test_size:
            raise ValueError("Not enough months for min_train_size + test_size")

    def get_hist_df(self, month):
        month_period = pd.to_datetime(month).to_period('M')
        return self.df[self.df[self.date_col].dt.to_period('M') < month_period].copy()

    def get_target_df(self, month, target_col, drop_cols):
        month_period = pd.to_datetime(month).to_period('M')
        mask = self.df[self.date_col].dt.to_period('M') == month_period
        filtered_df = self.df.loc[mask]
        
        index_df = filtered_df.drop(columns=[target_col], errors='ignore')
        target_series = filtered_df[target_col]
        
        index_df.drop(columns=drop_cols, errors='ignore', inplace=True)

        return index_df, target_series

    def split(self):
        months = self.months[self.skip_months:]
        train_months = months[:self.min_train_size]
        val_months = months[self.min_train_size:-(self.test_size + self.val_size)+1]
        test_months = months[-self.test_size:]
        return train_months, val_months, test_months

    def get_n_splits(self):
        return len(self.split())
