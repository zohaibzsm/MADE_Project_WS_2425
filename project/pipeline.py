# Write a script (for example in Python or Jayvee) that pulls the data sets 
# you chose from the internet, transforms it and fixes errors, and finally stores your data in the /data directory

# Place the script in the /project directory (any file name is fine)

# Add a /project/pipeline.sh that starts your pipeline as you would do from the command line as entry point:
# E.g. if you run your script on your command line using `python3 /project/pipeline.py`, create a /project/pipeline.sh with the content: 
# !/bin/bash
# python3 /project/pipeline.py

# The output of the script should be: datasets in your /data directory (e.g., as SQLite databases) 
# Do NOT check in your data sets, just your script
# You can use .gitignore to avoid checking in files on git
# This data set will be the base for your data report in future project work


###   Start of the Script   ###

import pandas as pd # type: ignore
import os
import subprocess
import zipfile
from sqlalchemy import create_engine # type: ignore
from tests import Test

class Pipeline():
    def __init__(self, kaggle_user_name, kaggle_key):
        self.kaggle_user_name = kaggle_user_name
        self.kaggle_key = kaggle_key
        
    def extract_Data(self):
        os.environ['KAGGLE_USERNAME'] = self.kaggle_user_name
        os.environ['KAGGLE_KEY'] = self.kaggle_key

        # dataset1 extraction
        dataset1 = "muonneutrino/us-census-demographic-data"
        subprocess.run(["kaggle", "datasets", "download", "-d", dataset1], check=True)

        # Unzip the downloaded file
        with zipfile.ZipFile("us-census-demographic-data.zip", 'r') as zip_ref:
            zip_ref.extractall("us-census-demographic-data")
        
        # verify if extracted successfully
        self.data1 = pd.read_csv("us-census-demographic-data/acs2017_county_data.csv")
        if self.data1 is not None:
            print("\nDataset 1 Extraction Success!\n")
        #(self.data1).to_csv("data1", index=False)

        # dataset2 extraction
        dataset2 = "teertha/ushealthinsurancedataset"
        subprocess.run(["kaggle", "datasets", "download", "-d", dataset2], check=True)

        # Unzip the downloaded file
        with zipfile.ZipFile("ushealthinsurancedataset.zip", 'r') as zip_ref:
            zip_ref.extractall("ushealthinsurancedataset")

        # verify if extracted successfully        
        self.data2 = pd.read_csv("ushealthinsurancedataset/insurance.csv")
        if self.data2 is not None:
            print("\nDataset 2 Extraction Success!\n")
        #(self.data2).to_csv("data1", index=False)

    def transform_Data(self):
        # making subset and dropping unnecessary columns from 1st dataset
        self.data1 = (self.data1).drop(columns=['CountyId','VotingAgeCitizen','IncomeErr','IncomePerCapErr','ChildPoverty'])

        # Dealing with missing values: 1st dataset

        # drop columns if at least 30% data is missing
        cols_to_drop = []
        perc_calc = 0.0
        for i in range(len(self.data1.columns)):
            perc_calc = self.data1.isnull().sum().values[i]/self.data1.shape[0]
            if perc_calc >= 0.3:
                cols_to_drop.append(self.data1.isnull().sum().index[i])
        self.data1.drop(columns=cols_to_drop, inplace = True)

        # filling values less than 30%
        self.data1.fillna(method='bfill', inplace=True)
        
        # Dealing with missing values: 2nd dataset

        # drop columns if at least 30% data is missing
        cols_to_drop = []
        perc_calc = 0.0
        for i in range(len(self.data2.columns)):
            perc_calc = self.data2.isnull().sum().values[i]/self.data2.shape[0]
            if perc_calc >= 0.3:
                cols_to_drop.append(self.data2.isnull().sum().index[i])
        self.data2.drop(columns=cols_to_drop, inplace = True)

        # filling values less than 30%
        self.data2.fillna(method='bfill', inplace=True)

        print("\nData Transformation Success!\n")

    def load_Data(self):
        # load data 1
        path = 'sqlite:///../data/' + self.kaggle_user_name + '0.sqlite'
        disk_engine = create_engine(path, echo = False)
        (self.data1).to_sql('US_demographics', disk_engine, if_exists='replace')
        disk_engine.dispose()
        (self.data1).to_csv("data1", index=False)

        # load data 2
        path = 'sqlite:///../data/' + self.kaggle_user_name + '1.sqlite'
        disk_engine = create_engine(path, echo = False)
        (self.data2).to_sql('ushealthinsurancedataset', disk_engine, if_exists='replace')
        disk_engine.dispose()
        (self.data2).to_csv("data2", index=False)
        (self.data2).head()

        print("\nData Load Success!\n")

    def execute_Pipeline(self):
        self.extract_Data()
        self.transform_Data()
        self.load_Data()
        
if __name__ == '__main__':

    # your_username and your_key for Kaggle data extraction
    pipe = Pipeline('kaggle username','kaggle key')
    print("\n\n*********************Pipeline started*********************\n\n")
    pipe.execute_Pipeline()
    print("\n*********************Pipeline ended*********************\n\n")

    test = Test("kaggle username") 
    print("\n*********************Test started*********************\n")
    test.test_pipeline()
    print("\n*********************Test ended*********************\n")