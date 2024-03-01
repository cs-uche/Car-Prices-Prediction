#!/usr/bin/env python3

import click
import os
import pandas as pd
import numpy as np
import sys

from datetime import datetime
from sklearn.preprocessing import FunctionTransformer
from utils.preprocessing_pipeline import preprocessing_pipeline


def clean_and_return_dataframe(df, has_header):
    """
    Cleans and pre-processes the raw DataFrame and returns it.

    Parameters:
    - df (pandas.DataFrame): Raw DataFrame to be cleaned.
    - has_header(boolean): Determines if the file is saved with/without headers

    Returns:
    - cleaned_df (pandas.DataFrame): returns a pre-processed Dataframe.

    Dependency:
    - utils.preprocessing_pipeline
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
        click.echo(f"Error during data transformation: {transformation_error}")
        sys.exit(1)


    return cleaned_data