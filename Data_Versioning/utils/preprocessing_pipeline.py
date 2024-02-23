#!/usr/bin/env python3

import pandas as pd
import numpy as np

from sklearn.compose import make_column_transformer
from sklearn.preprocessing import FunctionTransformer, OneHotEncoder, OrdinalEncoder


def preprocessing_pipeline(numeric_features_to_extract, ordinal_features, categorical_features, passthrough_feature, drop_features):
    """
    Perform pre-processing steps for features and return a numeric representation of all features for model training.

    Parameters:
    - numeric_features_to_extract (list): List of column names containing numeric features to extract.
    - ordinal_features (list): List of column names containing ordinal features to transform.
    - categorical_features (list): List of column names containing categorical features to transform.
    - passthrough_feature (list): List of column names to skip over during pre-processing.
    - drop_features (list): List of column names to drop during pre-processing.

    Returns:
    - column_transformer (ColumnTransformer): Scikit-learn ColumnTransformer object defining the pre-processing steps.
    """

    def extract_numeric_features(X, columns_to_extract):
        """
        Extract numeric features from specified columns by converting strings to numeric values.

        Parameters:
        - X (DataFrame): Input DataFrame.
        - columns_to_extract (list): List of column names to extract numeric features from.

        Returns:
        - X_copy (DataFrame): DataFrame with extracted numeric features.
        """
        X_copy = X.copy()
        for col in columns_to_extract:
            X_copy[col] = pd.to_numeric(X_copy[col].str.split(' ').str[0], downcast='float', errors='coerce')
        return X_copy[columns_to_extract]

    def preprocess_levy_and_fillna(X):
        """
        Preprocess 'Levy' column by filling missing values with the mean Levy for the corresponding production year.

        Parameters:
        - X (DataFrame): Input DataFrame.

        Returns:
        - X_copy (DataFrame): DataFrame with preprocessed 'Levy' column.
        """
        X_copy = X.copy()
        X_copy["Levy"] = X_copy["Levy"].replace("-", None)
    
        X_copy['Levy'] = pd.to_numeric(X_copy['Levy'], errors='coerce')
        mean_levy_by_year = X_copy.groupby('Prod. year')['Levy'].mean()
        mean_levy_by_year = mean_levy_by_year.fillna(0)
        
        for year in X_copy['Prod. year'].unique():
            mask = (X_copy['Prod. year'] == year) & X_copy['Levy'].isnull()
            X_copy.loc[mask, 'Levy'] = mean_levy_by_year[year]
        
        X_copy['Levy'] = X_copy['Levy'].astype(int)
        
        return X_copy
    
    column_transformer = make_column_transformer(
            (FunctionTransformer(preprocess_levy_and_fillna, validate=False), ['Prod. year', 'Levy']),
            (FunctionTransformer(extract_numeric_features, kw_args={'columns_to_extract': numeric_features_to_extract}), numeric_features_to_extract),
            (OrdinalEncoder(handle_unknown='use_encoded_value', unknown_value=-1, dtype=int), ordinal_features),
            (OneHotEncoder(drop='if_binary', handle_unknown='ignore', sparse_output=False), categorical_features),
            ("passthrough", passthrough_feature),
            ("drop", drop_features)
    )

    return column_transformer