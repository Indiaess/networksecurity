import os
import sys
import json
from dotenv import load_dotenv
import pandas as pd
import certifi
from pymongo import MongoClient
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

load_dotenv()

MONGO_DB_URL = os.getenv("MONGO_DB_URL")
print(MONGO_DB_URL)

ca = certifi.where()


class NetworkDataExtract:

    def __init__(self):
        try:
            self.mongo_client = MongoClient(MONGO_DB_URL, tlsCAFile=ca)
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def csv_to_json_converter(self, file_path):
        try:
            df = pd.read_csv(file_path)

            df.reset_index(drop=True, inplace=True)

            records = df.to_dict(orient="records")

            return records

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def insert_data_mongodb(self, records, database, collection):
        try:

            db = self.mongo_client[database]

            col = db[collection]

            col.insert_many(records)

            return len(records)

        except Exception as e:
            raise NetworkSecurityException(e, sys)


if __name__ == "__main__":

    FILE_PATH = r"D:\Personal_projects\ML_OPS\data_science_project_2\Netework_Data\phisingData.csv"

    DATABASE = "SatyamAI"

    COLLECTION = "network_data"

    networkobj = NetworkDataExtract()

    records = networkobj.csv_to_json_converter(FILE_PATH)

    print(f"Total records extracted: {len(records)}")

    no_of_records = networkobj.insert_data_mongodb(records, DATABASE, COLLECTION)

    print(f"Inserted {no_of_records} records into MongoDB")