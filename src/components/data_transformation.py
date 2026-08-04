import sys
from dataclasses import dataclass
import numpy as ny
import pandas as pd
from sklern.impute import SimpleImputer
from skelarn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler,OneHotEncoder

from src.exception import CustomException
from src.logger import logging

from src.utils import save_object

@dataclass 
class TransformationConfig:
    preprocessor_obj_file_path=os.path.join('artifacts','preprocessor.pkl')


class DataTransformation:
    def __init__(self):
        self.data_transformation_config=DataTransformationConfig()

    def get_data_transformation_object(self):
        try:
            numerical_columns=['writing_score','reading_score']
            categorical_columns=["gender","race_ethnicity","parental_level_of_education","lunch","test_preparation_course"]
            num_pipeline=Pipeline(
                steps=["imputer",SimpleImputer(strategy="median"),
                ("scaler",StandardScaler())])

            cat_pipeline=Pipeline(steps=[(
                "imputer",SimpleImputer(strategy="most_frequent")),
                ("one_hot_encoder",OneHotEncoder()),
                ("scaler",StandardScaler()) ])

            logging.info("Numerical Columns Standard scaling completed")
            logging.info("Categorical Columns encoding completed")

            preprocessor=ColumnTransformer([
                ("num_pipeline",num_pipeline,numerical_columns),
                ("cat_pipeline",cat_pipeline,categorical_columns)
            ])

            return preprocessor


        except Exception as e:
            logging.error("Error occurred in data transformation")
            raise CustomException(e, sys.exc_info())

def initiate_data_transformation(self,train_path,test_path):
    try:
        train_df=pd.read_csv(train_csv)
        test_df=pd.read_csv(test_csv)

        logging.info("Read train and test data completed")

        logging.info("Obtaining preprocessing object")

        preprocessng_obj=self.get_data_transformer_object()

        target_column_name="math_score"
        numerical_columns=['writing_score','reading_score']

        input_feature_train_df=train_df.drop(columns=["target_column_name"],axis=1)
        input_feature_test_df=test_df["target_column_name"]

        logging.info(f"Applied preprocessing object on training and testing datasets.")
s
        input_feature_train_arr=preprocessng_obj.fit_transform(input_feature_train_df)
        input_feature_test_arr=preprocessng_obj.transform(input_feature_test_df)

        train_arr=np.c_[input_feature_train_arr,np.array(target_feature_test_df)]
        test_arr=np.c_[input_feature_test_arr,np.array(target_feature_test_df)]

        logging.info(f"Saved preprocessing object.")

        save_object(file_path=self.data_transfrmation_config.preprocessor_obj_file_path,obj=preprocessng_obj)

        return(train_arr,test_arr,self.data_transformation_config.preprocessor_obj_file_path,)

    except exception as e:
        raise CustomException(e,sys)   
