#!/usr/bin/env python3

import os
import boto3
import pandas as pd

from sklearn.model_selection import train_test_split

from utils.create_bucket import create_bucket
from utils.clean_and_save_data_locally import clean_and_save_data_locally
from utils.upload_cleaned_data import upload_cleaned_data

def main():
    """
    Main function for saving the cleaned data to s3
    """
    
    # preprocessing
    data_dir = os.path.join('Car-Prices-Prediction', 'data') # /Car-Prices-Prediction/Data_Versioning/utils
    train_data_dir = os.path.join(data_dir, 'raw','train.csv')
    raw_train_data = pd.read_csv(train_data_dir)
    raw_train_data.drop('ID', axis=1, inplace=True)
    
    y = raw_train_data["Price"]
    X = raw_train_data.drop("Price", axis=1)
    
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=.2, random_state=42)
    
    train_df = pd.concat([X_train, y_train], axis=1)
    val_df = pd.concat([X_val, y_val], axis=1)
    
    # saving to s3
    bucket_name = "car-prices-prediction"
    region = boto3.session.Session().region_name
    
    if(create_bucket(bucket_name)):
        cleaned_train_path = clean_and_save_data_locally(train_df, 'train')
        cleaned_val_path = clean_and_save_data_locally(train_df, 'val')
        
        upload_cleaned_data(cleaned_train_path, bucket_name, 'train')
        upload_cleaned_data(cleaned_val_path, bucket_name, 'val')

if __name__ == "__main__":
    main()