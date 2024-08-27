import pymongo
import os
import sys
from sensor.logger import logging
from sensor.Exception import apsException
from sensor.Constants import DB_NAME,MONGODB_URL_KEY


class MongoDBClient:
    client = None
    def __init__(self,database_name=DB_NAME):
        try:
            if MongoDBClient.client is None:
                mongo_db_url=os.getenv(MONGODB_URL_KEY)
                if mongo_db_url is None:
                    raise Exception(f"enivornment key is not set or does not exist{MONGODB_URL_KEY}")
                
                MongoDBClient.client = pymongo.MongoClient(mongo_db_url)
                logging.info("Successfully connected to MongoDB")


            self.Client=MongoDBClient.client
            self.database_name=database_name
            self.database = self.Client[database_name]


            logging.info("MongoDB connection succesfull")

        except Exception as e:
            raise apsException(e,sys)     




