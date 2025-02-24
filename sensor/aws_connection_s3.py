from sensor.Exception import apsException
from sensor.logger import logging
from sensor.Constants import AWS_ACCESS_KEY_ID_ENV_KEY,AWS_SECRET_ACCESS_KEY_ENV_KEY,REGION_NAME,MODEL_BUCKET_NAME
import os
import boto3
import sys
from io import BytesIO



class S3_connection:
    def __init__(self):
        self.access_key_id = AWS_ACCESS_KEY_ID_ENV_KEY
        self.secret_access_key = AWS_SECRET_ACCESS_KEY_ENV_KEY
        self.region_name = REGION_NAME
        self.s3client_client = None  
        self.s3client_resource=None
        self.bucket_name=MODEL_BUCKET_NAME
        self.s3_key='model/model.pkl'


    def connect(self):
            #To connect to the high-level interface, you’ll follow a similar approach, but use resource():

           self.s3client_resource=boto3.resource('s3',
                                            aws_access_key_id=self.access_key_id,
                                            aws_secret_access_key=self.secret_access_key,
                                            region_name=self.region_name
                                            )
           

           self.s3client_client=boto3.client('s3',
                                            aws_access_key_id=self.access_key_id,
                                            aws_secret_access_key=self.secret_access_key,
                                            region_name=self.region_name
                                            )
           

    def s3_sync_upload(self,file_path) :
         try:
        
            self.bucket_name=MODEL_BUCKET_NAME
            self.local_path1=file_path

            if self.s3client_client is None:
                self.connect()

        
            self.s3client_client.upload_file(self.local_path1, self.bucket_name, self.s3_key)
            logging.info(f"File {self.local_path1} uploaded to S3 bucket {self.bucket_name}.")
         except Exception as e:
            raise apsException(f"Error uploading file to S3: {e}",sys)
         
    #This will correctly upload the file "final_model/model.pkl" to S3 at:
#s3://my-bucket/models/model.pkl  
# 
# 
    #In the event of an error, it will print an error message and exit the program.
    #Remember to replace "my-bucket" with your actual S3 bucket name.



    def is_bucket_present(self):
        """Check if the S3 bucket exists."""
        logging.info("Checking if the S3 bucket exists")
        # You can add error handling here if needed. For now, we'll just log the error and return False.
        # This is a placeholder, replace it with your own error handling code.
        try:
            if self.s3client_resource is None:
                self.connect()
            
            self.s3client_client.head_bucket(Bucket=self.bucket_name) 
            return True
        
        
        except Exception:
            return False  # ✅ Return False instead of raising an exception

    def if_model_exist_in_bucket(self):
        """Check if the model exists in S3."""
        logging.info("Checking if the model exists in_bu")
        try:
            if self.s3client_client is None:
                self.connect()
            response = self.s3client_client.list_objects_v2(Bucket=self.bucket_name)
            logging.info(response.get('Contents', []))     
            
            self.s3client_client.head_object(Bucket=self.bucket_name, Key=self.s3_key) 
            logging.info("✅ Model found in S3!") 
            return True 
        
        except Exception as e: 
            logging.error(f"❌ Error checking model in S3: {e}")
 # ✅ Catch exceptions (e.g., 404 Not Found)
            return False  # ✅ Return False instead of raising an exception

    def download_model_s3(self):
        """Download the model from S3."""
        try:
            if self.s3client_client is None:
                self.connect()
            
            response = self.s3client_client.get_object(Bucket=self.bucket_name, Key=self.s3_key) 
            model_data = response['Body'].read()
            logging.info(f"✅ Model downloaded from S3 bucket {self.bucket_name}.")
            return BytesIO(model_data)  # ✅ Return the binary object
            logging.info(f"Model downloaded from S3 bucket {self.bucket_name}.")
        except Exception as e:
            raise apsException(f"Error downloading file from S3: {e}",sys)