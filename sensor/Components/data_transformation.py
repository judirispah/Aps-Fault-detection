import sys

import numpy as np
import pandas as pd
from imblearn.combine import SMOTETomek
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import RobustScaler
from sklearn.impute import SimpleImputer

from sensor.Constants import SCHEMA_FILE_PATH

from sensor.entity.config_entity import DataTransformationConfig
from sensor.entity.artifact_entity import DataTransformationArtifact, DataIngestionArtifact, DataValidationArtifact
from sensor.Exception import apsException
from sensor.logger import logging
from sensor.utils.main_utils import save_object, save_numpy_array_data, read_yaml_file, drop_columns


class DataTransformation:
    def __init__(self, data_ingestion_artifact: DataIngestionArtifact,
                 data_transformation_config: DataTransformationConfig,
                 data_validation_artifact: DataValidationArtifact):
        """
        :param data_ingestion_artifact: Output reference of data ingestion artifact stage
        :param data_transformation_config: configuration for data transformation
        """
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_transformation_config = data_transformation_config
            self.data_validation_artifact = data_validation_artifact
            self._schema_config = read_yaml_file(file_path=SCHEMA_FILE_PATH)
        except Exception as e:
            raise apsException(e, sys)
        
    @staticmethod
    def read_data(file_path) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise apsException(e, sys)    
        
    def get_data_transformer_object(self) -> Pipeline:
        """
        Method Name :   get_data_transformer_object
        Description :   This method creates and returns a data transformer object for the data
        
        Output      :   data transformer object is created and returned 
        On Failure  :   Write an exception log and then raise an exception
        """
        logging.info(
            "Entered get_data_transformer_object method of DataTransformation class"
        )

        try:

            preprocessor = Pipeline(steps=[
            
                ('RobustScaler', RobustScaler())])

            logging.info("Initialized StandardScaler,")

            logging.info("Created preprocessor object from ColumnTransformer")

            logging.info(
                "Exited get_data_transformer_object method of DataTransformation class"
            )
            return preprocessor
        except Exception as e:
            raise apsException(e, sys) from e
        

    def initiate_data_transformation(self, ) -> DataTransformationArtifact:
        """
        Method Name :   initiate_data_transformation
        Description :   This method initiates the data transformation component for the pipeline 
        
        Output      :   data transformer steps are performed and preprocessor object is created  
        On Failure  :   Write an exception log and then raise an exception
        """
        try:
            if self.data_validation_artifact.validation_status:
                logging.info("Starting data transformation") 
                preprocessor = self.get_data_transformer_object() 
                train_df = DataTransformation.read_data(file_path=self.data_ingestion_artifact.trained_file_path)
                test_df = DataTransformation.read_data(file_path=self.data_ingestion_artifact.test_file_path)

                
                input_feature_train_df = train_df.drop(columns=self._schema_config['drop_col'], axis=1)
                target_feature_train_df = train_df[self._schema_config['target']]  
                target_feature_train_df =target_feature_train_df .replace({'neg':0,'pos':1})

                

                
                input_feature_test_df = test_df.drop(columns=self._schema_config['drop_col'], axis=1)
                target_feature_test_df = test_df[self._schema_config['target']]
                target_feature_test_df=target_feature_test_df.replace({'neg':0,'pos':1})

                logging.info("Got train features and test features of Testing dataset")

                logging.info(
                    "Applying preprocessing object on training dataframe and testing dataframe"
                )
                input_feature_train_arr = preprocessor.fit_transform(input_feature_train_df)
                logging.info(
                    "Used the preprocessor object to fit transform the train features"
                )

                input_feature_test_arr = preprocessor.transform(input_feature_test_df)

                logging.info("Used the preprocessor object to transform the test features")


                logging.info("Applying IMPUTER on Training dataset")
                imputer = SimpleImputer(strategy='constant', fill_value=0)
                input_feature_train_arr=imputer.fit_transform(input_feature_train_arr)
                logging.info("Applied imputer on training dataset")


                logging.info("Applying IMPUTER on Test dataset")
                
                input_feature_test_arr=imputer.transform(input_feature_test_arr)
                logging.info("Applied imputer on test dataset")


                logging.info("Applying SMOTEENN on Training dataset")

                smt = SMOTETomek(random_state=42,sampling_strategy='minority', n_jobs=-1 )


                input_feature_train_final, target_feature_train_final = smt.fit_resample(
                    input_feature_train_arr, target_feature_train_df
                )

                logging.info("Applied SMOTEENN on training dataset")

                logging.info("Applying SMOTEENN on testing dataset")

                input_feature_test_final, target_feature_test_final = smt.fit_resample(
                    input_feature_test_arr, target_feature_test_df
                )

                logging.info("Applied SMOTEENN on testing dataset")

                logging.info("Created train array and test array")


                train_arr = np.c_[
                    input_feature_train_final, np.array(target_feature_train_final)
                ]
                print(train_arr[0])
                print(type(train_arr))


                test_arr = np.c_[
                    input_feature_test_final, np.array(target_feature_test_final)
                ]

                save_object(self.data_transformation_config.transformed_object_file_path, preprocessor)
                save_numpy_array_data(self.data_transformation_config.transformed_train_file_path, array=train_arr)
                save_numpy_array_data(self.data_transformation_config.transformed_test_file_path, array=test_arr)

                data_transformation_artifact = DataTransformationArtifact(
                    transformed_object_file_path=self.data_transformation_config.transformed_object_file_path,
                    transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                    transformed_test_file_path=self.data_transformation_config.transformed_test_file_path
                )
                return data_transformation_artifact
            else:
                raise Exception(self.data_validation_artifact.message)

        except Exception as e:
            raise apsException(e, sys) from e







               


