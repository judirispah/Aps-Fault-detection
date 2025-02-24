import os
import sys
from pathlib import Path
from sensor.aws_connection_s3 import S3_connection
from sensor.entity.artifact_entity import DataIngestionArtifact,ModelTrainerArtifact,DataTransformationArtifact,ClassificationMetricArtifact
from sensor.Exception import apsException
from sensor.logger import logging
from dataclasses import dataclass, asdict
from sensor.entity.estimator import apsModel
import pickle
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from sensor.utils.main_utils import read_yaml_file,load_object,save_object,load_numpy_array_data,write_yaml_file

class Model_Pusher:
    def __init__(self,model_trainer_artfact:ModelTrainerArtifact,data_ingestion_artifact:DataIngestionArtifact,
                 data_transformation_artifact:DataTransformationArtifact):
        
            self.model_trainer_artifact = model_trainer_artfact
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_transformation_artifact = data_transformation_artifact
            self.s3 = S3_connection()
    

        

    def model(self) : 
        try:

            if self.s3.is_bucket_present():
                if self.s3.if_model_exist_in_bucket():
                    logging.info('Model already exists in the S3 bucket')
                    try:
                        model = self.s3.download_model_s3()

                        model_path = "downloaded_model.pkl"
                        with open(model_path, "wb") as f:
                            f.write(model.read())

                        with open(model_path, "rb") as f:
                            s3_unpickled_model = pickle.load(f)
                        
                    except Exception as e:
                        logging.error(f"Failed to download or unpickle model from S3: {str(e)}")
                        raise apsException(e, sys)
                    #preprocessing_obj = load_object(self.data_transformation_artifact.transformed_object_file_path)

                    logging.info('Model loaded from S3 bucket')
                    #s3_model=apsModel(preprocessing_obj,s3_unpickled_model)
                    x_data=load_numpy_array_data(self.data_transformation_artifact.transformed_test_file_path)[ : , :-1]
                    y_data=load_numpy_array_data(self.data_transformation_artifact.transformed_test_file_path)[ : ,-1]
                    prediction=s3_unpickled_model.predict(x_data)
                    s3_accuracy = accuracy_score(y_data, prediction)
                    
                    logging.info('Model prediction accuracyin s3: {}'.format(s3_accuracy))

                    local_model_metrics=read_yaml_file(self.model_trainer_artifact.metric_artifact)
                    local_model_accuracy = local_model_metrics.get('accuracy_score', 0)

                    logging.info('Local model accuracy: {}'.format(local_model_accuracy))
                    if local_model_accuracy > s3_accuracy:
                        local_model=self.model_trainer_artifact.trained_model_file_path
                        self.s3.s3_sync_upload(local_model)

                        logging.info("✅ Local model is better. Keeping the local model ans saving the new model to s3.")
                    else:
                         

                        logging.info("⚠️ S3 model is better or the same. Using the S3 model instead.")
                        save_object("final_model/model.pkl", model)




                else:
                    logging.info('Model does not exist in S3 bucket. Uploading the model to S3 bucket')
                    self.s3.s3_sync_upload('final_model/model.pkl')  
                    logging.info('Model uploaded to S3 bucket') 

            else:
                logging.error('S3 bucket not found')

        except Exception as e:
            raise apsException(e, sys) from e  



    def initiate_model_pusher(self):
        """
        This method of ModelPusher class is responsible for starting model pushing
        """
        logging.info("Entered the initiate_model_pusher method of ModelPusher class")
        try:
            self.model()
        except Exception as e:
            raise apsException(e, sys) from e