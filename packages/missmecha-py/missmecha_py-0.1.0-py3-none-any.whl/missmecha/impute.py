import numpy as np
import pandas as pd
from collections import defaultdict

class SimpleSmartImputer:
    def __init__(self, categorical_cols=None, verbose=True):
        """
        Parameters:
        - categorical_cols: Optional[List[str]]
            Manually specify which columns are categorical.
        - verbose: bool
            If True, prints out how each column is treated.
        """
        self.categorical_cols = categorical_cols
        self.verbose = verbose
        self.fill_values = {}
        self.col_types = {}  # 'numerical' or 'categorical'

    def _infer_column_types(self, df):
        inferred = {}
        for col in df.columns:
            if self.categorical_cols is not None:
                inferred[col] = 'categorical' if col in self.categorical_cols else 'numerical'
            elif pd.api.types.is_string_dtype(df[col]) or pd.api.types.is_categorical_dtype(df[col]):
                inferred[col] = 'categorical'
            else:
                inferred[col] = 'numerical'
        return inferred

    def fit(self, df):
        if not isinstance(df, pd.DataFrame):
            raise ValueError("Input must be a pandas DataFrame.")

        self.col_types = self._infer_column_types(df)

        for col, col_type in self.col_types.items():
            if col_type == 'numerical':
                self.fill_values[col] = df[col].mean()
            else:
                self.fill_values[col] = df[col].mode(dropna=True)[0]

            if self.verbose:
                print(f"[{self.__class__.__name__}] Column '{col}' treated as {col_type}. Fill value = {self.fill_values[col]}")

        return self

    def transform(self, df):
        if not isinstance(df, pd.DataFrame):
            raise ValueError("Input must be a pandas DataFrame.")

        df_filled = df.copy()
        for col in df.columns:
            if col in self.fill_values:
                df_filled[col] = df[col].fillna(self.fill_values[col])
        return df_filled

    def fit_transform(self, df):
        return self.fit(df).transform(df)
