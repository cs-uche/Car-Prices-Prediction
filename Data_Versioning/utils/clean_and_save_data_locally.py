#!/usr/bin/env python3

import os
import pandas as pd
import numpy as np

from datetime import datetime
from sklearn.preprocessing import FunctionTransformer
from utils.preprocessing_pipeline import preprocessing_pipeline


def clean_and_save_data_locally(df, data_directory, file_prefix, has_header):
    """
    Cleans the raw DataFrame and saves the cleaned data locally.

    Parameters:
    - df (DataFrame): Raw DataFrame to be cleaned.
    - data_directory(str): The directory to the data files.
    - file_prefix (str): Prefix indicating if it is a train/val/test file.
    - has_header(boolean): Determines if the file is saved with/without headers

    Returns:
    - cleaned_file_path (str): The path to the saved cleaned file.
    """
    numeric_features = df.select_dtypes(np.number).drop('Price', axis=1).columns.to_list()
    extract_num_feats = ['Mileage', 'Engine volume']
    ord_feats = ['Manufacturer', 'Model', 'Fuel type']
    cat_feats = ['Leather interior','Gear box type', 'Category']
    pass_feat = ["Price"]
    # Determine features to drop
    drop_features = list(set(df.columns) - set(numeric_features + extract_num_feats +
                                               ['Levy'] + cat_feats + ord_feats + pass_feat))
    
    # Apply pre-processing pipeline
    ct = preprocessing_pipeline(numeric_features_to_extract=extract_num_feats,
                                 categorical_features=cat_feats, 
                                 ordinal_features=ord_feats,
                                 passthrough_feature = pass_feat,
                                 drop_features=drop_features)

    # Transformation
    try:
        
        transformed_data = ct.fit_transform(df)
        
        if has_header:
            # get column names
            column_names = []
            for _, transformer, columns in ct.transformers_:
                if _ in ["drop", "remainder"]:
                    continue
            
                column_names.extend(columns if (type(transformer) == FunctionTransformer or _ == "passthrough")
                                        else transformer.get_feature_names_out().tolist())
            
            # Create DataFrame with column names
            cleaned_data = pd.DataFrame(transformed_data, columns=column_names)
        else:
            # Create DataFrame without column names
            cleaned_data = pd.DataFrame(transformed_data, columns=None)
        
    except Exception as transformation_error:
        print(f"Error during data transformation: {transformation_error}")
        return

    # Saving data
    try:
        if not os.path.exists(data_directory):
            os.makedirs(data_directory)

        cleaned_data_dir = os.path.join(data_directory, 'cleaned')
        if not os.path.exists(cleaned_data_dir):
            os.makedirs(cleaned_data_dir)

        
        version = datetime.now().strftime("%Y%m%d")
        cleaned_file_path = os.path.join(cleaned_data_dir, f'{file_prefix}_v{version}.csv')
        
        cleaned_data.to_csv(cleaned_file_path, index=False, header=has_header)
    except Exception as save_error:
        print(f"Error during data saving: {save_error}")
        return

    return cleaned_file_path