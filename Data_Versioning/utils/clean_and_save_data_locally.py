#!/usr/bin/env python3

import os
import sys
from datetime import datetime
from utils.clean_and_return_dataframe import clean_and_return_dataframe


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

    Dependency:
    - utils.clean_and_return_dataframe
    """

    cleaned_data = clean_and_return_dataframe(df=df, has_header=has_header)
    
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
        sys.exit(1)

    return cleaned_file_path