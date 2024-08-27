from sensor.Configuration.mongondb_connection import MongoDBClient
from sensor.Exception import apsException
from sensor.logger import logging
from sensor.Constants import DB_NAME,COLLECTION_NAME
import pandas as pd
import sys
import numpy as np
from typing import Optional


class APSdata:
    def __init__(self):
        try:
            self.mongo_client = MongoDBClient(database_name=DB_NAME)
        except Exception as e:
            raise apsException(e,sys)
        
    def export_collection_as_dataframe(self,collection_name:str,database_name:Optional[str] = None)->pd.DataFrame:

        try:

            if database_name is None:
                
                collection = self.mongo_client.database[collection_name]
            else:
                collection = self.mongo_client[database_name][collection_name]
            df = pd.DataFrame(list(collection.find()))
            if "_id" in df.columns.to_list():
                df = df.drop(columns=["_id"], axis=1)
            df.replace({"na":np.nan},inplace=True)
            return df
    
        except Exception as e:
            raise apsException(e,sys)
        