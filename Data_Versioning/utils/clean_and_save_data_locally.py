#!/usr/bin/env python3

import os
import pandas as pd
import numpy as np

from datetime import datetime
from utils.preprocessing_pipeline import preprocessing_pipeline


def clean_and_save_data_locally(df, file_prefix):
    """
    Cleans the raw DataFrame and saves the cleaned data locally.

    Parameters:
    - df (DataFrame): Raw DataFrame to be cleaned.
    - file_prefix (str): Prefix indicating if it is a train/val/test file.

    Returns:
    - cleaned_file_path (str): The path to the saved cleaned file.
    """
    numeric_features = df.select_dtypes(np.number).columns.to_list()
    extract_num_feats = ['Mileage', 'Engine volume']
    passthrough_features = ['Manufacturer', 'Model', 'Fuel type',
                            'Leather interior', 'Gear box type', 'Category', 'Price']
    
    # Determine features to drop
    drop_features = list(set(df.columns) - set(numeric_features + extract_num_feats +
                                               ['Levy'] + passthrough_features))
    
    # Apply pre-processing pipeline
    ct = preprocessing_pipeline(numeric_features_to_extract=extract_num_feats,
                                 passthrough_features=passthrough_features,
                                 drop_features=drop_features)

    # Transformation
    transformed_data = ct.fit_transform(df)
    transformers_info = ct.get_params()['transformers']
    column_names = [col for info in transformers_info for col in info[2] if info[1] != 'drop']
    
    cleaned_data = pd.DataFrame(transformed_data, columns=column_names)

    # Saving data
    data_dir = os.path.join('~', 'Car-Prices-Prediction', 'Data_Versioning', 'data', 'cleaned') # /Car-Prices-Prediction/Data_Versioning/utils
    os.makedirs(data_dir, exist_ok=True)
    
    version = datetime.now().strftime("%Y%m%d")
    cleaned_file_path = os.path.join(data_dir, f'{file_prefix}_v{version}.csv')
    
    cleaned_data.to_csv(cleaned_file_path, index=False)

    return cleaned_file_path