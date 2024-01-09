#!/usr/bin/env python3

import os
import boto3
import click
import pandas as pd

from sklearn.model_selection import train_test_split

from utils.create_bucket import create_bucket
from utils.clean_and_save_data_locally import clean_and_save_data_locally
from utils.upload_cleaned_data import upload_cleaned_data

@click.command()
@click.argument('data_directory', type=click.Path(exists=True), default=".")
def main(data_directory):
    """
    Main function for saving the cleaned data to s3
    """
    
    if data_directory == os.path.abspath("."):
        data_directory = os.path.join(data_directory, "data")
    
    
    # Check if the directory exists, if not, create it
    if not os.path.exists(data_directory):
        try:
            os.makedirs(data_directory)
        except Exception as dir_creation_error:
            click.echo(f"Error creating directory '{data_directory}': {dir_creation_error}")
            return


    train_data_dir = os.path.join(data_directory, 'raw','train.csv')
    if not os.path.exists(train_data_dir):
        click.echo(f"File '{train_data_dir}' does not exist.")
        return
    
    try:
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
            cleaned_train_path = clean_and_save_data_locally(train_df, data_directory, 'train')
            cleaned_val_path = clean_and_save_data_locally(train_df, data_directory, 'val')
            
            if os.path.exists(cleaned_train_path):
                upload_cleaned_data(cleaned_train_path, bucket_name, 'train')
            if os.path.exists(cleaned_train_path):
                upload_cleaned_data(cleaned_val_path, bucket_name, 'val')
    except Exception as data_processing_error:
        click.echo(f"Error processing data: {data_processing_error}")

if __name__ == "__main__":
    main()